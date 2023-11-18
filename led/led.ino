#include <Adafruit_NeoPixel.h> 

//Defines how many LEDS being used
#define LED_COUNT 72
#define LED_PIN 9
#define COM_PIN1 12
#define COM_PIN2 8
#define BRIGHTNESS 40

//Used to initialize
Adafruit_NeoPixel leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);



//Undos previous LED states
void clearLEDs() {  
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
  pinMode(COM_PIN1, INPUT); 
  pinMode(COM_PIN2, INPUT); 
  Serial.begin(9600);
}

void loop() { 
  switch (digitalRead(COM_PIN1) + digitalRead(COM_PIN2) * 2){
    case 1:
      robotOn();
      break;
    case 2:
      shoot();
      break;
    case 3:
      ballin();
      break;
    default:
      robotOff();
  }
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
    leds.setPixelColor(i, leds.ColorHSV(static_cast<unsigned long>(i)*1000 + cycleState));
  }
  cycleState += 1000;
}

int pulseState = 0;
//State for when the claw is being raised
void shoot(){
  for (int i=0; i < LED_COUNT; i++){
    leds.setPixelColor(i, leds.ColorHSV(15000, 255, 110 + 90*sin((i+pulseState)*0.2)));
  }
  pulseState++;
}

//State for when the claw is being lowered
void ballin(){
  for (int i=0; i < LED_COUNT; i++){
    leds.setPixelColor(i, leds.Color(0, 200, 0));
  }
}
