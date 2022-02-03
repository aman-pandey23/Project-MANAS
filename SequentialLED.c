struct led {
  int pin;
  bool state;
};
struct led LEDs[4] = {{3, LOW}, {4, LOW}, {5, LOW}, {6, LOW}};

int maxdelay = 500;

int button_switch = 2;

#define switched  true
#define triggered  true
#define debounce 20

// variable to determine status of interrupt process
volatile  bool interrupt_process_status = {
  !triggered
};
bool initialisation_complete = false;

int looprunning = HIGH;

unsigned long previousMillis = 0;
int interval;

int turn = 0;

// function that runs when the interrupt boolean is HIGH 
void button_interrupt_handler()
{
  //set saved states of led’s
  for (int i = 0; i < 4; i++) {
    digitalWrite(LEDs[i].pin, LEDs[i].state);
  }
  if (initialisation_complete == true)
  {
    if (interrupt_process_status == !triggered) {
      if (digitalRead(button_switch) == HIGH) {
        interrupt_process_status = triggered;
      }
    }
  }
}

//function to read button state with debouncing
bool read_button() {
  int button_reading;
  static bool switching_pending = false;
  static long int elapse_timer;
  if (interrupt_process_status == triggered) {
    button_reading = digitalRead(button_switch);
    if (button_reading == HIGH) {
      switching_pending = true;
      elapse_timer = millis();
    }
    if (switching_pending && button_reading == LOW) {
      if (millis() - elapse_timer >= debounce) {
        switching_pending = false;
        interrupt_process_status = !triggered;
        return switched;
      }
    }
  }
  return !switched;
}


void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(LEDs[i].pin, OUTPUT);
  }
  pinMode(button_switch, INPUT);
  pinMode(A0, INPUT);
  // attach a digital interrupt with the ISR being the button interrupt handler function
  attachInterrupt(digitalPinToInterrupt(button_switch), button_interrupt_handler, RISING);
  initialisation_complete = true;

  Serial.begin(9600);
}

void loop() {
  //read potentiometer value
  int potVal = analogRead(A0);
  potVal = map(potVal, 0, 1023, 0, maxdelay);
  interval = potVal + 1;
  unsigned long currentMillis = millis();
  if (read_button() == switched) {
    looprunning = !looprunning;
  }
  /* looprunning boolean is sued to make this run as a state machine dependent on the boolean to get into the led lighting up part */ 
  if (looprunning) {
    //if first condition ie the time diff = interval then do first state
    if (currentMillis - previousMillis == (interval)) {
      LEDs[0].state = HIGH;
      LEDs[1].state = LOW;
      LEDs[2].state = LOW;
      LEDs[3].state = LOW;
      for (int i = 0; i < 4; i++) {
        digitalWrite(LEDs[i].pin, LEDs[i].state);
      }
    }
    //if second condition ie the time diff = interval x 2 then do second state
    if (currentMillis - previousMillis == (interval * 2)) {
      LEDs[0].state = LOW;
      LEDs[1].state = HIGH;
      LEDs[2].state = LOW;
      LEDs[3].state = LOW;
      for (int i = 0; i < 4; i++) {
        digitalWrite(LEDs[i].pin, LEDs[i].state);
      }
    }
    //if third condition ie the time diff = interval x 3 then do third state
    if (currentMillis - previousMillis >= (interval * 3)) {
      LEDs[0].state = LOW;
      LEDs[1].state = LOW;
      LEDs[2].state = HIGH;
      LEDs[3].state = LOW;
      for (int i = 0; i < 4; i++) {
        digitalWrite(LEDs[i].pin, LEDs[i].state);
      }
    }
    //if fourth condition ie the time diff = interval x 4 then do fourth state
    if (currentMillis - previousMillis >= (interval * 4)) {
      previousMillis = currentMillis;
      LEDs[0].state = LOW;
      LEDs[1].state = LOW;
      LEDs[2].state = LOW;
      LEDs[3].state = HIGH;
      for (int i = 0; i < 4; i++) {
        digitalWrite(LEDs[i].pin, LEDs[i].state);
      }
    }
    // if it passed the fourth condition accidentall or due to a glitch then reset
    if (currentMillis - previousMillis > (interval * 4)) {
      previousMillis = currentMillis;
      for (int i = 0; i < 4; i++) {
        digitalWrite(LEDs[i].pin, LOW);
      }
    }
  }
}
