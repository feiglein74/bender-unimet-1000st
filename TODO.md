# TODO — Bender UNIMET 1000 ST

> ## ⛔ Projekt beendet am 2026-07-31
>
> Die **Messeinrichtung fehlt** — sie saß auf einer ausgebauten Steckkarte,
> zusammen mit der Netzschaltung. Das Gerät war zudem vor dem Verkauf zu einem
> **RS-485-Anzeigeterminal umgebaut** worden. Siehe `research/STAND.md`.
>
> Die folgenden Punkte sind damit **hinfällig**. Sie bleiben stehen, falls
> jemand mit einem vollständigen Gerät dieselben Fragen hat — die Wege dorthin
> waren alle gangbar.
>
> Was tatsächlich erreicht wurde, steht in `research/RELAISMATRIX.md`,
> `research/EPROM_ANALYSE.md` und `research/ANSCHLUESSE.md`.

---

## 1. Klemmender Kontakt: Defekt oder Absicht?

**Status:** offen — beide Deutungen plausibel

Mit abgezogenem Frontmatrix-Stecker erscheint `Diskette error - Press any key`
nur einmal und das BIOS wartet. Eine Matrixposition ist also dauerhaft
geschlossen.

**Deutung A — Defekt.** Verklebte Folientaste, gequetschte Ader, Korrosion.
Muss vor dem Normalbetrieb behoben werden.

**Deutung B — Absicht.** Bender wollte, dass das Gerät unbeaufsichtigt
durchbootet. Dafür spricht:

- Das BIOS-Setup bietet **keine Option**, Fehlermeldungen zu überspringen
  (weder `Halt On Errors` noch `Wait for F1` — siehe `EPROM_ANALYSE.md`)
- **Es wurde keine Batterie gefunden.** Ohne Pufferung meldet das BIOS bei
  jedem Kaltstart einen Konfigurationsfehler und würde jedes Mal warten
- Ein fest gebrückter Kontakt quittiert das automatisch

**Gegenargument zu B:** Eine dauerhaft geschlossene Taste erzeugt
Typematic-Repeat — der Tastaturpuffer läuft mit demselben Scancode voll.
`UNIMET.EXE` müsste das aktiv filtern. Möglich, aber unelegant; es sei denn,
die Position ist im SuperState-Scancode-Table auf etwas Folgenloses gemappt.

### Entscheidende Tests

- [ ] **Gehört das geschlossene Paar zu einer der acht Fronttasten?**
      → ja = Defekt · nein (neuntes Paar) = Absicht
- [ ] **Wo sitzt die Brücke?** Drahtschlaufe direkt am Steckergehäuse zwischen
      zwei Kontakten = eindeutig Absicht. Verbindung erst vorne in der Blende =
      spricht für Defekt.

**Konsequenz:** Ändert nichts am weiteren Vorgehen (Stecker bleibt vorerst ab),
aber es entscheidet, was beim Zusammenbau wieder dran muss.

---

## 2. Matrix kartieren

- [ ] Klemmendes Paar am abgezogenen Gegenstück ermitteln (ohne Tastendruck)
- [ ] Acht Fronttasten einzeln durchklingeln → Zeilen-/Spaltenpaare notieren
- [ ] Logic Analyzer auf die 26 Pins der Stiftleiste, Einschaltvorgang
      mitschneiden → gepulst = Zeile, statisch auf Pull-up = Spalte
- [ ] Matrixgeometrie ableiten, inklusive der unbeschalteten Positionen

⚠️ **Niemals Zeile↔Zeile oder Spalte↔Spalte brücken** — getriebene Ausgänge
gegeneinander.

---

## 3. Ins BIOS-Setup

- [ ] Zeile↔Spalte brücken, bis `F2` erzeugt wird (Live-Feedback: das BIOS
      wartet bei „Press any key", ein gültiges Paar lässt die Anzeige springen)
- [ ] Alle Setup-Seiten fotografieren, **bevor** etwas geändert wird
- [ ] `Diskette A:` → `PCMCIA`
- [ ] `Base Memory:` → 640 KB prüfen · `Display:` prüfen
- [ ] `F10` speichern, Reboot bestätigen

---

## 4. Falls das nicht bootet

- [ ] Diskettenlaufwerk oder **Gotek** an den 34-poligen Stecker der A104-MIO
- [ ] 5 V beschaffen (Gotek ≈ 0,2 A, mechanisches Laufwerk ≈ 1 A) — Kandidat:
      die vierpolige Einspeisung am CPU-Modul, vorher durchmessen
- [ ] `Diskette A:` → `3.5 Inch, 1.44 MB`, DOS von Diskette booten
- [ ] Von dort prüfen: Taucht der im BIOS deklarierte 512-kByte-Flash als
      Laufwerk auf? Hängt am IDE etwas? Ist `UNIMET.EXE` irgendwo vorhanden?

---

## 5. Rückfallebenen

- [ ] **Konfigurations-EEPROM** suchen (8-polig, `93C46`/`93C56`/`24Cxx` nahe
      dem F8680), mit dem T48 auslesen. Leer/Müll beweist die Diagnose;
      langfristig ließe sich die Konfiguration direkt hineinschreiben.
- [ ] **BIOS-Defaults patchen** und neues EPROM brennen — `Diskette A:` als
      Werkseinstellung auf `PCMCIA`. Umgeht die Tastaturfrage vollständig.

---

## 6. Anschlusssituation des CPU-Moduls vollständig aufnehmen

Siehe `research/ANSCHLUESSE.md` (in Arbeit).

---

## 7. Offene Kleinigkeiten

- [ ] **Batterie**: existiert überhaupt eine? Falls ja, wo — falls nein,
      als Befund festhalten
- [ ] **Netzteil** identifizieren, Typenschild und Ausgangsspannungen notieren
- [ ] **Herstellername des CPU-Moduls** — Siebdruck vollständig lesen
      (Lötseite, alle Ränder); bisher nur `…ARDS-B170X4` und im BIOS
      `BOARDS PC µC-BIOS`
- [ ] **Zweiter EPROM-Auslesevorgang** zum Vergleich, wenn der Baustein
      ohnehin einmal draußen ist
- [ ] **Verbliebene Sub-D-9 an der Rückwand**: RS-232 oder RS-485?
      (`NM232DD`-Strang verfolgen)
- [ ] **`disk_104`** weiterhin suchen — Vorbesitzer „PP3 Siersleben",
      mikrocontroller.net-Thread 566576, Bender/Karl-Heinz Rein
