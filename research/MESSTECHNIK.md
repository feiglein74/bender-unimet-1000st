# Prüf- und Messtechnik des UNIMET 1000 ST

**Was dieses Dokument enthält:** die technischen Daten des Geräts aus den
Herstellerunterlagen, die daraus und aus Messungen am offenen Gerät
rekonstruierte Architektur, und eine Einschätzung, was davon nachbaubar wäre.

**Reihenfolge:** Abschnitte 1 bis 3.4 stammen aus der Auswertung der
Herstellerunterlagen, bevor das Gerät verfügbar war. Ab 3.5 folgen Befunde vom
geöffneten Gerät. Abschnitt 3.6 enthält frühere Vermutungen, die sich als falsch
erwiesen haben — sie bleiben zur Nachvollziehbarkeit stehen.

**Kernaussage:** Das Messteil wurde über zwei getrennte Wege angesprochen — die
Relaismatrix per I²C über die zweckentfremdeten Tastaturpins des Prozessors, die
Messkarte per RS-485 über den UART. Die Messkarte selbst fehlt im untersuchten
Gerät.

Ausgewertet aus `docs/bender/Bedienungshandbuch_UNIMET_1000ST_1100ST_de.pdf` und
`docs/bender/UNIMET_Interface_Handbuch_de.pdf` (TGH1315/01.2006).

## 1. Was es gibt — und was nicht

**Nicht öffentlich:** Schaltpläne, Bestückungspläne, Serviceunterlagen des Messteils.
Bender/BENTRON hat dazu nie etwas publiziert; Kalibrierung und Abgleich waren
ausdrücklich dem Hersteller vorbehalten.

**Öffentlich und brauchbar — überraschend viel:**

1. **Vollständige technische Daten** = die Spezifikation, gegen die man bauen würde.
2. **Die Fernsteuerbefehle der Relaismatrix** im Interface-Handbuch. Weil jede
   Verschaltung über eine eigene Messnummer angesteuert wird, lässt sich die
   **Schalttopologie aus der Befehlsliste rekonstruieren** — ohne Schaltplan.

## 2. Technische Daten (Spezifikation)

| Messgröße | Wert |
|---|---|
| **Schutzleiterwiderstand** | Prüfspannung max. 14 V Netzfrequenz; Kurzschlussstrom ca. 10 A (Standard) bzw. 25 A ±10 % im Bereich 0,001–0,3 Ω (25-A-Version); Bereich 0,001–29,999 Ω |
| Genauigkeit | 0,001–0,2 Ω: ±0,02 Ω · 0,2–29,999 Ω: ±10 % v.M. |
| **Ableit-/Ersatzableitströme (direkt)** | 0,001–19,999 mA; Prüfspannung ≈ Netzspannung/Netzfrequenz; max. Prüfstrom 3,5 mA |
| Genauigkeit | bis 9,999 mA: ±5 % v.M. ±2 Digit · 10–19,999 mA: ±7 % ±2 Digit |
| **Differenzstromverfahren** | 0,02–19,99 mA; ±5 % v.M. ±5 Digit |
| **Patientenhilfsströme** | 0,001–19,99 mA; ±5 % v.M. ±2 Digit |
| **Isolationswiderstand** | Prüfspannung ca. **DC 500 V**, max. Prüfstrom 2,5 mA; 0,01–299,99 MΩ; ±5 % v.M. ±2 Digit |
| **Spannungsmessung** | 90–264 V, 50–60 Hz, ±2,5 % ±2 Digit |
| **Laststrommessung** | 0,005–16 A, ±2,5 % ±3 Digit |
| **Scheinleistung** | 0,005–3,8 kVA, ±5 % ±5 Digit |
| Versorgung | 90–264 V AC, 45–65 Hz, max. 40 VA Eigenverbrauch |
| Prüflingslast | max. 16 A / 3800 VA bei 230 V |
| Sonstiges | Schutzklasse I, IP20, 0…+50 °C, ca. 380×400×135 mm, ca. 10 kg |
| Kalibrierintervall | 24 Monate (Handbuch) bzw. 36 Monate (Bender-Blog, neuere Angabe) |

## 3. Rekonstruierte Schalttopologie der Patientenmatrix

Aus Interface-Handbuch Kap. 5.3. Verschaltung erfolgt per `:SYS:CTRL <Messnummer>`.

**Einzelne Patientenbuchse an den Messkreis** (Patientenableitstrom, auch mit
Netzspannung am Anwendungsteil):

```
PAT1 … PAT10  →  #1161 … #1170
```

**Patientenhilfsströme — je eine Buchse gegen alle übrigen** („REST"):

```
PAT1/REST … PAT10/REST  →  #1141 … #1150
```

**Gruppenkurzschluss zusammenhängender Buchsen** (Typ B / BF, alle Buchsen eines
Anwendungsteils werden zusammengeschaltet):

```
PAT 1+2        #1712      PAT 2+3        #1723      PAT 3+4     #1734
PAT 1+2+3      #1713      PAT 2+3+4      #1724      …
…                         …
PAT 1+…+10     #1720      PAT 2+…+10     #1730      PAT 9+10    #1799
```

Systematik: `#17<start><ende>` für den zusammenhängenden Bereich.
(Im PDF sind zwei Einträge fehlerhaft — `PAT 6+7+8+9+10` steht als `#1760`
doppelt, und die letzte Tabelle ist im Satz verrutscht.)

**Daraus folgt für die Hardware:**

- Jede der 10 Patientenbuchsen braucht **unabhängige Relaisansteuerung** mit
  mindestens drei Zielen: Messkreis, gemeinsame Sammelschiene (für Gruppen-
  kurzschluss), und offen.
- Zusätzlich muss **Netzspannung auf das Anwendungsteil** schaltbar sein
  (Prüfung „PABL mit U-Netz am Anwendungsteil") — sicherheitstechnisch der
  heikelste Teil des ganzen Geräts.
- Die **Phasenlage der Prüfsteckdose muss umkehrbar** sein („ph. rev." /
  umgekehrte Phasenlage).
- Der **Schutzleiter der Prüfsteckdose muss auftrennbar** sein (Ersatzableitstrom,
  Differenzstromverfahren).

## 3.1 Auswertung der 427 Prüfschritte

Aus `research/RS232_PROTOKOLL.md` ausgezählt. Jede Zeile ist ein Schaltzustand,
den die Hardware herstellen können muss — die Häufigkeit zeigt, wie zentral die
jeweilige Schaltdimension ist.

| Schaltdimension | Prüfschritte |
|---|---:|
| Anwendungsteil-Typ B / BF / CF getrennt behandelt | 222 |
| Phasenlage umkehrbar (`Phase rev.`) | 112 |
| DC-Ableitstrommessung | 98 |
| AC-Ableitstrommessung | 98 |
| Echteffektivwert (`TRMS`) | 96 |
| Schutzleiter auftrennbar (`PE offen`) | 85 |
| Netzleiter auftrennbar (`Netzl. offen`) | 83 |
| Funktionserde auflegbar (`FE geerdet`) | 56 |
| Interne Stromquelle zuschaltbar | 45 |
| Drehstrommessung (über Adapter) | 29 |
| Sichtprüfungs-Checklisten | 20 |
| Netzspannung auf das Anwendungsteil (`U-Netz am ATeil`) | 19 |
| Signal-Ein-/Ausgang | 12 |
| Elektrode gegen Elektrode | 11 |
| Anwendungsteil geerdet | 8 |

**Wichtigste Erkenntnis:** AC, DC und TRMS werden als getrennte Messungen
geführt (je ~98 Schritte). Das Gerät hat also **drei unterschiedliche
Messpfade** für Ableitströme, nicht einen mit umschaltbarer Auswertung.

## 3.2 Hardwarevarianten — relevant fürs eigene Gerät

Das Datenblatt der Prüfspitze **TP1010** nennt eine Bedingung, die belegt, dass
es **verschiedene Hardwarestände** gibt:

> „Für das Messen mit der Prüfspitze TP1010 muss das Unimet1000/1100ST mit der
> Betriebssoftware **Version 4.20 oder einer aktuelleren** ausgestattet sein.
> Außerdem muss **die Hardware des Unimet1000/1100ST für das Messen von AC- und
> DC-Ableitströmen ausgelegt** sein."

Nicht jedes UNIMET 1000ST kann also DC-Ableitströme messen. Beim eigenen Gerät
sind daher zu prüfen: **Softwareversion** (`:IDNF?` über RS232) und
**Hardwareversion** (`:IDNH?`).

## 3.3 Zubehör, das den Messumfang erweitert

| Teil | Funktion | Unterlage |
|---|---|---|
| **PK3** | Prüfkit mit Adaptern zum Anschluss elektromedizinischer Geräte | `docs/zubehoer/PK3_BP_deen.pdf` |
| **TP1010** | Prüfspitze für Labor-/Messgeräte nach IEC 61010-1 | `docs/zubehoer/TP1010_BP_deen.pdf` |
| **DS601** | Drehstromadapter (im PK3-Datenblatt genannt) | — |
| **TB3** | Anschlussadapter; die Prüfschritte weisen den Bediener an, Brücken zu stecken (`10a -> b`, `10d -> e`, `10h -> i`) und fordern U(N-PE) < 100 mV | nicht auffindbar |
| TM1000 | Tastaturmodul im Gehäusedeckel | Bedienungshandbuch |

## 3.4 Weitere Funde aus der Prüfschrittdatenbank

- **Sichtprüfungs- und Funktionsprüfungskataloge** sind als Prüfschritte
  hinterlegt, nicht nur Messungen — inklusive **krankenbettspezifischer**
  Punkte („Beschädigte Seitengitter/Holme", „Defekte Zugentlastung oder
  Kabelbefestigung im Bett", „Beschädigtes Motorgehäuse und Handschalter").
  Das Gerät deckt also die Bettenprüfung mit ab.
- **ANSI/AAMI ES1** wird referenziert — das Gerät beherrscht auch die
  US-amerikanische Prüfsystematik, nicht nur IEC/VDE.
- Die Datenbank enthält **Hinweistexte mit Platzhaltern** für den Bediener,
  z. B. „Bitte Phase `\PHASE` am Drehstromadapter einstellen". Die Firmware
  ersetzt Variablen im Text zur Laufzeit — nützlich zu wissen, falls man den
  Prüfschrittdatensatz je selbst erzeugen will.

## 3.5 Anbindung des Messteils — am Gerät festgestellt

**Befund am geöffneten Gerät:** Vom CPU-Modul führt ein **14-poliges
Flachbandkabel** zur **Relaisplatine**, und diese trägt ihrerseits ein
**Bussystem mit Steckplätzen für weitere Karten**.

Damit ist die Frage geklärt, und die frühere Vermutung in 3.5 („Messbaugruppe
als PC/104-Karte im Stapel") ist **überholt**. Die Messseite hängt nicht am
PC/104-Bus, sondern an einer eigenen schmalen Verbindung.

Bei 14 Adern plausibel:

- **schmaler I/O-Bus** — 8 Datenleitungen + `/RD` + `/WR` + 1–2 Auswahlleitungen
  + GND + VCC
- **serieller Steuerlink** — 2–4 Signalleitungen, Rest Versorgung

Unterscheidbar an den Bausteinen nahe dem Stecker auf der Relaisplatine:
Latches/Puffer (`74HCTxxx`, `8255`) sprechen für den Parallelbus, ein UART oder
Schieberegister für den seriellen Link.

### Topologie — bestätigt 2026-07-31

```
CPU-Modul ──14-polig──> Relaisplatine ──Flachband──> RS-485 (Rückwand)
                             │
                             └── Bussystem mit Steckplätzen für Messkarten
```

Die **RS-485-Schnittstelle kommt nicht vom CPU-Modul, sondern von der
Relaisplatine.** Sie hängt also am selben Strang wie das Messteil.

**Damit ist die frühere Hypothese belegt** (siehe 3.6, „RS-485-Port"): Das Messteil wird über einen RS-485-Bus angesprochen, und der
Serviceport an der Rückwand führt genau diesen Bus nach außen. Der
Rückseitenaufkleber „Datensichtgerät für RS 485 Schnittstelle — Bender SCPI
Protokoll" passt exakt dazu.

**Folge für den 14-poligen Strang:** Er ist damit sehr wahrscheinlich ein
**serieller Link** (TX, RX, Richtungsumschaltung, Versorgung) und **kein
Parallelbus**. Vierzehn Adern reichen dafür bequem. Für einen Mitschnitt genügt
ein serieller Sniffer statt eines 14-Kanal-Analyzers.

### 🔑 Architektur vollständig — durchgeklingelt 2026-07-31

**Bausteine auf der Relaisplatine** (Foto `bilder/20260731_075340.jpg`):

| Baustein | Anzahl | Funktion |
|---|---:|---|
| `PCF8574P` | 2 | **I²C-8-Bit-Portexpander** |
| `ULN2003A` | 3 | Darlington-Treiber → Relais |
| `74HCT14N` | 3 | Schmitt-Trigger |
| `LTC485` | 1 | **RS-485-Transceiver** |

Versorgungsnetze auf der Platine: `+12V`, `+5V`, `VCCD`, `GNDA`, `GNDD`, `-12V`
— analoge und digitale Masse getrennt geführt.

**Belegung des 14-poligen Steckers** (Header-Pin → F8680-Pin):

| Header | F8680 | Signal | Funktion |
|---:|---:|---|---|
| 1 | — | VCC | Versorgung |
| 2 | — | GND | Masse |
| 3 | 144? | `GRA8`? | **unplausibel, Zählung prüfen** — erwartet `PS1`…`PS4` (151–154) |
| 4 | 159 | `KBDATA` | **I²C `SDA`** |
| 5 | 160 | `KBCLK` | **I²C `SCL`** |
| 6 | 117 | `RESET` | Chip Reset |
| 7 | 155 | `PWRUP` | Power Up |
| 10 | 106 | `Rx` | **UART Empfang** |
| 11 | 107 | `Tx` | **UART Senden** |
| 13 | 108 | `RTS*` | **Richtungsumschaltung RS-485** |
| 14 | 89 | `GND` | Masse |

Noch offen: Header-Pin **8, 9, 12**.

### Die Architektur

```
F8680 ─┬─ KBCLK/KBDATA ──► I²C ──► PCF8574 ──► ULN2003 ──► Relais
       │                                    (Schaltmatrix, lokal)
       │
       └─ Rx/Tx/RTS ──────► LTC485 ──► RS-485-Bus
                                        ├──► Backplane / Messkarten
                                        └──► Rückwand (Service-Port)
```

**Zwei getrennte Steuerwege:**

- **I²C** (zweckentfremdete Tastaturpins) für das langsame Schalten der Relais
  direkt auf der Platine
- **RS-485** (der einzige UART des F8680, `RTS` als Richtungssteuerung) für die
  **Messkarten im Backplane** — adressierbar, störfest, backplanetauglich

**Messwerte kommen über RS-485 zurück**, nicht über I²C.

**Der Rückwand-Serviceport ist derselbe RS-485-Bus.** Der Aufkleber
„Datensichtgerät für RS 485 Schnittstelle — Bender SCPI Protokoll" beschreibt
also exakt den Messbus. Damit ist die Idee, das Messteil **direkt vom PC aus
anzusprechen**, keine Spekulation mehr — die Messkarten hängen an einem Bus,
der an der Rückwand anliegt, mit einem Protokoll, von dem wir 493 Befehle
dokumentiert haben (`RS232_PROTOKOLL.md`).

`RESET` und `PWRUP` auf demselben Stecker passen ins Bild: Die Relaisplatine
ist die Basis des Systems — das Schaltnetzteil speist sie, sie versorgt das
CPU-Modul über den Vierpoler und kann es zurücksetzen.

### Vorgeschichte: Takt-/Daten-Paar

**`KBCLK` (F8680 Pin 160) und `KBDATA` (Pin 159) gehen beide zur
Relaisplatine.** Bender hat die XT-Tastaturschnittstelle des F8680
**zweckentfremdet** und benutzt sie als synchronen seriellen Link zum Messteil.
Beide Pins sind im Datenblatt als `I/O` geführt, also frei ansteuerbar.

**Folgen:**

1. **Der serielle Tastaturweg ist damit belegt.** Eine XT-Tastatur lässt sich
   nicht anschließen, ohne der Messkommunikation dazwischenzufunken. Für den
   BIOS-Zugang bleibt nur die Matrix am 26-poligen Stecker.
2. **Fürs Reverse Engineering ist es ein Glücksfall:** Der gesamte Verkehr
   zwischen Rechner und Messteil läuft über **zwei Leitungen**. Zwei Kanäle
   mitschneiden statt vierzehn, kein Busdecoding nötig.

**Vermutung, noch zu prüfen:** Möglicherweise wurde nicht nur das Pinpaar,
sondern **das XT-Tastaturprotokoll selbst** übernommen — 9 Bit pro Frame,
ein Startbit, LSB zuerst, Takt von der Gegenseite. Der F8680 hat den Empfänger
dafür in Hardware; Antworten der Relaisplatine landeten dann ohne Bitfummelei
im Tastaturpuffer. Das würde erklären, warum ausgerechnet diese Pins gewählt
wurden. **Der erste Mitschnitt entscheidet es.**

### Chance: Messteil direkt ansprechen

Wenn die Messbaugruppen über RS-485 mit SCPI angesprochen werden und dieser Bus
an der Rückwand anliegt, lässt sich das Messteil **von einem PC aus direkt
ansteuern — möglicherweise ohne bootendes CPU-Modul.**

Startpunkt für Versuche: **9600 7E2** (wie für die RS-232 dokumentiert), `DC3`
zum Aktivieren des Remote-Betriebs, dann Befehle aus
`research/RS232_PROTOKOLL.md`. Ob dort dasselbe USP läuft oder ein eigener
Servicebefehlssatz, ist offen — der Aufkleber nennt SCPI, und das dokumentierte
USP *ist* SCPI.

Benötigt: RS-485-Adapter.

### Status: Relaisplatine noch unbekannt

**Die Relaisplatine ist vollständig eingebaut und bisher nicht untersucht.**
Alles darüber ist aus der Verkabelung erschlossen, nicht am Bauteil geprüft.
Offen bleibt:

- Anzahl und Belegung der Steckplätze auf dem Bussystem
- Siebdruck, Sachnummern, Revisionsstände
- Bausteine nahe dem 14-poligen Anschluss (RS-485-Transceiver? UART?
  Mikrocontroller?) — das würde die serielle Deutung endgültig bestätigen
- Beschriftung des 14-poligen Steckers an beiden Enden
- Ob die Relais direkt von der Platine oder von Steckkarten geschaltet werden

### Konsequenz fürs Reverse Engineering

**Dieser 14-polige Strang ist der ideale Messpunkt** — deutlich besser als der
PC/104-Bus. Er trägt ausschließlich den Verkehr zwischen Rechner und Messteil
und lässt sich mit einem 16-Kanal-Logic-Analyzer **vollständig** erfassen statt
nur ausschnittsweise. Jeder ausgeführte Prüfschritt läuft hier durch.

Zusammen mit der vollständigen Prüfschrittliste (`RS232_PROTOKOLL.md`, 427
Schaltzustände) und dem SCPI-Befehlssatz zum gezielten Auslösen ergibt das eine
ungewöhnlich gute Ausgangslage, um die Registerbelegung der Messhardware zu
rekonstruieren.

### Offene Punkte

- Anzahl der Steckplätze auf der Backplane, davon belegt
- Siebdruck/Sachnummern auf Relaisplatine und Steckkarten
- Beschriftung des 14-poligen Steckers an beiden Enden
- Bausteine nahe dem Stecker (entscheidet Parallelbus vs. seriell)

## 3.6 Frühere Vermutungen zur Anbindung ⛔

*Widerlegt durch die Messungen in 3.5. Bleibt zur Nachvollziehbarkeit stehen.*

### Ursprüngliche Überlegung

**Direkt dokumentiert ist das nirgends** — weder Bender noch Kontron haben ein
Blockschaltbild oder eine Verdrahtungsübersicht veröffentlicht. Was folgt, ist
aus den verfügbaren Schnittstellen des MOPS/386A und den beschriebenen
Gerätefunktionen abgeleitet und **am offenen Gerät zu verifizieren**.

| MOPS-Anschluss | Vermutete Verwendung | Belastbarkeit |
|---|---|---|
| **X1A/X1B PC/104-Bus** | Mess- und Steuerbaugruppe(n) als eigene PC/104-Karte(n) | **hoch** — der einzige Weg mit genügend Adressraum und Bandbreite für Relaismatrix + A/D-Wandlung |
| **X11 Tastaturmatrix** (26 pol.) | Fronttasten F1…F6, Info, Enter | **hoch** — klassische Matrixtastatur, genau wofür der Anschluss da ist |
| **X7 LPT** | externe Centronics-Druckerschnittstelle | hoch |
| X10 COM A | externe RS-232 (galvanisch getrennt) | mittel |
| COM B | RS-485 („für den BENTRON-Service") | mittel |
| X8 DOT-Matrix-LCD | vermutlich ungenutzt — die Anzeige läuft über die separate VGA-Karte | mittel |
| **X5 IDE** | **offen** — evtl. der PCMCIA-Slot, evtl. frei | **ungeklärt** |
| X12 Ethernet | vermutlich unbestückt | niedrig |

### ⚠️ Dokumentationslücke 1000ST vs. 1100ST

Das Handbuch TGH1256/03.2007 heißt zwar „UNIMET 1000ST **und** 1100ST", die
beschreibenden Kapitel sind aber durchgehend **1100ST-zentriert**: Kapitel 3.4
beginnt mit „Mit dem Prüfsystem UNIMET **1100ST** wird folgendes Zubehör
geliefert", die Frontansicht in 3.5 zeigt TFT-Farbdisplay und USB. Das 1000ST
wird nur in verstreuten Randbemerkungen abgegrenzt („UNIMET 1000ST älterer
Bauart haben eine PCMCIA-Karte…").

**Folge:** Weder der Lieferumfang noch die Schnittstellenbestückung des 1000ST
sind aus diesem Handbuch belastbar ableitbar. Konkret unklar:

- Hat das 1000ST **Centronics**, oder war das eine Option?
- Wie viele **serielle Ports** sind nach außen geführt (RS-232 und RS-485, oder nur einer)?
- **USB** hat das 1000ST mit Sicherheit nicht.

Am Gerät zu klären, nicht aus dem Handbuch.

### Die praktisch wichtige Unbekannte: der PCMCIA-Slot

Wie die „Memory Card" angebunden ist, wissen wir nicht. Drei Möglichkeiten:

1. **PCMCIA-ATA am IDE-Bus (X5)** — dann ist X5 bereits belegt, und die
   Backup-Strategie „CF-Karte an X5" braucht einen Plan B (Master/Slave oder
   temporäres Umstecken).
2. Eigener **PC/104-PCMCIA-Controller** im Stapel.
3. Proprietäre Anbindung über die Bender-Baugruppe.

**Vor dem Backup zu klären** — siehe `research/EINGANGSPRUEFUNG.md`, Phase 4.

### RS-485-Port: Aufkleber auf der Geräterückseite

Auf der Rückseite des erworbenen Geräts klebt ein gedrucktes Schild:

> **Datensichtgerät für RS 485 Schnittstelle — Bender SCPI Protokoll**

Das ist der bisher einzige Hinweis darauf, was auf dem Serviceport gesprochen
wird. **SCPI** (Standard Commands for Programmable Instruments) ist genau die
Syntaxfamilie, der auch das dokumentierte USP auf RS-232 folgt: hierarchischer
Doppelpunktpfad, `?` für Abfragen, `;` zum Verketten, Großbuchstaben-Kurzformen
(`ATTRibut?` → `:ATTR?`).

**Folge:** Der RS-485-Port ist womöglich nicht so verschlossen wie gedacht —
plausibel ist dieselbe Befehlsfamilie, nur auf anderem physikalischem Layer.
Das wäre mit einem RS-485-Adapter ausprobierbar.

**Vorbehalt zur Herkunft des Aufklebers:** „Datensichtgerät" beschreibt kein
Prüfgerät — der Begriff passt eher zu einem Anzeigegerät an einem Bender-Bus.
Möglich, dass das Schild von anderer Stelle stammt.

> **Nachtrag 2026-07-31 — Hypothese bestätigt.** Die RS-485 wird von der
> **Relaisplatine** zur Rückwand geführt, nicht vom CPU-Modul. Der Serviceport
> hängt also tatsächlich am Bus des Messteils. Siehe Abschnitt 3.4a,
> „Topologie".

### Nebenbefund: TB3 ist eine Testbox, kein bloßer Adapter

Im Bedienungshandbuch (4.5.5) gibt es einen **Systemselbsttest in zwei Stufen**:

- **intern**, ca. 30 s, prüft die Grundfunktionen — ohne Zubehör durchführbar,
  nur an geerdetem Netz (kein IT-Netz), ohne angeschlossene Prüflinge
- **erweitert mit der Testbox TB3**

Der interne Selbsttest ist damit die erste sinnvolle Funktionsprüfung, sobald
das Gerät bootet — er braucht kein Zubehör und markiert nicht bestandene
Prüfschritte mit `*`.

## 4. Die eigentliche Bauanleitung sind die Normen

Die Messanordnungen selbst stammen nicht von Bender, sondern aus:

- **IEC 62353 / DIN VDE 0751-1** — Wiederholungsprüfung medizinischer elektrischer
  Geräte. Definiert die Messverfahren (direkt, Differenzstrom, Ersatzableitstrom)
  und die Grenzwerte.
- **IEC 60601-1** — enthält das normative **Messgerät (MD)**, also das
  frequenzbewertete RC-Netzwerk, über dem der Ableitstrom gemessen wird. Ohne
  dieses Netzwerk misst man etwas anderes als einen Ableitstrom.
- **DIN VDE 0701-0702** — nichtmedizinische Geräte.
- **IEC 61010** — Laborgeräte.

Diese Normen sind kostenpflichtig (Beuth/VDE-Verlag), aber sie sind die normative
Quelle. Ein Nachbau ohne sie ist sinnlos, weil die Messnetzwerke und Grenzwerte
genau dort stehen.

## 5. Einschätzung Eigenbau

**Realistisch nachbaubar:**
- Schutzleiterwiderstand (Konstantstromquelle ~10 A bei ≤14 V, Vierleitermessung)
- Isolationsmessung (500 V DC, strombegrenzt auf 2,5 mA)
- Differenzstrommessung (Summenstromwandler)
- Spannung / Laststrom / Scheinleistung

**Der harte Teil:**
- **10-Kanal-Patientenmatrix** mit sicherer Trennung und definierten Kriechstrecken
- **Netzspannung aufs Anwendungsteil** — hier hängt die Sicherheit des Prüfers dran
- **Rückführbare Kalibrierung.** Ein Prüfgerät, dessen Messwerte nicht rückführbar
  kalibriert sind, taugt für Selbstbau-Zwecke, aber nicht als Nachweis.

**Rechtlicher Rahmen:** Für gewerbliche sicherheitstechnische Kontrollen nach
MPBetreibV muss das Prüfmittel geeignet und kalibriert sein. Ein Eigenbau erfüllt
das nicht. Für Lernzwecke, Eigenbedarf an nichtmedizinischen Geräten oder als
Ergänzung ist er dagegen völlig legitim.

**Fazit:** Der Nachbau ist als Projekt reizvoll und die Spezifikation ist
vollständig dokumentiert — aber das Original zu reparieren ist um Größenordnungen
billiger und liefert ein kalibrierbares Gerät.

## 6. Hinweis zur Textextraktion

Die Abkürzungstabelle in Kapitel 9.1.4 des Bedienungshandbuchs ist im
`pdftotext`-Auszug **spaltenverschoben** — dort stehen Kürzel und Erklärungen
gegeneinander versetzt. Nicht aus `research/text/` zitieren, sondern im
Original-PDF nachsehen.
