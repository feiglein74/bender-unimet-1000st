#!/usr/bin/env python3
"""Parst die Prüfschritt- und Befehlsliste des UNIMET-Interface-Handbuchs.

Quelle: docs/bender/UNIMET_Interface_Handbuch_de.pdf (TGH1315/01.2006)
Die Tabellen lassen sich nur im pdftotext-RAW-Modus zuverlässig auslesen;
-layout verschiebt die Spalten gegeneinander.

Aufruf:  python tools/parse_interface.py
Ergebnis: research/RS232_PROTOKOLL.md
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "docs/bender/UNIMET_Interface_Handbuch_de.pdf"
OUT = ROOT / "research/RS232_PROTOKOLL.md"

# Seitenbereiche laut Inhaltsverzeichnis (Handbuchseiten == PDF-Seiten)
STEPS_1000 = (21, 37)   # 5.1 Liste der Prüfschritte UNIMET 1000/1100ST
CMDS_1000 = (38, 72)    # 5.2 Liste der Befehle UNIMET 1000/1100ST
STEPS_300 = (14, 14)    # 4.2 Liste der Prüfschritte UNIMET 300ST

NOISE = re.compile(
    r"^(TGH\d+|\d{1,3}$|\d{1,3}\s+TGH\d|Schnittstellenbeschreibung|Schritt\b|"
    r"Befehl\b|Allgemeine Bezeichnung|Spezielle Bezeichnung)"
)


def pages(first, last):
    """Seitenbereich im RAW-Modus als Zeilenliste, ohne Kopf-/Fußzeilen."""
    txt = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), "-raw", "-enc", "UTF-8",
         str(PDF), "-"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    out = []
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln and not NOISE.match(ln):
            out.append(ln)
    return out


# Wörter, die nach einem Bindestrich am Zeilenende KEINE Silbentrennung sind
# ("Ein- und Ausgang"), sondern eine echte Auslassung.
NO_MERGE = {"und", "oder", "bzw", "bzw.", "sowie", "bis"}


def join_lines(lines):
    """Fügt Zeilen zusammen und behandelt Bindestriche am Zeilenende.

    Folgt Kleinschreibung, ist es Silbentrennung  -> Bindestrich entfällt
        'Strom-' + 'quelle'      -> 'Stromquelle'
    Folgt Großschreibung, ist der Bindestrich echt -> er bleibt erhalten
        'U-' + 'Netz am ATeil'   -> 'U-Netz am ATeil'
    """
    out = ""
    for ln in lines:
        if not out:
            out = ln
        elif out.endswith("-") and ln[:1].isalpha() and \
                ln.split(None, 1)[0] not in NO_MERGE:
            out = (out[:-1] if ln[:1].islower() else out) + ln
        else:
            out += " " + ln
    return out


def split_repeat(text):
    """Trennt 'Allgemeine Bezeichnung' von 'Spezielle Bezeichnung'.

    Im PDF stehen beide Spalten hintereinander, wobei die spezielle
    Bezeichnung mit der allgemeinen beginnt:
        'Isolationswiderstand Isolationswiderstand Gehäuse'
    Gesucht ist die längste Aufteilung, bei der Teil 2 mit Teil 1 anfängt.
    """
    words = text.split()
    for cut in range(len(words) - 1, 0, -1):
        head = " ".join(words[:cut])
        tail = " ".join(words[cut:])
        if tail.startswith(head):
            return head, tail
    return text, text


def parse_steps(first, last):
    """Zeilen der Form '<nr> <allgemein> <speziell>' mit Fortsetzungszeilen."""
    steps, num, buf = [], None, []

    def flush():
        if num is not None:
            gen, spec = split_repeat(join_lines(buf))
            steps.append((num, gen, spec))

    for ln in pages(first, last):
        m = re.match(r"^(\d{1,3})\s+(\D.*)$", ln)
        if m:
            flush()
            num, buf = int(m.group(1)), [m.group(2)]
        elif num is not None:
            buf.append(ln)
    flush()
    return steps


UNITS = {"Ohm", "MOhm", "mA", "A", "V", "kVA", "kW", "W", "s"}


def parse_steps_300(first, last):
    """UNIMET 300ST: '<nr> <name…> [<einheit>] <min> <max>' (fünf Spalten)."""
    rows = []
    for ln in pages(first, last):
        m = re.match(r"^(\d{1,3}\*?)\s+(\D.*)$", ln)
        if not m:
            continue
        tok = m.group(2).split()
        if len(tok) < 3:
            continue
        lo, hi = tok[-2], tok[-1]
        if not re.fullmatch(r"[\d.]+", lo) or not re.fullmatch(r"[\d.]+", hi):
            continue
        rest = tok[:-2]
        unit = rest.pop() if rest and rest[-1] in UNITS else ""
        rows.append((m.group(1), " ".join(rest), unit, lo, hi))
    return rows


def parse_commands(first, last):
    """Befehlszeilen ':...' mit Langform und Kommentar; Zwischenüberschriften."""
    entries, cur = [], None

    def flush():
        if cur:
            entries.append(("cmd", cur[0], cur[1], join_lines(cur[2]).strip()))

    for ln in pages(first, last):
        if ln.startswith(":"):
            flush()
            parts = ln.split(None, 2)
            cmd = parts[0]
            long = parts[1] if len(parts) > 1 else ""
            rest = [parts[2]] if len(parts) > 2 else []
            cur = [cmd, long, rest]
        elif ln.startswith("U1000") or ln.startswith("U1100"):
            flush()
            cur = None
            entries.append(("head", ln, "", ""))
        elif cur:
            cur[2].append(ln)
    flush()
    return entries


def main():
    steps = parse_steps(*STEPS_1000)
    steps300 = parse_steps_300(*STEPS_300)
    cmds = parse_commands(*CMDS_1000)
    ncmd = sum(1 for e in cmds if e[0] == "cmd")

    L = []
    A = L.append
    A("# UNIMET 1000/1100 ST — RS232-Referenz\n")
    A("Maschinell erzeugt aus `docs/bender/UNIMET_Interface_Handbuch_de.pdf`")
    A("(TGH1315/01.2006) via `tools/parse_interface.py`. Bei Zweifeln gilt das PDF.\n")
    A(f"Umfang: **{len(steps)} Prüfschritte**, **{ncmd} Befehle**.\n")

    A("## 1. Schnittstelle\n")
    A("| Parameter | Wert |")
    A("|---|---|")
    A("| Physik | RS-232, galvanisch getrennt, 9-polig |")
    A("| Baudrate | 300 / 4800 / **9600** (Werkseinstellung) |")
    A("| Format | **7 Datenbit, 2 Stoppbit, Parität gerade (7E2)** |")
    A("| Übertragungsart | asynchron |")
    A("| Pegel | log. 1: +1,2 V … −12 V · log. 0: +1,5 V … +12 V |")
    A("| Max. Länge | 5 m |")
    A("| Kabel | Nullmodem |\n")

    A("### Nullmodem-Belegung\n")
    A("| Signal PC | DB25 | DB9 | Richtung | Unimet | Signal Unimet |")
    A("|---|---|---|---|---|---|")
    for a, b, c, d, e, f in [
        ("RxD", 3, 2, "&larr;", 3, "TxD"), ("TxD", 2, 3, "&rarr;", 2, "RxD"),
        ("RTS", 4, 7, "&rarr;", 8, "CTS"), ("CTS", 5, 8, "&larr;", 7, "RTS"),
        ("GND", 7, 5, "&mdash;", 5, "GND"), ("DTR", 20, 4, "&rarr;", 6, "DSR"),
        ("DSR", 6, 6, "&larr;", 4, "DTR"),
    ]:
        A(f"| {a} | {b} | {c} | {d} | {e} | {f} |")
    A("")

    A("## 2. Protokoll (Unimet Standard Protokoll, USP)\n")
    A("**Remote aktivieren:** `DC3` (ASCII 19) senden &rarr; Antwort "
      "`Unimet in Remote`. Die Gerätetastatur ist dann gesperrt.")
    A("**Remote beenden:** `DC4` (ASCII 20), keine Antwort.")
    A("Alternativ am Gerät: Hauptmenü &rarr; F5 Systemverwaltung &rarr; "
      "F2 Schnittstellen &rarr; F3 Unimet Standard Protokoll.\n")
    A("**USP ist SCPI.** Die Syntax folgt durchgängig *Standard Commands for "
      "Programmable Instruments*: hierarchischer Doppelpunktpfad, `?` für "
      "Abfragen, `;` zum Verketten auf gleicher Ebene, und Langformen, bei "
      "denen die Großbuchstaben die Kurzform ergeben (`ATTRibut?` → `:ATTR?`). "
      "Ein Rückseitenaufkleber des Geräts nennt für die RS-485-Schnittstelle "
      "ausdrücklich das „Bender SCPI Protokoll\" — vermutlich dieselbe "
      "Befehlsfamilie auf dem Serviceport.\n")
    A("Befehle sind hierarchisch (`:DATA:CAT:ID:FIRS?`). Sie lassen sich "
      "komplett senden oder ebenenweise; auf gleicher Ebene genügt danach "
      "`;NEXT?`. Für einen Wechsel der Ebene muss wieder bei Root begonnen "
      "werden.\n")
    A("### Antwortcodes\n")
    A("| Antwort | Bedeutung |")
    A("|---|---|")
    for k, v in [
        ("`1234…`", "abgefragter Wert"),
        ("`#NULL#`", "Empfangsbestätigung ohne Datenabfrage"),
        ("`#NOCMD#`", "Befehl ungültig oder unbekannt"),
        ("`#ERROR#`", "ungültige/unbekannte Messung, allgemeiner Fehler"),
        ("`#OFFLINE#`", "Remote-Betrieb beendet, oder Datenbankfehler "
                        "(Datenbankreparatur am Gerät nötig)"),
        ("`#VOID#`", "Leerstring"),
        ("`#IDCFULL#`", "Gerätekatalog voll"),
        ("`#TYPCFULL#`", "Typenkatalog voll"),
    ]:
        A(f"| {k} | {v} |")
    A("")

    A("## 3. Prüfschritte UNIMET 1000/1100 ST\n")
    A("Auswahl per `:MEAS:STEP <nr>`, Auslösen per `:SYS:CTRL <nr>`.")
    A("Abkürzungen: **NC** Normalzustand · **SFC** erster Fehlerfall · "
      "**TRMS** Effektivwertmessung · **ATeil** Anwendungsteil · "
      "**FE** Funktionserde · **PE** Schutzleiter · **SK** Schutzklasse · "
      "**Phase rev.** umgekehrte Phasenlage · **Netzl. offen** "
      "Netzleiter unterbrochen.\n")
    A("| Nr. | Allgemeine Bezeichnung | Spezielle Bezeichnung |")
    A("|---:|---|---|")
    for n, g, s in steps:
        A(f"| {n} | {g} | {s} |")
    A("")

    if steps300:
        A("### Prüfschritte UNIMET 300 ST (zum Vergleich, mit Grenzwerten)\n")
        A("Diese Tabelle nennt zusätzlich Einheit und Grenzwertbereich. "
          "`*` = aus Kompatibilität zum Unimet 1100 separat geführt "
          "(106 entspricht 6, 107 entspricht 5).\n")
        A("| Nr. | Messname | Einheit | min. | max. |")
        A("|---:|---|---|---:|---:|")
        for n, name, unit, lo, hi in steps300:
            A(f"| {n} | {name} | {unit} | {lo} | {hi} |")
        A("")

    A("## 4. Befehlsliste UNIMET 1000/1100 ST\n")
    A("Befehle mit `?` sind Abfragen, solche ohne setzen einen Wert. Die "
      "Spalte *Langform* zeigt die Schreibweise des Handbuchs, bei der die "
      "Großbuchstaben die Kurzform ergeben.\n")
    open_table = False
    for kind, a, b, c in cmds:
        if kind == "head":
            if open_table:
                A("")
            A(f"### {a}\n")
            A("| Befehl | Langform | Bedeutung |")
            A("|---|---|---|")
            open_table = True
        else:
            if not open_table:
                A("| Befehl | Langform | Bedeutung |")
                A("|---|---|---|")
                open_table = True
            A(f"| `{a}` | {b} | {c} |")
    A("")

    A("## 5. Patientenbuchsen-Matrix\n")
    A("Verschaltung per `:SYS:CTRL <Messnummer>` während einer laufenden "
      "Messung. Siehe `research/MESSTECHNIK.md` für die daraus abgeleitete "
      "Hardware-Topologie.\n")
    A("| Funktion | Messnummern |")
    A("|---|---|")
    A("| Einzelne Patientenbuchse PAT1…PAT10 an den Messkreis | `#1161`…`#1170` |")
    A("| Patientenhilfsstrom PATn gegen alle übrigen (REST) | `#1141`…`#1150` |")
    A("| Gruppenkurzschluss zusammenhängender Buchsen | `#1712`…`#1799` |")
    A("")
    A("Gruppenschema `#17<start><ende>`, z. B. `#1712` = PAT 1+2, "
      "`#1720` = PAT 1…10, `#1799` = PAT 9+10.")
    A("Im PDF sind zwei Einträge fehlerhaft: `#1760` erscheint doppelt "
      "(PAT 5+6+7+8+9+10 und PAT 6+7+8+9+10), und die letzte Teiltabelle "
      "ist im Satz verrutscht.\n")

    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(steps)} Prüfschritte, {ncmd} Befehle, "
          f"{len(L)} Zeilen")


if __name__ == "__main__":
    main()
