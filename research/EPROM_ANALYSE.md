# BIOS-EPROM des UNIMET 1000 ST — Auslesung und Analyse

Ausgelesen am 2026-07-30 mit XGecu T48.

## Baustein

| | |
|---|---|
| Typ | **NM27C010Q** (National Semiconductor), 1 MBit UV-EPROM, 128 K × 8 |
| Gehäuse | Keramik-DIP32 mit Quarzfenster, gesockelt |
| Aufkleber | handschriftlich **`V: 0.91`** (Etikett beim Ablösen zerfallen, mit Isopropanol gereinigt) |
| Datei | `firmware/BIOS_V0.91_NM27C010_20260730.bin` |
| Größe | 131.072 Bytes |
| SHA-256 | `6b9027f9690de099e6fe46a3f3af1a1958f5b75d0a350a1e7b40c9fe620a63b6` |
| MD5 | `22c0e11ff92ba649d767d311da96867c` |

## Aufbau

- **Untere 64 KB (`0x00000`–`0x0FFFF`): leer**, durchgehend mit `0x90` gefüllt
- **Obere 64 KB (`0x10000`–`0x1FFFF`): das eigentliche BIOS**
- Keine Spiegelung — der Baustein ist tatsächlich 128 KB groß, nur halb genutzt
- **Reset-Vektor** bei `0x1FFF0`: `EA 3A BF 00 F0` = `JMP F000:BF3A`
- Direkt dahinter **BIOS-Datum als ASCII: `04/06/93`**, danach Modellbyte **`FE`** (PC/XT-Klasse)

## Identifikation

```
CHIPS PC/CHIP Superstate Software Version 124
BOARDS PC · C-BIOS F8680A LCD 512k x 16;
512 kByte Flash ab 2 MB
(C)Copyright Chips & Technologies, Inc. 1991, All Rights Reserved
Evaluation · Development · Copy Only - Not for Resale or Distribution
```

Bemerkenswert:

- **`512 kByte Flash ab 2 MB`** ist **deutsch** — das BIOS wurde von einem
  deutschen Boardhersteller angepasst und deklariert einen 512-kByte-Flash
  ab physikalischer Adresse 2 MB. Starker Kandidat für das Bootmedium.
- `LCD 512k x 16` passt zu den beiden NEC `424800-70` auf der Platine
  (2 × 512K×8 = 512K×16 = 1 MB), davon 640 KB konventionell.
- Die C&T-Bausteine tragen den Vermerk **„Evaluation / Development /
  Copy Only - Not for Resale or Distribution"** — ausgeliefert wurde also ein
  Entwicklungs-BIOS.

## Bootmeldungen — Herkunft geklärt

Die Meldungen vom Verkaufsfoto stehen wörtlich in diesem ROM:

| Offset | Meldung |
|---|---|
| `0x1E0CF` | `Using defaults for system configuration` |
| `0x1E1B1` | `Diskette error - Press any key` |
| `0x1E23D` | `K Base RAM Passed` |
| `0x1E071` | `System battery is dead - Replace and run SETUP` |
| `0x1E1DF` | `Bad diskette boot record - Press any key` |
| `0x1E22D` | `Memory size does not match CMOS - Run SETUP` |
| `0x1E162` | `Real time clock error`, `Keyboard error`, `Diskette drive failure on drive` |

**Wichtig:** Auf dem Bootbildschirm erschien `Using defaults…`, **nicht**
`System battery is dead`. Das BIOS hätte die tote Batterie also gemeldet, wenn
sie das Problem wäre. Die Batteriespur ist damit endgültig erledigt.

## Das Setup — und damit der Reparaturweg

```
Press <F1> to continue, <F2> to Setup ...
```

**Setup-Taste ist `F2`.** Titel: *Chips and Technologies, Inc. System
Configuration Utility*, zwei Seiten.

Bedienung: Pfeiltasten wählen, `+`/`-` ändern, `PgUp`/`PgDn` blättern,
`ESC` beendet **ohne** Speichern, **`F10` speichert und beendet**.
Danach: `Changes require reboot to take effect. Reboot now? (Y/N)`

### Seite 1 — STANDARD SETUP OPTIONS

| Feld | Auswahl |
|---|---|
| `Time:` / `Date:` | Uhrzeit / Datum |
| **`Diskette A:`** | `Not Installed` · `5.25 Inch, 360 KB` · `5.25 Inch, 1.2 MB` · `3.5 Inch, 720 KB` · `3.5 Inch, 1.44 MB` · **`PCMCIA`** |
| **`Diskette B:`** | dieselbe Liste |
| `Hard Disk:` | `Not Installed` … mit Geometrie `Cyl / Hd / Pre / LZ / Sec / Size` |
| `Base Memory:` | 32 KB … 640 KB in 32-KB-Schritten |
| `Display:` | `EGA or VGA` · `Color (40x25)` · `Color (80x25)` · `Monochrome` |

### Seite 2 — ADVANCED FEATURE CONTROL

`Text Font` (None/Normal/Bold) · `Inverse Video` · `Speaker` ·
`Serial Power Down` · `Power Saving mode` (None / Smart Sleep /
Smart Sleep & Suspend) · `Shadow Ram for:` C0000…F8000 ·
`Serial Port Timeout` · `Suspend Timeout` · `Wake Up Time`

**Keine Flash- oder Massenspeicheroptionen auf dieser Seite.** Die gesamte
Laufwerkskonfiguration steht auf Seite 1.

## Schlussfolgerung

**`PCMCIA` ist ein wählbarer Laufwerkstyp für `Diskette A:` bzw. `Diskette B:`.**
Das ist der Mechanismus, über den dieses Gerät bootet — entweder von der
Frontsteckplatz-Karte oder vom onboard deklarierten 512-kByte-Flash, den der
F8680 über dieselbe Speicherkarten-Schnittstelle adressiert.

Mit geladenen Werkseinstellungen steht `Diskette A:` auf `Not Installed` oder
einem Diskettentyp → kein Bootmedium → `Diskette error`. Genau das Symptom.

### Vorgehen am Gerät

1. Tastatur anschließen, einschalten, **`F2`** drücken
2. **Alle Setup-Seiten abfotografieren** (Ist-Zustand dokumentieren)
3. `Diskette A:` auf **`PCMCIA`** stellen
4. `Base Memory:` auf **640 KB** prüfen
5. `Display:` prüfen — voraussichtlich `EGA or VGA`
6. `Hard Disk:` beachten, falls über die A104-MIO ein IDE-Medium hängt
7. **`F10`** speichern, Reboot bestätigen

Bleibt es beim `Diskette error`, ist das Bootmedium tatsächlich die fehlende
PCMCIA-Karte — dann führt kein Weg an einer passenden Karte mit dem
Originalinhalt vorbei.
