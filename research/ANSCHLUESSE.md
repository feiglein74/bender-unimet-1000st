# Anschlussbelegung des CPU-Moduls

Vollständige Aufnahme aller Steckverbinder des F8680-Moduls, ermittelt durch
Durchklingeln am geöffneten Gerät. Dazu die für dieses Gerät relevanten Pins
des Prozessors und die Daten des Displays.

**Kernaussage:** Von sechs Steckverbindern des Moduls sind nur vier beschaltet.
Das Modul ist ein Standardprodukt mit vollem I/O-Satz, von dem Bender nur einen
Teil genutzt hat.

## Was das Modul herausführen muss

Der F8680 integriert CPU, Speichercontroller, **LCD-/Videocontroller**,
**Tastatur**, **zwei serielle Schnittstellen**, **einen Parallelport** und die
**PCMCIA-Schnittstelle**. Entsprechend müssen vom Modul herunter:

| Funktion | Erwartete Aderzahl | Bemerkung |
|---|---|---|
| **LCD-Panel** | 14–20 | mono/STN, Datenbits + CL1/CL2/FLM/M + Versorgung |
| **Tastaturmatrix** | 26 | ✅ **bestätigt**, linker Rand, dünn belegt |
| **Seriell (1–2×)** | 10 je Port | `LT1137ACG` sitzt auf dem Modul → RS-232-Pegel |
| **Parallel** | 26 | evtl. ungenutzt, A104-MIO hat einen eigenen |
| **PCMCIA** | — | **kein Stecker** — Steckplatz sitzt auf der Rückseite desselben Moduls |
| **Messteil** | 14 | ✅ **bestätigt**, zur Relais-/Backplane-Platine |
| **Versorgung** | 4 | rot/blau/gelb/schwarz, kleiner Steckverbinder |
| **PC/104-Bus** | 64 + 40 | schwarze Stapelverbinder |

## Ergebnis — Verkabelung des Geräts (Stand 2026-07-31)

Konvention: **Bus immer oben**, bei jeder Richtungsangabe, auf beiden Seiten.

```
                    ┌─────────────────────────┐
                    │   CPU-Modul  B170X4     │
                    │   F8680 · PCMCIA hinten │
                    └─┬───┬────────┬────────┬─┘
         4-pol Versorgung │        │        │
    26-pol Einzeladern ───┘        │        │
      → Frontblende (Matrix)       │        │
                                   │        │
            14-pol #1 ─────────────┘        │
              → Relaisplatine               │
                 └→ Bus mit Steckplätzen    │
                 └→ Flachband → RS-485 (Rückwand)
                                            │
            14-pol #2 ──────────────────────┘
              → Verteilerplatine (Display/IO)
                 └→ dünnes Flachband → Display-Panel
                 └→ Flachband → RS-232 Rückwand (galv. getrennt, NM232DD)
                 └→ CCFL-Inverter PCU-554 (Hintergrundbeleuchtung)
```

**Nur vier Anschlüsse des CPU-Moduls sind überhaupt beschaltet.** Alles Weitere
ist Modulfunktion eines Standardprodukts, die Bender nicht genutzt hat.

**Vollständige Aufnahme, von links nach rechts (Bus oben):**

| # | Pins | Belegt | Funktion im Gerät |
|---|---:|:---:|---|
| 1 | 4 | ✅ | **Versorgung** — gelb +5 V, schwarz GND, rot/blau 12 V |
| 2 | 26 | ❌ | ungenutzt — `MC34063AP1` daneben, Kandidat LCD-Variante oder Parallelport |
| 3 | 10 | ❌ | ungenutzt — Bauform einer seriellen Schnittstelle |
| 4 | 14 | ✅ | **zur Relaisplatine** — Messteil + RS-485-Pfad |
| 5 | 14 | ✅ | **zur Verteilerplatine** — Display + RS-232 + Versorgung |
| 6 | 26 | ✅ | **Tastaturmatrix** — Einzeladern, nur ~6–10 der 26 Positionen belegt |

Dazu oben der **PC/104-Stapel** (64 + 40 pol.) und auf der **Rückseite** der
PCMCIA-Steckplatz sowie die unbestückten Plätze `U6`, `U7` (DIP-28) und `U16`
(PLCC-44).

**Vier von sechs Anschlüssen beschaltet** — das Modul kann mehr, als das Gerät
nutzt.

**Belegung des 14-Polers #2 (rechnerisch plausibel):** 4 Datenbits, CL1, CL2,
FLM, M für das STN-Panel = 8 · dazu +5 V, GND, VEE = 11 · plus TX, RX,
Signalmasse = **14**.

**Kontrasteinstellung** sitzt auf der **Verteilerplatine**, prominent und
unmittelbar neben dem dünnen FFC zum Panel — also dort, wo man sie beim Blick
auf den Bildschirm bedienen kann.

**`RP1`** auf dem CPU-Modul ist damit ungeklärt. Entweder ein
**Widerstandsnetzwerk** (dafür spricht der Bezeichner `RP`; in dieser Rolle am
ehesten **Pull-ups für die Tastaturmatrix**) oder ein Trimmer des Moduls für
eine hier ungenutzte Funktion. Für das Gerät ohne Belang.

## F8680 — relevante Pins (160-Pin PQFP, Datenblatt Table 1)

| Pin | Signal | Bedeutung |
|---:|---|---|
| **160** | **`KBCLK*`** | **Keyboard Clock** |
| **159** | **`KBDATA*`** | **Keyboard Data** |
| 158 | `SPKR` | Lautsprecher |
| 157 | `GND` | Masse |
| 151–154 | `PS1`…`PS4` | Programmable Pins — `PS4` gehört laut Design Guide Fig. 6-1 zur Tastaturbeschaltung |
| 107 / 106 | `Tx` / `Rx` | UART (nur **einer** vorhanden, wahlweise COM1 oder COM2) |
| 108–113 | `RTS*`, `CTS*`, `RI*`, `DSR*`, `CD*`, `DTR*` | Modemsteuerung |
| 98–102 | `DOT0/B`…`DOT3/I` | **4 Datenbits zum LCD** — passt zum DMF-50840 |
| 103–105 | `HS/LP`, `VS/FLM`, `DOTCLOCK` | Bildtiming |
| 90–97 | `MCCE1/2*`, `MCRDY`, `MCCD1/2*`, `MCBAT1/2`, `CARDB` | **PCMCIA-Kartensignale**, inkl. Kartenbatterie-Überwachung |
| 48 | `ROMCS*` | ROM Chip Select — das BIOS-EPROM |
| 121–150 | `GRD0`…`GRD7`, `GRA0`…`GRA14`, `GRACS*`, `GRAOE*`, `GRAWE*` | **Grafikspeicher-Bus** zum `D43256AGU-10L` |
| 1, 41, 59, 82, 121, 145 | `VCCPAD` | Versorgung der **Ausgangstreiber** (Eingang, keine Quelle) |
| 19, 115 | `VCC` | Kernversorgung |

**`KBCLK` und `KBDATA` sind die beiden letzten Pins des Gehäuses** und sitzen
damit unmittelbar um die Ecke neben Pin 1 — ohne Abzählen auffindbar.

**Pin 1 ist `VCCPAD`, nicht Masse.** Masse liegt u. a. auf 5, 13, 30, 49, 65,
72, 89, 100, 118, 125, 137, 157.

## Display: Optrex DMF-50840

| | |
|---|---|
| Auflösung | **320 × 240** (QVGA) |
| Typ | F-STN monochrom, transmissiv, 5,7" |
| Datenübertragung | **4 Bit parallel** |
| Anschluss | **14-poliges FFC, 1,25 mm Raster** — das dünne Band von der Verteilerplatine |
| Beleuchtung | **CCFL**, versorgt vom `TDK PCU-554` auf der Verteilerplatine |
| Kontrastverhältnis | 15:1 typ. |
| Temperatur | 0…50 °C Betrieb |

Datenblatt: alldatasheet.com / datasheetcatalog.com unter `DMF-50840`
(Direktabruf von dort blockiert, noch nicht lokal gesichert).

**Folge für den Bildschirmmodus:** Bei 320 × 240 läuft der Bootbildschirm in
**40×25 Text**, nicht 80×25 — passt zu den Zeilenlängen auf dem Verkaufsfoto.
Im BIOS-Setup steht bei `Display:` entsprechend `Color (40x25)` zur Wahl.
Die Handbuch-Screenshots mit 321×201 px sind der Grafikmodus **320×200**, den
`UNIMET.EXE` benutzt.

Das Panel ist ein gängiges 5,7"-Industriedisplay und als Ersatzteil weiterhin
beschaffbar.

## Anhang: elektrischer Fingerabdruck — so ordnet man Anschlüsse zu

Gerät eingeschaltet, Messung gegen Masse:

| Befund | Bedeutung |
|---|---|
| **0 V**, Durchgang zum Massepunkt | GND |
| **+5 V** fest, belastbar | Versorgung |
| **−9 … −12 V** im Ruhezustand | **RS-232-Ausgang** (`LT1137`) — unverwechselbar |
| **+9 … +12 V** | RS-232, aktiver Pegel |
| **hochfrequente Aktivität**, Kabel zum Display | **LCD-Panel** |
| **reihum gepulst** | Matrix-**Zeile** (getriebener Ausgang) |
| **statisch +5 V, bricht unter 10 kΩ ein** | Matrix-**Spalte** oder anderer Eingang mit Pull-up |
| statisch +5 V, bleibt stabil | getriebener Ausgang high |

⚠️ Am **feinpoligen QFP** nur im ausgeschalteten Zustand antasten. An
Pfostensteckern im 2,54-mm-Raster ist Messen im Betrieb unkritisch.

## Bekannte Topologie

- **PCMCIA** braucht keinen Stecker — der Steckplatz sitzt auf der Rückseite
  des CPU-Moduls.
- **Display und COM verlassen das Modul über Flachbandkabel**, laufen zunächst
  zu einer anderen Baugruppe (Verteilerplatine mit CCFL-Inverter `PCU-554`,
  `NM232DD` und `74HCT14N`) und werden erst **dort** wieder herausgeführt.
  Es geht also kein Kabel direkt vom CPU-Modul zum Display oder zur Rückwand.
- Die Zuordnung aller sechs Steckverbinder ist abgeschlossen (Tabelle oben).

## Offene Fragen

- **Welcher Stecker trägt was?** Zuordnung Stecker → Flachbandkabel →
  Zielbaugruppe ist noch offen
- Ist der **Parallelport** des F8680 überhaupt herausgeführt, oder kommt
  Centronics ausschließlich von der A104-MIO?
- Vollständiger **Siebdruck** des Moduls — Herstellername fehlt noch
