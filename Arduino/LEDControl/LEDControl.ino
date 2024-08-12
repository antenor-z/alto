#define RED_PIN 11
#define GREEN_PIN 10
#define BLUE_PIN 9

#define PWM_FUNCTION '#'

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
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
  }
}
