int lsron;
int lsroff;
int lsrout = 12;
#include <Wire.h>
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(lsrout, OUTPUT);
  String data = "s";
  while (data == "s"){
      data = mySerial.readStringUntil("|");
      int ind = data.indexOf(',');
      lsron = data.substring(0,ind).toInt();
      lsroff = data.substring(ind+1).toInt(); 
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  String a = Serial.readStringUntil("2");
  int r = a.toInt();
  if (r == 1){
    digitalWrite(lsrout, HIGH);
    delay(lsron);
    digitalWrite(lsrout, LOW);
    delay(lsroff);
  }
  else if (r == 0){
    digitalWrite(lsrout, LOW);
  }

}
