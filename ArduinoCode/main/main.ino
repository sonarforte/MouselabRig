
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

volatile int currentChA = 0, currentChB = 0;
volatile long ticks = 0;
volatile int valveOff;
volatile boolean sendMsg;



/*-------------------------Helper FCNs--------------------------------------------
--------------------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

	
	// Format message string and send to Pi
	
	// sendMsg = false;			// reset outgoing message flag
	snprintf(ardMsg, 64, 
		"ARD,N,%lu,MS,%lu,PS,%d,TKS,%ld,\n", 
		msgNo, millis(), digitalReadFast(PHOTO_PIN), ticks); 
	
	Serial.print(ardMsg);
	msgNo++;
	 
	
	
}



// Called when there is incoming information from the Pi
// Returns true for valid message, false otherwise
// Supports messages under 100 characters, with under 10 comma-separated keywords, that ends in '\n' 
boolean processPiData( void ) {

	char piMsg[64];


	boolean proceed = Serial.readBytesUntil('\n', piMsg, 100);
	if (proceed) {
	
		// Serial.print("Reading from Pi\n");

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

			if (strcmp(strptr[numWords], "RES") == 0) {

				long resetFlag = strtol(token, &ptr, 10);
				
				// Reset the Arduino with watchdog timer
				if (resetFlag) {

					reset();

				}

			} else if ((strcmp(strptr[numWords], "VAL") == 0)) {

				long openTime = strtol(token, &ptr, 10);
				if (openTime) {

					valveOff = valveOpen(openTime);

				}

			}

			numWords++;					// increment the number of words added (NOT an index)

		}

		return true;

	}

	return false;
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

	// Optical encoder ChA interrupt									
	// EIMSK |= (1 << INT0);					// enable external interrupt INT0 (I/O pin 2)
	// // EICRA |= ((1 << ISC01) | (1 << ISC00));	// trigger INT0 on rising edge
	// // EICRA |= (1 << ISC00);					// trigger INT0 on logical change
	// EICRA |= (1 << ISC01); 					// trigger INT0 on falling edge

	// Optical enncoder ChB interrupt
	EIMSK |= (1 << INT1);					// enable external interrupt INT1 (I/O pin 3)
	// EICRA |= ((1 << ISC11) | (1 << ISC10));	// trigger INT1 on rising edge
	EICRA |= (1 <<ISC10);					// trigger INT1 on a logical change


	// Photo sensor interrupt
	PCICR |= (1 << PCIE2);					// enable Pin Change Interrupt 2 (AVR pins 23-16)
	PCMSK2 |= (1 << PCINT21);				// enable PCIR on AVR PD5 (I/O pin 5) 


	// Setup Timer 1
	TCCR1A = 0;								// set settings register A to 0
	TCCR1B = 0;								// set settings register B to 0
	
	// OCR1A = 15624;
	TCCR1B |= (1 << WGM12);					// turn on CTC mode (allows for variable overflow time)
	
	
	// // // set 64 prescaler
	// // TCCR1B |= (1 << CS10);							
	// // TCCR1B |= (1 << CS11);
	

	// // // Set 1024 prescaler
	// // TCCR1B |= (1 << CS10);
	// // TCCR1B |= (1 << CS12);	

	// // Set 256 prescaler
	// TCCR1B |= (1 << CS12);
 	
 // 	TIMSK1 |= (1 << OCIE1A);				// turn on interrupt detection for timer 1
 	

	sei();									// enable global interrupts

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() {
	
	if (millis() - lastTime >= 10) {

		lastTime = millis();

		sendSensorData();

	}

	
	if (Serial.available()) processPiData();


	if (millis() >= valveOff) valveClose();

	// if (sendMsg) sendSensorData();
			

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

	sendMsg = true; 		// dont need if send messages at predetermined intervals?

}

ISR(TIMER1_COMPA_vect) {

	
	Serial.println(millis());
	digitalWriteFast(LED_PIN, !digitalReadFast(LED_PIN));
	
	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));
	// digitalWriteFast(VALVE_PIN, LOW);
	// TIMSK1 &= ~(1 << OCIE1A);

}