#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9
const int IR_SENSOR_PIN = 2 ;// Replace with your IR sensor pin number
#define SERVO_PIN 7
int ledPin1 = 8;
int ledPin2 = 4;
int trigger=0;


MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servo;
 

bool authenticated = false;

void setup() {
  pinMode(ledPin1, OUTPUT); 
  pinMode(ledPin2, OUTPUT); 
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(IR_SENSOR_PIN, INPUT);
  servo.attach(SERVO_PIN);
  servo.write(0); // Initialize the servo to the closed position
}

void loop() {
  // Check for RFID card
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    
    Serial.println(uid);
    mfrc522.PICC_HaltA();
    delay(1000); // Delay to avoid reading the same card repeatedly
    mfrc522.PICC_HaltA();
  }
  
  if (Serial.available() > 0) {

    trigger = Serial.parseInt();
    Serial.println(trigger);
   

    // Control the LED based on the trigger variable
    if (trigger == 1) {
   
      digitalWrite(ledPin1, HIGH);
      digitalWrite(ledPin2, LOW); 
      servo.write(90);

   

      
      while (digitalRead(IR_SENSOR_PIN)==LOW){
          delay(100);
      }
      delay(2000);
     
      servo.write(0);
      digitalWrite(ledPin1, LOW);
      digitalWrite(ledPin2, HIGH);
     

    }
    

    // Perform servo control or other actions based on triggerVariable
  }
  
    
    
}
