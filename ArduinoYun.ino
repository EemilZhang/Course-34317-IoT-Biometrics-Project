// ========================== Library Import ========================== //
#include <aws_iot_mqtt.h>
#include <aws_iot_version.h>
#include <Wire.h>
#include "aws_iot_config.h"

// ========================== Variable Setup ========================== //

aws_iot_mqtt_client myClient; // init iot_mqtt_client
char JSON_buf[100];
char JSONUpload_buf[100];
char float_buf[5];
int cnt = 0; // loop counts
int rc = -100; // return value placeholder
int bpm;
char float_bpm[6];
int spo2;
char float_spo2[5];
int boolValue;
char float_boolValue[5];
char requestValue[3];
int ledPin12 = 12;
int ledPin11 = 11;
int ledPin10 = 10;
bool success_connect = false; // whether it is connected
bool current_request = false; // whether there is currently a pending request.

// =================================================================== //

// ============================ Functions ============================ //

// Basic Callback Function (Message Print Out) <<<<<<<<<
void msg_callback(char* src, unsigned int len, Message_status_t messageStatusT) {
  if(messageStatusT == 2) {
    myClient.getDesiredValueByKey(src, "diagnostic", JSON_buf, 100);

    if(JSON_buf[0] == 'R') {
      current_request = true;
    }
    else  {
      current_request = false;
    }
  }
}

void receiveEvent(int howMany) {
  digitalWrite(ledPin10,HIGH);
 
  int bpm = Wire.read();
  Serial.print("Bpm = ");
  Serial.println(bpm);
  int spo2 = Wire.read();
  Serial.print("Spo2 = ");
  Serial.println(spo2);

  dtostrf(bpm, 5, 1, float_bpm);
  float_bpm[5] = '\0'; 
  sprintf_P(JSONUpload_buf, PSTR("{\"state\":{\"reported\":{\"BPM\":%s}}}"), float_bpm);
  myClient.shadow_update("Eemil", JSONUpload_buf, strlen(JSONUpload_buf), NULL, 5);

  dtostrf(spo2, 4, 1, float_spo2);
  float_spo2[4] = '\0';
  sprintf_P(JSONUpload_buf, PSTR("{\"state\":{\"reported\":{\"SPO2\":%s}}}"), float_spo2);
  myClient.shadow_update("Eemil", JSONUpload_buf, strlen(JSONUpload_buf), NULL, 5);

  if(current_request) {
    int boolValue = 0;
    dtostrf(boolValue, 4, 1, float_boolValue);
    float_boolValue[4] = '\0';
    sprintf_P(JSONUpload_buf, PSTR("{\"state\":{\"reported\":{\"userDiagnostic\":%s}}}"), float_boolValue);
    myClient.shadow_update("Eemil", JSONUpload_buf, strlen(JSONUpload_buf), NULL, 5);

    current_request = false;
  }
  else {
    int boolValue = 1;
    dtostrf(boolValue, 4, 1, float_boolValue);
    float_boolValue[4] = '\0';
    sprintf_P(JSONUpload_buf, PSTR("{\"state\":{\"reported\":{\"userDiagnostic\":%s}}}"), float_boolValue);
    myClient.shadow_update("Eemil", JSONUpload_buf, strlen(JSONUpload_buf), NULL, 5);
  }
  
  digitalWrite(ledPin10,LOW);
  delay(250);
}

// ========================== Setup Function ======================== //
void setup() {
  Serial.begin(115200);
  // Start Serial for print-out and wait until it's ready
  pinMode(ledPin12, OUTPUT);
  pinMode(ledPin11, OUTPUT);
  pinMode(ledPin10, OUTPUT);

  while(success_connect == false) {

  // Set up the client
  if((rc = myClient.setup(AWS_IOT_CLIENT_ID, true, MQTTv31, true)) == 0) {
    // Load user configuration
    if((rc = myClient.configWss(AWS_IOT_MQTT_HOST, AWS_IOT_MQTT_PORT, AWS_IOT_ROOT_CA_PATH)) == 0) {
      // Use default connect: 60 sec for keepalive
      if((rc = myClient.connect()) == 0) {
        digitalWrite(ledPin12, HIGH);
        success_connect = true;
        myClient.shadow_init(AWS_IOT_MY_THING_NAME);
        myClient.shadow_init("Eemil");
        myClient.shadow_get("Eemil", msg_callback, 5);
        myClient.yield();
      }
    }
  }
  // Delay to make sure SUBACK is received, delay time could vary according to the server
  delay(2000);
  Wire.begin(8);
  Wire.onReceive(receiveEvent);
}
}

// ========================== Loop Function ========================= //
void loop() {
  if(success_connect) {
    if(current_request) {
      digitalWrite(ledPin11, HIGH);
    }
    else {
      digitalWrite(ledPin11, LOW);
    }
     
    myClient.shadow_get("Eemil", msg_callback, 5);
    myClient.yield();
    
    delay(5500);
  }
}
