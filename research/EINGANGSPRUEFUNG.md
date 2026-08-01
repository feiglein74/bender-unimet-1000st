# Checkliste zur Erstinbetriebnahme

> **Entstanden, bevor das Gerät eintraf.** Die Reihenfolge folgt dem Grundsatz,
> dass jeder Schritt Information sichert, die ein späterer zerstören könnte.
>
> **Teilweise überholt.** Die Diagnose stützte sich damals auf die Annahme eines
> Kontron MOPS/386A — tatsächlich sitzt im Gerät ein Chips & Technologies F8680.
> Die BIOS-Angaben in Phase 5 gelten deshalb nicht; die zutreffenden stehen in
> `EPROM_ANALYSE.md`. Was das Gerät tatsächlich ist, steht in `STAND.md`.
>
> **Weiterhin brauchbar** ist das Vorgehen als solches: Reihenfolge,
> Sicherheitshinweise, Dokumentationsschritte und die Phasen 0 bis 4. Wer ein
> vergleichbares Altgerät vor sich hat, kann sich daran entlanghangeln.

> **⚠️ Sicherheit.** Das Gerät führt Netzspannung auf die Prüfsteckdose, erzeugt
> DC 500 V für die Isolationsmessung und schaltet Netzspannung auf
> Anwendungsteil-Prüfkreise. Vor jedem Öffnen: Netzstecker ziehen und einige
> Minuten warten (Zwischenkreis-/Siebelkos). Nicht am geöffneten Gerät messen.

---

## Phase 0 — noch vor der Lieferung: Fragen an den Verkäufer

- [ ] Ist die **PCMCIA-Speicherkarte** dabei? (trägt bei älterer Bauart die Kataloge)
- [ ] Welches **Zubehör** liegt bei: Messleitung, aktive Prüfspitze TP2,
      Prüfklemme, Kaltgeräteadapter VK701-7, Nullmodemkabel, Tastaturmodul TM1000,
      Tragetasche?
      *(Diese Liste ist der Lieferumfang des **1100ST** — der des 1000ST ist
      nicht dokumentiert, siehe `MESSTECHNIK.md` 3.6. Als Orientierung brauchbar,
      nicht als Sollzustand.)*
- [ ] **Foto der seitlichen Anschlussleiste** erbitten und prüfen: welche
      Schnittstellen sind bestückt, welche fehlen, gibt es Blindplatten oder
      leere Ausbrüche mit Schraubenlöchern? (→ Unterschied „nie bestückt"
      gegenüber „ausgebaut")
- [ ] Wurde das Gerät **geöffnet**? Ist im BIOS etwas verstellt worden?
- [ ] Liegt ein **Kalibrierprotokoll** oder Serviceunterlagen bei?
- [ ] **Seriennummer** erfragen — wird für jede Rückfrage bei Bender gebraucht.

### Spur zum Vorbesitzer

Auf der Rückseite klebt ein Inventaraufkleber **„PP3 Siersleben"**. Das Gerät
stammt also aus einem Betrieb oder einer Einrichtung, nicht aus Privatbesitz.

- [ ] Verkäufer fragen, **woher** das Gerät stammt und ob Kontakt zur Einrichtung besteht
- [ ] Falls die Quelle greifbar ist, dort nachfragen nach: **PCMCIA-Karte**,
      Zubehörtasche, Handbuch-CD, Kalibrierzertifikat, Prüfprotokollen — und vor
      allem nach einem **Service-/Verwaltungs-PC** mit UniBackup oder UNIData1100.
      Dort könnte das `disk_104`-Updatepaket liegen (siehe `BEFUNDE.md` 5.1.1).

Das ist der aussichtsreichste Weg zum OS-Image nach dem eigenen Flash.

## Phase 1 — dokumentieren, ohne zu öffnen

- [ ] Gerät **allseitig fotografieren**, bevor irgendetwas bewegt wird
- [ ] **Typenschild** abfotografieren: Typ, Seriennummer, Baujahr, Hardwarestand
- [ ] **Kalibriersiegel / Prüfplaketten** fotografieren — Datum notieren, Zustand
      (unversehrt? durchtrennt? nachgeklebt?)
- [ ] **Gehäuseschrauben** ansehen: Schlitze angeschlagen? Farbe/Typ uneinheitlich?
      Fehlende Schrauben? → deutet auf früheres Öffnen hin
- [ ] **Memory-Card-Slot**: Karte gesteckt? Auswerfer in Ruhelage?
- [ ] **Zubehör inventarisieren** und mit der Liste aus Phase 0 abgleichen
- [ ] Alle Fotos ins Projekt unter `fotos/eingang/` ablegen

## Phase 2 — erster Einschaltversuch

Noch ohne Prüfling, nichts an den Buchsen angeschlossen.

- [ ] Netzkabel prüfen (fest montiert), Schutzleiterdurchgang messen
- [ ] Einschalten, **Bildschirm durchgehend filmen oder abfotografieren** —
      die POST-Meldungen laufen schnell durch
- [ ] Notieren: erscheint `Press <F2> to enter Setup`?
- [ ] Notieren: identische Fehlermeldung wie auf dem Verkaufsfoto, oder eine andere?
- [ ] Notieren: Zeigt der POST eine **Speichergröße über 640 K**? (Hinweis auf
      Erweiterungs-RAM)
- [ ] Auf Geräusche/Gerüche achten; bei Knistern oder Geruch sofort abschalten

**Bewertung:** Läuft der POST durch und bleibt nur der `Diskette error`, ist die
Diagnose aus `BEFUNDE.md` bestätigt und die Sache voraussichtlich eine reine
BIOS-Einstellung.

### Tastatur — erst klären, welcher Weg gilt

Das Tastaturmodul **TM1000 ist keine Standardtastatur**: Kurzhub-/Folienlayout
mit deutschem QWERTZ, aber ohne F1–F12-Reihe, ohne Esc und ohne Ziffernblock;
die oberste Reihe dupliziert die Gerätefunktionstasten der Frontblende. Es wird
in den Gehäusedeckel geklemmt und per Rundstecker an die **Tastaturbuchse am
Gerät** angeschlossen (Handbuch 4.2.2).

**Offen ist, worauf diese Buchse führt** — das MOPS hat beide Möglichkeiten:

| | Hinweis darauf | Konsequenz |
|---|---|---|
| **X4** (AT/PS-2) | Buchse hat **5 oder 6 Pins** | Jede PS/2-Tastatur funktioniert dort. BIOS-Zugang ohne Öffnen. |
| **X11** (Tastaturmatrix, 26 pol.) | Buchse hat **deutlich mehr Pins**, dickes vieladriges Kabel | Keine Standardtastatur an dieser Buchse. BIOS-Zugang nur über PS/2 **intern an X4**, also mit Öffnen. |

Für X11 spricht, dass Kontron eigens eine Matrix-Schnittstelle, eine
Matrix-Keyboard-BIOS-Extension und das Werkzeug `P389MTX` zum Programmieren der
Dekodiertabelle anbietet — gemacht für genau solche kundenspezifischen
Folientastaturen.

**Wahrscheinlichste Aufteilung:** Fronttasten auf **X11** (8 Tasten, intern,
kurzes Flachband), TM1000 auf **X4** (ca. 60 Tasten über steckbares Außenkabel —
als Matrix bräuchte das 26 Adern, als AT-Tastatur vier). Die
Matrix-BIOS-Extension übersetzt Matrixanschläge in normale Scancodes und legt
sie in denselben BIOS-Tastaturpuffer; für DOS sind beide dann *eine* Tastatur.

- [ ] **Kostet nichts, zuerst probieren:** beim Einschalten die **`F2`-Taste auf
      der Frontblende** drücken. Liefert die Matrix echte Scancodes, kommt man
      damit schon ohne jede Tastatur ins Setup.
- [ ] **Pins an der Tastaturbuchse zählen** → entscheidet den Weg
- [ ] PS/2-Tastatur anstecken und `F2` probieren
- [ ] Kommt das Phoenix-Setup: **alle Menüs abfotografieren**, dann
      **nichts speichern** und mit *Exit Discarding Changes* verlassen

Vorzubereiten: gebrauchte **PS/2-Tastatur** plus **PS/2→AT-Adapter**. Wird in
beiden Fällen gebraucht — im Matrix-Fall intern an X4. USB funktioniert nicht:
kein USB am Board, kein USB-Legacy im 386er-BIOS.

## Phase 3 — öffnen und begutachten

- [ ] Netzstecker ziehen, einige Minuten warten
- [ ] Deckel ab, **sofort Übersichtsfotos** vom gesamten Innenaufbau, bevor
      irgendetwas angefasst wird
- [ ] Jede Baugruppe einzeln fotografieren, **jeden Steckverbinder im gesteckten
      Zustand** — falls später etwas abgezogen wird, weißt du, wie es saß

Worauf achten:

- [ ] **Batterie**: Typ, Spannung messen (Soll 3,0–4,0 V, empfohlen 3,6 V).
      **Auf Auslaufspuren prüfen** — weißes/grünes Kristallwachstum, korrodierte
      Leiterbahnen. Bei Leckage: nichts einschalten, erst reinigen und neutralisieren.
- [ ] **Fremdlötstellen** — bleifrei/glänzend gegen matt, Flussmittelreste,
      nachgelötete Bauteile, Drahtbrücken
- [ ] **Lose oder falsch sitzende Flachbandkabel**, verpolte Pfostenstecker
- [ ] **Verschmorte Bauteile**, gewölbte Elkos, Brandspuren
- [ ] **Fehlende Abschirmbleche oder Isolierfolien** — bei einem Gerät mit
      Netzspannung auf Prüfkreisen sicherheitsrelevant
- [ ] **Relais** der Messmatrix: verkohlte Kontakte, klebende Anker
- [ ] Sitzt zusätzlich ein **IDE-Medium** (CF-Karte, 2,5"-Platte) im Gerät?
- [ ] **Netzteil identifizieren**: Hersteller, Typ, Ausgangsspannungen vom
      Typenschild abfotografieren. Erwartet wird ein OEM-Schaltnetzteilmodul mit
      Weitbereichseingang (90–264 V) und niedrigem Ableitstrom, **kein**
      PC-Netzteil — ein Prüfgerät für Ableitströme kann sich die Y-Kondensatoren
      eines Standard-PC-Netzteils nicht leisten. Ggf. mehrere getrennte
      Versorgungen für PC-Teil und Messteil. Bei einem Standardmodul wäre ein
      Defekt vergleichsweise leicht zu beheben.

## Phase 4 — Board identifizieren, Steckverbinder abgleichen

- [ ] **Boardaufdruck lesen**: Steht dort tatsächlich `MOPS/386A` bzw. `JUMPtec`?
      Andere MOPS-Variante möglich — dann gilt deren Handbuch, nicht unseres.
- [ ] **PC/104-Stapel** dokumentieren: Wie viele Module? Welche? Die VGA-Karte
      mit Chips-&-Technologies-Controller muss dabei sein.
- [ ] Steckverbinder gegen die folgende Tabelle prüfen (Quelle: Kontron
      MOPS/386A User's Guide Rev. 1.5, Anhang E). **Pin 1 ist auf der
      Board-Unterseite durch ein rechteckiges Pad markiert.**

| Stecker | Funktion | Raster / Pins |
|---|---|---|
| X1A / X1B | PC/104-Bus (XT- bzw. AT-Teil) | 2,54 mm, 64 / 40 pol. |
| X1C | Power Connector | 2,54 mm |
| **X4** | **Tastatur & Feature — hier liegt auch die Batterie** | 2,54 mm, 10 pol. |
| **X5** | **IDE (für das Backup!)** | **2 mm, 44 pol.** |
| X6 | Floppy | 2,54 mm, 26 pol. |
| X7 | Parallel / LPT | 2 mm, 16 pol. |
| X8 | DOT-Matrix-LCD | 2,54 mm, 10 pol. |
| X9 | PS/2-Maus (nicht auf Standardboards) | 2 mm, 8 pol. |
| X10 | Serielle Schnittstelle COM A | 2,54 mm, 10 pol. |
| X11 | Tastaturmatrix | 2 mm, 26 pol. |
| X12 | Ethernet | 8 pol. |

**X4 Pinbelegung** (für Tastatur und Batterie):

| Pin | Signal | Funktion | 5-pol. DIN | 6-pol. MiniDIN (PS/2) |
|---:|---|---|---:|---:|
| 1 | Speaker | Lautsprecher | | |
| 2 | GND | Masse | | |
| 3 | /RESIN | Reset-Eingang | | |
| 4 | /KBLOCK | Tastatursperre | | |
| 5 | KBDAT | Tastaturdaten | 2 | 1 |
| 6 | KBCLK | Tastaturtakt | 1 | 5 |
| 7 | GND | Masse | 4 | 3 |
| 8 | VCC | +5 V | 5 | 4 |
| **9** | **BATT** | **Batterie ein (3,6 V)** | | |
| 10 | PWRGOOD | Powergood | | |

- [ ] **Tastatur anschließen** (5-pol. DIN oder PS/2 über Adapterkabel an X4)

### Vorrangig: die Anschlussleiste

Auf Verkaufsfotos sind **zwei der vier Positionen leer** — oben der Centronics
und unten ein Sub-D-9. Zwei Positionen sind noch bestückt. Zu klären:

- [ ] **Welche Schnittstelle ist die verbliebene Sub-D-9 — RS-232 oder RS-485?**
      Beschriftung der Anschlussleiste lesen; falls unbeschriftet, das Kabel
      innen bis zum Board verfolgen. **Davon hängt ab, ob das dokumentierte USP
      direkt nutzbar ist.**
- [ ] Sind die **internen Kabel zu den leeren Positionen noch vorhanden**?
      Baumelnde Pfostenstecker oder Pigtails → Nachrüsten ist trivial.
      Abgeknipst oder ausgelötet → mehr Aufwand.
- [ ] Sitzen die Anschlüsse auf einer **eigenen Interface-Platine**? Wenn ja:
      ist sie noch da, teilbestückt, oder ganz entfernt?
- [ ] Ausbrüche fotografieren: saubere Blindplatte oder freiliegende Öffnung
      mit Schraubenlöchern und Kabelresten?

**Falls die RS-232 fehlt**, gibt es zwei Wege: COM A intern an **X10** des
MOPS herausführen (Kontron-Adapterkabel KAB-DSUB9-2, 2,54 mm 10-polig) — für
Backup und BIOS-Arbeit ohne angeschlossenen Prüfling unbedenklich, für den
Messbetrieb fehlt dann aber die galvanische Trennung. Oder über die RS-485
gehen; der Rückseitenaufkleber nennt dort das Bender-SCPI-Protokoll, also
vermutlich dieselbe Befehlsfamilie (siehe `MESSTECHNIK.md` 3.6).

### Verdrahtung aufnehmen — welcher Anschluss geht wohin?

Das ist nirgends dokumentiert (siehe `MESSTECHNIK.md` 3.6). Beim offenen Gerät
lässt es sich aber ablesen und ist die Grundlage für alles Weitere:

- [ ] **PC/104-Stapel von der Seite fotografieren**, Module zählen und von oben
      nach unten durchnummerieren
- [ ] Auf jeder Nicht-Kontron-Platine **Aufdruck und Sachnummer** notieren —
      Bender-eigene Baugruppen tragen eigene Nummern und meist einen Datumscode
- [ ] Für **jeden** belegten Anschluss X4…X12 notieren, wohin das Kabel führt
- [ ] **X5 (IDE) prüfen: belegt oder frei?** Falls belegt — wohin geht es?
      Zum PCMCIA-Slot? Zu einem versteckten Speichermedium?
      **Davon hängt die Backup-Strategie in Phase 6 ab.**
- [ ] Anbindung des **PCMCIA-Slots** verfolgen: IDE-Bus, eigener PC/104-Controller
      oder Bender-Baugruppe?
- [ ] Geht ein Kabel von **X11 (Tastaturmatrix)** zur Fronttastatur? (erwartet)
- [ ] Ist **X12 (Ethernet)** überhaupt bestückt?

## Phase 5 — BIOS-Setup

`F2` beim Boot. Zielkonfiguration:

| Menü | Einstellung | Wert |
|---|---|---|
| Main → JUMPtec Flash Disk | **INT 13h Drive Mapping** | **Drive 80** (= C:) |
| Main → JUMPtec Flash Disk | **Erase On Next Boot** | **Disabled** ⚠️ prüfen! |
| Main → JUMPtec Flash Disk | Write Protect | Disabled (bis das Backup steht) |
| Main | Legacy Diskette A / B | Not installed (kein Laufwerk vorhanden) |
| Boot | Boot sequence | C: then A: |
| Advanced → I/O Device Config | Hard disk controller | Enabled |
| Advanced | Large Disk Access Mode | DOS |
| Advanced | Halt On Errors | No |
| Main | System Date / Time | nach Batteriewechsel neu stellen |

- [ ] Vor dem Speichern **alle Menüs abfotografieren** — dokumentiert den
      Auslieferungszustand
- [ ] Exit → **Exit Saving Changes**

## Phase 6 — Backup, bevor irgendetwas anderes passiert

- [ ] Bootet DOS: **mehrfach `Strg+C`**, Abbruch der Batchdatei mit **`J`**
      bestätigen → DOS-Prompt statt `UNIMET.EXE`
- [ ] `DIR C:\ /S` → Verzeichnisbaum fotografieren/abtippen
- [ ] CF-Karte oder 2,5"-Platte an **X5** (44 pol., 2 mm) anschließen
- [ ] Kompletten Inhalt kopieren, Karte am PC auslesen, Image sichern
- [ ] Erst **danach** experimentieren

Details und Hintergründe in `research/BEFUNDE.md`.

## Tabu

- ❌ **`Erase On Next Boot` aktivieren** — löscht DOS und `UNIMET.EXE`
- ❌ **FDISK oder andere Partitionierer** auf der Silicon-Disk
- ❌ **Format C:**
- ❌ Firmware-Update versuchen, solange kein Backup existiert
- ❌ Am geöffneten, eingeschalteten Gerät hantieren

## Danach: erste Funktionsprüfung ohne Zubehör

Sobald `UNIMET.EXE` startet, gibt es einen eingebauten Selbsttest — er braucht
kein Zubehör und ist der schnellste Weg zu wissen, ob das Messteil lebt:

`Hauptmenü → F5 Systemverwaltung → F4 System Info → F1 Systemselbsttest → F1 intern`

Voraussetzungen laut Handbuch:

- [ ] an **geerdeter Netzversorgung** (kein IT-Netz)
- [ ] **keine Prüflinge oder Adapter** angeschlossen
- [ ] **kein geerdeter Drucker** angeschlossen
- [ ] Dauer ca. 30 s; nicht bestandene Prüfschritte werden mit `*` markiert
- [ ] Ergebnis fotografieren, Detailinformationen über `<<` aufrufen

Der erweiterte Selbsttest setzt die Testbox **TB3** voraus, die wir nicht haben.

## Danach: Gerätestand feststellen

**Am schnellsten direkt am Bildschirm** — keine Schnittstelle nötig:

`Hauptmenü → F5 Systemverwaltung → F4 System Info`

Diese Maske zeigt **Software-, Firmware- und Hardwareversion sowie den Typ des
verbauten PC-Moduls**. Beim 1100ST steht dort z. B. `PC: ETX-PM 246MB`; bei
deinem 1000ST muss dort das PC/104-Board erscheinen. Damit ist die Plattform
belegt, ohne das Gerät zu öffnen.

- [ ] `System Info` aufrufen und **abfotografieren**

Alternativ über RS232 (9600 **7E2**, Nullmodem, `DC3` senden):

- [ ] `:IDNF?` → Softwareversion (≥ 4.20 nötig für TP1010 und UniBackup)
- [ ] `:IDNH?` → Hardwareversion
- [ ] `:IDNS?` → Seriennummer
- [ ] `:IDPC?` → PC-Hardwareversion

Damit klärt sich unter anderem, ob dein Gerät **DC-Ableitströme** messen kann —
siehe `research/MESSTECHNIK.md`, Abschnitt 3.2. Befehlsreferenz in
`research/RS232_PROTOKOLL.md`.
