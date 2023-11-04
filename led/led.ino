#include <Adafruit_NeoPixel.h> 

//Defines how many LEDS being used
#define LED_COUNT 72
#define LED_PIN 9
#define BRIGHTNESS 20

//Used to initialize
Adafruit_NeoPixel leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

//Undos previous LED states
void clearLEDs() 
{  
  for (int i=0; i < LED_COUNT; i++){
    leds.setPixelColor(i,0); 
    leds.show();
  }
}

void setup() {
  leds.begin(); //starts leds
  clearLEDs();  //Turns off leds
  //Not sure why this is necessary since I'd assume the brightness would be controlled by the rgb values?
  leds.setBrightness(BRIGHTNESS); 
}

void loop() { 
  /* Right now we're just running the idle state, but eventually
  we're gonna have multiple states and there will be a switch case 
  statement that decides which function to run*/
  robotOn();
  leds.show(); //Shows modifications
  delay(50);
} 

//State for when there's no input from the vex brain, indicating that the robot is disabled
void robotOff(){
  for (int i=0; i < LED_COUNT; i++){
    leds.setPixelColor(i, leds.Color(200, 0, 0));
  }
}

//Default idle state for robot
int cycleState = 0;
void robotOn(){
  for (int i=0; i < LED_COUNT; i++){
    leds.setPixelColor(i, leds.ColorHSV(i*800 + cycleState));
  }
  cycleState += 800;
}

//State for when the claw is being raised
void clawUp(){

}

//State for when the claw is being lowered
void clawDown(){

}
