# Arbeitsstand — abgeschlossen 2026-07-31

> ## 🔚 Abschließende Deutung: Das Gerät wurde umgebaut, nicht ausgeschlachtet
>
> **Es gibt an mehreren Stellen gezielt gefräste Leiterbahnunterbrechungen** —
> unter einer Widerstandsgruppe an zwei Punkten, und auf der Verteilerplatine
> wurde der **V24-Teil** (RS-232) auf dieselbe Weise stillgelegt.
>
> Wer Teile stiehlt, lötet aus oder knipst ab. Wer mit dem Fräser an definierten
> Punkten auftrennt, **verändert eine Funktion mit Absicht und Sorgfalt.**
>
> Zusammen mit dem Rückwandaufkleber ergibt das ein stimmiges Bild:
>
> > **Datensichtgerät für RS 485 Schnittstelle — Bender SCPI Protokoll**
>
> Der Aufkleber beschreibt nicht, was das Gerät **war**, sondern **wozu es
> umgebaut wurde**: ein Anzeigeterminal für einen Bender-RS-485-Bus.
>
> | Beobachtung | Passt zum Umbau |
> |---|---|
> | Messkarte ausgebaut | ein Anzeigegerät misst nicht |
> | Centronics und ein Sub-D-9 an der Rückwand entfernt | nicht mehr gebraucht |
> | V24-Teil weggefräst | RS-232 abgeschaltet, **RS-485 bleibt** |
> | Widerstandsgruppe aufgetrennt | weitere stillgelegte Funktion |
> | Patientenbuchsen unbeschaltet | für ein Terminal sinnlos |
> | PCMCIA-Karte fehlt | dort lag die **Anzeigesoftware**, nicht `UNIMET.EXE` |
>
> **Konsequenz:** `disk_104` und `UNIMET.EXE` waren auf diesem Gerät zuletzt gar
> nicht mehr installiert. Die Suche danach hätte es nie in den
> Auslieferungszustand zurückversetzt. Der Vorbesitzer („PP3 Siersleben") hat es
> als Anzeige an einer Bender-Anlage betrieben, nicht als Prüfgerät.
>
> Das erklärt auch, warum nichts nach Gewalt aussah: **Es wurde nichts
> kaputtgemacht, es wurde umgewidmet.**

---

# Arbeitsstand — 2026-07-30

Gerät ist eingetroffen und geöffnet. Erste Sichtprüfung ohne Befund: keine
aufgeblähten Kondensatoren, keine Schmorspuren, kein Geruch.

## Hardware — bestätigt am offenen Gerät

**CPU-Modul** — Aufdruck `…ARDS-B170X4`

- **Chips & Technologies F8680 „PC/CHIP"**, `TM1478A`, Datumscode `9444`, **14 MHz**
  → 8086-/XT-klassiger Ein-Chip-PC, **kein** 386SX, **kein** Kontron MOPS
- 2× NEC `424800-70` DRAM (zusammen 1 MB, davon 640 K konventionell)
- NEC `D43256AGU-10L` SRAM · `LT1137ACG` RS-232-Transceiver
- `ICD2027SC-1` Taktgeber, Quarz 14,318 MHz · `MC34063AP1` Schaltregler
- Glue-Logik unter dem EPROM-Sockel: `HCT244`, `HCT138`, `14093B`
- **BIOS-EPROM `NM27C010Q`**, Keramik-DIP32, gesockelt, Etikett `V: 0.91`
  → **ausgelesen und analysiert**, siehe `EPROM_ANALYSE.md`

**Multi-I/O `A104-MIO`, VER: B**

- `UMC UM82C863F` Super-I/O, `PAL16L8ACN`, Quarz 24,000 MHz
- RS-232-Treiber `GD75188`/`GD75189A`/`MC1488`/`SN75189`
- Stecker: 2× 10-pol (RS-232), 26-pol (LPT), **34-pol (Diskette)**, **40-pol (IDE)**
- Viele Jumper, Konfiguration undokumentiert

### ⚠️ Schlüsselbefund 2026-07-31: PCMCIA-Karte ist das Bootmedium

Auf der Rückseite des CPU-Moduls sind **drei Bestückungsplätze leer**:

| Platz | Bauform | Deutung |
|---|---|---|
| `U6`, `U7` | DIP, **28 Pins**, kein Typaufdruck | **offen** — max. 64 KB je Baustein, siehe unten |
| `U16` | quadratisch, **11 Pads je Seite = PLCC-44** | vermutlich Steuerlogik/PLD |

**Zur Arithmetik:** Ein 28-poliger Speicherplatz fasst in dieser Ära höchstens
64 KB (`27C512`, `28F512`, `62512`). Zwei davon ergeben 128 KB — **nicht** die
512 kByte aus dem BIOS-String. `U6`/`U7` sind also *nicht* der dort genannte
Flash.

**Bessere Lesart des BIOS-Strings `512 kByte Flash ab 2 MB`:** Er beschreibt
**die PCMCIA-Karte selbst** — eine 512-kByte-Flash-Karte, vom F8680 über sein
Speicherkartenfenster ab Adresse 2 MB eingeblendet.

**Konsequenz:** Das Bootmedium dieses Geräts ist **die PCMCIA-Karte**. Damit
erklärt sich alles widerspruchsfrei — `Diskette A: = PCMCIA` war die einzig
mögliche Einstellung, die Karte fehlt, also kein Bootmedium, Rückfall auf A:,
`Diskette error`. Der BIOS-String benennt das fehlende Teil sogar samt Größe.

`U6`/`U7`/`U16` bleiben eine nicht gelieferte Ausbaustufe unbekannten Zwecks —
denkbar SRAM (`62256`) für eine gepufferte RAM-Disk oder EPROM-Erweiterung.
Zu prüfen: Führen Pads von `U16` zu `U6`/`U7`? Dann gehören sie zusammen.

**Und weiter:** Auf der Karte lag nicht nur die Datenbank, sondern das
**komplette System** — MS-DOS 5.0 und `UNIMET.EXE`. Deshalb spricht das
Handbuch beim 1000ST vom „PCMCIA-**Laufwerk**", und deshalb bekam es beim
Update das Verzeichnis `disk_104` aufgespielt.

Ohne Karte hat die Maschine **keine Software**. Rechner, BIOS und vermutlich
auch das Messteil sind in Ordnung — es fehlt buchstäblich die Festplatte.

**Damit rückt `disk_104` von „wäre schön" auf „ist der Kern der Sache".**

Zu prüfen: Führen Pads von `U16` zu `U6`/`U7`? Dann gehören sie als
Options-Gruppe zusammen. Führen sie stattdessen zum PCMCIA-Steckplatz, wäre
`U16` eher ein Kartenpuffer.

**Rückseite desselben CPU-Moduls** — nicht etwa eine eigene Platine

- AMP-**PCMCIA-Steckplatz** = frontseitige „Memory Card", **Karte fehlt**
- Zahlreiche Jumper `JP1`…`JP26`, `74HCT245`, `U6`/`U7` unbestückt
- **Werksseitige Änderung (ECO):** axiales Bauteil auf Kapton, Kupferlackdraht
  quer zum Steckplatz. Sauber ausgeführt, gealtert. **Nicht anfassen.**

Das Modul trägt also F8680-Seite und PCMCIA-Seite auf einer Platine — beide
Fotos zeigen dieselbe Baugruppe `B170X4`.

**Weitere Baugruppen**

- Verteilerplatine mit **CCFL-Inverter `TDK PCU-554`**, `74HCT14N`,
  **`NM232DD`** (Murata/Newport — die galvanische Trennung der RS-232)
- **Relaisplatine mit eigenem Bussystem und Steckplätzen für weitere Karten**
- Anbindung ans CPU-Modul über **14-poliges Flachbandkabel** (siehe
  `MESSTECHNIK.md` 3.4a)

**Stecker am unteren Rand des CPU-Moduls:** ca. 26-, 20- und 14-polig.
Der 14-polige geht zur Relaisplatine.

**Netzteil, Batterie:** nicht identifiziert. Batterie bislang nicht gefunden —
irrelevant, da der F8680 seine Konfiguration im EEPROM hält und das BIOS bei
leerer Batterie eine eigene Meldung ausgäbe (`System battery is dead`), die
nicht erscheint.

## Frontblende — Tastatursituation

- **Kein extern anschließbarer Tastaturanschluss.** Diese Variante hat die
  Option nicht; das Referenzgerät mit TM1000 schon.
- Die Fronttasten hängen als **Matrix** an einem **26-poligen IDC-Stecker
  (2×13)** am linken Rand des CPU-Moduls. Statt Flachband sind **einzelne Adern
  in etwa 6–10 der 26 Positionen eingepresst**; der Rest ist leer.
- Das deckt sich mit dem F8680 Design Guide: SuperState-Code tastet die Matrix
  direkt ab, die serielle Tastaturschnittstelle (`KBCLK`/`KBDATA`) bleibt
  ungenutzt.
- **Die leeren Positionen sind die restliche Matrix** — dort hängen beim TM1000
  die übrigen ~56 Tasten inklusive Pfeiltasten, Esc und F-Tasten.

## ⛔ Schlüsselbefund 2026-07-31: Die Messkarte fehlt

**Das Gerät kann in diesem Zustand nicht messen — unabhängig von jeder Software.**

Nach vollständiger Durchsicht aller Baugruppen ist **keine Messkette vorhanden**:
keine Operationsverstärker, keine Spannungsreferenz, kein A/D- oder
V/F-Wandler, keine Abgleichtrimmer. Weder auf der Bestückungs- noch auf der
Lötseite irgendeiner Platine.

**Der Beweis:** Die Messleitungen der Prüfsonde führen von der Frontplatte
direkt auf einen **Messkarten-Anschluss, der unbelegt ist.**

### Vollständige Baugruppenbilanz

| Baugruppe | Funktion | Messfähigkeit |
|---|---|---|
| CPU-Modul `B170X4` | F8680-Rechner | — |
| `A104-MIO` | Schnittstellen | — |
| Relaisplatine | Schaltmatrix, Treiber, Trafo, `LTC485` | — |
| Verteilerplatine | Displayversorgung, galvanische Trennung | — |
| Schaltnetzteil | Versorgung | — |
| **Messkarte** | **FEHLT** | — |

### Weitere Hinweise auf eine sparsame Grundkonfiguration

- **Die zehn Patientenbuchsen sind rückseitig nicht angeschlossen** — die
  Anwendungsteil-Messung war eine nicht bestellte Option
- **`U6`, `U7`, `U16`** auf dem CPU-Modul unbestückt
- Frontseitig beschaltet ist nur die **Prüfsteckdose** — mit **zwei Drähten je
  Pol** (2× N, 2× L, 1× PE), also **Vierleitermessung**: ein Paar führt den
  Strom, das andere greift die Spannung ab. So misst man Schutzleiterwiderstände
  im Milliohm-Bereich.
- dazu zwei Prüfbuchsen für die Isolationsmesssonde

### Umfang des Verlusts — präzisiert 2026-07-31

Weitere Messungen zeigen: Die fehlende Karte trug **mehr als nur die Messkette**.

- **Die Relaisplatine hat 11 Relais — keines davon führt L oder N.**
  Die Prüfschritte verlangen aber Netzleiter auftrennen (`Netzl. offen`, 83
  Schritte), Phasenlage tauschen (`Phase rev.`, 112 Schritte) und Schutzleiter
  unterbrechen (`PE offen`, 85 Schritte). Diese Netzschaltung saß folglich
  **auf der fehlenden Karte**.
- **Der I²C-Bus wird über den Kartenanschluss geführt.** Ohne Karte ist er
  unterbrochen — deshalb findet ein Busscan am 14-poligen Stecker keine
  `PCF8574`, obwohl die Bausteine versorgt sind und der Bus sauber auf 5 V
  liegt. *(Umgehung für Experimente: Bus Pirate direkt an Pin 14/15 eines
  `PCF8574` klemmen.)*
- Die **Prüfsteckdose** führt zwei Adern je Pol. Eine geht zum Netzzweig, die
  zweite mutmaßlich zum Kartenanschluss.

**Auf der Karte saßen also:** Netzschaltung (L, N, Phasenlage,
Netzleiter-Unterbrechung), die vollständige Messkette (Verstärker, Referenz,
Wandler), die Ansteuerung der 500-V-Erzeugung und der Durchlauf des I²C-Bus.

**Das war die Hauptbaugruppe des Geräts.** Die elf Relais auf der Relaisplatine
schalten den Rest: Messpfade, Sondenanbindung und die zehn Patientenbuchsen,
die bei diesem Gerät ohnehin nicht bestückt sind.

Was bleibt, ist ein Gehäuse mit Rechner, Anzeige und Hilfsplatine.

### Konsequenz für das Projekt

Es fehlen **zwei** Dinge, nicht eines:

1. **Das Bootmedium** — PCMCIA-Karte mit DOS und `UNIMET.EXE` bzw. `disk_104`
2. **Die Messkarte** — Bender-Spezialanfertigung, kein Standardteil,
   keine bekannte Bezugsquelle

Punkt 2 ist die härtere Nuss. Realistische Wege: ein vollständiges
Zweitgerät als Teilespender, oder das Gerät als **Plattform** nutzen —
Gehäuse, Frontplatte, Relaismatrix, Trafo und Netzteil sind vorhanden und
verstanden, die Relaisansteuerung über I²C ist dokumentiert. Ein eigener
Messkopf plus eigener Controller wäre technisch schlüssig.

### Noch zu dokumentieren

- Bauform und Pinzahl des **Messkarten-Anschlusses**
- Beschriftung im Siebdruck daneben (`X…`, Sachnummer, Kartenname)
- Welche Leitungen dort auflaufen: nur die Prüfsonde, oder auch Versorgung,
  I²C, Signale von der Relaisplatine?

## Der Blocker (Bootmedium)

**`F2` fürs BIOS-Setup lässt sich nicht auslösen.** Keine Fronttaste bewirkt
etwas — auch nicht bei laufender `Diskette error - Press any key`-Schleife.

### ✅ BESTÄTIGT am 2026-07-31: klemmende Taste

**Test:** Frontmatrix-Stecker abgezogen, eingeschaltet.
**Ergebnis:** Die Meldung erscheint **einmal** und das BIOS **wartet auf eine
Taste**.

Damit ist die Ursache eindeutig: eine **dauerhaft geschlossene Matrixposition**
in der Frontblende quittierte jedes „Press any key" sofort. Folgen: gestapelte
Fehlermeldung, weggeklicktes `Press <F2> to Setup`-Fenster, wirkungslose
Tastendrücke.

**Die BIOS-Tastatureingabe selbst funktioniert einwandfrei.**

Der klemmende Kontakt ist ein **echter Defekt** (verklebte Folientaste,
gequetschte Ader, Korrosion) und muss vor dem Normalbetrieb behoben werden.
Für die Inbetriebnahme reicht der abgezogene Stecker.

### Ursprüngliche Hypothese (jetzt bestätigt)

Auf dem Bootfoto steht `Diskette error - Press any key` **rund zwölfmal
untereinander**. Bei einem BIOS, das auf eine Taste wartet, dürfte die Meldung
genau einmal erscheinen. Dass sie sich stapelt, deutet darauf hin, dass etwas
sie fortlaufend quittiert — etwa eine **dauerhaft geschlossene Matrixposition**.
Das würde auch erklären, warum eigene Tastendrücke wirkungslos bleiben und
warum das `Press <F2> to Setup`-Fenster nie stehen bleibt.

## Nächste Schritte, in dieser Reihenfolge

1. **Einschalttest mit abgezogenem Frontmatrix-Stecker.**
   Erscheint die Meldung jetzt **einmal und bleibt stehen** → klemmende Taste
   bestätigt. Stapelt sie sich weiter → Frontblende unschuldig.
2. **Gegenstück kartieren** (Gerät aus): Durchgangsprüfer an den abgezogenen
   Stecker, jede der acht Fronttasten drücken, notieren welche zwei Positionen
   schließen. → acht Ankerpunkte im Raster.
3. **Stiftleiste mitschneiden** (Logic Analyzer, 26 Kanäle): Welche Leitungen
   werden reihum gepulst → **Zeilen**. Welche nur gelesen → **Spalten**.
   → Matrixgeometrie vollständig, inklusive unbeschalteter Positionen.
4. **Tasten gezielt erzeugen:** Zeile↔Spalte brücken. Damit `F2` ins Setup.
   ⚠️ **Niemals Zeile↔Zeile oder Spalte↔Spalte brücken** — getriebene Ausgänge
   gegeneinander.
5. **Im Setup** (`F2`, Bedienung siehe `EPROM_ANALYSE.md`):
   `Diskette A:` → **`PCMCIA`**, `Base Memory:` → 640 KB, dann **`F10`**.
6. **Falls das nicht bootet:** Diskettenlaufwerk oder Gotek an den 34-poligen
   Stecker der A104-MIO, `Diskette A:` → `3.5 Inch, 1.44 MB`, DOS von Diskette
   booten. Stromversorgung ~5 V nötig (Gotek ≈ 0,2 A, echtes Laufwerk ≈ 1 A).

### Rückfallebenen

- **Konfigurations-EEPROM** suchen (8-polig, `93C46`/`93C56`/`24Cxx` nahe dem
  F8680) und mit dem T48 auslesen. Leer/Müll würde die Diagnose beweisen;
  langfristig ließe sich die Konfiguration direkt hineinschreiben.
- **BIOS-Defaults patchen** und neues EPROM brennen — `Diskette A:` als
  Werkseinstellung auf `PCMCIA`. Umgeht die Tastaturfrage vollständig.

## Werkzeuge, die zur Verfügung stehen

XGecu T48 Programmiergerät · Logic Analyzer · Multimeter

## Langfristig

Der **14-polige Strang zur Relaisplatine** ist der ideale Messpunkt, um die
Registerbelegung der Messhardware zu rekonstruieren — vollständig erfassbar,
und mit den 427 dokumentierten Prüfschritten sowie dem SCPI-Befehlssatz lassen
sich einzelne Schaltzustände gezielt auslösen und mitschneiden. Setzt ein
bootendes Gerät voraus.
