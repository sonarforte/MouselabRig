// main.ino
// Communicates with RPi through serial data stream
// Steven Rofrano
// 2014-07-28


#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern "C" {

	#include "devices.h"

}


#define sensorCycle 10

unsigned long lastCycleMillis = 0;
char piMsg[100];
unsigned long valveMs;		// declare all the values the Arduino needs to pull from the stream  


// Helper functions

// cycleCheck - returns true if "cycle" time has elapsed since "lastMillis"
boolean cycleCheck( unsigned long *lastMillis, unsigned int cycle )
{
	unsigned long currentMillis = millis();
	if (currentMillis - *lastMillis >= cycle) {

		*lastMillis = currentMillis;
		return true;

	}
	else {

		return false;

	}
}



// // Define data output functions

// // numLaps - Returns int value of total laps completed
// int lastLap = 0, lastPhotoState = 0;
// int numLaps( int *lastState ) {
	
// 	int currentState;
// 	currentState = digitalRead(photoPin);
// 	if (currentState != 0) {

// 		if (currentState != *lastState) {

// 			lastLap++;
		
// 		}

// 	}

// 	*lastState = currentState;
// 	return lastLap;

// }


// sendSensorData - Prints sensor information to serial data stream 
// Initialized with "DATA" and terminated with newline
void sendSensorData() {

	if (cycleCheck(&lastCycleMillis, sensorCycle)) {
		
		Serial.print("ARD,");						// entry 1 - data header
		Serial.print("MS,");
		Serial.print(millis());						// entry 2 - number of ms since runtime
		Serial.print(",");
		Serial.print("PHOTO_STATE,");
		Serial.print(photoState());					// entry 4 - state of photoPin
		Serial.print(",");
		Serial.print("\n");							// EOL

	}

}

// Called when there is incoming information from the Pi
// Returns true for valid message, false otherwise
// Supports messages under 100 characters, with under 10 comma-separated keywords, that ends in '\n' 
boolean processPiData() {

	boolean proceed = Serial.readBytesUntil('\n', piMsg, 100);
	if (proceed) {
	
		// Serial.print("Reading from Pi\n");

		char s[] = ",", *token, *endptr;
		char *strptr[10];			// strptr holds pointers to each keyword in the data stream
		int numWords = 0;

		// Begin parsing process
		token = strtok(piMsg, s);

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


void setup() 
{

	pinMode(photoPin, INPUT);			// open pin for reading input
	pinMode(valvePin, OUTPUT);
	Serial.begin(9600);					// initialize serial data stream

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() 
{
	
	// Test the relay...
	// digitalWrite(valvePin, HIGH);
	// delay(2000);
	// digitalWrite(valvePin, LOW);
	// delay(2000);



	int prevPhotoState = photoState();
	delay(200);								
	// !! REMOVE DELAY !!
	if (photoState() != prevPhotoState) {

		sendSensorData();

	}


	if (Serial.available() > 0) {

		// Serial.print("data available\n");
		processPiData();

		// if (parse) {

		// 	// event handling

		// } else {

		// 	// error handling

		// }

	}


}