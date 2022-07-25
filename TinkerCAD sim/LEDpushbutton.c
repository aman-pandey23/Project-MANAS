bool val;
int but = 6;
int led = 7;
void setup()
{
  pinMode(led, OUTPUT);
  pinMode(but, INPUT);
}

void loop()
{
  // read button value
  val = digitalRead(but);

  // turn led on or off depending on state of button
  if(val == HIGH){
    digitalWrite(led, HIGH);
  }
  else{
    digitalWrite(led, LOW);
  }
  delay(10);
}
