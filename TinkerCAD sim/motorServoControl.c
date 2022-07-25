#include <Servo.h>

Servo myservo;

int enA = 9;
int in1 = 8;
int in2 = 7;
//variables to allow for debouncing of both buttons
int bmode = 5;
int bmodestate;
int lbmodestate;
int bmotor = 4;
int bmotorstate;
int lbmotorstate;

unsigned long lastDebounceTime = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long debounceDelay = 50;

boolean clockw = true;

boolean motormode = false;

//sets the dirstio  of the motor based on a boolean clockw
void setDir() {
  if (clockw == true) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
}

void setup() {
  //myservo.attach(3);
  
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(A0, INPUT);
  pinMode(bmotor, INPUT);
  pinMode(bmode, INPUT);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);

  Serial.begin(9600);
}

void loop() {
  // code for debouncing
  unsigned long currentMillis = millis();
  int reading2 = digitalRead(bmode);
  if (reading2 != lbmodestate) {
    lastDebounceTime2 = millis();
  }
  if ((currentMillis - lastDebounceTime2) > debounceDelay) {
    if (reading2 != bmodestate) {
      bmodestate = reading2;
      if (bmodestate == HIGH) {
        motormode = !motormode;
      }
    }
  }
  // if in motor control state of code then this part of code runs
  if (motormode == true) {
    int reading = digitalRead(bmotor);
    if (reading != lbmotorstate) {
      lastDebounceTime = millis();
    }
    if ((currentMillis - lastDebounceTime) > debounceDelay) {
      if (reading != bmotorstate) {
        bmotorstate = reading;
        if (bmotorstate == HIGH) {
          clockw = !clockw;
        }
      }
    }
    // get reading for speed of motor from potentiometer
    int mspeed = analogRead(A0);
    mspeed = map(mspeed, 0, 1023, 255, 0);
    setDir();
    analogWrite(enA, mspeed);
  }
  if (motormode != true) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    int servospeed = analogRead(A0);
    servospeed = map(servospeed, 0, 1023, 10, 100);
  }
  delay(1);
}
