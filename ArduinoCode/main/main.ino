
// main.ino
// Communicates with RPi through serial data stream
// Steven Rofrano
// 2014-07-28


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include "digitalWriteFast.h"

extern "C" {

	#include "devices.h"

}

/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


unsigned long lastCycleMillis = 0;
char piMsg[100];

unsigned long valveMs;		// declare all the values the Arduino needs to pull from the stream  
unsigned long lastTime = 0;

volatile boolean sendMsg = false;	// send message flag - write true if new info to send
char ardMsg[100];
unsigned long msgNo = 0;

volatile int currentChA, currentChB, prevChA, prevChB;

/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

		// Format message string and send to Pi
		msgNo++;
		snprintf(ardMsg, 64, 
			"ARD,N,%lu,MS,%lu,PS,%d,CHA,%d,CHB,%d,EOL,\n", 
			msgNo, millis(), digitalReadFast(PHOTO_PIN), digitalReadFast(OPT_CHA_PIN), 
			digitalReadFast(OPT_CHB_PIN)); 
		
		Serial.print(ardMsg);
		
		sendMsg = false;			// reset outgoing message flag
}



// Called when there is incoming information from the Pi
// Returns true for valid message, false otherwise
// Supports messages under 100 characters, with under 10 comma-separated keywords, that ends in '\n' 
boolean processPiData( void ) {

	boolean proceed = Serial.readBytesUntil('\n', piMsg, 100);
	if (proceed) {
	
		// Serial.print("Reading from Pi\n");

		char s[] = ",", *token, *endptr;
		char *strptr[10];			// strptr holds pointers to each keyword in the data stream
		int numWords = 0;

		// Begin parsing process
		token = strtok(piMsg, s);

		// Go through the rest of PiMsg (pass NULL to continue parsing piMsg)
		//+ and assign each keyword to the next entry of strptr
		while (token != NULL) {

			strptr[numWords] = token;	// add the keyword pointer to the pointer array
			token = strtok(NULL, s);	// find the next keyword
			numWords++;					// increment the number of words added (NOT an index)	

		}

		// Run through the array of words assign values to the variables
		for(int i = 0; i < numWords; i++) {

			if (strcmp(strptr[i], "VALVE_MS") == 0) {

				valveMs = strtoul(strptr[i + 1], &endptr, 10);
				// Serial.print("valveMs assigned: ");
				// Serial.print(valveMs);
				// Serial.print("\n");

			}
		    
		}

		return true;

	}

	return false;
}


/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


void setup() {

	// Configure pins
	pinMode(PHOTO_PIN, INPUT_PULLUP);	// open pin for reading input
	pinMode(VALVE_PIN, OUTPUT);			// open pin attached to relay board
	pinMode(LED_PIN, OUTPUT);			// open LED for visual feedback
	
	// Open optical encoder pins
	pinMode(OPT_CH1_PIN, INPUT);
	pinMode(OPT_CHA_PIN, INPUT);
	pinMode(OPT_CHB_PIN, INPUT);


	Serial.begin(115200);					// initialize serial data stream
	
	// Configure interrupts
									
	// Optical encoder ChA interrupt									
	// EIMSK |= (1 << INT0);					// enable external interrupt INT0 (I/O pin 2)
	// // EICRA |= ((1 << ISC01) | (1 << ISC00));	// trigger INT0 on rising edge
	// // EICRA |= (1 << ISC00);					// trigger INT0 on logical change
	// EICRA |= (1 << ISC01); 					// trigger INT0 on falling edge

	// Optical enncoder ChB interrupt
	EIMSK |= (1 << INT1);					// enable external interrupt INT1 (I/O pin 3)
	// EICRA |= ((1 << ISC11) | (1 << ISC10));	// trigger INT1 on rising edge
	EICRA |= (1 << ISC10);					// trigger INT1 on a logical change


	// Photo sensor interrupt
	PCICR |= (1 << PCIE2);					// enable Pin Change Interrupt 2 (AVR pins 23-16)
	PCMSK2 |= (1 << PCINT21);				// enable PCIR on AVR PD5 (I/O pin 5) 

	sei();									// enable global interrupts

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() {
	
	// if (millis() - lastTime >= 500) {

	// 	lastTime = millis();
	// 	// sendSensorData();
	// 	digitalWrite(LED_PIN, !digitalRead(LED_PIN));


	// }



	// Test the relay...
	// digitalWrite(VALVE_PIN, HIGH);
	// delay(2000);
	// digitalWrite(VALVE_PIN, LOW);
	// delay(2000);



	// if (Serial.available() > 0) {

	// 	// Serial.print("data available\n");
	// 	processPiData();

	// 	// if (parse) {

	// 	// 	// event handling

	// 	// } else {

	// 	// 	// error handling

	// 	// }

	// }




	if (sendMsg) sendSensorData();
	

}

/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


// Deal with the interrupts

// ISR for INT0 (PHOTO_PIN) 
ISR(INT0_vect) {

	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));		// indicator that interrupt fired
	

	sendMsg = true;


}

ISR(INT1_vect) {

	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));		// indicator that interrupt fired
	sendMsg = true;

}

// Responds to interrupt from PD5
ISR(PCINT2_vect) {

	sendMsg = true;

}