/*

Author:
	Baher Kher Bek

*/


#define enA 23 // left motor
#define in1 17
#define in2 18
#define enB 22 // right motor
#define in3 19
#define in4 21
#define ID 2

const int freq = 5000;
const int ledChannel = 0; // enA
const int ledC = 1; // enB
const int resolution = 10;

void setup(){

  ledcSetup(ledChannel, freq, resolution);
  ledcSetup(ledC, freq, resolution);
  ledcAttachPin(enA, ledChannel);
  ledcAttachPin(enB, ledC);

  // Pins
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH); 



}

void loop(){
  
  ledcWrite(ledChannel, 1000);
  ledcWrite(ledC, 1000);
}
