#include <Bridge.h>

const int lightresist = 2;
const int led = 3;
const int button = 4;

void setup() {
  //Bridge.begin();
  Serial.begin(9600); //Debug
  pinMode(lightresist, OUTPUT);
  digitalWrite(lightresist, LOW);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  pinMode(button, INPUT);
  //for (int i = 5; i <= 13; i++) {
  for (int i = 13; i <= 13; i++) { //Debug
    pinMode(i, INPUT);
  }
}

String readData() {
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(lightresist, HIGH);
  String a;
  //for (int i = 5; i <= 13; i++) {
  for (int i = 13; i <= 13; i++) { //Debug
    a += String(digitalRead(i));
  }
  digitalWrite(led, LOW);
  digitalWrite(lightresist, LOW);
  return a;
}

void loop() {
  //Serial.println(digitalRead(button));
  if (digitalRead(button) == HIGH) {
    String output = readData();
    Serial.println(output); //Debug
    // transfer output to linux part

    // end
    delay(1800);
  }
  delay(200);
}
