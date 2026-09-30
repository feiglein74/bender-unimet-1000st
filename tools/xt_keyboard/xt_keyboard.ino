// XT-Tastatur-Emulator für den Bender UNIMET 1000 ST
//
// Erzeugt XT-Tastaturframes auf KBCLK/KBDATA des Chips & Technologies F8680.
// Scancodes kommen über die serielle Konsole vom PC — es wird also keine
// echte Tastatur gebraucht.
//
// ZIELPLATTFORM: 5-V-Arduino (Nano, Uno, Pro Micro 5V).
//   Kein Pegelwandler nötig. Ein Pico/ESP32 wäre hier der umständlichere Weg,
//   weil deren GPIOs nicht 5-V-tolerant sind.
//
// ANSCHLUSS an den 14-poligen Stecker Nr. 4 des CPU-Moduls:
//
//   Header-Pin 1  ── +5 V   (nur als Referenz, Arduino separat versorgen)
//   Header-Pin 2  ── GND    ── Arduino GND      ← zwingend gemeinsam
//   Header-Pin 4  ── KBDATA ── Arduino D3
//   Header-Pin 5  ── KBCLK  ── Arduino D2
//
//   Liegen KBCLK/KBDATA im Ruhezustand nicht auf ~5 V, fehlen die Pull-ups:
//   dann je 4,7 kΩ von D2 bzw. D3 nach +5 V ergänzen.
//
// PROTOKOLL (F8680 System Design Guide, Kap. 6):
//   9 Bit pro Frame — ein Startbit, dann 8 Datenbits, LSB zuerst.
//   Der Takt kommt von der Tastaturseite, also von uns.
//   Make-Code = Scancode, Break-Code = Scancode | 0x80.
//
// Die Leitungen werden als OPEN DRAIN betrieben: LOW aktiv treiben, HIGH nur
// freigeben. So kann der Host jederzeit inhibieren, ohne dass etwas gegeneinander
// arbeitet.

const uint8_t PIN_CLK  = 2;
const uint8_t PIN_DATA = 3;

// Timing in Mikrosekunden. Grosszuegig gewaehlt (~12 kHz Takt).
// Falls der Host nichts erkennt: zuerst T_LOW/T_HIGH verdoppeln, dann
// START_BITS auf 2 setzen (manche Klontastaturen senden zwei Startbits).
const unsigned T_SETUP     = 25;
const unsigned T_LOW       = 40;
const unsigned T_HIGH      = 40;
const unsigned T_FRAME_GAP = 3000;
const uint8_t  START_BITS  = 1;

// ── Leitungssteuerung ──────────────────────────────────────────────────────
inline void driveLow(uint8_t pin) { pinMode(pin, OUTPUT); digitalWrite(pin, LOW); }
inline void release(uint8_t pin)  { pinMode(pin, INPUT); }   // Pull-up zieht hoch
inline bool readPin(uint8_t pin)  { return digitalRead(pin); }

void setBit(uint8_t pin, bool v) { v ? release(pin) : driveLow(pin); }

// ── Ein Frame senden ───────────────────────────────────────────────────────
void sendByte(uint8_t code) {
  // Warten, bis der Host die Taktleitung freigibt (Inhibit beachten)
  unsigned long t0 = millis();
  while (!readPin(PIN_CLK)) {
    if (millis() - t0 > 500) break;      // Notausstieg
  }

  for (uint8_t i = 0; i < START_BITS; i++) {
    setBit(PIN_DATA, true);              // Startbit = 1
    delayMicroseconds(T_SETUP);
    driveLow(PIN_CLK);  delayMicroseconds(T_LOW);
    release(PIN_CLK);   delayMicroseconds(T_HIGH);
  }

  for (uint8_t i = 0; i < 8; i++) {      // 8 Datenbits, LSB zuerst
    setBit(PIN_DATA, code & 0x01);
    code >>= 1;
    delayMicroseconds(T_SETUP);
    driveLow(PIN_CLK);  delayMicroseconds(T_LOW);
    release(PIN_CLK);   delayMicroseconds(T_HIGH);
  }

  release(PIN_DATA);
  delayMicroseconds(T_FRAME_GAP);
}

void tap(uint8_t code) {                 // Taste druecken und loslassen
  sendByte(code);
  sendByte(code | 0x80);
}

// ── Tastennamen ────────────────────────────────────────────────────────────
// Bewusst NICHT im PROGMEM: dort landen zwar die Zeiger im Flash, die
// Zeichenketten aber im RAM. Sie dann als Flash-Adressen zu lesen liefert
// Bruchstuecke fremder Texte. Die Tabelle kostet im RAM keine 200 Byte.
struct Key { const char* name; uint8_t code; };
const Key KEYS[] = {
  {"F1",0x3B},{"F2",0x3C},{"F3",0x3D},{"F4",0x3E},{"F5",0x3F},{"F6",0x40},
  {"F7",0x41},{"F8",0x42},{"F9",0x43},{"F10",0x44},
  {"UP",0x48},{"DOWN",0x50},{"LEFT",0x4B},{"RIGHT",0x4D},
  {"PLUS",0x4E},{"MINUS",0x4A},{"PGUP",0x49},{"PGDN",0x51},
  {"ENTER",0x1C},{"ESC",0x01},{"SPACE",0x39},{"TAB",0x0F},
  {"Y",0x15},{"N",0x31},{"J",0x24},
};
const uint8_t NKEYS = sizeof(KEYS) / sizeof(KEYS[0]);

// ── Konsole ────────────────────────────────────────────────────────────────
void help() {
  Serial.println(F("XT-Tastatur-Emulator  —  UNIMET 1000 ST"));
  Serial.println(F("  3C          Scancode hex, Make + Break"));
  Serial.println(F("  F2          Taste per Name"));
  Serial.println(F("  !3C         nur Make (Taste haelt)"));
  Serial.println(F("  ~3C         nur Break (Taste loesen)"));
  Serial.println(F("  ?           diese Hilfe, Tastenliste"));
  Serial.println(F("Mehrere Angaben mit Leerzeichen getrennt."));
  Serial.print(F("Tasten:"));
  for (uint8_t i = 0; i < NKEYS; i++) {
    Serial.print(' ');
    Serial.print(KEYS[i].name);
  }
  Serial.println();
}

int lookup(const char* s) {
  for (uint8_t i = 0; i < NKEYS; i++) {
    if (!strcasecmp(s, KEYS[i].name)) return KEYS[i].code;
  }
  return -1;
}

void handleToken(char* t) {
  bool makeOnly = false, breakOnly = false;
  if (*t == '!') { makeOnly  = true; t++; }
  else if (*t == '~') { breakOnly = true; t++; }
  if (!*t) return;

  int code = lookup(t);
  if (code < 0) {                                   // sonst als Hex deuten
    char* end;
    long v = strtol(t, &end, 16);
    if (*end || v < 0 || v > 0xFF) {
      Serial.print(F("unbekannt: ")); Serial.println(t);
      return;
    }
    code = (uint8_t)v;
  }

  if (makeOnly)       sendByte(code);
  else if (breakOnly) sendByte(code | 0x80);
  else                tap(code);

  Serial.print(F("gesendet 0x"));
  if (code < 16) Serial.print('0');
  Serial.print(code, HEX);
  Serial.println(makeOnly ? F(" (make)") : breakOnly ? F(" (break)") : F(" (make+break)"));
}

void setup() {
  release(PIN_CLK);
  release(PIN_DATA);
  Serial.begin(115200);
  while (!Serial) { }
  help();
  Serial.println(F("Monitor auf 115200, Zeilenende \"Neue Zeile\"."));
  Serial.print(F("> "));
}

void loop() {
  static char buf[64];
  static uint8_t n = 0;

  while (Serial.available()) {
    char c = Serial.read();

    // Sowohl LF als auch CR beenden die Eingabe — damit ist die
    // Zeilenende-Einstellung des Monitors egal (ausser "kein Zeilenende").
    if (c == '\n' || c == '\r') {
      if (n == 0) continue;                // leere Zeile, etwa das CR von CRLF
      Serial.println();
      buf[n] = 0; n = 0;
      if (buf[0] == '?') { help(); continue; }
      for (char* t = strtok(buf, " \t"); t; t = strtok(NULL, " \t")) handleToken(t);
      Serial.print(F("> "));
    } else if (c >= ' ' && n < sizeof(buf) - 1) {
      buf[n++] = c;
      Serial.write(c);                     // Echo, damit man das Tippen sieht
    }
  }
}
