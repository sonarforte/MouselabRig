
// main.ino
// Communicates with RPi through serial data stream
// Steven Rofrano
// 2014-07-28


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include "digitalWriteFast.h"

extern "C" {

	#include "devices.h"

}

/*----------------------------Global Declarations-----------------------------------------
----------------------------------------------------------------------------------------*/



char piMsg[64];

unsigned long valveMs;		// declare all the values the Arduino needs to pull from the stream  
unsigned long lastTime = 0;

volatile boolean sendMsg = false;	// send message flag - write true if new info to send
char ardMsg[100];
unsigned long msgNo = 0;

volatile int currentChA = 0, currentChB = 0;
volatile long ticks = 0;


/*-------------------------Helper FCNs--------------------------------------------
--------------------------------------------------------------------------------*/


// sendSensorData - Prints sensor information to serial data stream 
// Headed with "ARD" and terminated with newline
void sendSensorData( void ) {

	
	// Format message string and send to Pi
	
	sendMsg = false;			// reset outgoing message flag
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

					valveOpenTest(openTime);
					Serial.print("got ms\n");
				}

			}

			numWords++;					// increment the number of words added (NOT an index)

		}

		return true;

	}

	return false;
}

// Resets the Arduino when called through the watchdog timer
void reset() {

	cli();
	wdt_enable(WDTO_500MS);
	while(1);
	sei();

}


void valveOpenTest(int ms) {


	TCNT1  = 0;				// reset counter to 0
	OCR1A = 31249;			// .5 seconds with 256 prescaler
	TCCR1B |= (1 << WGM12);					// turn on CTC mode
	Serial.print("valveOpen\n");
	digitalWriteFast(LED_PIN, !digitalReadFast(LED_PIN));
	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));
	// cli();
	// OCR1A = (ms * 250) - 1;
	// OCR1A = s * 15625 - 1;
	// OCR1A = 15624;
				// one second with 64 prescaler

	// ms = ms / 1000;
	// OCR1A = ms * 15625 - 1;

	// TIMSK1 |= (1 << OCIE1A);
	// sei();

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
	// TCCR1B |= (1 << WGM12);					// turn on CTC mode (allows for variable overflow time)
	
	
	// // set 64 prescaler
	// TCCR1B |= (1 << CS10);							
	// TCCR1B |= (1 << CS11);
	

	// // Set 1024 prescaler
	// TCCR1B |= (1 << CS10);
	// TCCR1B |= (1 << CS12);	

	// Set 256 prescaler
	TCCR1B |= (1 << CS12);
 	
 	TIMSK1 |= (1 << OCIE1A);				// turn on interrupt detection for timer 1
 	

	sei();									// enable global interrupts

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() {
	
	if (millis() - lastTime >= 200) {

		lastTime = millis();




		sendSensorData();
		// digitalWrite(LED_PIN, !digitalRead(LED_PIN));
		// valveOpenTest(1);
		// digitalWriteFast(6, HIGH);
		// digitalWriteFast(LED_PIN, !digitalReadFast(LED_PIN));

		// TIMSK1 &= ~(1 << OCIE1A);
	}
	// delay(500);
	// digitalWriteFast(6, LOW);

	if (Serial.available()) {

		// Serial.print("data available\n");
		processPiData();


	}

	// if (sendMsg) sendSensorData();
			

	// digitalWriteFast(6, HIGH);
	// delay(200);
	// digitalWriteFast(6, LOW);
	// delay(1000);

}

/*--------------------------ISRs-------------------------------------------
-------------------------------------------------------------------------*/


// Deal with the interrupts

// // ISR for INT0 (ChA) 
// ISR(INT0_vect) {

// 	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));		// indicator that interrupt fired
// 	// prevChA = currentChA;
// 	// prevChB = currentChB;
// 	currentChB = digitalReadFast(OPT_CHB_PIN);
// 	currentChA = digitalReadFast(OPT_CHA_PIN);
	

// 	sendMsg = true;
// }

// ISR for INT1 (ChB)
ISR(INT1_vect) {

	currentChA = digitalReadFast(OPT_CHA_PIN);
	currentChB = digitalReadFast(OPT_CHB_PIN);
	
	if (currentChA != currentChB) ticks++;
	else ticks--;
	sendMsg = true;

}

// ISR for PCIC2 (photoPin)
ISR(PCINT2_vect) {

	// sendMsg = true; 		// dont need if send messages at predetermined intervals?

}

ISR(TIMER1_COMPA_vect) {

	TCCR1B &= ~(1 << WGM12);
	Serial.println(millis());
	digitalWriteFast(LED_PIN, !digitalReadFast(LED_PIN));
	
	// digitalWrite(LED_PIN, !digitalRead(LED_PIN));
	// digitalWriteFast(VALVE_PIN, LOW);
	// TIMSK1 &= ~(1 << OCIE1A);

}