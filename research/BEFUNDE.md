# Diagnoseprotokoll — von der Fehlermeldung zur Fehldiagnose und zurück

> **Dieses Dokument ist ein Protokoll, keine Gerätebeschreibung.**
>
> Es entstand, **bevor** das Gerät eintraf, allein anhand eines Fotos des
> Bootbildschirms und der Herstellerunterlagen. Die zentrale Annahme darin —
> im Gerät sitze ein Kontron MOPS/386A — **war falsch**. Sie stammte aus einem
> Forenthread, der ein anderes Baujahr beschreibt.
>
> Die Fehlspur ist samt Widerruf stehen geblieben, weil sie zeigt, wie weit man
> mit plausibler Dokumentenrecherche kommt und wo sie kippt. Wer die
> **tatsächliche** Hardware sucht, liest `STAND.md` und `ANSCHLUESSE.md`.
>
> Weiterhin gültig sind die Abschnitte 5 bis 7: die Suche nach dem Bootmedium,
> die Verfügbarkeit von Herstellersoftware und die Frontplattenbelegung.

## Ausgangslage

Stand: 2026-07-27. Gerät noch nicht eingetroffen; Analyse basiert auf dem POST-Foto
(`s-l1600.webp`) plus Herstellerdokumentation.

## 1. Symptom

Foto des Boot-Bildschirms zeigt:

```
(C)Copyright Chips & Technologies, Inc.
0640K Base RAM Passed
Using defaults for system configuration
Diskette error - Press any key      (in Endlosschleife)
```

Bewertung Zeile für Zeile:

| Zeile | Bedeutung |
|---|---|
| `Chips & Technologies` | **Video-BIOS**, nicht das System-BIOS. C&T-Flachbildschirm-Controller (65545/65550-Klasse) auf einer separaten PC/104-VGA-Karte. |
| `0640K Base RAM Passed` | Speichertest bestanden — CPU, RAM, Chipsatz arbeiten. |
| `Using defaults for system configuration` | **Kernbefund.** BIOS konnte die gespeicherte Konfiguration nicht laden und hat Werkseinstellungen geladen. |
| `Diskette error` | Folge der Zeile darüber, nicht eigenständiger Fehler. Kein Laufwerk C: gefunden → Rückfall auf A: → dort nichts. |

> ## ⛔ WIDERRUFEN am 2026-07-30 — Plattform ist NICHT das Kontron MOPS/386A
> 
> Fotos vom geöffneten Gerät (`bilder/20260730_*.jpg`) zeigen als CPU-Baugruppe
> ein Modul mit **Chips & Technologies F8680 „PC/CHIP"** (Aufdruck
> `F8680 A / TM1478A / 9444 HONG KONG`, Taktangabe **14 MHz**), NEC-SRAMs
> `D43256AGU-10L` und einem Taktgeber `ICD2027SC-1`.
> 
> Damit ist **Abschnitt 2 und der darauf aufbauende Reparaturweg in Abschnitt 4
> hinfällig.** Der Forenthread mikrocontroller.net/566576 beschrieb ein anderes
> Baujahr bzw. eine andere Revision des UNIMET 1000 ST.
> 
> **Ungültig:** JUMPtec-Flash-Disk-Submenü, `INT 13h Drive Mapping`, `Erase On
> Next Boot`, `SSDINIT.EXE`, Phoenix-Setup per `F2`, Steckerbezeichnungen
> X4/X5/X11, Batterie an X1C Pin 3 / X4 Pin 9.
> 
> **Weiterhin gültig:** die gesamte Bender-Seite (Handbücher, Prüfschritte,
> RS-232/SCPI-Referenz, Messtechnik) und der Grundsatz *Backup vor jedem
> Experiment*.
> 
> Neue Plattformunterlagen liegen in `docs/f8680/`. Aktueller Stand siehe
> Abschnitt 2a.

## 2. Tatsächliche Hardware (Korrektur vom 2026-07-30, aus Fotos)

Der PC/104-Stapel besteht aus mindestens drei Baugruppen:

**1. CPU-Modul — Chips & Technologies F8680 „PC/CHIP"**

- 8086-/XT-kompatibler Ein-Chip-PC, integriert CPU, Tastaturcontroller,
  Displayinterface, Parallelport und **zwei serielle Ports**
- Aufdruck `F8680 A`, `TM1478A`, Datumscode `9444` (KW 44/1994), `14 MHZ`
- NEC `D43256AGU-10L` SRAM (32K×8), Taktgeber IC Designs `ICD2027SC-1`
- **Native PCMCIA-2.0-Unterstützung** für Speicher- und I/O-Karten
- **Systemkonfiguration liegt in einem 4-kBit-Konfigurations-EEPROM**
  (2 kBit davon für Anwender- und Tastaturlayout)

Das erklärt den Bootbildschirm: `(C)Copyright Chips & Technologies, Inc.` ist
das **System-BIOS des F8680**, nicht ein Video-BIOS. `0640K Base RAM Passed`
passt zur XT-Klasse. Die frühere Deutung „separate VGA-Karte mit C&T-Controller"
war falsch.

**2. Multi-I/O — „A104-MIO", VER: B**

- Super-I/O `UMC UM82C863F` (9448), `PAL16L8ACN`, Quarz 24,000 MHz
- RS-232-Pegelwandler: `GD75188`, `GD75189A`, `MC1488N`, `SN75189N`
- Stecker: 2× 10-polig (CN1/CN2 = 2× RS-232), 26-polig (LPT/Centronics),
  34-polig (Diskettenlaufwerk), 40-polig (IDE)
- Zahlreiche Jumper JP1…JP26 — Konfiguration undokumentiert, **vor jeder
  Änderung fotografieren**

**3. PCMCIA — auf der Rückseite desselben CPU-Moduls**

Korrektur (2026-07-31): Das ist **keine eigene Trägerplatine**, sondern die
Lötseite des CPU-Moduls. Beide Fotos zeigen dieselbe Baugruppe `B170X4`.

- AMP-PCMCIA-Steckplatz = die frontseitige „Memory Card"
- Sehr viele Jumper (JP1…JP26), `74HCT245`, `U6`/`U7` unbestückt
- Kapton-Klebeband mit aufgelötetem Bauteil und Kupferlackdraht — werksseitige
  Änderung, gealtert, **nicht anfassen**

Da der F8680 PCMCIA nativ unterstützt, ist **die Speicherkarte als Boot- oder
Massenspeichermedium plausibel** — nicht nur als Katalogspeicher. Das würde das
Symptom ebenso erklären: keine Karte → kein `C:` → Rückfall auf A:.

## 2b. Die widerlegte Annahme: Kontron MOPS/386A ⛔

*Der folgende Abschnitt beschreibt, wovon wir vor Eintreffen des Geräts
ausgingen. Er ist **falsch** und bleibt nur zur Nachvollziehbarkeit stehen.*

Laut Forenthread mikrocontroller.net/topic/566576 (zwei Geräte, gleiches Symptomumfeld):

- **Kontron / JUMPtec MOPS/386A**, PC/104-Einplatinenrechner
  - 386SX @ 40 MHz, 2 MB DRAM (verlötet)
  - **Onboard-Silicon-Disk: 1,8 MB oder 3,8 MB bootbarer Flash, verlötet** — das Boot-Medium
  - Phoenix BIOS in Flash-EEPROM, dazu Kontron-BIOS-Extensions
  - IDE (44-pol, 2 mm Raster — Notebook-/CF-tauglich), FDC, 2×COM, LPT, Tastatur, 10-MBit-LAN (CS8900A)
- **Separate PC/104-VGA-Karte** — das MOPS/386A hat *keine* Onboard-Grafik, nur ein
  alphanumerisches Zeichen-LCD-Interface (max. 40×4). Das Foto zeigt aber einen
  vollen 80×25-Textbildschirm ⇒ zusätzliche Grafikkarte mit C&T-Controller vorhanden.
- **Messteil** — eigene Baugruppe(n), nicht Teil des PC-Systems.

Software-Stack: **MS-DOS 5.0** auf dem Flash, startet per AUTOEXEC.BAT die
Anwendung **`UNIMET.EXE`** — das ist die eigentliche Gerätesoftware.

## 3. Diagnose

Widerlegt: *„leere CMOS-Batterie hat die Konfiguration gelöscht"*. Das MOPS/386A
speichert die Setup-Konfiguration **im EEPROM**, nicht in batteriegepuffertem RAM.
Handbuch Rev. 1.5, Abschnitt BATT:

> „An external battery on this pin is only required for the update of the RTC.
> The CMOS setup configuration data is stored in an onboard EEPROM and will not
> get lost, even without a battery connected."

Eine leere Batterie kostet also **nur Datum/Uhrzeit** — relevant für Zeitstempel in
Prüfprotokollen, aber kein Boothindernis.

**Wahrscheinlichste Ursache:** Die BIOS-Konfiguration im EEPROM ist verloren/ungültig
(Checksummenfehler, oder jemand hat „Load Setup Defaults" ausgelöst). In den
Werkseinstellungen steht die Silicon-Disk auf **`INT 13h Drive Mapping = Disabled`**.
Damit verschwindet das Boot-Flash als Laufwerk C:, das BIOS findet keine Festplatte,
fällt auf A: zurück — und meldet `Diskette error`.

Das erklärt beide Bildschirmzeilen mit einer einzigen Ursache und ist **rein per
BIOS-Setup behebbar**, sofern der Flash-Inhalt intakt ist.

Alternativursachen, falls das nicht greift: Flash-Inhalt beschädigt/gelöscht,
defektes EEPROM (Konfiguration hält nicht), oder ein zusätzliches IDE-Medium fehlt.

## 4. Reparaturweg

Reihenfolge einhalten — Backup vor Schreibzugriffen.

1. **Tastatur anschließen** (5-pol DIN oder PS/2 mini-DIN, siehe Handbuch Anhang E).
2. **`F2` beim Boot** → Phoenix BIOS Setup.
3. **Main → JUMPtec Flash Disk Submenu** → `INT 13h Drive Mapping` auf **`Drive 80`**
   (entspricht C: unter DOS).
4. **Boot Menu** → `Boot sequence` auf `C: then A:`.
5. **Exit → Exit Saving Changes.**
6. Bootet DOS: **mehrfach `Strg+C`** drücken, Abbruch der Batchdatei mit **`J`**
   bestätigen → DOS-Prompt statt UNIMET.EXE.
7. **Backup:** 2,5"-IDE-Platte oder CF-Karte am 44-poligen IDE-Anschluss anschließen
   und den kompletten Flash-Inhalt kopieren. Alternativ per Nullmodem über COM.

### ⚠️ Fallen im BIOS-Setup

- **`Erase On Next Boot` niemals auf `Enabled`** — löscht beim nächsten Start das
  komplette Flash-Volume inklusive DOS und `UNIMET.EXE`. Das ist der Totalverlust.
- **Kein FDISK / kein Partitionierungstool** auf der Silicon-Disk. Handbuch:
  „potential risk for data damage or loss". Nach einem Erase ist zwingend
  `SSDINIT.EXE` (Kontron) nötig, um überhaupt wieder eine DOS-Partition anzulegen.
- Nach erfolgreichem Backup: `Write Protect = Enabled` schützt den Flash im Betrieb.

## 5. Software-/Firmware-Verfügbarkeit

- **`UNIMET.EXE` ist nirgends öffentlich verfügbar.** Keine Image-Dumps, keine
  Firmware-Archive gefunden. Der Forenthread von 04/2024 endet ohne Ergebnis; eine
  Anfrage des Threadstarters bei Kontron wurde abgelehnt.
- **Offizieller Weg war BENTRON GmbH & Co. KG** (Bender-Tochter für UNIMET-Service),
  Carl-Benz-Straße 8, 35305 Grünberg, Tel. +49 6401 807-730.
  **`bentron.de` ist tot** — die Domain liefert heute eine fremde 503-Seite
  („IHK Baustellennavi"), TLS-Zertifikat verweist auf `sylphen.com`.
  Aktueller Kontaktweg daher über Bender direkt bzw. das Bender-Connect-Portal.
- **PC-Software** (setzt laufendes Gerät voraus, Firmware ≥ 4.20):
  - `UniBackup` — Stammdaten/Gerätekatalog sichern, Firmware-Updates einspielen
  - `UNIData1100` — PC-Auswertung, kann auch die Gerätedatenbank reparieren
  - Beide liefen auf Win95/98/2000/XP, Übertragung über RS232.
- **Kalibrierung** darf laut Bender nur BENTRON oder autorisierte Stellen durchführen;
  empfohlenes Intervall 36 Monate.

**Konsequenz:** Der Flash-Inhalt ist das einzige Unikat im Gerät. Es gibt keine
Bezugsquelle für ein Ersatz-Image. Backup hat Priorität vor allem anderen.

### 5.1 Wichtigste Spur: das Update-Verzeichnis `disk_104`

Bedienungshandbuch, Abschnitt 6.3.4 (Firmware-Update über UniBackup):

> „1. Geben Sie an, wo sich das Updateverzeichnis befindet.
>  – Für UNIMET® 1100ST benötigen Sie das Verzeichnis „disk_ETX".
>  – **Für UNIMET® 1000ST mit PCMCIA-Laufwerk benötigen Sie das Verzeichnis „disk_104".**"

Zwei Schlüsse daraus:

1. **Unabhängige Bestätigung der Hardware.** `104` = PC/104 (das MOPS-Board),
   `ETX` = ETX-Modul im neueren 1100ST. Deckt sich mit dem Forenbefund.
2. **Ein Firmware-Update-Paket ist faktisch das Disk-Image des Boot-Mediums.**
   Ein `disk_104`-Verzeichnis wäre damit genau das Recovery-Image, das für den
   Totalverlust-Fall fehlt.

**Damit ist `disk_104` das lohnendste Suchziel.** Mögliche Quellen: alte
BENTRON-/Bender-Update-CDs, Service-PCs in Medizintechnik-Werkstätten,
Restbestände bei Händlern, die UNIMETs gewartet haben.

### 5.1.1 Ergebnis der `disk_104`-Suche (2026-07-27)

**Ergebnis: nicht öffentlich verfügbar.** Im Detail:

- **bentron.de ist im Wayback-Archiv erhalten**, inklusive Download-Bereich. Die
  Software-Liste von 08/2003 (`downloadfiles.asp?lng=1031&typ=s`) führte genau zwei
  Einträge:
  - „UNIMET®300 Software, Version 1.02" → `products/Unimet300.zip`
  - **„Unibackup (Version 1.1) — Backupsoftware für das UNIMET1000 und UNIMET1100",
    4084 KB** → `products/s/0/UniBackupV1.1.zip`
- **Die ZIP-Datei selbst wurde nie gecrawlt.** Nur der Link ist archiviert; direkte
  Abrufversuche über mehrere Wayback-Timestamps liefern 404.
- Ab ca. 2006 verwies bentron.de für Software auf die Hauptseite der Dipl.-Ing. W.
  Bender GmbH — **hinter einer Anmeldung**. Login-geschützte Dateien hat der Crawler
  nie erfasst.
- Einziges erhaltenes Binary auf bentron.de: `Unimet300_V110.exe` (gesichert unter
  `software/archive/`). Es ist ein WinZip-Self-Extractor mit **`unimet300.hex`** —
  also Intel-HEX-Firmware für einen Mikrocontroller. Der 300ST ist damit eine völlig
  andere Architektur als der 1000ST (PC/104 + DOS + Verzeichnis). Für `disk_104`
  ohne Erkenntniswert, bestätigt aber die Paketierungskonvention.
- **Bender selbst hat den 1000ST aus dem Support genommen.** Die aktuelle Übersicht
  „Informationen zum Software-Update für UNIMET®" (2024) behandelt ausschließlich
  300/400/610/800/810ST. 1000ST und 1100ST kommen nicht mehr vor.

**Wichtige Unterscheidung:** UniBackup ist *nicht* das OS. Es ist das PC-seitige
Übertragungswerkzeug. `disk_104` war ein separates Update-Paket, das BENTRON auf
Anfrage lieferte. Selbst ein Fund von UniBackup brächte das Betriebssystem nicht.

#### Verbleibende Beschaffungswege, nach Erfolgsaussicht

1. **Das eigene Gerät.** Der Flash ist mit hoher Wahrscheinlichkeit intakt — die
   Störung ist eine BIOS-Einstellung, kein gelöschtes Medium. Damit wäre das eigene
   Gerät die Quelle des Images, nicht dessen Empfänger. Kostenlos, sofort, höchste
   Erfolgswahrscheinlichkeit. **Genau deshalb ist `Erase On Next Boot` tabu.**
2. **Forenkontakt.** Der Threadstarter auf mikrocontroller.net (Matthias M.,
   Benutzer `nadmin1706`, Thread 566576, 04/2024) besitzt **zwei** UNIMET 1000ST und
   wollte den Flash auslesen. Möglicherweise inzwischen erfolgreich. Direkte Anfrage
   lohnt.
3. **Bender/BENTRON-Service.** Gerät ist EOL, das Unternehmen existiert. Im
   Update-PDF genannter Ansprechpartner für UNIMET-Software: Karl-Heinz Rein,
   karl-heinz.rein@bender.de. Bei abgekündigter Hardware werden Altbestände
   erfahrungsgemäß eher unbürokratisch herausgegeben.
4. **Medizintechnik-Werkstätten** mit alten Service-Rechnern; Restbestände von
   Händlern, die UNIMETs gewartet haben.

### 5.2 Memory Card (PCMCIA)

> „UNIMET® 1000ST älterer Bauart haben eine PCMCIA-Karte zum Speichern der
> **Kataloge**. Während aller Arbeiten, die den Gerätekatalog oder den
> Typenkatalog betreffen, darf diese Karte nicht entnommen werden."

Die Karte trägt also die **Datenbank** (Geräte-/Typenkatalog), **nicht** das
Betriebssystem. Ein leerer Slot erklärt den Bootfehler folglich nicht — der
tritt im BIOS auf, lange vor DOS und Anwendung.

Offen: ob `UNIMET.EXE` ohne gesteckte Karte überhaupt startet oder mit einem
Datenbankfehler stehenbleibt. Die Karte sollte beim Verkäufer erfragt werden.

## 5.3 Frontplatte (Anschlussbelegung)

| Kennung | Funktion |
|---|---|
| `[E]` | Prüfsteckdose — Netzkabel des Prüflings |
| `1…10` | Buchsen für **Patientenelektroden** (Anwendungsteile) |
| `[A]` + `[B]` | aktive Prüfspitze TP2 mit Drucktaster |
| `[B]` | einpolige Messleitung (passive Prüfspitze) |
| `[C]` | Potentialausgleich |
| `[D]` FE | Funktionserde |

Die zehn Patientenelektroden-Buchsen belegen die Medizin-Variante
(Patientenableitströme nach IEC 62353 mit Anwendungsteilen).

Hinweis: Die Farbzuordnung im Handbuch (`[B]` violett) stammt aus dem
1100ST-Kapitel; am 1000ST auf dem Foto sind `[A]` gelb und `[B]` grün.

## 6. Gesicherte Dokumente

```
docs/kontron/MOPS386A_Users_Guide_rev1.5.pdf     Board-Handbuch (maßgeblich)
docs/kontron/MOPS386A_Users_Guide_rev1.4.pdf     ältere Revision
docs/bender/Bedienungshandbuch_UNIMET_1000ST_1100ST_de.pdf
docs/bender/UNIMET_Interface_Handbuch_de.pdf     Schnittstellen/UniBackup/UNIData
docs/bender/UNIMET300ST_Handbuch_de.pdf
docs/bender/UNIMET800ST_Controlcenter_de.pdf
docs/bender/UNIMET1100_Flyer_de.pdf
docs/diskonchip/DiskOnChip_Software_Utilities.pdf
research/MOPS386A_manual.txt                     durchsuchbarer Volltext
research/threads/mikrocontroller_566576.{html,txt}   nur lokal, Thread: mikrocontroller.net/topic/566576
```

## 7. Offene Punkte (nach Eintreffen zu klären)

- Board tatsächlich MOPS/386A? Aufdruck prüfen — andere MOPS-Varianten möglich.
- Sitzt zusätzlich ein IDE-Medium (CF/Platte) im Gerät?
- Batterietyp und -zustand: 3,0–4,0 V, empfohlen 3,6 V, an Pin 9 (BATT) des
  Power-Connectors oder Pin 3. Auf Auslaufspuren prüfen.
- Wo liegen die **Kalibrierdaten** — auf dem Flash oder im EEPROM des Messteils?
  Entscheidet, ob das Flash-Backup auch die Kalibrierung sichert.

## Quellen

- https://www.mikrocontroller.net/topic/566576
- https://www.kontron.com/en/products/mops-386a/p86800
- https://www.kontron.com/downloads/manuals/m_mops386a_p389m115.pdf
- https://www.bender-in.com/fileadmin/content/Products/m/d/Unimet1100ST_TGH_de.pdf
- https://www.bender.es/fileadmin/content/Products/m/d/Unimet-Interface_TGH_de.pdf
- https://www.bender.de/blog/post/unimet-sicherheitstester-kalibrieren/
