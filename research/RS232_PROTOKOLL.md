# UNIMET 1000/1100 ST — RS232-Referenz

Maschinell erzeugt aus `docs/bender/UNIMET_Interface_Handbuch_de.pdf`
(TGH1315/01.2006) via `tools/parse_interface.py`. Bei Zweifeln gilt das PDF.

Umfang: **427 Prüfschritte**, **493 Befehle**.

## 1. Schnittstelle

| Parameter | Wert |
|---|---|
| Physik | RS-232, galvanisch getrennt, 9-polig |
| Baudrate | 300 / 4800 / **9600** (Werkseinstellung) |
| Format | **7 Datenbit, 2 Stoppbit, Parität gerade (7E2)** |
| Übertragungsart | asynchron |
| Pegel | log. 1: +1,2 V … −12 V · log. 0: +1,5 V … +12 V |
| Max. Länge | 5 m |
| Kabel | Nullmodem |

### Nullmodem-Belegung

| Signal PC | DB25 | DB9 | Richtung | Unimet | Signal Unimet |
|---|---|---|---|---|---|
| RxD | 3 | 2 | &larr; | 3 | TxD |
| TxD | 2 | 3 | &rarr; | 2 | RxD |
| RTS | 4 | 7 | &rarr; | 8 | CTS |
| CTS | 5 | 8 | &larr; | 7 | RTS |
| GND | 7 | 5 | &mdash; | 5 | GND |
| DTR | 20 | 4 | &rarr; | 6 | DSR |
| DSR | 6 | 6 | &larr; | 4 | DTR |

## 2. Protokoll (Unimet Standard Protokoll, USP)

**Remote aktivieren:** `DC3` (ASCII 19) senden &rarr; Antwort `Unimet in Remote`. Die Gerätetastatur ist dann gesperrt.
**Remote beenden:** `DC4` (ASCII 20), keine Antwort.
Alternativ am Gerät: Hauptmenü &rarr; F5 Systemverwaltung &rarr; F2 Schnittstellen &rarr; F3 Unimet Standard Protokoll.

**USP ist SCPI.** Die Syntax folgt durchgängig *Standard Commands for Programmable Instruments*: hierarchischer Doppelpunktpfad, `?` für Abfragen, `;` zum Verketten auf gleicher Ebene, und Langformen, bei denen die Großbuchstaben die Kurzform ergeben (`ATTRibut?` → `:ATTR?`). Ein Rückseitenaufkleber des Geräts nennt für die RS-485-Schnittstelle ausdrücklich das „Bender SCPI Protokoll" — vermutlich dieselbe Befehlsfamilie auf dem Serviceport.

Befehle sind hierarchisch (`:DATA:CAT:ID:FIRS?`). Sie lassen sich komplett senden oder ebenenweise; auf gleicher Ebene genügt danach `;NEXT?`. Für einen Wechsel der Ebene muss wieder bei Root begonnen werden.

### Antwortcodes

| Antwort | Bedeutung |
|---|---|
| `1234…` | abgefragter Wert |
| `#NULL#` | Empfangsbestätigung ohne Datenabfrage |
| `#NOCMD#` | Befehl ungültig oder unbekannt |
| `#ERROR#` | ungültige/unbekannte Messung, allgemeiner Fehler |
| `#OFFLINE#` | Remote-Betrieb beendet, oder Datenbankfehler (Datenbankreparatur am Gerät nötig) |
| `#VOID#` | Leerstring |
| `#IDCFULL#` | Gerätekatalog voll |
| `#TYPCFULL#` | Typenkatalog voll |

## 3. Prüfschritte UNIMET 1000/1100 ST

Auswahl per `:MEAS:STEP <nr>`, Auslösen per `:SYS:CTRL <nr>`.
Abkürzungen: **NC** Normalzustand · **SFC** erster Fehlerfall · **TRMS** Effektivwertmessung · **ATeil** Anwendungsteil · **FE** Funktionserde · **PE** Schutzleiter · **SK** Schutzklasse · **Phase rev.** umgekehrte Phasenlage · **Netzl. offen** Netzleiter unterbrochen.

| Nr. | Allgemeine Bezeichnung | Spezielle Bezeichnung |
|---:|---|---|
| 1 | Schutzleiterwiderstand | Schutzleiterwiderstand Gehäuse Schutzleiter |
| 2 | Schutzleiterwiderstand | Schutzleiterwiderstand Leitung |
| 3 | Schutzleiterwiderstand | Schutzleiterwiderstand feste Leitung |
| 4 | Schutzleiterwiderstand | Schutzleiterwiderstand festangeschlossenes Gerät |
| 5 | Isolationswiderstand | Isolationswiderstand Gehäuse |
| 6 | Isolationswiderstand | Isolationswiderstand Schutzleiter |
| 7 | Erdableitstrom NC | Erdableitstrom NC Standard |
| 8 | Erdableitstrom NC | Erdableitstrom NC Phase rev. |
| 9 | Erdableitstrom SFC | Erdableitstrom SFC Netzl. offen |
| 10 | Erdableitstrom SFC | Erdableitstrom SFC Netzl. offen Phase rev. |
| 11 | Erdableitstrom SFC | Erdableitstrom SFC ATeil geerdet |
| 12 | Erdableitstrom NC | Erdableitstrom NC FE geerdet |
| 13 | Erdableitstrom SFC | Erdableitstrom SFC ATeil und FE geerdet Netzl. offen |
| 14 | Gehäuseableitstrom NC | Gehäuseableitstrom NC Standard |
| 15 | Gehäuseableitstrom NC | Gehäuseableitstrom NC Phase rev. |
| 16 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC PE offen |
| 17 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC PE offen Phase rev. |
| 18 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC Netzl. offen |
| 19 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC Netzl. offen Phase rev. |
| 20 | Gehäuseableitstrom NC | Gehäuseableitstrom NC ATeil geerdet |
| 21 | Gehäuseableitstrom NC | Gehäuseableitstrom NC FE geerdet |
| 22 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC ATeil FE geerdet PE offen |
| 23 | Patientenableitstrom NC TRMS | Patientenableitstrom NC TRMS Standard |
| 24 | Patientenableitstrom NC TRMS | Patientenableitstrom NC TRMS Phase rev. |
| 25 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS PE offen |
| 26 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS PE offen Phase rev. |
| 27 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS Netzl. offen |
| 28 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS Netzl. offen Phase rev. |
| 29 | Patientenableitstrom NC TRMS | Patientenableitstrom NC TRMS FE geerdet |
| 30 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS FE geerdet; PE offen |
| 31 | Patientenableitstrom SFC mit U-Netz am ATeil | Patientenableitstrom SFC mit U-Netz am ATeil Standard |
| 32 | Patientenableitstrom SFC mit U-Netz am ATeil | Patientenableitstrom SFC mit U-Netz am ATeil Phase rev. |
| 33 | Patientenableitstrom SFC Phase rev. mit U-Netz am ATeil | Patientenableitstrom SFC Phase rev. mit U-Netz am ATeil Standard |
| 34 | Patientenableitstrom SFC mit U-Netz am ATeil | Patientenableitstrom SFC mit U-Netz am ATeil FE geerdet |
| 35 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Standard |
| 36 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Phase rev. |
| 37 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS PE offen |
| 38 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS PE offen Phase rev. |
| 39 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Netzl. offen |
| 40 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Netzl. offen Phase rev. |
| 41 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS FE geerdet |
| 42 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS PE offen; FE geerdet |
| 44 | Ersatzgeräteableitstrom | Ersatzgeräteableitstrom SK I |
| 45 | Ersatzpatientenableitstrom | Ersatzpatientenableitstrom SK I |
| 46 | Ersatzgeräteableitstrom | Ersatzgeräteableitstrom SK II |
| 47 | Ersatzpatientenableitstrom | Ersatzpatientenableitstrom SK II |
| 48 | Gehäuseableitstrom NC | Gehäuseableitstrom NC interne Stromquelle |
| 49 | Patientenableitstrom NC TRMS | Patientenableitstrom NC TRMS interne Stromquelle |
| 50 | Patientenableitstrom SFC mit U-Netz am ATeil | Patientenableitstrom SFC mit U-Netz am ATeil interne Stromquelle |
| 51 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS interne Stromquelle Signal E/A |
| 52 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS interne Stromquelle |
| 53 | Isolationswiderstand | Isolationswiderstand ATeil Schutzleiter |
| 54 | Isolationswiderstand | Isolationswiderstand ATeil Gehäuse |
| 58 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Elektrode zu Elektrode interne Stromquelle |
| 59 | Gehäuseableitstrom NC | Gehäuseableitstrom NC festangeschlossenes Gerät |
| 60 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK I |
| 61 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK I Phase rev. |
| 62 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II |
| 63 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II Phase rev. |
| 64 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Elektrode zu Elektrode |
| 65 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Elektrode zu Elektrode Phase rev. |
| 66 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS PE offen Elektrode zu Elektrode |
| 67 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS PE offen Elektrode zu Elektrode Phase rev. |
| 68 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Elektrode zu Elektrode Netzl. offen |
| 69 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Elektrode zu Elektrode Netzl. offen Phase rev. |
| 70 | Erdableitstrom SFC | Erdableitstrom SFC Netzl. offen Drehstrom |
| 71 | Erdableitstrom SFC | Erdableitstrom SFC ATeil und FE geerdet Netzl. offen Drehstrom |
| 72 | Gehäuseableitstrom SFC | Gehäuseableitstrom SFC Netzl. offen Drehstrom |
| 73 | Patientenableitstrom SFC TRMS | Patientenableitstrom SFC TRMS Netzl. offen Drehstrom |
| 74 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Netzl. offen Drehstrom |
| 75 | Patientenhilfsstrom SFC TRMS | Patientenhilfsstrom SFC TRMS Elektrode zu Elektrode Netzl. offen Drehstrom |
| 80 | Laststrom | Laststrom Standard |
| 81 | Betriebsspannung | Betriebsspannung Standard |
| 82 | Leistungsaufnahme | Leistungsaufnahme Standard |
| 83 | PE-Messtrom | PE-Messtrom Standard |
| 90 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 Summe SK I |
| 91 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 Summe SK II |
| 92 | Berührungsspannung NC AC | Berührungsspannung NC AC Standard |
| 93 | Berührungsspannung NC AC | Berührungsspannung NC AC Phase rev. |
| 94 | Berührungsspannung SFC AC | Berührungsspannung SFC AC PE offen |
| 95 | Berührungsspannung SFC AC | Berührungsspannung SFC AC PE offen Phase rev. |
| 96 | Berührungsspannung NC DC | Berührungsspannung NC DC Standard |
| 97 | Berührungsspannung NC DC | Berührungsspannung NC DC Phase rev. |
| 98 | Berührungsspannung SFC DC | Berührungsspannung SFC DC PE offen |
| 99 | Berührungsspannung SFC DC | Berührungsspannung SFC DC PE offen Phase rev. |
| 106 | Isolationswiderstand | Isolationswiderstand Schutzleiter |
| 107 | Isolationswiderstand | Isolationswiderstand Gehäuse |
| 108 | Schutzleiterwiderstand | Schutzleiterwiderstand VK701 |
| 109 | Ersatzgeräteableitstrom | Ersatzgeräteableitstrom SK I |
| 110 | Ersatzgeräteableitstrom | Ersatzgeräteableitstrom SK II |
| 111 | Schutzleiterstrom | Schutzleiterstrom direkte Messung |
| 112 | Schutzleiterstrom | Schutzleiterstrom direkte Messung Phase rev. |
| 113 | Schutzleiterstrom | Schutzleiterstrom Differenzstrom |
| 114 | Schutzleiterstrom | Schutzleiterstrom Differenzstrom Phase rev. |
| 115 | Berührungsstrom | Berührungsstrom direkte Messung |
| 116 | Berührungsstrom | Berührungsstrom direkte Messung Phase rev. |
| 117 | Berührungsstrom | Berührungsstrom Differenzstrom |
| 118 | Berührungsstrom | Berührungsstrom Differenzstrom Phase rev. |
| 120 | Isolationswiderstand Leitung | Isolationswiderstand Leitung L1 und L2 - PE |
| 121 | Isolationswiderstand Leitung | Isolationswiderstand Leitung VK701 L1 - PE |
| 122 | Isolationswiderstand Leitung | Isolationswiderstand Leitung VK701 L2 - PE |
| 123 | Isolationswiderstand Leitung | Isolationswiderstand Leitung VK701 L3 - PE |
| 124 | Isolationswiderstand Leitung | Isolationswiderstand Leitung VK701 N - PE |
| 125 | Isolationswiderstand Leitung | Isolationswiderstand Leitung VK701 L1 L2 L3 N - PE |
| 130 | Ers.ger.ableitstrom SKI/II VDE 0701 | Ers.ger.ableitstrom SKI/II VDE 0701 SK I Gehäuse n. mit PE verb. Teile |
| 131 | Isolationswiderstand SKI/II VDE 0701 | Isolationswiderstand SKI/II VDE 0701 SK I Gehäuse n. mit PE verb. Teile |
| 132 | Berührungsstrom NC AC | Berührungsstrom NC AC Standard |
| 133 | Berührungsstrom NC AC | Berührungsstrom NC AC Phase rev. |
| 134 | Berührungsstrom SFC AC | Berührungsstrom SFC AC PE offen |
| 135 | Berührungsstrom SFC AC | Berührungsstrom SFC AC PE offen Phase rev. |
| 136 | Berührungsstrom NC DC | Berührungsstrom NC DC Standard |
| 137 | Berührungsstrom NC DC | Berührungsstrom NC DC Phase rev. |
| 138 | Berührungsstrom SFC DC | Berührungsstrom SFC DC PE offen |
| 139 | Berührungsstrom SFC DC | Berührungsstrom SFC DC PE offen Phase rev. |
| 141 | Isolationswiderstand | Isolationswiderstand Systemselbsttest |
| 142 | Ersatzgeräteableitstrom | Ersatzgeräteableitstrom Systemselbsttest |
| 143 | Schutzleiterwiderstand | Schutzleiterwiderstand Systemselbsttest |
| 144 | Patientenhilfsstrom NC TRMS | Patientenhilfsstrom NC TRMS Systemselbsttest |
| 151 | Durchgang | Durchgang VK701 L1 - L1 |
| 152 | Durchgang | Durchgang VK701 L2 - L2 |
| 153 | Durchgang | Durchgang VK701 L3 - L3 |
| 154 | Durchgang | Durchgang VK701 N - N |
| 155 | Adern vertauscht | Adern vertauscht VK701 L1 - L2 |
| 156 | Adern vertauscht | Adern vertauscht VK701 L1 - L3 |
| 157 | Adern vertauscht | Adern vertauscht VK701 L1 - N |
| 158 | Adern vertauscht | Adern vertauscht VK701 L2 - L3 |
| 159 | Adern vertauscht | Adern vertauscht VK701 L2 - N |
| 160 | Adern vertauscht | Adern vertauscht VK701 L3 - N |
| 161 | ?-32000 Drehstrom Bitte Phase \PHASE am Drehstromadapter einstellen | ?-32000 Drehstrom Bitte Phase \PHASE am Drehstromadapter einstellen |
| 162 | ?-32000 Um alle Bedingungen nach ANSI/AAMI ES1 zu erfüllen; wie z.B. den Kurzschluss einer Isolierschicht der doppelten Isolation; ziehen Sie bitte die Norm zu Rate. | ?-32000 Um alle Bedingungen nach ANSI/AAMI ES1 zu erfüllen; wie z.B. den Kurzschluss einer Isolierschicht der doppelten Isolation; ziehen Sie bitte die Norm zu Rate. |
| 163 | ?-32000 Die prüfung mu¯ bei der höchstmöglichen Nennspannung des Prüflings durchgeführt werden.\nBsp.: Ein 120/230 Volt Gerät muss bei 230 Volt getestet werden. | ?-32000 Die prüfung mu¯ bei der höchstmöglichen Nennspannung des Prüflings durchgeführt werden.\nBsp.: Ein 120/230 Volt Gerät muss bei 230 Volt getestet werden. |
| 164 | ?-32000 Bitte stecken Sie die folgenden Brücken auf der TB3.\n\n\t10a -> b\n\t10d -> e\n\t10h -> i | ?-32000 Bitte stecken Sie die folgenden Brücken auf der TB3.\n\n\t10a -> b\n\t10d -> e\n\t10h -> i |
| 165 | ?-32000 Um Toleranzabweichungen beim Betrieb der TB3 zu vermeiden; sollte die Spannung zwischen N und PE < 100 mV sein. | ?-32000 Um Toleranzabweichungen beim Betrieb der TB3 zu vermeiden; sollte die Spannung zwischen N und PE < 100 mV sein. |
| 169 | Sichtprüfung Kurze Sichtprüfung | Sichtprüfung Kurze Sichtprüfung |
| 170 | Sichtprüfung Schäden am Gehäuse | Sichtprüfung Schäden am Gehäuse |
| 171 | Sichtprüfung -u¯ere Mängel der Anschlu¯leitungen | Sichtprüfung -u¯ere Mängel der Anschlu¯leitungen |
| 172 | Sichtprüfung Mängel an Biegeschutz und Zugentlastung | Sichtprüfung Mängel an Biegeschutz und Zugentlastung |
| 173 | Sichtprüfung Falsche Gerätesicherung\n(Nennstrom; Nennspannung;\nAbschaltcharakteristik) | Sichtprüfung Falsche Gerätesicherung\n(Nennstrom; Nennspannung;\nAbschaltcharakteristik) |
| 174 | Sichtprüfung Fehlende oder defekte Schutzabdeckungen | Sichtprüfung Fehlende oder defekte Schutzabdeckungen |
| 175 | Sichtprüfung Beschädigtes Netzkabel; Steuerkabel und Steckverbinder | Sichtprüfung Beschädigtes Netzkabel; Steuerkabel und Steckverbinder |
| 176 | Sichtprüfung Defekte Zugentlastung oder Kabelbefestigung im Bett | Sichtprüfung Defekte Zugentlastung oder Kabelbefestigung im Bett |
| 177 | Sichtprüfung Beschädigtes MotorGehäuse und Handschalter | Sichtprüfung Beschädigtes MotorGehäuse und Handschalter |
| 178 | Sichtprüfung Beschädigte Seitengitter - Holme | Sichtprüfung Beschädigte Seitengitter - Holme |
| 179 | Sichtprüfung Mängel an Schweissnähten bzw. verbogene Metallrahmenkonstruktion | Sichtprüfung Mängel an Schweissnähten bzw. verbogene Metallrahmenkonstruktion |
| 180 | Sichtprüfung Verschlissene Teile : Laufrollen; Bremsen; Gelenkpunkte etc. | Sichtprüfung Verschlissene Teile : Laufrollen; Bremsen; Gelenkpunkte etc. |
| 183 | Sichtprüfung Anzeichen von _berlastung und unsachgemä¯em Gebrauch | Sichtprüfung Anzeichen von _berlastung und unsachgemä¯em Gebrauch |
| 184 | Sichtprüfung Unzulässige Eingriffe und -nderungen | Sichtprüfung Unzulässige Eingriffe und -nderungen |
| 185 | Sichtprüfung Sicherheitsbeeinträchtigende Verschmutzung oder Korrosion | Sichtprüfung Sicherheitsbeeinträchtigende Verschmutzung oder Korrosion |
| 186 | Sichtprüfung Nicht alle erforderlichen Luftfilter sind vorhanden | Sichtprüfung Nicht alle erforderlichen Luftfilter sind vorhanden |
| 187 | Sichtprüfung Nicht alle vorhandenen Kühlöffnungen sind frei | Sichtprüfung Nicht alle vorhandenen Kühlöffnungen sind frei |
| 188 | Sichtprüfung Nicht alle sicherheits-\ndienlichen Aufschriften sind\neinwandfrei lesbar | Sichtprüfung Nicht alle sicherheits-\ndienlichen Aufschriften sind\neinwandfrei lesbar |
| 189 | Sichtprüfung Gefährdung durch erkennbare;\näu¯erliche Mängel | Sichtprüfung Gefährdung durch erkennbare;\näu¯erliche Mängel |
| 190 | Sichtprüfung Defekte Überdruckschutzeinrichtung | Sichtprüfung Defekte Überdruckschutzeinrichtung |
| 199 | Funktionsprüfung | Funktionsprüfung Standard |
| 210 | Geräteableitstrom VDE 0751 Geräteeräteableitstrom VDE 0751 SK I direkte Messung | Geräteableitstrom VDE 0751 Geräteeräteableitstrom VDE 0751 SK I direkte Messung |
| 211 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK I direkte Messung Phase rev. |
| 212 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK I Differenzstrom |
| 213 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK I Differenzstrom Phase rev. |
| 214 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II direkte Messung |
| 215 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II direkte Messung Phase rev. |
| 216 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II Differenzstrom |
| 217 | Geräteableitstrom VDE 0751 | Geräteableitstrom VDE 0751 SK II Differenzstrom Phase rev. |
| 219 | Ersatzpatientenableitstrom Typ BF | Ersatzpatientenableitstrom Typ BF SK I |
| 220 | Ersatzpatientenableitstrom Typ CF | Ersatzpatientenableitstrom Typ CF SK I |
| 221 | Ersatzpatientenableitstrom Typ BF | Ersatzpatientenableitstrom Typ BF SK II |
| 222 | Ersatzpatientenableitstrom Typ CF | Ersatzpatientenableitstrom Typ CF SK II |
| 223 | Patientenableitstrom NC DC | Patientenableitstrom NC DC Standard |
| 224 | Patientenableitstrom NC DC | Patientenableitstrom NC DC Phase rev. |
| 225 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC PE offen |
| 226 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC PE offen Phase rev. |
| 227 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC Netzl. offen |
| 228 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC Netzl. offen Phase rev. |
| 229 | Patientenableitstrom NC DC | Patientenableitstrom NC DC FE geerdet |
| 230 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC FE geerdet; PE offen |
| 235 | Patientenhilfsstrom NC DC | Patientenhilfsstrom NC DC Standard |
| 236 | Patientenhilfsstrom NC DC | Patientenhilfsstrom NC DC Phase rev. |
| 237 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC PE offen |
| 238 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC PE offen Phase rev. |
| 239 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC Netzl. offen |
| 240 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC Netzl. offen Phase rev. |
| 241 | Patientenhilfsstrom NC DC | Patientenhilfsstrom NC DC FE geerdet |
| 242 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC PE offen; FE geerdet |
| 249 | Patientenableitstrom NC DC | Patientenableitstrom NC DC interne Stromquelle |
| 251 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC interne Stromquelle Signal E/A |
| 252 | Patientenhilfsstrom NC DC | Patientenhilfsstrom NC DC interne Stromquelle |
| 273 | Patientenableitstrom SFC DC | Patientenableitstrom SFC DC Netzl. offen Drehstrom |
| 274 | Patientenhilfsstrom SFC DC | Patientenhilfsstrom SFC DC Netzl. offen Drehstrom |
| 280 | Patientenableitstrom Typ BF mit U-Netz am ATeil | Patientenableitstrom Typ BF mit U-Netz am ATeil Standard |
| 281 | Patientenableitstrom Typ CF mit U-Netz am ATeil | Patientenableitstrom Typ CF mit U-Netz am ATeil Standard |
| 282 | Patientenableitstrom Typ BF Phase rev. mit U-Netz am ATeil | Patientenableitstrom Typ BF Phase rev. mit U-Netz am ATeil Standard |
| 283 | Patientenableitstrom Typ CF Phase rev. mit U-Netz am ATeil | Patientenableitstrom Typ CF Phase rev. mit U-Netz am ATeil Standard |
| 284 | Ersatzpatientenableitstrom | Ersatzpatientenableitstrom interne Stromquelle |
| 286 | Patientenableitstrom Typ B DC | Patientenableitstrom Typ B DC Standard |
| 287 | Patientenableitstrom Typ BF DC | Patientenableitstrom Typ BF DC Standard |
| 288 | Patientenableitstrom Typ CF DC | Patientenableitstrom Typ CF DC Standard |
| 289 | Patientenableitstrom Typ B DC | Patientenableitstrom Typ B DC Phase rev. |
| 290 | Patientenableitstrom Typ BF DC | Patientenableitstrom Typ BF DC Phase rev. |
| 291 | Patientenableitstrom Typ CF DC | Patientenableitstrom Typ CF DC Phase rev. |
| 292 | Patientenableitstrom Typ B AC | Patientenableitstrom Typ B AC Standard |
| 293 | Patientenableitstrom Typ BF AC | Patientenableitstrom Typ BF AC Standard |
| 294 | Patientenableitstrom Typ CF AC | Patientenableitstrom Typ CF AC Standard |
| 295 | Patientenableitstrom Typ B AC | Patientenableitstrom Typ B AC Phase rev. |
| 296 | Patientenableitstrom Typ BF AC | Patientenableitstrom Typ BF AC Phase rev. |
| 297 | Patientenableitstrom Typ CF AC | Patientenableitstrom Typ CF AC Phase rev. |
| 323 | Patientenableitstrom NC AC | Patientenableitstrom NC AC Standard |
| 324 | Patientenableitstrom NC AC | Patientenableitstrom NC AC Phase rev. |
| 325 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC PE offen |
| 326 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC PE offen Phase rev. |
| 327 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC Netzl. offen |
| 328 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC Netzl. offen Phase rev. |
| 329 | Patientenableitstrom NC AC | Patientenableitstrom NC AC FE geerdet |
| 330 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC FE geerdet; PE offen |
| 335 | Patientenhilfsstrom NC AC | Patientenhilfsstrom NC AC Standard |
| 336 | Patientenhilfsstrom NC AC | Patientenhilfsstrom NC AC Phase rev. |
| 337 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC PE offen |
| 338 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC PE offen Phase rev. |
| 339 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC Netzl. offen |
| 340 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC Netzl. offen Phase rev. |
| 341 | Patientenhilfsstrom NC AC | Patientenhilfsstrom NC AC FE geerdet |
| 342 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC PE offen; FE geerdet |
| 349 | Patientenableitstrom NC AC | Patientenableitstrom NC AC interne Stromquelle |
| 351 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC interne Stromquelle Signal E/A |
| 352 | Patientenhilfsstrom NC AC | Patientenhilfsstrom NC AC interne Stromquelle |
| 373 | Patientenableitstrom SFC AC | Patientenableitstrom SFC AC Netzl. offen Drehstrom |
| 374 | Patientenhilfsstrom SFC AC | Patientenhilfsstrom SFC AC Netzl. offen Drehstrom |
| 401 | Patientenableitstrom Typ B NC TRMS | Patientenableitstrom Typ B NC TRMS Standard |
| 402 | Patientenableitstrom Typ BF NC TRMS | Patientenableitstrom Typ BF NC TRMS Standard |
| 403 | Patientenableitstrom Typ CF NC TRMS | Patientenableitstrom Typ CF NC TRMS Standard |
| 404 | Patientenableitstrom Typ B NC TRMS | Patientenableitstrom Typ B NC TRMS Phase rev. |
| 405 | Patientenableitstrom Typ BF NC TRMS | Patientenableitstrom Typ BF NC TRMS Phase rev. |
| 406 | Patientenableitstrom Typ CF NC TRMS | Patientenableitstrom Typ CF NC TRMS Phase rev. |
| 407 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS PE offen |
| 408 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS PE offen |
| 409 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS PE offen |
| 410 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS PE offen Phase rev. |
| 411 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS PE offen Phase rev. |
| 412 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS PE offen Phase rev. |
| 413 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS Netzl. offen |
| 414 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS Netzl. offen |
| 415 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS Netzl. offen |
| 416 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS Netzl. offen Phase rev. |
| 417 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS Netzl. offen Phase rev. |
| 418 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS Netzl. offen Phase rev. |
| 419 | Patientenableitstrom Typ B NC TRMS | Patientenableitstrom Typ B NC TRMS FE geerdet |
| 420 | Patientenableitstrom Typ BF NC TRMS | Patientenableitstrom Typ BF NC TRMS FE geerdet |
| 421 | Patientenableitstrom Typ CF NC TRMS | Patientenableitstrom Typ CF NC TRMS FE geerdet |
| 422 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS FE geerdet; PE offen |
| 423 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS FE geerdet; PE offen |
| 424 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS FE geerdet; PE offen |
| 425 | Patientenhilfsstrom Typ B NC TRMS | Patientenhilfsstrom Typ B NC TRMS Standard |
| 426 | Patientenhilfsstrom Typ BF NC TRMS | Patientenhilfsstrom Typ BF NC TRMS Standard |
| 427 | Patientenhilfsstrom Typ CF NC TRMS | Patientenhilfsstrom Typ CF NC TRMS Standard |
| 428 | Patientenhilfsstrom Typ B NC TRMS | Patientenhilfsstrom Typ B NC TRMS Phase rev. |
| 429 | Patientenhilfsstrom Typ BF NC TRMS | Patientenhilfsstrom Typ BF NC TRMS Phase rev. |
| 430 | Patientenhilfsstrom Typ CF NC TRMS | Patientenhilfsstrom Typ CF NC TRMS Phase rev. |
| 431 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS PE offen |
| 432 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS PE offen |
| 433 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS PE offen |
| 434 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS PE offen Phase rev. |
| 435 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS PE offen Phase rev. |
| 436 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS PE offen Phase rev. |
| 437 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS Netzl. offen |
| 438 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS Netzl. offen |
| 439 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS Netzl. offen |
| 440 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS Netzl. offen Phase rev. |
| 441 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS Netzl. offen Phase rev. |
| 442 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS Netzl. offen Phase rev. |
| 443 | Patientenhilfsstrom Typ B NC TRMS | Patientenhilfsstrom Typ B NC TRMS FE geerdet |
| 444 | Patientenhilfsstrom Typ BF NC TRMS | Patientenhilfsstrom Typ BF NC TRMS FE geerdet |
| 445 | Patientenhilfsstrom Typ CF NC TRMS | Patientenhilfsstrom Typ CF NC TRMS FE geerdet |
| 446 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS PE offen; FE geerdet |
| 447 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS PE offen; FE geerdet |
| 448 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS PE offen; FE geerdet |
| 449 | Patientenableitstrom Typ B NC TRMS | Patientenableitstrom Typ B NC TRMS interne Stromquelle |
| 450 | Patientenableitstrom Typ BF NC TRMS | Patientenableitstrom Typ BF NC TRMS interne Stromquelle |
| 451 | Patientenableitstrom Typ CF NC TRMS | Patientenableitstrom Typ CF NC TRMS interne Stromquelle |
| 452 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS interne Stromquelle Signal E/A |
| 453 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS interne Stromquelle Signal E/A |
| 454 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS interne Stromquelle Signal E/A |
| 455 | Patientenhilfsstrom Typ B NC TRMS | Patientenhilfsstrom Typ B NC TRMS interne Stromquelle |
| 456 | Patientenhilfsstrom Typ BF NC TRMS | Patientenhilfsstrom Typ BF NC TRMS interne Stromquelle |
| 457 | Patientenhilfsstrom Typ CF NC TRMS | Patientenhilfsstrom Typ CF NC TRMS interne Stromquelle |
| 458 | Patientenhilfsstrom Typ B NC TRMS | Patientenhilfsstrom Typ B NC TRMS Elektrode zu Elektrode interne Stromquelle |
| 459 | Patientenhilfsstrom Typ BF NC TRMS | Patientenhilfsstrom Typ BF NC TRMS Elektrode zu Elektrode interne Stromquelle |
| 460 | Patientenhilfsstrom Typ CF NC TRMS | Patientenhilfsstrom Typ CF NC TRMS Elektrode zu Elektrode interne Stromquelle |
| 461 | Patientenableitstrom Typ B SFC TRMS | Patientenableitstrom Typ B SFC TRMS Netzl. offen Drehstrom |
| 462 | Patientenableitstrom Typ BF SFC TRMS | Patientenableitstrom Typ BF SFC TRMS Netzl. offen Drehstrom |
| 463 | Patientenableitstrom Typ CF SFC TRMS | Patientenableitstrom Typ CF SFC TRMS Netzl. offen Drehstrom |
| 464 | Patientenhilfsstrom Typ B SFC TRMS | Patientenhilfsstrom Typ B SFC TRMS Netzl. offen Drehstrom |
| 465 | Patientenhilfsstrom Typ BF SFC TRMS | Patientenhilfsstrom Typ BF SFC TRMS Netzl. offen Drehstrom |
| 466 | Patientenhilfsstrom Typ CF SFC TRMS | Patientenhilfsstrom Typ CF SFC TRMS Netzl. offen Drehstrom |
| 467 | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil Standard |
| 468 | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil Standard |
| 469 | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil Phase rev. |
| 470 | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil Phase rev. |
| 471 | Patientenableitstrom Typ BF SFC Phase rev. mit U-Netz am ATeil | Patientenableitstrom Typ BF SFC Phase rev. mit U-Netz am ATeil Standard |
| 472 | Patientenableitstrom Typ CF SFC Phase rev. mit U-Netz am ATeil | Patientenableitstrom Typ CF SFC Phase rev. mit U-Netz am ATeil Standard |
| 473 | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil FE geerdet |
| 474 | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil FE geerdet |
| 475 | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil | Patientenableitstrom Typ BF SFC mit U-Netz am ATeil interne Stromquelle |
| 476 | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil | Patientenableitstrom Typ CF SFC mit U-Netz am ATeil interne Stromquelle |
| 501 | Patientenableitstrom Typ B NC DC | Patientenableitstrom Typ B NC DC Standard |
| 502 | Patientenableitstrom Typ BF NC DC | Patientenableitstrom Typ BF NC DC Standard |
| 503 | Patientenableitstrom Typ CF NC DC | Patientenableitstrom Typ CF NC DC Standard |
| 504 | Patientenableitstrom Typ B NC DC | Patientenableitstrom Typ B NC DC Phase rev. |
| 505 | Patientenableitstrom Typ BF NC DC | Patientenableitstrom Typ BF NC DC Phase rev. |
| 506 | Patientenableitstrom Typ CF NC DC | Patientenableitstrom Typ CF NC DC Phase rev. |
| 507 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC PE offen |
| 508 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC PE offen |
| 509 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC PE offen |
| 510 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC PE offen Phase rev. |
| 511 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC PE offen Phase rev. |
| 512 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC PE offen Phase rev. |
| 513 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC Netzl. offen |
| 514 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC Netzl. offen |
| 515 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC Netzl. offen |
| 516 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC Netzl. offen Phase rev. |
| 517 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC Netzl. offen Phase rev. |
| 518 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC Netzl. offen Phase rev. |
| 519 | Patientenableitstrom Typ B NC DC | Patientenableitstrom Typ B NC DC FE geerdet |
| 520 | Patientenableitstrom Typ BF NC DC | Patientenableitstrom Typ BF NC DC FE geerdet |
| 521 | Patientenableitstrom Typ CF NC DC | Patientenableitstrom Typ CF NC DC FE geerdet |
| 522 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC FE geerdet; PE offen |
| 523 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC FE geerdet; PE offen |
| 524 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC FE geerdet; PE offen |
| 525 | Patientenhilfsstrom Typ B NC DC | Patientenhilfsstrom Typ B NC DC Standard |
| 526 | Patientenhilfsstrom Typ BF NC DC | Patientenhilfsstrom Typ BF NC DC Standard |
| 527 | Patientenhilfsstrom Typ CF NC DC | Patientenhilfsstrom Typ CF NC DC Standard |
| 528 | Patientenhilfsstrom Typ B NC DC | Patientenhilfsstrom Typ B NC DC Phase rev. |
| 529 | Patientenhilfsstrom Typ BF NC DC | Patientenhilfsstrom Typ BF NC DC Phase rev. |
| 530 | Patientenhilfsstrom Typ CF NC DC | Patientenhilfsstrom Typ CF NC DC Phase rev. |
| 531 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC PE offen |
| 532 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC PE offen |
| 533 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC PE offen |
| 534 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC PE offen Phase rev. |
| 535 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC PE offen Phase rev. |
| 536 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC PE offen Phase rev. |
| 537 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC Netzl. offen |
| 538 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC Netzl. offen |
| 539 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC Netzl. offen |
| 540 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC Netzl. offen Phase rev. |
| 541 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC Netzl. offen Phase rev. |
| 542 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC Netzl. offen Phase rev. |
| 543 | Patientenhilfsstrom Typ B NC DC | Patientenhilfsstrom Typ B NC DC FE geerdet |
| 544 | Patientenhilfsstrom Typ BF NC DC | Patientenhilfsstrom Typ BF NC DC FE geerdet |
| 545 | Patientenhilfsstrom Typ CF NC DC | Patientenhilfsstrom Typ CF NC DC FE geerdet |
| 546 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC PE offen; FE geerdet |
| 547 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC PE offen; FE geerdet |
| 548 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC PE offen; FE geerdet |
| 549 | Patientenableitstrom Typ B NC DC | Patientenableitstrom Typ B NC DC interne Stromquelle |
| 550 | Patientenableitstrom Typ BF NC DC | Patientenableitstrom Typ BF NC DC interne Stromquelle |
| 551 | Patientenableitstrom Typ CF NC DC | Patientenableitstrom Typ CF NC DC interne Stromquelle |
| 552 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC interne Stromquelle Signal E/A |
| 553 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC interne Stromquelle Signal E/A |
| 554 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC interne Stromquelle Signal E/A |
| 555 | Patientenhilfsstrom Typ B NC DC | Patientenhilfsstrom Typ B NC DC interne Stromquelle |
| 556 | Patientenhilfsstrom Typ BF NC DC | Patientenhilfsstrom Typ BF NC DC interne Stromquelle |
| 557 | Patientenhilfsstrom Typ CF NC DC | Patientenhilfsstrom Typ CF NC DC interne Stromquelle |
| 558 | Patientenableitstrom Typ B SFC DC | Patientenableitstrom Typ B SFC DC Netzl. offen Drehstrom |
| 559 | Patientenableitstrom Typ BF SFC DC | Patientenableitstrom Typ BF SFC DC Netzl. offen Drehstrom |
| 560 | Patientenableitstrom Typ CF SFC DC | Patientenableitstrom Typ CF SFC DC Netzl. offen Drehstrom |
| 561 | Patientenhilfsstrom Typ B SFC DC | Patientenhilfsstrom Typ B SFC DC Netzl. offen Drehstrom |
| 562 | Patientenhilfsstrom Typ BF SFC DC | Patientenhilfsstrom Typ BF SFC DC Netzl. offen Drehstrom |
| 563 | Patientenhilfsstrom Typ CF SFC DC | Patientenhilfsstrom Typ CF SFC DC Netzl. offen Drehstrom |
| 601 | Patientenableitstrom Typ B NC AC | Patientenableitstrom Typ B NC AC Standard |
| 602 | Patientenableitstrom Typ BF NC AC | Patientenableitstrom Typ BF NC AC Standard |
| 603 | Patientenableitstrom Typ CF NC AC | Patientenableitstrom Typ CF NC AC Standard |
| 604 | Patientenableitstrom Typ B NC AC | Patientenableitstrom Typ B NC AC Phase rev. |
| 605 | Patientenableitstrom Typ BF NC AC | Patientenableitstrom Typ BF NC AC Phase rev. |
| 606 | Patientenableitstrom Typ CF NC AC | Patientenableitstrom Typ CF NC AC Phase rev. |
| 607 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC PE offen |
| 608 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC PE offen |
| 609 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC PE offen |
| 610 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC PE offen Phase rev. |
| 611 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC PE offen Phase rev. |
| 612 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC PE offen Phase rev. |
| 613 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC Netzl. offen |
| 614 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC Netzl. offen |
| 615 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC Netzl. offen |
| 616 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC Netzl. offen Phase rev. |
| 617 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC Netzl. offen Phase rev. |
| 618 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC Netzl. offen Phase rev. |
| 619 | Patientenableitstrom Typ B NC AC | Patientenableitstrom Typ B NC AC FE geerdet |
| 620 | Patientenableitstrom Typ BF NC AC | Patientenableitstrom Typ BF NC AC FE geerdet |
| 621 | Patientenableitstrom Typ CF NC AC | Patientenableitstrom Typ CF NC AC FE geerdet |
| 622 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC FE geerdet; PE offen |
| 623 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC FE geerdet; PE offen |
| 624 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC FE geerdet; PE offen |
| 625 | Patientenhilfsstrom Typ B NC AC | Patientenhilfsstrom Typ B NC AC Standard |
| 626 | Patientenhilfsstrom Typ BF NC AC | Patientenhilfsstrom Typ BF NC AC Standard |
| 627 | Patientenhilfsstrom Typ CF NC AC | Patientenhilfsstrom Typ CF NC AC Standard |
| 628 | Patientenhilfsstrom Typ B NC AC | Patientenhilfsstrom Typ B NC AC Phase rev. |
| 629 | Patientenhilfsstrom Typ BF NC AC | Patientenhilfsstrom Typ BF NC AC Phase rev. |
| 630 | Patientenhilfsstrom Typ CF NC AC | Patientenhilfsstrom Typ CF NC AC Phase rev. |
| 631 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC PE offen |
| 632 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC PE offen |
| 633 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC PE offen |
| 634 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC PE offen Phase rev. |
| 635 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC PE offen Phase rev. |
| 636 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC PE offen Phase rev. |
| 637 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC Netzl. offen |
| 638 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC Netzl. offen |
| 639 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC Netzl. offen |
| 640 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC Netzl. offen Phase rev. |
| 641 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC Netzl. offen Phase rev. |
| 642 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC Netzl. offen Phase rev. |
| 643 | Patientenhilfsstrom Typ B NC AC | Patientenhilfsstrom Typ B NC AC FE geerdet |
| 644 | Patientenhilfsstrom Typ BF NC AC | Patientenhilfsstrom Typ BF NC AC FE geerdet |
| 645 | Patientenhilfsstrom Typ CF NC AC | Patientenhilfsstrom Typ CF NC AC FE geerdet |
| 646 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC PE offen; FE geerdet |
| 647 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC PE offen; FE geerdet |
| 648 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC PE offen; FE geerdet |
| 649 | Patientenableitstrom Typ B NC AC | Patientenableitstrom Typ B NC AC interne Stromquelle |
| 650 | Patientenableitstrom Typ BF NC AC | Patientenableitstrom Typ BF NC AC interne Stromquelle |
| 651 | Patientenableitstrom Typ CF NC AC | Patientenableitstrom Typ CF NC AC interne Stromquelle |
| 652 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC interne Stromquelle Signal E/A |
| 653 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC interne Stromquelle Signal E/A |
| 654 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC interne Stromquelle Signal E/A |
| 655 | Patientenhilfsstrom Typ B NC AC | Patientenhilfsstrom Typ B NC AC interne Stromquelle |
| 656 | Patientenhilfsstrom Typ BF NC AC | Patientenhilfsstrom Typ BF NC AC interne Stromquelle |
| 657 | Patientenhilfsstrom Typ CF NC AC | Patientenhilfsstrom Typ CF NC AC interne Stromquelle |
| 658 | Patientenableitstrom Typ B SFC AC | Patientenableitstrom Typ B SFC AC Netzl. offen Drehstrom |
| 659 | Patientenableitstrom Typ BF SFC AC | Patientenableitstrom Typ BF SFC AC Netzl. offen Drehstrom |
| 660 | Patientenableitstrom Typ CF SFC AC | Patientenableitstrom Typ CF SFC AC Netzl. offen Drehstrom |
| 661 | Patientenhilfsstrom Typ B SFC AC | Patientenhilfsstrom Typ B SFC AC Netzl. offen Drehstrom |
| 662 | Patientenhilfsstrom Typ BF SFC AC | Patientenhilfsstrom Typ BF SFC AC Netzl. offen Drehstrom |
| 663 | Patientenhilfsstrom Typ CF SFC AC | Patientenhilfsstrom Typ CF SFC AC Netzl. offen Drehstrom |

### Prüfschritte UNIMET 300 ST (zum Vergleich, mit Grenzwerten)

Diese Tabelle nennt zusätzlich Einheit und Grenzwertbereich. `*` = aus Kompatibilität zum Unimet 1100 separat geführt (106 entspricht 6, 107 entspricht 5).

| Nr. | Messname | Einheit | min. | max. |
|---:|---|---|---:|---:|
| 3 | Schutzleiterwiderstand feste Leitung | Ohm | 0.001 | 30 |
| 5 | Isolationswiderstand SK2 | MOhm | 0.01 | 300 |
| 6 | Isolationswiderstand SKI | MOhm | 0.01 | 300 |
| 80 | Laststrom | A | 0.005 | 16 |
| 81 | Netzspannung | V | 94 | 264 |
| 82 | Leistungsaufnahme | kVA | 0.005 | 3.600 |
| 106* | Isolationswiderstand SKI | MOhm | 0.01 | 300 |
| 107* | Isolationswiderstand SKII | MOhm | 0.01 | 300 |
| 109 | Ersatzgeräteableitstrom SKI | mA | 0.001 | 20 |
| 110 | Ersatzgeräteableitstrom SKII | mA | 0.001 | 20 |
| 113 | Schutzleiterstrom | mA | 0.02 | 20 |
| 114 | Schutzleiterstrom Phase rev. | mA | 0.02 | 20 |
| 117 | Berührungsstrom | mA | 0.02 | 20 |
| 118 | Berührungsstrom Phase rev. | mA | 0.02 | 20 |
| 120 | Isolationswiderstand Verl.-Leitg. | MOhm | 0.01 | 300 |
| 169 | Sichtprüfung kurz |  | 0 | 1 |
| 199 | Funktionsprüfung |  | 0 | 1 |
| 212 | Geräteableitstrom SK1 | mA | 0.02 | 20 |
| 213 | Geräteableitstrom SK1 Phase rev. | mA | 0.02 | 20 |
| 216 | Geräteableitstrom SK2 | mA | 0.02 | 20 |
| 217 | Geräteableitstrom SK2 Phase rev. | mA | 0.02 | 20 |

## 4. Befehlsliste UNIMET 1000/1100 ST

Befehle mit `?` sind Abfragen, solche ohne setzen einen Wert. Die Spalte *Langform* zeigt die Schreibweise des Handbuchs, bei der die Großbuchstaben die Kurzform ergeben.

### U1000 Query

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :SYStem

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :SYStem:CTRL

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:IDNR?` | IDNR? | Abfrage Hersteller |
| `:IDNM?` | IDNModel? | Abfrage Gerätebezeichnung |
| `:IDNF?` | IDNFirmware? | Abfrage der Firmware(Software-Version) |
| `:IDNH?` | IDNHardware? | Abfrage Hardware-Version |
| `:IDNS?` | IDNSerialnumber? | Abfrage Seriennummer des Gerätes |
| `:IDPC?` | IDPCversion? | Abfrage der PC Hardwareversion |
| `:SYS` | SYStem | Systemabfrage |
| `:DATA` | DATAbase | Datenbankabfragen |
| `:MEAS` | MEASurement | Zugriff auf Messungen |
| `:SYS:CTRL` | CTRL | Controller |
| `:SYS:CTRL:NR1I` | NR1I | Auslösen der Messnummer NR1I |
| `:DATA:ACT` | ACTuell | Aktueller Datenbankeintrag |
| `:DATA:CAT` | CATalogue | Kataloge bearbeiten |

### U1000 Query :DATAbase:ACTuell

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:ATTR?` | ATTRibut? | Abfrage des aktuellen Datensatzattributes |
| `:DATA:ACT:ID?` | ID? | Abfrage der Geräte ID im aktuellen Datensatz |
| `:DATA:ACT:ID` | ID |  |
| `:DATA:ACT:TYP?` | TYP? | Abfrage des Gerätetypes im aktuellen Datensatz |
| `:DATA:ACT:TYP` | TYP |  |
| `:DATA:ACT:SNO?` | SerialNumerO? | Abfrage der Seriennummer im aktuellen Datensatz |
| `:DATA:ACT:SNO` | SerialNumerO |  |
| `:DATA:ACT:MANU?` | MANUfactur? | Abfrage des Herstellers im aktuellen Datensatz |
| `:DATA:ACT:MANU` | MANUfactur |  |
| `:DATA:ACT:DEVD?` | DEViceDesignation? | Abfrage der Gerätebezeichnung im aktuellen Datensatz |
| `:DATA:ACT:TSTM?` | TeSTMode? | Abfrage der Prüfablaufes (Ziffer) des aktuellen Datensatzes |
| `:DATA:ACT:TSTM` | TeSTMode |  |
| `:DATA:ACT:CLAS?` | CLASs? | Abfrage der Schutzklasse (Ziffer) des akt. Datensatzes |
| `:DATA:ACT:CLAS` | CLASs |  |
| `:DATA:ACT:AP?` | AppliedPart? | Abfrage des Anwendungsteiles(ziffer) des akt.Datens. |
| `:DATA:ACT:AP` | AppliedPart |  |
| `:DATA:ACT:ELEC?` | ELECtrodes? | Abfrage der Anzahl der Elektroden im akt. Datensatz |
| `:DATA:ACT:ELEC` | ELECtrodes |  |
| `:DATA:ACT:EINF?` | ElectrodesINFo? | Abfrage Patientenbuchsen Info |
| `:DATA:ACT:EINF` | ElectrodesINFo |  |
| `:DATA:ACT:CHAR?` | CHARacteristics? | Abfrage der Gerätebezeichnung(Ziffer) im akt. Datensatz |
| `:DATA:ACT:CHAR` | CHARacteristics |  |
| `:DATA:ACT:NO?` | NumerOortransformers? | Abfrage der Trafoanzahl(Ziffer) im akt.Datensatz |
| `:DATA:ACT:NO` | NumerOortransformers |  |
| `:DATA:ACT:TSTD?` | TestSTanDard? | Abfrage der Prüfnorm(Ziffer) im akt. Datensatz |
| `:DATA:ACT:TSTD` | TestSTanDard |  |
| `:DATA:ACT:UMT?` | UserModifiedTest? | Abfrage nach modif. Prüfablauf(Ziffer) im akt. Datensatz |
| `:DATA:ACT:UMT` | UserModifiedTest |  |
| `:DATA:ACT:POOC?` | PowerOnOffControl? | Abfrage nach Warmlaufphase(Ziffer) im akt. Datensatz |
| `:DATA:ACT:POOC` | PowerOnOffControl |  |
| `:DATA:ACT:WARN?` | WARNing? | Abfrage nach Warnhinweis(Ziffer) im akt. Datensatz |
| `:DATA:ACT:WARN` | WARNing |  |
| `:DATA:ACT:CLEN?` | CordLENth? | Abfrage der Leitungslänge im akt. Datensatz |
| `:DATA:ACT:CLEN` | CordLENth |  |
| `:DATA:ACT:NPWR?` | NominalPoWeRconsumtion? | Abfrage der Leistungsaufnahme(Großküche) im akt. Datens. |
| `:DATA:ACT:NPWR` | NominalPoWeRconsumtion |  |
| `:DATA:ACT:DAT?` | DATe? | Abfrage des Datums(Seriell sek. nach 1970) im akt. Datens. |
| `:DATA:ACT:DAT` | DATe |  |
| `:DATA:ACT:ENG?` | testENGineer? | Abfrage des Prüfernamen im akt. Datensatz |
| `:DATA:ACT:ENG` | testENGineer |  |
| `:DATA:ACT:VNO?` | VoltageNOminal? | Abfrage der Nennspannung im akt. DAtensatz |
| `:DATA:ACT:VNO` | VoltageNOminal |  |
| `:DATA:ACT:RDAT?` | RefDATe? | Abfrage des Referenzdatums(seriell) im akt. Datensatz |
| `:DATA:ACT:RDAT` | RefDATe |  |
| `:DATA:ACT:RENG?` | ReferencetestENGineer? | Abfrage des Referenzprüfernamen im akt. Datensatz |
| `:DATA:ACT:RENG` | ReferencetestENGineer |  |
| `:DATA:ACT:RVNO?` | ReferenceVoltageNOminal? | Abfrage der Referenznennspannung im akt. Datensatz |
| `:DATA:ACT:RVNO` | ReferenceVoltageNOminal |  |
| `:DATA:ACT:FSTR?` | FktSTR? | Abfrage der Klassifikationsstringes im akt. Datensatz |
| `:DATA:ACT:FSTR` | FktSTR |  |
| `:DATA:ACT:COMT?` | COMenT? | Abfrage des Kommentars im akt. Datensatz |
| `:DATA:ACT:COMT` | COMenT |  |
| `:DATA:ACT:P1?` | Place1building? | Abfrage des Gebäudes im akt. Datensatz |
| `:DATA:ACT:P1` | Place1building |  |
| `:DATA:ACT:P2?` | Place2department? | Abfrage der Abteilung im akt. Datensatz |
| `:DATA:ACT:P2` | Place2department |  |
| `:DATA:ACT:P3?` | Place3room? | Abfrage des Zimmers im akt. Datensatz |
| `:DATA:ACT:P3` | Place3room |  |
| `:DATA:ACT:PRIC?` | PRICe? | Abfrage des Preises im akt. Datensatz |
| `:DATA:ACT:PRIC` | PRICe |  |
| `:DATA:ACT:TEST` | TESTstep | Prüfschrittabfrage |

### U1000 Query :DATAbase:ACTuell:ID

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:TYP

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:SerialNumerO

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:MANUfactur

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:DEViceDesignation?

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:TeSTMode

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:ID:WIDT?` | WIDTh? | Abfrage der Feldbreite für Geräte ID im aktuellen Datensatz |
| `:DATA:ACT:TYP:WIDT` |  | ? WIDTh? Abfrage der Feldbreite für Gerätetyp im aktuellen Datensatz |
| `:DATA:ACT:SNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Seriennr. im aktuellen Datensatz |
| `:DATA:ACT:MANU:WIDT?` | WIDTh? | Abfrage der Feldbreite für Hersteller im aktuellen Datensatz |
| `:DATA:ACT:DEVD?:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gerätebezeichnung im aktuellen Datensatz |
| `:DATA:ACT:TSTM:NAME?` | NAME? | Abfrage der Prüfablaufes (Name) des aktuellen Datensatzes |
| `:DATA:ACT:TSTM:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfablaufes (Name) des akt. Datensatzes |

### U1000 Query :DATAbase:ACTuell:CLASs

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:AppliedPart

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:ELECtrodes

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:ElectrodesINFo

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:CHARacteristics

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:NumerOortransformers

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:CLAS:NAME?` | NAME? | Abfrage der Schutzklasse (Name) des akt. Datensatzes |
| `:DATA:ACT:CLAS:WIDT?` | WIDTh? | Abfrage der Feldbreite für Schutzklasse (Name) des akt. Datensatzes |
| `:DATA:ACT:AP:NAME?` | NAME? | Abfrage des Anwendungsteiles(Name) des akt.Datens. |
| `:DATA:ACT:AP:WIDT?` | WIDTh? | Abfrage der Feldbreite des Anwendungsteiles(Name) des akt.Datens. |
| `:DATA:ACT:ELEC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Elektrodenanzahl |
| `:DATA:ACT:EINF:WIDT?` | WIDTh? | Noch nicht verwendet |
| `:DATA:ACT:CHAR:NAME?` | NAME? | Abfrage der Gerätebezeichnung(Name) im akt. Datensatz |
| `:DATA:ACT:CHAR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gerätebez.(NAme) im akt. Datens. |
| `:DATA:ACT:NO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Trafoanzahl in akt. Datens. |

### U1000 Query :DATAbase:ACTuell:TestSTanDard

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:UserModifiedTest

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:PowerOnOffControl

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:WARNing

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:CordLENth

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:TSTD:NAME?` | NAME? | Abfrage der Prüfnorm(Name) im akt. Datensatz |
| `:DATA:ACT:TSTD:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfnorm(Name) im akt. Datens. |
| `:DATA:ACT:UMT:NAME?` | NAME? | Abfrage nach modif. Prüfablauf(Name) im akt.Datensatz |
| `:DATA:ACT:UMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Modif. Prüfablauf(Name) im akt. Datens. |
| `:DATA:ACT:POOC:NAME?` | NAME? | Abfrage nach Warmlaufphase(Name) im akt.Datensatz |
| `:DATA:ACT:POOC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Warmlaufphase(Name) im akt. Datens. |
| `:DATA:ACT:WARN:NAME?` | NAME? | Abfrage nach Warnhinweis(Name) im akt.Datensatz |
| `:DATA:ACT:WARN:WIDT?` | WIDTh? | Abfrage der Feldbreite für Warnhinweis(Name) im akt. Datens. |
| `:DATA:ACT:CLEN:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leitungslänge im akt. Datensatz |

### U1000 Query :DATAbase:ACTuell:NominalPoWeRconsumtion

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:DATe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:testENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:VoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:RefDATe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:ReferencetestENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:NPWR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leistungsaufnahme(Großküche) im akt. Datens. |
| `:DATA:ACT:DAT:NAME?` | NAME? | Abfrage des Datums(dd.mm.yyyy) im akt. Datensatz |
| `:DATA:ACT:DAT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Datum(dd.mm.yyyy) im akt. Datensatz |
| `:DATA:ACT:ENG:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfername im akt. Datensatz |
| `:DATA:ACT:VNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Nennspannung im akt. Datensatz |
| `:DATA:ACT:RDAT:NAME?` | NAME? | Abfrage des Referenzdatums(dd.mm.yyyy) im akt.Datensatz |
| `:DATA:ACT:RDAT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzdatum(seriell) im akt. Datens. |
| `:DATA:ACT:RENG:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzprüfernamen im akt. Datens. |

### U1000 Query :DATAbase:ACTuell:ReferenceVoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:FktSTR

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:COMenT

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:Place1building

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:Place2department

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:Place3room

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:RVNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenznennspannung im akt. Datens. |
| `:DATA:ACT:FSTR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Klassifikationsstring im akt. Datens. |
| `:DATA:ACT:COMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Kommentar im akt. Datensatz |
| `:DATA:ACT:P1:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gebäude im akt. Datensatz |
| `:DATA:ACT:P2:WIDT?` | WIDTh? | Abfrage der Feldbreite für Abteilung im akt. Datensatz |
| `:DATA:ACT:P3:WIDT?` | WIDTh? | Abfrage der Feldbreite für Zimmer im akt.Datensatz |

### U1000 Query :DATAbase:ACTuell:PRICe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:TESTstep

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:TESTstep:ThREShold

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:PRIC:WIDT?` | WIDTh? | Abfrage der Feldbreite für akt. Datensatz |
| `:DATA:ACT:TEST:FIRS?` | FIRStstepno? | Abfrage der ersten Messnummer im akt. Datensatz |
| `:DATA:ACT:TEST:NEXT?` | NEXTstepno? | Abfrage der nächsten Messnummer im akt. Datensatz |
| `:DATA:ACT:TEST:STEP?` | STEPno? | Abfrage der augenblicklichen Messnummer im akt. DAtensatz |
| `:DATA:ACT:TEST:IDX?` | InDeX? | Abfrage der Prüfschrittnummer im akt. Datensatz |
| `:DATA:ACT:TEST:TRES?` | ThREShold? | Abfrage des moment. Grenzwertes des akt. Datensatzes |
| `:DATA:ACT:TEST:TRES` | ThREShold |  |
| `:DATA:ACT:TEST:RVAL?` | ReferenceVALue? | Abfrage des moment. Referenzmesswertes im akt. Datensatz |
| `:DATA:ACT:TEST:RVAL` | ReferenceVALue |  |
| `:DATA:ACT:TEST:VAL?` | VALue? | Abfrage des moment. Messwertes im akt.Datensatz |
| `:DATA:ACT:TEST:VAL` | VALue |  |
| `:DATA:ACT:TEST:UNIT?` | UNIT? | Abfrage der moment. Einheit im akt. Datensatz |
| `:DATA:ACT:TEST:HLO?` | HighLowOfftoleranz? | Abfrage der moment. Toleranzbewertung im akt. Datensatz |
| `:DATA:ACT:TEST:NAME?` | NAME? | Abfrage der Messung (Name komplett) im akt. Datensatz |
| `:DATA:ACT:TEST:SHOR?` | SHORtname? | Abfrage der Messung (Name kurz) im akt.Datensatz |
| `:DATA:ACT:TEST:CODE?` | CODE? | Datenbankzugriffe |
| `:DATA:ACT:TEST:TRES:WIDT?` | WIDTh? | Abfrage der Feldbreite für moment. Grenzwert im akt. Datensatz |

### U1000 Query :DATAbase:ACTuell:TESTstep:ReferenceVALue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:ACTuell:TESTstep:VALue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:ACT:TEST:RVAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für moment. Referenzmesswert im akt. Datensatz |
| `:DATA:ACT:TEST:VAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für moment. Messwert im akt. Datensatz |
| `:DATA:CAT:ID` | ID | Geraetekatalog |
| `:DATA:CAT:TYP` | TYP | Typenkatalog |
| `:DATA:CAT:ID:FIRS?` | FIRStid? | Abfrage erster Geräteeintrag im Gerätekatalog |
| `:DATA:CAT:ID:NEXT?` | NEXTid? | Abfrage der nächsten Geräte ID im Gerätekatalog |
| `:DATA:CAT:ID:FIND` | FIND | Direktes Suchen im Gerätekatalog |
| `:DATA:CAT:ID:DEL` | DELeteid | Anlegen einer neuen Geräte ID im Gerätekatalog |
| `:DATA:CAT:ID:NEW` | NEWid |  |
| `:DATA:CAT:ID:EDIT` | EDITid | Editieren der Geräte ID im akt. Gerätedatensatz |
| `:DATA:CAT:ID:UPNEW` | UPdateNEWid | Abspeichern der aktuellen Geräte ID im Gerätekatalog und anlegen einer neuen Geräte ID |
| `:DATA:CAT:ID:UP` | UPdateid | Abspeichern der aktuellen Geräte ID |
| `:DATA:CAT:ID:ID?` | ID? | Abfrage der Geräte ID im Gerätekatalog |
| `:DATA:CAT:ID:ID` | ID | Schreiben einer neuen Geräte ID im Gerätekatalog |
| `:DATA:CAT:ID:TYP?` | TYP? | Abfrage des Gerätetypes im Gerätekatalog |
| `:DATA:CAT:ID:TYP` | TYP | Schreiben eines neuen Types im Gerätekatalog |
| `:DATA:CAT:ID:SNO?` | SerialNumerO? | Abfrage der Seriennummer im aktuellen Gerätedatensatz |
| `:DATA:CAT:ID:SNO` | SerialNumerO | Schreiben einer neuen Seriennummer im aktuellen Gerätedatensatz |
| `:DATA:CAT:ID:MANU?` | MANUfactur? | Abfrage des Herstellers im aktuellen Gerätedatensatz |
| `:DATA:CAT:ID:MANU` | MANUfactur | Schreiben eines neuen Herstellers in aktuellen Gerätedatensatz |
| `:DATA:CAT:ID:DEVD?` | DEViceDesignation? | Abfrage der Gerätebezeichnung im aktuellen Gerätedatensatz |
| `:DATA:CAT:ID:DEVD` | DEViceDesignation | Schreiben einer neuen Gerätebez. im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TSTM?` | TeSTMode? | Abfrage des Prüfablaufes(Ziffer) des aktuellen Gerätedatensatzes |
| `:DATA:CAT:ID:TSTM` | TeSTMode |  |
| `:DATA:CAT:ID:CLAS?` | CLASs? | Abfragen der Schutzklasse(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CLAS` | CLASs |  |
| `:DATA:CAT:ID:AP?` | AppliedPart? | Abfrage des Anwendungsteiles(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:AP` | AppliedPart |  |
| `:DATA:CAT:ID:ELEC?` | ELECtrodes? | Abfrage der Anzahl der Elektroden im akt. Gerätedatensatz |
| `:DATA:CAT:ID:ELEC` | ELECtrodes | Schreiben der Anzahl der Elektroden im akt. Gerätedatensatz |
| `:DATA:CAT:ID:EINF?` | ElectrodesINFo? | Abfrage Patientenbuchsen Info |
| `:DATA:CAT:ID:EINF` | ElectrodesINFo | Schreiben Patientenbuchsen Info |
| `:DATA:CAT:ID:CHAR?` | CHARacteristics? | Abfrage der Geräteart(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CHAR` | CHARacteristics |  |
| `:DATA:CAT:ID:NO?` | NumerOortransformers? | Abfrage der Trafoanzahl(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:NO` | NumerOortransformers | Schreiben der Trafoanzahl(Ziffer) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:TSTD?` | TestSTanDard? | Abfrage der Prüfnorm(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TSTD` | TestSTanDard |  |
| `:DATA:CAT:ID:UMT?` | UserModifiedTest? | Abfrage nach modifiziertem Prüfablauf(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:UMT` | UserModifiedTest |  |
| `:DATA:CAT:ID:POOC?` | PowerOnOffControl? | Abfrage nach Warmlaufphase(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:POOC` | PowerOnOffControl |  |
| `:DATA:CAT:ID:WARN?` | WARNing? | Abfrage nach Warnhinweis(ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:WARN` | WARNing |  |
| `:DATA:CAT:ID:CLEN?` | CordLENth? | Abfrage der Leitungslänge im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CLEN` | CordLENth | Schreiben der Leitungslänge in akt. Gerätedatensatz |
| `:DATA:CAT:ID:NPWR?` | NominalPoWeRconsumtion? | Abfrage der Leistungsaufnahme(Großküchengeräte ) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:NPWR` | NominalPoWeRconsumtion | Schreiben der Leistungsaufnahme in akt. Gerätedatensatz |
| `:DATA:CAT:ID:DAT?` | DATe? | Abfrage des Prüfdatums(Seriell sek. nach 1970) im akt. Gerätekatalog |
| `:DATA:CAT:ID:DAT` | DATe |  |
| `:DATA:CAT:ID:ENG?` | testENGineer? | Abfrage des Prüfernamens im akt. Gerätedatensatz |
| `:DATA:CAT:ID:ENG` | testENGineer | Schreiben des Prüfernamen in den akt. Gerätedatensatz |
| `:DATA:CAT:ID:VNO?` | VoltageNOminal? | Abfrage der Nennspannung im akt. Gerätedatensatz |
| `:DATA:CAT:ID:VNO` | VoltageNOminal | Schreiben der Nennspannung in akt. Gerätedatensatz |
| `:DATA:CAT:ID:RDAT?` | RefDATe? | Abfrage des Referenzdatums(seriell) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:RDAT` | RefDATe |  |
| `:DATA:CAT:ID:RENG?` | ReferencetestENGineer? | Abfrage des Referenzprüfernamen im akt. Gerätekatalog |
| `:DATA:CAT:ID:RENG` | ReferencetestENGineer | Schreiben des Referenzprüfernamen in akt. Gerätedatensatz |
| `:DATA:CAT:ID:RVNO?` | ReferenceVoltageNOminal? | Abfrage der Referenznennspannung im akt. Gerätedatensatz |
| `:DATA:CAT:ID:RVNO` | ReferenceVoltageNOminal | Schreiben der Referenznennspannung in akt. Gerätedatensatz |
| `:DATA:CAT:ID:FSTR?` | FktSTR? | Abfrage des Klassifikationsstrings im akt. Gerätedatensatz |
| `:DATA:CAT:ID:FSTR` | FktSTR | Schreiben des Klassifikationsstrings in akt. Gerätedatensatz |
| `:DATA:CAT:ID:COMT?` | COMenT? | Abfrage des Kommentares im akt. Gerätedatensatz |
| `:DATA:CAT:ID:COMT` | COMenT | Schreiben des Kommentares in akt. Gerätedatensatz |
| `:DATA:CAT:ID:P1?` | Place1building? | Abfrage des Gebäudes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:P1` | Place1building | Schreiben des Gebäudes im akt. Gerätdatensatz |
| `:DATA:CAT:ID:P2?` | Place2department? | Abfrage der Abteilung im akt. Gerätedatensatz |
| `:DATA:CAT:ID:P2` | Place2department | Schreiben der Abteilung in akt. Gerätedatensatz |
| `:DATA:CAT:ID:P3?` | Place3room? | Abfrage des Raumes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:P3` | Place3room | Schreiben des Raumes in akt. Gerätedatensatz |

### U1000 Query :DATAbase:CATalogue:ID:FIND

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:NEWid

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:EDITid

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:UPdateNEWid

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:ID

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:PRIC?` | PRICe? | Abfrage des Preise im akt. Gerätedatensatz |
| `:DATA:CAT:ID:PRIC` | PRICe | Schreiben des Preises in akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST` | TESTstep |  |
| `:DATA:CAT:ID:FIND:NRS` | NRS | Suche Geräte-ID im Gerätekatalog |
| `:DATA:CAT:ID:NEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:EDIT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:UPNEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:ID:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:ID:WIDT?` | WIDTh? | Abfrage der Feldbreite für Geräte ID im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:TYP

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:SerialNumerO

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:MANUfactur

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:DEViceDesignation?

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:DEViceDesignation

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:TYP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TYP:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gerätetyp im Gerätekatalog |
| `:DATA:CAT:ID:SNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:SNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Seriennummer im Geräatekatalog |
| `:DATA:CAT:ID:MANU:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:MANU:WIDT?` | WIDTh? | Abfragen der Feldbreite für Hersteller im Gerätekatalog |
| `:DATA:CAT:ID:DEVD?:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gerätebez. im Gerätekatalog |
| `:DATA:CAT:ID:DEVD:NRS` | NRS | NRS ist Argument |

### U1000 Query :DATAbase:CATalogue:ID:TeSTMode

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:CLASs

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:AppliedPart

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:ELECtrodes

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:ElectrodesINFo

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:TSTM:NAME?` | NAME? | Schreiben eines neuen Prüfablaufes(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TSTM:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TSTM:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfablauf(Name) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CLAS:NAME?` | NAME? | Schreiben der Schutzklasse(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CLAS:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:CLAS:WIDT?` | WIDTh? | Abfragen der Feldbreite für Schutzklasse(Name) im Gerätekatalog |
| `:DATA:CAT:ID:AP:NAME?` | NAME? | Schreiben desAnwendungsteiles(Ziffer) im akt. Datensatz |
| `:DATA:CAT:ID:AP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:AP:WIDT?` | WIDTh? | Abfragen der Feldbreite für Anwendungsteil(Name) im Gerätekatalog |
| `:DATA:CAT:ID:ELEC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:ELEC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Elektrodenanzahl |
| `:DATA:CAT:ID:EINF:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:EINF:WIDT?` | WIDTh? | Abfrage der Feldbreite für Elektroden Info im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:CHARacteristics

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:NumerOortransformers

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TestSTanDard

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:UserModifiedTest

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:PowerOnOffControl

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:CHAR:NAME?` | NAME? | Schreiben der Geräteart(Ziffer) im akt. Gerätedatensatz |
| `:DATA:CAT:ID:CHAR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:CHAR:WIDT?` | WIDTh? | Abfragen der Feldbreite für Geräteart(Name) im Gerätekatalog |
| `:DATA:CAT:ID:NO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:NO:WIDT?` | WIDTh? | Abfragen der Feldbreite für Trafoanzahl(Ziffer) im Gerätekatalog |
| `:DATA:CAT:ID:TSTD:NAME?` | NAME? | Schreiben der Prüfnorm(Ziffer) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:TSTD:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TSTD:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfnorm(Name) im Gerätekatalog |
| `:DATA:CAT:ID:UMT:NAME?` | NAME? | Schreiben modifizierter Prüfablauf(Ziffer) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:UMT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:UMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für modifizierten Prüfablauf(Name) im Gerätekatalog |
| `:DATA:CAT:ID:POOC:NAME?` | NAME? | Schreiben der Warmlaufphase(Ziffer) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:POOC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:POOC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Warmlaufphase(Name) im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:WARNing

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:CordLENth

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:NominalPoWeRconsumtion

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:DATe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:testENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:WARN:NAME?` | NAME? | Schreiben des Wqarnhinweises(Ziffer) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:WARN:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:WARN:WIDT?` | WIDTh? | Abfragen dert Feldbreite für Warnhinweis(NAme) im Gerätekatalog |
| `:DATA:CAT:ID:CLEN:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:CLEN:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leitungslänge im Gerätekatalog |
| `:DATA:CAT:ID:NPWR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:NPWR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leistungsaufnahme(Großküchen) im Gerätekatalog |
| `:DATA:CAT:ID:DAT:NAME?` | NAME? | Schreiben des Prüfdatums (seriell) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:DAT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:DAT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfdatum(tt.mm.yyyy) im Gerätekatalog |
| `:DATA:CAT:ID:ENG:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:ENG:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfernamen im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:VoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:RefDATe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:ReferencetestENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:ReferenceVoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:FktSTR

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:VNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:VNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Nennspannung im Gerätekatalog |
| `:DATA:CAT:ID:RDAT:NAME?` | NAME? | Schreiben des Referenzdatums(seriell) in akt. Gerätedatensatz |
| `:DATA:CAT:ID:RDAT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:RDAT:WIDT?` | WIDTh? | Abfarge der Feldbreite für Referenzdatum im Gerätekatalog |
| `:DATA:CAT:ID:RENG:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:RENG:WIDT?` | WIDTh? | Abfarge der Feldbreite für Referenzprüfernamen im Gerätekatalog |
| `:DATA:CAT:ID:RVNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:RVNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenznennspannung im Gerätekatalog |
| `:DATA:CAT:ID:FSTR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:FSTR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Klassifikationsstring im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:COMenT

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:Place1building

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:Place2department

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:Place3room

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:PRICe

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:COMT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:COMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Kommentar im Gerätekatalog |
| `:DATA:CAT:ID:P1:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:P1:WIDT?` | WIDTh? | Abfragen der Feldbreite für Gebäude im Gerätekatalog |
| `:DATA:CAT:ID:P2:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:P2:WIDT?` | WIDTh? | Abfrage der Feldbreite für Abteilung im Gerätekatalog |
| `:DATA:CAT:ID:P3:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:P3:WIDT?` | WIDTh? | Abfrage der Feldbreite für Raum im Gerätekatalog |
| `:DATA:CAT:ID:PRIC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:PRIC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Preis im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:TESTstep

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:TEST:FIRS?` | FIRStstepno? | Abfrage des ersten Prüfschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:NEXT?` | NEXTstepno? | Abfrage des nächsten Prüfschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:DEL` | DELetestepno | Löschen des akt. Prüfschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:NEW` | NEWstepno | Anlegen eines neuen Prüfschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:EDIT` | EDITstepno | Editieren eines Prüfschrittes |
| `:DATA:CAT:ID:TEST:UPNEW` | UPdateNEWstepno | Abspeichern des letzen Prüfschrittes und anlegen eines neuen Prüfschrittes |
| `:DATA:CAT:ID:TEST:UP` | UPdatestepno | Letzten Prüfschritt im akt. gerätzedatensatz abspeichern |
| `:DATA:CAT:ID:TEST:STEP?` | STEPno? | Abfrage des Prüfdschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:STEP` | STEPno | Schreiben des Prüfschrittes im akt. Gerätedatensatzes |
| `:DATA:CAT:ID:TEST:IDX?` | InDeX? | Abfrage von Index des Prüfschrittes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:IDX` | InDeX | Schreiben von Index des Prüfschrittes im akt. Gerätedatensatzes |
| `:DATA:CAT:ID:TEST:TRES?` | ThREShold? | Abfrage des Grenzwertes vom moment. Prüfschritt im akt. Gerä#tedatensatz |
| `:DATA:CAT:ID:TEST:TRES` | ThREShold | Schreiben des Grenzwertes vom moment. Prüfschritt im akt. Gerätedatensatz; |
| `:DATA:CAT:ID:TEST:RVAL?` | ReferenceVALue? | Abfrage des Referenzmesswertes vom moment. Prüfschritt des akt. Gerätedatensatzes |
| `:DATA:CAT:ID:TEST:RVAL` | ReferenceVALue | Schreiben des Referenzmesswertes im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:VAL?` | VALue? | Abfrage des Messwertes vom moment. Prüfschritt im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:VAL` | VALue | Schreiben des Messwertes vom moment. Prüfschritt im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:UNIT?` | UNIT? | Abfrage der Einheit vom moment. Prüfschritt im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:HLO?` | HighLowOfftoleranz? | Abfrage der Toleranzbewertung vom moment.Prüfschritt im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:NAME?` | NAME? | Abfrage des Namens der Messnummer(kompletter Messname) vom moment. Prüfschritt im akt. Ger |
| `:DATA:CAT:ID:TEST:SHOR?` | SHORtname? | Abfrage des Namens der Messnummer(kurzer Messname) vom moment. Prüfschritt im akt. Geräted |
| `:DATA:CAT:ID:TEST:CODE?` | CODE? | Abfrage des Prüfschritt-Codes |

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:NEWstepno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:EDITstepno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:UPdateNEWstepno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:STEPno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:InDeX

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:ThREShold

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:TEST:NEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:EDIT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:UPNEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:STEP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:IDX:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:TRES:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:TRES:WIDT?` | WIDTh? | Abfrage der Feldbreite für den Grenzwert im Gerätekatalog |

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:ReferenceVALue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:ID:TESTstep:VALue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:ID:TEST:RVAL:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:RVAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzmesswert im akt. Gerätedatensatz |
| `:DATA:CAT:ID:TEST:VAL:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:ID:TEST:VAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für Messwert im akt. Gerätekatalog |
| `:DATA:CAT:TYP:FIRS?` | FIRSttyp? | Abfrage erster Typeintrag im Typenkatalog |
| `:DATA:CAT:TYP:NEXT?` | NEXTtyp? | Abfrage des nächsten Typ im Typenkatalog |
| `:DATA:CAT:TYP:FIND` | FIND | Direktes suchen im Typenkatalog |
| `:DATA:CAT:TYP:DEL` | DELetetyp | Löschen des momentanen Types aus dem Typenkatalog |
| `:DATA:CAT:TYP:NEW` | NEWtyp | Anlegen eines neuen Types im Typenkatalog |
| `:DATA:CAT:TYP:EDIT` | EDITtyp | Editieren Typennamens |
| `:DATA:CAT:TYP:UPNEW` | UPdateNEWtyp | Abspeichern des aktuellen Types im Typenkatalog und anlegen eines neuen Types |
| `:DATA:CAT:TYP:UP` | UPdatetyp | Abspeichern des aktuellen Types im Typenkatalog |
| `:DATA:CAT:TYP:TYP?` | TYP? | Abfrage des Gerätetypes im Typenkatalog |
| `:DATA:CAT:TYP:TYP` | TYP | Schreiben des Typennamens im Typenkatalog |
| `:DATA:CAT:TYP:ID?` | ID? | Abfrage der Geräte ID im Typenkatalog |
| `:DATA:CAT:TYP:ID` | ID | Schreiben der Geräte ID im Typenkatalog |
| `:DATA:CAT:TYP:SNO?` | SerialNumerO? | Abfrage der Seriennummer im akt. Typendatensatz |
| `:DATA:CAT:TYP:SNO` | SerialNumerO | Schreiben einer neuen Seriennummer im akt. Typendatensatz |
| `:DATA:CAT:TYP:MANU?` | MANUfactur? | Abfrage des Herstellers im akt. Typendatensatz |
| `:DATA:CAT:TYP:MANU` | MANUfactur | Schreiben eines neuen Herstellers in akt. Typendatensatz |
| `:DATA:CAT:TYP:DEVD?` | DEViceDesignation? | Abfrage der Gerätebezeichnung im Typendatensatz |
| `:DATA:CAT:TYP:DEVD` | DEViceDesignation | Schreiben einer neuen Gerätebez. im akt. Typendatensatz |
| `:DATA:CAT:TYP:TSTM?` | TeSTMode? | Abfrage des Prüfablaufes(Ziffer) des akt. Typendatensatzes |
| `:DATA:CAT:TYP:TSTM` | TeSTMode | Zugriff auf Messungen |
| `:DATA:CAT:TYP:CLAS?` | CLASs? | Abfrage der Schutzklasse(Ziffer) im akt. Typendatensatz |
| `:DATA:CAT:TYP:CLAS` | CLASs | Zugriff auf Messungen |
| `:DATA:CAT:TYP:AP?` | AppliedPart? | Abfrage des Anwendungsteiles(Ziffer) im akt. Typendatensatz |
| `:DATA:CAT:TYP:AP` | AppliedPart | Zugriff auf Messungen |
| `:DATA:CAT:TYP:ELEC?` | ELECtrodes? | Abfrage der Elektrodenanzahl im akt. Typendatensatz |
| `:DATA:CAT:TYP:ELEC` | ELECtrodes | Schreiben der Elektrodenanzahl in akt. Typendatensatz |
| `:DATA:CAT:TYP:EINF?` | ElectrodesINFo? | Abfrage Patientenbuchsen Info |
| `:DATA:CAT:TYP:EINF` | ElectrodesINFo | Schreiben Patientenbuchsen Info |
| `:DATA:CAT:TYP:CHAR?` | CHARacteristics? | Abfarge der Geräteart(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:CHAR` | CHARacteristics | Zugriff auf Messungen |
| `:DATA:CAT:TYP:NO?` | NumerOortransformers? | Abfrage der Trafoanzahl im akt. Typendatensatz |
| `:DATA:CAT:TYP:NO` | NumerOortransformers | Schreiben der Trafoanzahl in akt. Typendatensatz |
| `:DATA:CAT:TYP:TSTD?` | TestSTanDard? | Abfrage der Prüfnorm(Ziffer) im akt. Typendatensatz |
| `:DATA:CAT:TYP:TSTD` | TestSTanDard | Zugriff auf Messungen |
| `:DATA:CAT:TYP:UMT?` | UserModifiedTest? | Abfrage nach modifiziertem Prüfablauf(Ziffer)im akt. Typendatensatz |
| `:DATA:CAT:TYP:UMT` | UserModifiedTest | Zugriff auf Messungen |
| `:DATA:CAT:TYP:POOC?` | PowerOnOffControl? | Abfrage nach Warmaufphase(Ziffer) im akt. Typendatensatz |
| `:DATA:CAT:TYP:POOC` | PowerOnOffControl | Zugriff auf Messungen |
| `:DATA:CAT:TYP:WARN?` | WARNing? | Abfrage nach Warnhinweis(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:WARN` | WARNing | Zugriff auf Messungen |
| `:DATA:CAT:TYP:CLEN?` | CordLENth? | Abfrage der Leitungslänge im akt.Typendatensatz |
| `:DATA:CAT:TYP:CLEN` | CordLENth | Schreiben der Leitungslänge in akt. Typendatensatz |
| `:DATA:CAT:TYP:NPWR?` | NominalPoWeRconsumtion? | Abfrage der Leistungsaufnahme (Großküchengeräte) im akt. Typendatensatz |
| `:DATA:CAT:TYP:NPWR` | NominalPoWeRconsumtion | Schreiben der Leistungsaufnahme im akt. Typendatensatz |
| `:DATA:CAT:TYP:DAT?` | DATe? | Abfrage des Prüfdatums(Seriell sek. nach 1970) im akt. Typendatensatz |
| `:DATA:CAT:TYP:DAT` | DATe | Zugriff auf Messungen |
| `:DATA:CAT:TYP:ENG?` | testENGineer? | Abfrage des Prüfernamen im akt. Typendatensatz |
| `:DATA:CAT:TYP:ENG` | testENGineer | Schreiben des Prüfernamen in den akt. Typendatensatz |
| `:DATA:CAT:TYP:VNO?` | VoltageNOminal? | Abfrage der Nennspannung im Typendatensatz |
| `:DATA:CAT:TYP:VNO` | VoltageNOminal | Schreiben der Nennspannung in den akt. Typendatensatz |
| `:DATA:CAT:TYP:RDAT?` | RefDATe? | Abfrage des Referenzdatums (seriell) im akt. Typendatensatz |
| `:DATA:CAT:TYP:RDAT` | RefDATe | Zugriff auf Messungen |
| `:DATA:CAT:TYP:RENG?` | ReferencetestENGineer? | Abfrage des Referenzprüfernamen im akt. Typendatensatz |
| `:DATA:CAT:TYP:RENG` | ReferencetestENGineer | Schreiben des Referenzprüfernamen in akt. Typendatensatz |
| `:DATA:CAT:TYP:RVNO?` | ReferenceVoltageNOminal? | Abfrage der Referenznennspannung im akt. Typendatensatz |
| `:DATA:CAT:TYP:RVNO` | ReferenceVoltageNOminal | Schreiben der Referenznennspannung in akt. Typendatensatz |
| `:DATA:CAT:TYP:FSTR?` | FktSTR? | Abfrage des Klassifikationsstringes im akt. Typendatensatz |
| `:DATA:CAT:TYP:FSTR` | FktSTR | Schreiben des Klassifikationsstringes in akt. Typendatensatz |
| `:DATA:CAT:TYP:COMT?` | COMenT? | Abfrage des Kommentares im akt. Typendatensatz |
| `:DATA:CAT:TYP:COMT` | COMenT | Schreiben des Kommentares in den akt. Typendatensatz |
| `:DATA:CAT:TYP:P1?` | Place1building? | Abfrage des Gebäudes im akt. Typendatensatz |
| `:DATA:CAT:TYP:P1` | Place1building | Schreiben des Gebäudes in den akt. Typendatensatz |
| `:DATA:CAT:TYP:P2?` | Place2department? | Abfrage der Abteilung im akt. Typendatensatz |
| `:DATA:CAT:TYP:P2` | Place2department | Schreiben der Abteilung in den akt. Typendatensatz |
| `:DATA:CAT:TYP:P3?` | Place3room? | Abfrage des Raumes im akt. Typendatensatz |

### U1000 Query :DATAbase:CATalogue:TYP:FIND

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:NEWtyp

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:EDITtyp

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:UPdateNEWtyp

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TYP

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:P3` | Place3room | Schreiben des Raumes in den akt. Typendatensatz |
| `:DATA:CAT:TYP:PRIC?` | PRICe? | Abfrage des Preise im akt. Typendatensatz |
| `:DATA:CAT:TYP:PRIC` | PRICe | Schreiben des Preise in den akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST` | TESTstep | Prüschritte im Typenkatalog |
| `:DATA:CAT:TYP:FIND:NRS` | NRS | Suche Geräte-Typ im Typenkatalog |
| `:DATA:CAT:TYP:NEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:EDIT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:UPNEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TYP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TYP:WIDT?` | WIDTh? | Abfrage der Feldbreite Gerätetyp im Typenkatalog |

### U1000 Query :DATAbase:CATalogue:TYP:ID

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:SerialNumerO

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:MANUfactur

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:DEViceDesignation?

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:DEViceDesignation

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:ID:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:ID:WIDT?` | WIDTh? | Abfrage der Feldbreite für Geräte ID im Typenkatalog |
| `:DATA:CAT:TYP:SNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:SNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Seriennummer im Typenkatalog |
| `:DATA:CAT:TYP:MANU:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:MANU:WIDT?` | WIDTh? | Abfrage der Feldbreite für Hersteller im Typenkatalog |
| `:DATA:CAT:TYP:DEVD?:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gerätebez. im Typenkatalog |
| `:DATA:CAT:TYP:DEVD:NRS` | NRS | NRS ist Argument |

### U1000 Query :DATAbase:CATalogue:TYP:TeSTMode

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:CLASs

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:AppliedPart

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:ELECtrodes

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:ElectrodesINFo

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:TSTM:NAME?` | NAME? | Schreiben des Prüfablaufes(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:TSTM:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TSTM:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfablauf(Name) im akt. Typendatensatz |
| `:DATA:CAT:TYP:CLAS:NAME?` | NAME? | Schreiben der Schutzklasse(Ziffer) im akt. Typendatensatz |
| `:DATA:CAT:TYP:CLAS:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:CLAS:WIDT?` | WIDTh? | Abfrage der Feldbreite für Schutzklasse(NAme) im akt. Typendatensatz |
| `:DATA:CAT:TYP:AP:NAME?` | NAME? | Schreiben des Anwendungsteiles(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:AP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:AP:WIDT?` | WIDTh? | Abfrage der Feldbreite für Anwendungsteil(Name) im akt. Typenkatalog |
| `:DATA:CAT:TYP:ELEC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:ELEC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Elektrodenanzahl |
| `:DATA:CAT:TYP:EINF:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:EINF:WIDT?` | WIDTh? | Abfrage der Feldbreite(noch nicht verwendet) |

### U1000 Query :DATAbase:CATalogue:TYP:CHARacteristics

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:NumerOortransformers

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TestSTanDard

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:UserModifiedTest

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:CHAR:NAME?` | NAME? | Schreiben der Geräteart(Ziffer)= in akt. Typendatensatz |
| `:DATA:CAT:TYP:CHAR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:CHAR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Geräteart(Name) im Typenkatalog |
| `:DATA:CAT:TYP:NO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:NO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Trafoanzahl im Typenkatalog |
| `:DATA:CAT:TYP:TSTD:NAME?` | NAME? | Schreiben der Prüfnorm(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:TSTD:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TSTD:WIDT?` | WIDTh? | Abfrage der Feldbreite(Name) für Prüfnorm im Typenkatalog |
| `:DATA:CAT:TYP:UMT:NAME?` | NAME? | Schreiben modifizierter Prüfablauf(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:UMT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:UMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für modif. Prüfablauf(Name) im Typenkatalog |

### U1000 Query :DATAbase:CATalogue:TYP:PowerOnOffControl

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:WARNing

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:CordLENth

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:NominalPoWeRconsumtion

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:POOC:NAME?` | NAME? | Schreiben der Warmlaufphase(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:POOC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:POOC:WIDT?` | WIDTh? | Abfrage der Feldbreite(NAme) für Warmlaufphase im Typenkatalog |
| `:DATA:CAT:TYP:WARN:NAME?` | NAME? | Schreiben des Warnhinweises(Ziffer) in akt. Typendatensatz |
| `:DATA:CAT:TYP:WARN:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:WARN:WIDT?` | WIDTh? | Abfarge der Feldbreite(Name) für Warnhinweis im akt. Typenkatalog |
| `:DATA:CAT:TYP:CLEN:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:CLEN:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leitungslänge im Typenkatalog |
| `:DATA:CAT:TYP:NPWR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:NPWR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Leistungsaufnahme(Großküchengeräte) im Typenkatalog |

### U1000 Query :DATAbase:CATalogue:TYP:DATe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:testENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:VoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:RefDATe

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:DAT:NAME?` | NAME? | Schreiben des Prüfdatums(seriell) in akt. Typendatensatz |
| `:DATA:CAT:TYP:DAT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:DAT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Prüfdatum(dd.mm.yyyy) imTypenkatalog |
| `:DATA:CAT:TYP:ENG:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:ENG:WIDT?` | WIDTh? | Abfragen der Feldbreite für Prüfernamen im Typenkatalog |
| `:DATA:CAT:TYP:VNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:VNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Nennspannung im Typenkatalog |
| `:DATA:CAT:TYP:RDAT:NAME?` | NAME? | Schreiben des Referenzdatums(seriell) in akt. Typendatensatz |
| `:DATA:CAT:TYP:RDAT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:RDAT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzdatum(dd.mm.yyyy) im Typenkatalog |

### U1000 Query :DATAbase:CATalogue:TYP:ReferencetestENGineer

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:ReferenceVoltageNOminal

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:FktSTR

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:COMenT

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:Place1building

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:RENG:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:RENG:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzprüfernamen im Typenkatalog |
| `:DATA:CAT:TYP:RVNO:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:RVNO:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenznennspannung im Typenkatalog |
| `:DATA:CAT:TYP:FSTR:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:FSTR:WIDT?` | WIDTh? | Abfrage der Feldbreite für Klassifikationsstring im Typenkatalog |
| `:DATA:CAT:TYP:COMT:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:COMT:WIDT?` | WIDTh? | Abfrage der Feldbreite für Kommentar im akt. Typendatensatz |
| `:DATA:CAT:TYP:P1:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:P1:WIDT?` | WIDTh? | Abfrage der Feldbreite für Gebäude im Typenkatalog |

### U1000 Query :DATAbase:CATalogue:TYP:Place2department

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:Place3room

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:PRICe

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:P2:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:P2:WIDT?` | WIDTh? | Abfrage der Feldbreite für Abteilung im Typenkatalog |
| `:DATA:CAT:TYP:P3:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:P3:WIDT?` | WIDTh? | Abfrage der Feldbreite für Raum im Typenkatalog |
| `:DATA:CAT:TYP:PRIC:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:PRIC:WIDT?` | WIDTh? | Abfrage der Feldbreite für Preis im Typenkatalog |
| `:DATA:CAT:TYP:TEST:FIRS?` | FIRStstepno? | Abfrage des ersten Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:NEXT?` | NEXTstepno? | Abfrage des nächsten Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:DEL` | DELetestepno | Löschen des akt. Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:NEW` | NEWstepno | Anlegen eines neuen Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:EDIT` | EDITstepno | Editieren des akt. Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:UPNEW` | UPdateNEWstepno | Abspeichern des letzten Prüfschrittes und anlegen eines neuen Prüfschrittes im akt. Type |

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:NEWstepno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:EDITstepno

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:TEST:UP` | UPdatestepno | Letzten Prüfschritt im akt. Typendatensatz abspeichern |
| `:DATA:CAT:TYP:TEST:STEP?` | STEPno? | Abfrage des akt. Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:STEP` | STEPno | Schreiben des Prüfschrittes im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:IDX?` | InDeX? | Abfrage des INdex vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:IDX` | InDeX | Schreiben des Index für akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:TRES?` | ThREShold? | Abfrage des Grenzwertes vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:TRES` | ThREShold | Schreiben des Grenzwertes vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:RVAL?` | ReferenceVALue? | Abfrage des Referenzmesswertes vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:RVAL` | ReferenceVALue | Schreiben des Referenzmesswertes vom akt. Prüfschritt in akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:VAL?` | VALue? | Abfrage des Messwertes vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:VAL` | VALue | Schreiben des Messwertes vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:UNIT?` | UNIT? | Abfrage der Einheit vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:HLO?` | HighLowOfftoleranz? | Abfrage der Toleranzbewertung vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:NAME?` | NAME? | Abfrage des Prüfschrittnamens (kompl. Messname) vom akt. Prüfschritt im akt. Typendatens |
| `:DATA:CAT:TYP:TEST:SHOR?` | SHORtname? | Abfrage des Prüfschrittnamens(kurzer Messname) vom akt. Prüfschritt im akt. Typendatensatz |
| `:DATA:CAT:TYP:TEST:NEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:EDIT:NRS` | NRS | NRS ist Argument |

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:UPdateNEWstepno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:STEPno

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:InDeX

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:ThREShold

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:ReferenceVALue

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :DATAbase:CATalogue:TYP:TESTstep:VALue

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:TEST:UPNEW:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:STEP:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:IDX:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:TRES:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:TRES:WIDT?` | WIDTh? | Abfrage der Feldbreite für Grenwert im akt. Typenkatalog |
| `:DATA:CAT:TYP:TEST:RVAL:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:RVAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für Referenzmesswert im Typenkatalog Schreiben des Messwertes vom akt. Prüfschritt im akt. Typendatensatz |

### U1000 Query :MEASurement

| Befehl | Langform | Bedeutung |
|---|---|---|

### U1000 Query :MEASurement:STEPno

| Befehl | Langform | Bedeutung |
|---|---|---|
| `:DATA:CAT:TYP:TEST:VAL:NRS` | NRS | NRS ist Argument |
| `:DATA:CAT:TYP:TEST:VAL:WIDT?` | WIDTh? | Abfrage der Feldbreite für Messwert im Typenkatalog |
| `:MEAS:STEP` | STEPno | Zugriff auf Messnummer |
| `:MEAS:STEP:NRS` | NRS | Starten der Einzelmessung; NRS ist Argument |
| `:MEAS:STEP:VAL?` | VALue? | Abfrage des Messwertes der zuvor gestarteten Einzelmessung |
| `:MEAS:STEP:EXIT` | EXIT | Beenden der Einzelmessung |
| `:MEAS:STEP:UNIT?` | UNIT? | Abfrage der Einheit von der ausgeführten Einzelmessung |
| `:MEAS:STEP:NAME?` | NAME? | Abfrage des Messnamens(kompletter Messname) der ausgeführten Einzelmessung |
| `:MEAS:STEP:SHOR?` | SHORtname? | Abfrage des Messnamens(kurzer Messname) der ausgeführten Einzelmessung |
| `:MEAS:STEP:CODE?` | CODE? | Abfrage des Prüfschritt-Codes |

## 5. Patientenbuchsen-Matrix

Verschaltung per `:SYS:CTRL <Messnummer>` während einer laufenden Messung. Siehe `research/MESSTECHNIK.md` für die daraus abgeleitete Hardware-Topologie.

| Funktion | Messnummern |
|---|---|
| Einzelne Patientenbuchse PAT1…PAT10 an den Messkreis | `#1161`…`#1170` |
| Patientenhilfsstrom PATn gegen alle übrigen (REST) | `#1141`…`#1150` |
| Gruppenkurzschluss zusammenhängender Buchsen | `#1712`…`#1799` |

Gruppenschema `#17<start><ende>`, z. B. `#1712` = PAT 1+2, `#1720` = PAT 1…10, `#1799` = PAT 9+10.
Im PDF sind zwei Einträge fehlerhaft: `#1760` erscheint doppelt (PAT 5+6+7+8+9+10 und PAT 6+7+8+9+10), und die letzte Teiltabelle ist im Satz verrutscht.
