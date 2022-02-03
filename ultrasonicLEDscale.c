struct led {
  int pin;
  bool state;
};
struct led LEDs[6] = {{2, LOW}, {3, LOW}, {4, LOW}, {5, LOW}, {6, LOW}, {7, LOW}};

#define echoPin 9
#define trigPin 8
long duration;
int distance;

int ledVal;

void setup()
{
  //set all led’s as output
  for (int i = 0; i < 6; i++) {
    pinMode(LEDs[i].pin, OUTPUT);
  }
  //set sensor pins modes
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
  Serial.begin(9600);
}

void loop()
{
  /*activate trigger for a short time and get reading from the echo pin the time for which echo      pin stays high is time taken by sound to travel to object reflect and come back */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  //distance calculation
  distance = duration * 0.034 / 2;
  ledVal = map(distance, 0, 332, 0, 6);
  // map value of the distance reading (0 to 332 cm s) to 0 o 6 to use for lighting up led’s
  for (int i = 0; i < ledVal; i++) {
    digitalWrite(LEDs[i].pin, HIGH);
  }
  if (ledVal == 0){
    digitalWrite(LEDs[0].pin, LOW);
  }
  /set states of led’s appropriately based on the value of the mapped variable
  for (int i = 6; i > ledVal; i--) {
    digitalWrite(LEDs[i].pin, LOW);
  }
  Serial.println(ledVal);
  delay(1);
}
