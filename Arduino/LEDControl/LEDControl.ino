#include <IRremote.hpp>
#include "ac_LG.hpp"

#define RED_PIN 11
#define GREEN_PIN 10
#define BLUE_PIN 9
#define TMP_FUNCTION 'T'
#define PWM_FUNCTION '#'
#define AC_FUNCTION 'A'
#define LM35_PIN A0
#define IR_PIN 3

Aircondition_LG MyLG_Aircondition;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(100);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(IR_PIN, OUTPUT);
  analogWrite(RED_PIN, 0);
  analogWrite(GREEN_PIN, 0);
  analogWrite(BLUE_PIN, 0);
  IrSender.begin(IR_PIN);
  MyLG_Aircondition.setType(LG_IS_WALL_TYPE);
}

char serialInput[7];
void loop() {
  if (Serial.readBytes(serialInput, 7) > 0) {
    if (serialInput[0] == PWM_FUNCTION) {
      char* hexColor = serialInput + 1;
      long color = strtol(hexColor, NULL, 16);

      byte red = color / 256 / 256;
      byte green = color / 256;
      byte blue = color;

      analogWrite(RED_PIN, red);
      analogWrite(GREEN_PIN, green);
      analogWrite(BLUE_PIN, blue);
    }
    else if (serialInput[0] == TMP_FUNCTION) {
      int temperature = (analogRead(A0) * 5000L) / 1023;
      Serial.print(temperature);
      Serial.print('\n');
    }
    else if (serialInput[0] == AC_FUNCTION) {
      if (serialInput[1] == 'T') {
        unsigned char temperature = (serialInput[2] - '0') * 10 + serialInput[3] - '0';
        if (temperature >= 18 && temperature <= 30) {
          MyLG_Aircondition.sendCommandAndParameter('t', temperature);
        }
      }
      else if (serialInput[1] == 'F') {
        unsigned char fanSpeed = serialInput[2] - '0';
        if (fanSpeed < 3) {
          MyLG_Aircondition.sendCommandAndParameter('f', fanSpeed);
        }
        MyLG_Aircondition.sendCommandAndParameter('0', 0);
      }
      else if (serialInput[1] == 'L') {
        MyLG_Aircondition.sendCommandAndParameter('l', 0);
      }
      else if (serialInput[1] == '0') {
        MyLG_Aircondition.sendCommandAndParameter('0', 0);
      }
      else if (serialInput[1] == '1') {
        MyLG_Aircondition.sendCommandAndParameter('1', 0);
      }
    }
  }
}

