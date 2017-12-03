final int led = 3;
final int button = 4;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(button, INPUT);
  for (int i = 5; i <= 13; i++) {
    pinMode(i, INPUT);
  }
}

String readData() {
  for (int i = 5; i <= 13; i++) {
    digitalRead(i);
    // do stuff
  }
  return stuff
}

void loop() {
  if (digitalRead(4) == HIGH) {
    output = readData();
    // transfer output to linux part
    delay(1800);
  }
  delay(200);
}
