
// main.ino
// Communicates with RPi through serial data stream
// Steven Rofrano
// 2014-07-28


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/io.h>


extern "C" {

	#include "devices.h"

}


/*----------------------------Global Declarations-----------------------------------------
----------------------------------------------------------------------------------------*/


unsigned long lastTime = 0;

// volatile boolean sendMsg = false;	// send message flag - write true if new info to send
char ardMsg[100];
unsigned long msgNo = 0;

volatile int currentChA = 0, currentChB = 0, photoState;
volatile long ticks = 0;
volatile boolean sendMsg;
unsigned long closeTime; 

/*-------------------------Helper FCNs--------------------------------------------
--------------------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

	// Format message string and send to Pi
	
	snprintf(ardMsg, 64, 
		"ARD,N,%lu,MS,%lu,PS,%d,TKS,%ld,\n", 
		msgNo, millis(), photoState, ticks); 
	
	Serial.print(ardMsg);
	msgNo++;
	sendMsg = false;			// reset outgoing message flag
		
}

// Called when there is incoming information from the Pi
// Returns true for valid message, false otherwise
// Supports messages under 100 characters, with under 10 comma-separated keywords, that ends in '\n' 
void processPiData( void ) {

	char piMsg[64];
	boolean proceed = Serial.readBytesUntil('\n', piMsg, 64);

	if (proceed) {
	
		char s[] = ",", *token, *ptr;
		char *strptr[10];			// strptr holds pointers to each keyword in the data stream
		int numWords = 0;

		// Begin parsing process
		token = strtok(piMsg, s);

		// Go through the rest of PiMsg (pass NULL to continue parsing piMsg)
		//+ and assign each keyword to the next entry of strptr
		while (token != NULL) {

			strptr[numWords] = token;	// add the keyword pointer to the pointer array
			token = strtok(NULL, s);	// find the next keyword

			if (strcmp(strptr[numWords], "MORE") == 0) {

				long moreData = strtol(token, &ptr, 10);
				if (moreData) {

					sendMsg = true;
					// return;

				}
			
			} else if ((strcmp(strptr[numWords], "VAL") == 0)) {

				long openTime = strtol(token, &ptr, 10);
				if (openTime) closeTime = valveOpen(openTime);

			} else if (strcmp(strptr[numWords], "RES") == 0) {

				long resetFlag = strtol(token, &ptr, 10);
				
				// Reset the Arduino with watchdog timer
				if (resetFlag) reset();

			} 

			numWords++;					// increment the number of words added (NOT an index)

		}

	}

}


/*-----------------------Setup & Main----------------------------------------------
---------------------------------------------------------------------------------*/


void setup() {


	wdt_disable();

	// Configure pins
	pinMode(PHOTO_PIN, INPUT_PULLUP);	// open pin for reading input
	pinMode(6, OUTPUT);			// open pin attached to relay board
	pinMode(LED_PIN, OUTPUT);			// open LED for visual feedback
	
	// Open optical encoder pins
	pinMode(OPT_CH1_PIN, INPUT);
	pinMode(OPT_CHA_PIN, INPUT);
	pinMode(OPT_CHB_PIN, INPUT);


	Serial.begin(115200);					// initialize serial data stream
	
	// Configure interrupts
	
	cli();

	// Optical enncoder ChB interrupt
	EIMSK |= (1 << INT1);					// enable external interrupt INT1 (I/O pin 3)
	EICRA |= (1 <<ISC10);					// trigger INT1 on a logical change


	// Photo sensor interrupt
	PCICR |= (1 << PCIE2);					// enable Pin Change Interrupt 2 (AVR pins 23-16)
	PCMSK2 |= (1 << PCINT21);				// enable PCIR on AVR PD5 (I/O pin 5) 
 	

	sei();									// enable global interrupts

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() {
	
	// if (millis() - lastTime >= 10) {

	// 	lastTime = millis();

	// 	sendSensorData();

	// }

	
	if (Serial.available()) {

		processPiData();

	}
	
	if (sendMsg) {
	
		sendSensorData();

	}
	
	if (millis() >= closeTime) {

		valveClose();

	}

}

/*--------------------------ISRs-------------------------------------------
-------------------------------------------------------------------------*/


// Deal with the interrupts

// ISR for INT1 (ChB)
ISR(INT1_vect) {

	currentChA = digitalReadFast(OPT_CHA_PIN);
	currentChB = digitalReadFast(OPT_CHB_PIN);
	
	if (currentChA != currentChB) ticks++;
	else ticks--;

}

// ISR for PCIC2 (photoPin)
ISR(PCINT2_vect) {

	photoState = digitalReadFast(PHOTO_PIN);

}
