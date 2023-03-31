/*

Author:
	Baher Kher Bek

*/

#include <ros.h>
#include <geometry_msgs/Point.h>


#define enA 23 // left motor
#define in1 17
#define in2 18
#define enB 22 // right motor
#define in3 19
#define in4 21
#define ID 2

const int freq = 400;
const int ledChannel = 0; // enA
const int ledC = 1; // enB
const int resolution = 10;


void callback(const geometry_msgs :: Point& msg){
  if (msg.x == ID){

    if(msg.y < 0){
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
    }
    else {
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
    }

    if(msg.z < 0){
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
    }
    else {
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
    }

    ledcWrite(ledChannel, abs(msg.z));
    ledcWrite(ledC, abs(msg.y));

    
    
  }
}

const char* ssid  = "RobotTeam";
const char* password = "Swarm1234";
IPAddress server(192,168,0,107); //Roscore

const uint16_t serverPort = 11411;

ros :: NodeHandle nh;
ros :: Subscriber <geometry_msgs:: Point> sub("Control", callback);

void setup(){

//  analogWrite(enA, 0);
//  analogWrite(enB, 0);

  ledcSetup(ledChannel, freq, resolution);
  ledcSetup(ledC, freq, resolution);
  ledcAttachPin(enA, ledChannel);
  ledcAttachPin(enB, ledC);

  
  WiFi.begin(ssid, password);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  nh.getHardware()->setConnection(server, serverPort);
  nh.initNode();
  nh.subscribe(sub);

  
}

void loop(){
  nh.spinOnce();
}
