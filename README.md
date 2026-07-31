# Bender UNIMET 1000 ST — Archiv & Instandsetzung

Unterlagensammlung und Reparaturdokumentation zu einem gebraucht erworbenen
Bender UNIMET® 1000 ST (Prüfsystem für die elektrische Sicherheit medizinischer
elektrischer Geräte, IEC 62353 / DIN VDE 0751).

## Status: abgeschlossen (2026-07-31)

Das Gerät wurde **nicht** wiederhergestellt. Grund ist nicht der ursprüngliche
Bootfehler — der war vollständig aufgeklärt —, sondern ein Befund, der erst bei
der Untersuchung der Baugruppen auftauchte:

**Die Messeinrichtung fehlt.** Auf der ausgebauten Steckkarte saßen die
gesamte Messkette, die Netzschaltung (L, N, Phasenlage, Netzleiter-Unterbrechung)
und der Durchlauf des I²C-Bus. Ohne sie ist das Gerät ein Rechner mit Anzeige
und Schaltmatrix.

**Und das Gerät wurde vor dem Verkauf umgebaut**, nicht ausgeschlachtet: gezielt
gefräste Leiterbahnunterbrechungen, entfernte Rückwandanschlüsse, stillgelegte
RS-232 — zu einem **Anzeigeterminal für einen Bender-RS-485-Bus**, wie der
Rückwandaufkleber es benennt. `UNIMET.EXE` war zuletzt gar nicht mehr installiert.

Alles andere wäre rekonstruierbar gewesen: BIOS gedumpt und verstanden, Display
ansteuerbar, Relaismatrix über I²C entschlüsselt, Befehlssatz dokumentiert.
Nur der analoge Messkopf war unersetzlich.

Das Gehäuse wird weiterverwendet.

---

**Ausgangslage:** Gerät bootete nicht — `Using defaults for system configuration`
und `Diskette error` in Endlosschleife.

## Wo was steht

| Datei | Inhalt |
|---|---|
| **`research/STAND.md`** | **Arbeitsstand und nächste Schritte. Hier weitermachen.** |
| **`research/EPROM_ANALYSE.md`** | BIOS-Dump ausgewertet: Setup-Struktur, Bootmeldungen, Reparaturweg |
| `firmware/` | ausgelesenes BIOS-EPROM (NM27C010, `V: 0.91`) |
| **`research/EINGANGSPRUEFUNG.md`** | Checkliste zur Erstinbetriebnahme |
| **`research/BEFUNDE.md`** | Fehlerdiagnose, Reparaturweg, Fallen, Suche nach dem OS-Image |
| **`research/MESSTECHNIK.md`** | Prüfhardware: technische Daten, rekonstruierte Relaistopologie, Nachbau-Einschätzung |
| **`research/RS232_PROTOKOLL.md`** | Vollständige Schnittstellenreferenz: 435 Prüfschritte, 493 Befehle, Protokoll, Verkabelung |
| `tools/parse_interface.py` | erzeugt die RS232-Referenz aus dem Interface-Handbuch neu |
| `research/text/` | Alle PDFs als durchsuchbarer Text (`pdftotext -layout`) |
| `research/threads/` | Archivierter Forenthread mikrocontroller.net/topic/566576 |
| `docs/bender/` | Bender-/BENTRON-Handbücher (1000ST/1100ST, Interface, UNIData1100, 300ST, 800ST/810ST) |
| `docs/kontron/` | Kontron MOPS/386A — Handbücher Rev. 1.1/1.4/1.5, Datenblatt, Reports |
| `docs/diskonchip/` | M-Systems DiskOnChip Utilities |
| `software/kontron/` | **`SSDINIT.EXE`** (Silicon-Disk-Initialisierung), JIDA-Treiber |
| `software/archive/` | `Unimet300_V110.exe` — einziges erhaltenes bentron.de-Binary |
| `s-l1600*.webp` | Fotos: Bootbildschirm, Frontplatte |

## Kurzfassung des Befunds

Im Gerät steckt ein **Kontron/JUMPtec MOPS/386A** (PC/104, 386SX 40 MHz) mit
**MS-DOS 5.0** und der Anwendung **`UNIMET.EXE`** auf einem verlöteten
1,8/3,8-MB-Flash. Die BIOS-Konfiguration ist verloren; in den Werkseinstellungen
steht die Silicon-Disk auf `INT 13h Drive Mapping = Disabled`, wodurch Laufwerk C:
verschwindet und der Rechner auf Diskette zurückfällt.

Behebung voraussichtlich rein über das BIOS-Setup (`F2`). Details in
`research/BEFUNDE.md`.

## ⚠️ Vor dem ersten Einschalten lesen

- **`Erase On Next Boot` im BIOS niemals aktivieren** — löscht DOS und `UNIMET.EXE`.
- **Kein FDISK** auf der Silicon-Disk.
- **`UNIMET.EXE` ist nirgends öffentlich verfügbar.** Es existiert kein
  beschaffbares Ersatz-Image. Backup des Flash-Inhalts hat Priorität vor jedem
  anderen Eingriff.
- Netzstecker ziehen vor dem Öffnen — das Gerät erzeugt 500 V DC für die
  Isolationsprüfung und schaltet Netzspannung auf Prüfkreise.
