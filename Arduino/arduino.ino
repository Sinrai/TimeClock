#include <Mailbox.h>

const int lightresist = 2;
const int led = 3;
const int button = 4;

void setup() {
  Mailbox.begin();
  pinMode(lightresist, OUTPUT);
  digitalWrite(lightresist, LOW);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  pinMode(button, INPUT);
  for (int i = 5; i <= 13; i++) {
    pinMode(i, INPUT);
  }
}

String readData() {
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(lightresist, HIGH);
  String a;
  for (int i = 5; i <= 13; i++) {
    a += String(digitalRead(i));
  }
  digitalWrite(led, LOW);
  digitalWrite(lightresist, LOW);
  return a;
}

void loop() {
  if (digitalRead(button) == HIGH) {
    String output = readData();
    Mailbox.writeMessage(output);
    delay(1800);
  }
  delay(200);
}
