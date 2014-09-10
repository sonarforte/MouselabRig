
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


/*----------------------------Global Declarations-----------------------------------------
----------------------------------------------------------------------------------------*/


unsigned long lastTime = 0;

// volatile boolean sendMsg = false;	// send message flag - write true if new info to send
char ardMsg[100];
unsigned long msgNo = 0;

volatile int currentChA = 0, currentChB = 0, photoState, valveState = 0;
volatile long ticks = 0;
volatile boolean sendMsg = true;
unsigned long closeTime = 0; 


/*-------------------------Helper FCNs--------------------------------------------
--------------------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

	// Format message string and send to Pi
	
	snprintf(ardMsg, 64, 
		"ARD,N,%lu,MS,%lu,PS,%d,TKS,%ld,VAL,%d,\n", 
		msgNo, millis(), photoState, ticks, valveState); 
	while(Serial.available()) Serial.read();
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

			if ((strcmp(strptr[numWords], "VAL") == 0)) {

				long openTime = strtol(token, &ptr, 10);
				if (openTime) {

					closeTime = valveOpen(openTime);
					sendMsg = true;
					return;
				}
			
			} else if (strcmp(strptr[numWords], "MORE") == 0) {

				long moreData = strtol(token, &ptr, 10);
				if (moreData) {

					sendMsg = true;
					return;
				}

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

/* Setup routine. Run once upon Arduino startup and contains configuration settings 
for the hardware on the chip and boar. Initializes pins for I/O and sets up  interrupts. */
void setup() {

	// Disable watchdog timer (used for software reset in devices.c)
	wdt_disable();						

	// Configure pins for digital I/O
	pinMode(PHOTO_PIN, INPUT_PULLUP);	// open pin for photo sensor as input
	pinMode(VALVE_PIN, OUTPUT);			// open pin attached to relay 1 (controls the valve)
	pinMode(LED_PIN, OUTPUT);			// open builtin LED (pin 13) for visual feedback
	// pinMode(8, OUTPUT);					// open second LED
	pinMode(OPT_CH1_PIN, INPUT);		// open pin for encoder Ch1
	pinMode(OPT_CHA_PIN, INPUT);		// open pin for encoder ChA
	pinMode(OPT_CHB_PIN, INPUT);		// open pin for encoder ChB

	// Initialize serial data stream between Arduino and Pi
	Serial.begin(115200);				
	
	// Configure interrupts
	cli();								// shut off global interrupts

	// Configure INT1 interrupt register settings for encoder ChB
	EIMSK |= (1 << INT1);				// enable external interrupt INT1 (I/O pin 3)
	EICRA |= (1 <<ISC10);				// trigger INT1 on a logical change

	// Configure PCIE2 interrupt register settings for photo sensor
	PCICR |= (1 << PCIE2);				// enable Pin Change Interrupt 2 (AVR pins 23-16)
	PCMSK2 |= (1 << PCINT21);			// enable PCICR on AVR PD5 (I/O pin 5) 

	sei();								// enable global interrupts

}


/* Main loop. Sends sensor data if Pi has requested a new message. 
If no message is to be sent, checks for incoming serial data and processes it.
Shuts off the valve at the end of the loop if its open duration has expired. */
void loop() {
	
	/* Send new data if it's Arduino's turn to message Pi	
	Test the sendMsg flag (only set upon successful parsing by processPiData()) */
	if (sendMsg) {
		
		/* Send the most recent sensor values which have been updated 
		in the background by interrupts */
		sendSensorData();		

	/* Check for new data if it is not Arduino's turn to send a new message. If there is, parse
	and process (checking only to open the valve, send new data, or reset) */
	} else if (Serial.available()) {

		/* Checks for a command to open the valve and opens it (setting closeTime in the process)
		If not, then Arduino is ready to send a reply back to Pi */
		processPiData();

	}
	
	/* Shuts off the valve after the requested time has elapsed. Executes valveClose() only if 
	the valve is currently on and closeTime (set by valveOpen()) has been reached. */
	if (valveState) {
		if (millis() >= closeTime) {

			valveClose();		// closes the valve and sets valveState to zero

		}
	
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
