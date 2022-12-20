#include "driver/gpio.h"

#define AXIS_Y  25
#define AXIS_X  26

#define DIR_Y   16
#define DIR_X   17

#define ENABLE  12

volatile byte dir_x = 0;
volatile byte dir_y = 0;
hw_timer_t * timer_x = NULL;
hw_timer_t * timer_y = NULL;

volatile byte start_y = 0;
volatile byte start_x = 0;




// setting PWM properties
const int freq = 1000;
const int ledChannel_x = 0;
const int ledChannel_y = 1;
const int resolution = 8;
 
void init_timer_x(){
  // configure LED PWM functionalitites
  ledcSetup(ledChannel_x, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(AXIS_X, ledChannel_x);
}

void init_timer_y(){
  // configure LED PWM functionalitites
  ledcSetup(ledChannel_y, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(AXIS_Y, ledChannel_y);
}

/*
volatile byte state_x = LOW;
void IRAM_ATTR   timer_x_handler(){
  state_x = !state_x;
  gpio_set_level(GPIO_NUM_26, state_x);
}

void init_timer_x()
{
  timer_x = timerBegin(0, 80, true);

  timerAttachInterrupt(timer_x, &timer_x_handler, true);

  timerAlarmWrite(timer_x, 5000, true);


  ///timerAlarmEnable(timer_x);
 
}

volatile byte state_y = LOW;
void  IRAM_ATTR  timer_y_handler(){
  state_y = !state_y;
  //digitalWrite(AXIS_Y, state_y);
  gpio_set_level(GPIO_NUM_25, state_y);
}

void init_timer_y()
{
  timer_y = timerBegin(1, 80, true);
  timerAttachInterrupt(timer_y, &timer_y_handler, true);
  timerAlarmWrite(timer_y, 5000, true);
  ///timerAlarmEnable(timer_y);

}

void stop_motor(int pin)
{
  switch(pin)
  {
    case AXIS_Y:
      timerAlarmDisable(timer_y);
      break;

    case AXIS_X:
      timerAlarmDisable(timer_x);
      break;
  }
  
  digitalWrite(pin, HIGH);
}
*/

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(80);
  pinMode(AXIS_Y, OUTPUT);
  pinMode(AXIS_X, OUTPUT);
  digitalWrite(AXIS_Y, HIGH);
  digitalWrite(AXIS_X, HIGH);
  
  pinMode(DIR_Y, OUTPUT);
  pinMode(DIR_X, OUTPUT);
  init_timer_x();
  init_timer_y();
}


void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    delay(20);
    String data = Serial.readString();
    Serial.flush();

    if(data.indexOf("YUP") != -1)
    {
      dir_y = LOW;
      digitalWrite(DIR_Y, dir_y);
      delay(10);
      ledcWrite(ledChannel_y, 127);
      Serial.println("ok");
    }

    if(data.indexOf("YDOWN") != -1)
    {
      dir_y = HIGH;
      digitalWrite(DIR_Y, dir_y);
      delay(10);
      ledcWrite(ledChannel_y, 127);
      Serial.println("ok");
    }

    if(data.indexOf("YSTOP") != -1)
    {
      digitalWrite(AXIS_Y, HIGH);
      ledcWrite(ledChannel_y, 0);
      Serial.println("ok");
    }


    
    if(data.indexOf("XLEFT") != -1)
    {
      dir_x = HIGH;
      digitalWrite(DIR_X, dir_x);
      delay(10);
      ledcWrite(ledChannel_x, 127);
      Serial.println("ok");
    }

    if(data.indexOf("XRIGTH") != -1)
    {
      dir_x = LOW;
      digitalWrite(DIR_X, dir_x);
      delay(10);
      ledcWrite(ledChannel_x, 127);
      Serial.println("ok");
    }

    if(data.indexOf("XSTOP") != -1)
    {
      digitalWrite(AXIS_X, HIGH);
      ///timerAlarmDisable(timer_x);
      ledcWrite(ledChannel_x, 0);
      Serial.println("ok");
    }

    if(data.indexOf("START") != -1)
    {
      Serial.println("ok");
    }
    
  }
}
