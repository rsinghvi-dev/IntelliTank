#include "stdio.h"
#include "string.h"
#include "SPI.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"

#define TFT_DC 9
#define TFT_CS 10
#define MAX_MESSAGE_LENGTH 100

void split_buf(char *buf);
char sensor_data[4][10]; // 0-tb  1-ph  2-temp 3-tds 
unsigned long dataDisp();

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

void setup() {
  Serial.begin(9600);
  tft.begin();
  tft.setRotation(1);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0)
 {
   //Create a place to hold the incoming message
   static char message[MAX_MESSAGE_LENGTH];
   static unsigned int message_pos = 0;

   //Read the next available byte in the serial receive buffer
   char inByte = Serial.read();

   //Message coming in (check not terminating character) and guard for over message size
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   //Full message received...
   else
   {
     //Add null character to string
     message[message_pos] = '\0';

     //Print the message (or do other things)
     split_buf(message);
     dataDisp();
     Serial.println("Data:");
     int i;
     for (i=0; i<4; i++) {
      Serial.println(sensor_data[i]);
     }
//     Serial.println(message);
     sensor_data[0][0] = '\0';

     //Reset for the next message
     message_pos = 0;
   }
 }
}

void split_buf(char *buf) {
  const char s[2] = ",";
  char *token;
  char buf_temp[100];
  token = strtok(buf, s);
  int i = 0;
  while( token != NULL ) {
    strcpy(sensor_data[i], token );
    token = strtok(NULL, s);
    i++;
  }
  return;
}


unsigned long dataDisp() {
  tft.fillScreen(ILI9341_BLACK);
  unsigned long start = micros();
  tft.setCursor(0, 0);
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(2);
  tft.println("IntelliTank");
  tft.println();
  tft.println();
  tft.setTextColor(ILI9341_YELLOW);
  tft.setTextSize(2);
  tft.println("Temperature:");
  tft.print(sensor_data[2]);
  tft.println(" C");
  tft.println();
  tft.setTextColor(ILI9341_RED);
  tft.setTextSize(2);
  tft.println("Turbidity:");
  tft.println(sensor_data[0]);
  tft.println();
  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(2);
  tft.println("pH:");
  tft.println(sensor_data[1]);
  tft.println();
  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(2);
  tft.println("TDS:");
  tft.print(sensor_data[3]);
  tft.println(" ppm");
  return micros() - start;
}
