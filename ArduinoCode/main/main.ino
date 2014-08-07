// main.ino
// Communicates with RPi through serial data stream
// Steven Rofrano
// 2014-07-28


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>

extern "C" {

	#include "devices.h"

}

/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


unsigned long lastCycleMillis = 0;
char piMsg[64];
char ardMsg[64];
unsigned long valveMs;		// declare all the values the Arduino needs to pull from the stream  

volatile boolean sendMsg = false;	// send message flag - write true if new info to send


/*---------------------------------------------------------------------
---------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

		// Format message string and send to Pi
		snprintf( ardMsg, 64, "ARD,MS,%lu,PHOTO_STATE,%d,\n", millis(), photoState() );
		Serial.print( ardMsg );
		
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
	pinMode(photoPin, INPUT_PULLUP);	// open pin for reading input
	pinMode(valvePin, OUTPUT);			// open pin attached to relay board
	pinMode(ledPin, OUTPUT);			// open LED for visual feedback

	Serial.begin(9600);					// initialize serial data stream
	
	// Configure interrupts
	sei();								// enable global interrupts
	EIMSK |= (1 << INT0);				// enable external interrupt INT0 (I/O pin 2)
	EICRA |= (1 << ISC00);				// trigger INT0 on any logical change


}


// Main loop - Prints sensor data. Rinse and repeat
void loop() {
	
	// Test the relay...
	// digitalWrite(valvePin, HIGH);
	// delay(2000);
	// digitalWrite(valvePin, LOW);
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

// ISR for INT0 (photoPin) 
ISR(INT0_vect) {

	digitalWrite(ledPin, !digitalRead(ledPin));			// indicator that interrupt fired
	sendMsg = true;


}