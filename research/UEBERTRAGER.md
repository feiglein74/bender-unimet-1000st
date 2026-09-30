# Übertrager `BG160 805 Q3995` — Bauteilcharakterisierung

Bender-Sonderanfertigung ohne öffentliche Unterlagen. Ausgelötet am 2026-08-03,
seither freies Bauteil auf dem Tisch.

**Zweck dieses Dokuments:** das Datenblatt zu erarbeiten, das es nie gab. Kein
Reparaturziel — das Gerät existiert nicht mehr. Gegenstand ist ausschließlich das
Bauteil und die Frage, was es kann.

## Grundsatz: isolierte Prüfung

Geprüft wird das Einzelteil, ohne Abhängigkeiten, die nicht selbst aufgebaut
sind. Jede Stufe fügt höchstens eine hinzu, und zwar eine bekannte.

Der Grund ist nicht Bequemlichkeit, sondern Zurechenbarkeit: läuft ein Bauteil im
Verbund, ist jedes abweichende Verhalten mehrdeutig — es kann vom Prüfling
kommen oder von jedem anderen Glied der Kette. Am freien Bauteil mit
selbstgebauter Ansteuerung gibt es diese Mehrdeutigkeit nicht.

Dazu kommt ein Vorteil, den ein intaktes Gerät nie böte: **das Bauteil darf am
Ende zerstört werden.** Damit wird die Gegenprobe möglich — jede indirekt
bestimmte Größe lässt sich zum Schluss gegen die direkte Zählung prüfen. Das
prüft nicht nur den Übertrager, sondern die Messmethode selbst.

## 1. Messprotokoll

### 1.1 Widerstände (2026-08-03)

| Knoten | Pins | Widerstand |
|---|---|---:|
| links oben | 2 | **396 Ω** |
| links unten | 2 × 2, gebrückt | **0,12 Ω** |
| rechts oben | 2 | **29 Ω** |
| rechts unten | 2 | **24 Ω** |

Physisch sechs Pins links, vier rechts; die unteren vier links sind paarweise
gebrückt. **Zwischen keinen zwei Wicklungen besteht Durchgang** — vier
galvanisch getrennte Wicklungen, kein gemeinsamer Rückleiter.

### 1.2 Vorbehalte zu diesen Werten

⚠️ **Die Knotenzählung links unten ist eine Annahme, keine Messung.** Die vier
Pins wurden als *zwei* Knoten behandelt, was Brücken `1–2` und `3–4`
voraussetzt — also je zwei Pins parallel. Verbindet die Brücke stattdessen
`2–3`, sind es **drei** Knoten und der Brückenpunkt ist eine
**Mittelanzapfung**. Beide Topologien ergeben zwischen den äußeren Pins denselben
Wert von 0,12 Ω. Die Unterscheidung steht aus (Programmpunkt 1).

⚠️ **Messschnurabgleich fehlt.** Bei 0,12 Ω ist der Schnurwiderstand in derselben
Größenordnung wie das Messobjekt. Der reale Wert liegt vermutlich bei 30–60 mΩ.

## 2. Warum der Widerstand allein wenig sagt

Für eine Wicklung gilt

```
R = ρ · N · l_m / A
```

ρ = spezifischer Widerstand Kupfer, N = Windungszahl, l_m = mittlere
Windungslänge, A = Drahtquerschnitt. l_m ist durch den Wickelkörper für alle
Wicklungen näherungsweise gleich. Es bleiben **zwei Unbekannte pro Wicklung bei
einer Messung** — das System ist entartet.

Ein kleiner Widerstand kann von **dickem Draht** kommen oder von **wenigen
Windungen**. Gleicher Messwert, physikalisch völlig verschiedene Bauteile.

Konkret, mit l_m ≈ 5 cm:

| Wicklung | bei d = 0,05 mm | bei d = 0,5 mm | bei d = 1,0 mm |
|---|---:|---:|---:|
| 396 Ω | ≈ 900 Wdg. | — | — |
| 24 Ω | ≈ 55 Wdg. | ≈ 5500 Wdg. | — |
| 0,12 Ω | — | ≈ 27 Wdg. | ≈ 110 Wdg. |

**Daraus folgt eine Warnung vor der naheliegenden Faustregel.** „Kleiner
Widerstand = Hochstromwicklung" gilt nur, wenn die Windungszahl bekannt ist. Bei
einer Hochsetzstufe ist eine niederohmige Primärwicklung bereits die Folge
weniger Windungen — sie sagt über die Strombelastbarkeit nichts. Belastbar wäre
das nur über die **gemessene Drahtstärke**.

Auch die gedoppelten Pins sind nur ein schwaches Indiz für Strom: dicker Draht
lässt sich an einem einzelnen Wickelkörperstift schlecht terminieren, das kann
rein mechanisch begründet sein.

**Was die Entartung auflöst:** `U₂/U₁ = N₂/N₁` misst N direkt und **unabhängig
von A**. Damit fällt eine Unbekannte weg, und der Querschnitt ist rückrechenbar.

## 3. Was sich schon ableiten lässt

Die Verlustleistung `P = I²R` hängt **nur** vom gemessenen Widerstand ab, nicht
von N und A einzeln. Die folgenden Schlüsse sind daher querschnittsunabhängig.

| Wicklung | bei 2,5 mA | bei 0,3 A | bei 2 A | bei 12 A |
|---|---:|---:|---:|---:|
| 396 Ω | 2,5 mW | 36 W | — | — |
| 24 Ω | — | 2,2 W | 96 W | 3,5 kW |
| 0,12 Ω | — | 11 mW | 0,5 W | 17 W |

- **396 Ω ist eine Milliampere-Wicklung.** Oberhalb einiger Milliampere wird sie
  unbrauchbar heiß. Als Wicklung an einer Niederspannungsquelle ausgeschlossen.
- **24 Ω und 29 Ω tragen wenige hundert Milliampere.** Als Primärwicklung an
  12 V läge der Wirkungsgrad schon bei rund 2 W Ausgangsleistung bei etwa 50 %.
  Ein Leistungspfad ist das nicht.
- **Nur die 0,12-Ω-Wicklung ist verlustseitig für Ampere geeignet** — was nach
  Abschnitt 2 nicht heißt, dass sie dafür ausgelegt *ist*.

### 3.1 Das Paar 24 Ω / 29 Ω

Rund 20 % Unterschied bei sonst gleicher Bauart ist das Bild zweier Wicklungen
**gleicher Windungszahl**, nacheinander statt bifilar gewickelt: die äußere Lage
hat den längeren mittleren Windungsweg. `R_außen/R_innen = l_außen/l_innen`, und
29/24 = 1,21 ist ein realistisches Verhältnis benachbarter Lagen.

Zwei gleiche Wicklungen deuten auf eine symmetrische Funktion — zwei Treiber,
zwei Hilfsspannungen, oder zwei Hälften einer gemeinsamen Wicklung. Welche,
entscheidet das Übersetzungsverhältnis gegen die dicke Wicklung:

| Verhältnis zur 0,12-Ω-Wicklung | Deutung |
|---|---|
| nahe 1:1 | Spannungen im Bereich einer Gate-Treiberspannung |
| deutlich größer | Hilfsspannung für eine nachgelagerte Baugruppe |

Endgültig klärt es die Lage im Wickelaufbau (Programmpunkt 8): Treiberwicklungen
liegen aus Kopplungsgründen dicht an der Primärwicklung, Hilfswicklungen können
außen liegen.

## 4. Kontext

*Nicht Gegenstand dieser Untersuchung, aber nützlich beim Deuten der Messwerte.*

Der Übertrager saß auf der Relaisplatine eines Bender UNIMET 1000 ST, wurde aus
der 12-V-Schiene gespeist und hatte keinen Netzanschluss. Zwei `BUK456`
(N-Kanal-Leistungs-MOSFET, TO-220) bildeten die Endstufe. Das Gerät spezifizierte
eine Isolationsprüfung mit **ca. 500 V DC bei max. 2,5 mA**.

Die 396-Ω-Wicklung passt dazu: bei 2,5 mA fällt über ihr 1 V ab, also unter
einem halben Prozent der Ausgangsspannung. Mehr als eine Plausibilität ist das
nicht — bestätigt wird es erst durch das Übersetzungsverhältnis.

## 5. Programm

Reihenfolge zwingend: alles Zerstörungsfreie zuerst, jede endgültige Messung
erst, wenn sie nichts mehr blockiert.

| | Messung | Werkzeug | Weg zurück |
|---|---|---|---|
| 1 | **Brückentopologie links unten** | Multimeter | — |
| 2 | Windungsverhältnisse, Wickelsinn | Generator, 2-Kanal-Scope | — |
| 3 | Hauptinduktivität je Wicklung | Generator, Scope, bekannter R | — |
| 4 | Streuinduktivität, Kopplungsfaktor | dto., Sekundär kurzgeschlossen | — |
| 5 | Eigenresonanz | Generator, durchfahren | — |
| 6 | Sättigungseinsatz | Generator, Shunt, Amplitude steigern | reversibel |
| 7 | Isolationswiderstand, Stufenprüfung | Isolationsprüfer | — |
| 8 | **Abwickeln, zählen, Kern öffnen** | Seitenschneider | endgültig |

### 5.1 Zu Punkt 1 — die Brückentopologie

Vorrangig, weil die Deutung der gesamten Primärseite daran hängt. Die vier Pins
einzeln nummerieren und **alle sechs Paarungen** messen, statt die gebrückten
Pins vorab zu einem Knoten zusammenzufassen.

| Befund | Topologie |
|---|---|
| zwei Paare mit je ≈ 0 Ω, dazwischen 0,12 Ω | verdoppelte Anschlüsse, keine Anzapfung |
| eine Brücke ≈ 0 Ω, von dort je ≈ 0,06 Ω nach außen | **Mittelanzapfung** |

Die zu unterscheidenden Halbwicklungen liegen bei rund 60 mΩ und damit unter der
Auflösung eines gewöhnlichen Multimeters. Der Ausweg ist ein **Differenzvergleich
statt einer Absolutmessung**: beide Hälften nacheinander mit denselben Schnüren
in identischer Anordnung messen. Der Schnurwiderstand geht als gleicher
systematischer Offset in beide Messungen ein und kürzt sich beim Vergleich
heraus. Ob zwei Ablesungen gleich sind, ist weit unterhalb der absoluten
Genauigkeit entscheidbar.

Liegt die Brücke offen als Drahtschlaufe über den Stiften, klärt schon ein Blick
die Geometrie.

### 5.2 Zu Punkt 2 — Einspeiserichtung

In die **396-Ω-Wicklung** einspeisen, nicht in die dicke: ein Generator hat 50 Ω
Innenwiderstand und wird von einer niederohmigen Wicklung heruntergezogen. Kanal
1 direkt an die gespeiste Wicklung legen, nicht an den Generatorausgang — dann
kürzt sich der Innenwiderstand aus dem Verhältnis heraus, und die Anzeige des
Generators ist gleichgültig.

### 5.3 Zu Punkt 4 — wo sitzt die Strombegrenzung?

Bei einer Hochspannungsquelle mit 2,5 mA Grenzstrom ist die Begrenzung
sicherheitsrelevant. Solche Begrenzungen werden häufig **in den Übertrager
hineinkonstruiert**, über gezielt große Streuinduktivität — ein magnetisch
ballastierter Ausgang kann nicht ausfallen, ein Vorwiderstand oder eine Regelung
schon.

Prüfbar nur am freien Bauteil: Hochspannungswicklung kurzschließen, primär die
verbleibende Induktivität messen. Groß = die Begrenzung sitzt im Eisen.
Klein = sie saß außen.

### 5.4 Zu Punkt 6 — Sättigung

Die einzige Messung, die die **Leistungsfähigkeit des Kerns** bestimmt, und zwar
unabhängig von Drahtstärke und Windungszahl. Sie umgeht damit die Entartung aus
Abschnitt 2 vollständig.

Sinus fester Frequenz auf eine Wicklung, kleiner Shunt in Reihe, Amplitude
langsam steigern. Solange der Kern linear arbeitet, ist der Magnetisierungsstrom
sinusförmig; am Sättigungseinsatz kippt er in charakteristische Spitzen um. Das
Volt-Sekunden-Produkt am Knie ist `B_max · A_e · N` und damit der nutzbare
Flusshub — daraus folgt die übertragbare Leistung bei gegebener Frequenz.

### 5.5 Zu Punkt 7 — Isolation

Ein Isolationsprüfer misst den Isolationswiderstand bei definierter, begrenzter
Prüfspannung. Er zerstört nichts und liefert **keine** Durchschlagsspannung —
das sind zwei verschiedene Fragen.

Aussagekräftig ist die **Stufenprüfung**: bei 250 V, dann 500 V, wenn möglich
1000 V. Eine gesunde Isolation zeigt einen weitgehend spannungsunabhängigen
Widerstand; ein deutlicher Abfall mit steigender Spannung zeigt Kriechpfade,
Feuchtigkeit oder Alterung. Die Spannungsabhängigkeit ist die Diagnose, nicht
der Einzelwert.

Alle Paarungen messen, **einschließlich gegen den Kern**.

### 5.6 Zu Punkt 8 — die Gegenprobe

Abwickeln und zählen liefert die Wahrheit zu allem Vorherigen: Windungszahl je
Wicklung, Drahtstärke, Wickelreihenfolge, Isolationsaufbau, Kernmaterial,
Luftspalt.

Damit lässt sich prüfen, ob die indirekten Verfahren getragen haben — ob die
20 % Widerstandsunterschied wirklich aus der Wickelreihenfolge kommen, ob eine
gemessene Streuinduktivität zu einem sichtbaren Luftspalt gehört, ob die
Rückrechnung auf den Querschnitt stimmt. Diese Kontrolle ist an einem Bauteil,
das man behalten will, nicht möglich.

## 6. Spezifikation

*Zu füllen, während das Programm läuft.*

| Größe | Wert |
|---|---|
| Knotenplan | — |
| Windungszahlen | — |
| Drahtstärken | — |
| Gleichstromwiderstände, vierleitrig | — |
| Übersetzungsverhältnisse | — |
| Wickelsinn | — |
| Hauptinduktivität | — |
| Streuinduktivität | — |
| Kopplungsfaktor | — |
| Eigenresonanz | — |
| Sättigungsflusshub | — |
| Übertragbare Leistung, Frequenzband | — |
| Isolationswiderstand je Paarung | — |
| Kernmaterial, Bauform, Luftspalt | — |

## 7. Wiederverwendbarkeit

Zu beantworten, sobald Punkt 6 und 7 vorliegen: In welchem Frequenzband und bei
welcher Leistung ließe sich der Übertrager in einem eigenen Aufbau einsetzen?
Die naheliegende Verwendung ist die, für die er gebaut wurde — eine
strombegrenzte Hochspannungsquelle aus einer Niederspannungsschiene. Ob er dafür
über den ursprünglichen Arbeitspunkt hinaus taugt, entscheidet der
Sättigungsflusshub.

Vorbehalt: nach Punkt 8 ist das Bauteil zerstört. Die Frage der
Wiederverwendbarkeit ist also **vor** dem Abwickeln zu beantworten — oder das
Ergebnis bleibt eine Konstruktionsvorlage statt eines Bauteils.
