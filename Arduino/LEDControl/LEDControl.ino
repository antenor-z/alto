#define RED_PIN 11
#define GREEN_PIN 10
#define BLUE_PIN 9
#define TMP_FUNCTION 'T'
#define PWM_FUNCTION '#'
#define LM35_PIN A0


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(100);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  analogWrite(RED_PIN, 0);
  analogWrite(GREEN_PIN, 0);
  analogWrite(BLUE_PIN, 0);
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
  }
}

