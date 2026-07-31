# Relaisplatine — I²C-Ansteuerung und Bitbelegung

Ermittelt am 2026-07-31 mit XGecu-Bus-Pirate am I²C-Bus. Unvollständig —
das Projekt wurde beendet, bevor die Kartierung abgeschlossen war.

## Ansteuerungskette

```
F8680 Pin 160 (KBCLK) ──► I²C SCL ─┐
F8680 Pin 159 (KBDATA) ─► I²C SDA ─┴─► PCF8574 ──► 74HCT14 ──► ULN2003 ──► Relaisspule
```

Bender hat die **XT-Tastaturschnittstelle des F8680 als I²C-Bus zweckentfremdet**.
Die Pins sind im Datenblatt als `I/O` geführt, also frei ansteuerbar.

**Der Bus wird über den Steckplatz der Messkarte geschleift.** Ohne Karte ist er
unterbrochen — ein Busscan am 14-poligen Stecker findet deshalb nichts, obwohl
die `PCF8574` versorgt sind und der Bus sauber auf 5 V liegt.

**Umgehung:** Bus Pirate direkt an **Pin 15 (`SDA`)**, **Pin 14 (`SCL`)** und
**Pin 8 (`GND`)** eines `PCF8574` klemmen.

## Buskonfiguration

| Parameter | Wert |
|---|---|
| Geschwindigkeit | **100 kHz** — der `PCF8574` ist nicht schneller spezifiziert |
| Pull-ups | **keine auf der Platine** — die stellte das CPU-Modul. Bus Pirate: `Vpu` an +5 V, dann `P` |
| Adressen | **`0x24`** und **`0x25`** (7 Bit) |
| Bus-Pirate-Schreibweise | `0x24` → schreiben `0x48`, lesen `0x49` · `0x25` → schreiben `0x4A`, lesen `0x4B` |

## Logik ist invertiert

Zwischen `PCF8574` und `ULN2003` sitzen die **`74HCT14`-Inverter**. Nötig, weil
der `PCF8574` seine High-Pegel nur mit rund 100 µA treibt — zu wenig für einen
Darlington-Eingang, aber ausreichend für einen CMOS-Schmitt-Trigger.

> **`0` schreiben = Relais zieht an. `1` = Relais fällt ab.**

Nach Reset stehen alle Ausgänge auf High → alle Relais abgefallen. Sicherer
Grundzustand.

⚠️ **Nie `0x00` schreiben** — das zöge alle Relais gleichzeitig an.
Immer bei `0xFF` beginnen und einzelne Bits löschen.

## Bitbelegung

### Baustein `0x24` (schreiben: `0x48`)

| Bit | Wert | Relais |
|---:|---|---|
| 0 | `0xFE` | **`K1.1` + `K1.2`** gemeinsam |
| 1 | `0xFD` | offen — vermutlich lautloses Zettler-Relais |
| 2 | `0xFB` | `K3` |
| 3 | `0xF7` | `K4` |
| 4 | `0xEF` | `K6` |
| 5 | `0xDF` | `K5` |
| 6 | `0xBF` | `K11` |
| 7 | `0x7F` | Zettler-Relais, nicht zugänglich (Netzteil davor verschraubt) |

### Baustein `0x25` (schreiben: `0x4A`)

| Bit | Wert | Relais |
|---:|---|---|
| 0 | `0xFE` | Zettler, unbestimmt |
| 1 | `0xFD` | `K13` |
| 2 | `0xFB` | Zettler, unbestimmt |
| 3 | `0xF7` | **nicht ermittelt** |
| 4 | `0xEF` | **nicht ermittelt** |
| 5 | `0xDF` | `K15` |
| 6 | `0xBF` | `K16` — schaltet etwas zur zweiten Messbuchse |
| 7 | `0x7F` | **nicht ermittelt** |

`K1.1` und `K1.2` hängen an einem Bit, arbeiten also zwingend gemeinsam. Zwei
Zweifach-Wechsler ergeben **vier Umschaltkontakte für eine Funktion** — passt zu
einer mittenangezapften Primärwicklung.

## Relaisbestand

| Lage | Relais |
|---|---|
| neben dem Trafo | `K1.1`, `K1.2`, `K3`, `K4`, `K5`, `K6` |
| in Trafonähe | `K11`, `K12` |
| zwischen den beiden Steckkartenbuchsen | `K13`, `K15` |
| unterhalb des Logikteils | `K16` |

Zwei Bauarten:

- **größere Relais im klaren Gehäuse**, 12 V DC — Leistungspfade
- **Zettler `AZ830-2C-12DSEA`** — subminiatur, zwei Wechsler, 12 V, gekapselt.
  Signalrelais für Messpfade: kleiner und stabiler Übergangswiderstand, geringe
  Thermospannung. **Schalten nahezu lautlos**, deshalb akustisch nicht
  auffindbar. Es sind `K6`, `K7`, `K8` und `K12`.

**Keines der elf Relais führt L oder N.** Die Netzschaltung saß auf der
fehlenden Messkarte.

## Detektionsmethoden

Weil die Zettler lautlos schalten und der Stromzuwachs einer Kleinrelaisspule
(10–20 mA) im Verbrauch des Schaltnetzteils untergeht:

**Am `ULN2003`-Ausgang messen.** Die Spulen hängen zwischen +12 V und dem
Treiberausgang.

| Messwert am Ausgangspin | Bedeutung |
|---|---|
| ~12 V | Kanal aus |
| ~1 V | Kanal aktiv (Darlington-Sättigung) |

`ULN2003` DIP-16: Pin 1–7 Eingänge, Pin 8 GND, Pin 9 `COM` (Freilaufdioden nach
+12 V), Pin 10–16 Ausgänge (Pin 16 = `OUT1`, Pin 10 = `OUT7`).

Drei `ULN2003` = 21 Kanäle für 16 Bits. Fünf Kanäle bleiben also ungenutzt —
oder führen über den Kartenanschluss zu Spulen auf der fehlenden Karte.

## Deutung der Baugruppe (unbestätigt)

Die Relaisplatine ist vermutlich die **Quellen- und Bereichsplatine**:

- **Zerhacker** aus zwei `BUK456` (N-Kanal-Leistungs-MOSFET, TO-220) in
  Gegentakt
- **Übertrager** `BG160 805 Q3995`, kein Netztrafo — er wird aus der 12-V-Schiene
  gespeist. Die Platine hat **keinen 230-V-Anschluss**.
- **Relais schalten Wicklungsanzapfungen** für die verschiedenen Prüfgrößen:
  500 V bei 2,5 mA für die Isolationsprüfung, 14 V bei 10 A für den
  Schutzleiterwiderstand
- Vermutlich erzeugt ein `74HCT14`-Gatter als Rechteckoszillator die
  Schaltfrequenz — drei Bausteine à sechs Inverter sind mehr, als die drei
  `ULN2003` benötigen

**Zu prüfen wäre gewesen:** Wicklungswiderstände des Übertragers messen
(unter 1 Ω = Primär-/Hochstromwicklung, hunderte Ω bis kΩ = Hochspannungs-
wicklung) und verfolgen, an welchen Wicklungsenden Relaiskontakte hängen.

## So ließe sich die Kartierung fortsetzen

1. Restliche Bits durchgehen, Detektion über `ULN2003`-Ausgänge
2. Pro Relais: Spulenpins per Widerstandsmessung finden (Spule = einige hundert
   Ω, Kontakte = 0 oder unendlich)
3. Relais anziehen lassen, dann am **Kartenanschluss** und an der Frontplatte
   durchklingeln, welche Kontakte verbunden werden
4. Aus der Topologie die Funktion erschließen — L+N gebrückt = Isolationsprüfung,
   PE auf die Sonde = Schutzleiterwiderstand, und so fort
