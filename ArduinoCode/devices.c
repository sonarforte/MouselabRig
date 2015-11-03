  // devices.c
// Defines device interface functions 
// Steven John 
// 2014-07-28

#include "devices.h"


volatile int valveOff;
extern volatile int valveState;

// Opens valve and sets time to close it
unsigned long valveOpen( int ms ) {

	// digitalWriteFast(LED_PIN, HIGH);
	digitalWriteFast(VALVE_PIN, HIGH);
	unsigned long timeOff = millis() + ms;
	valveState = 1;
	return timeOff;

}


void valveClose( void ) {
	// digitalWriteFast(LED_PIN, LOW);
	digitalWriteFast(VALVE_PIN, LOW);
	valveState = 0;

}

// Resets the Arduino when called through the watchdog timer
void reset( void ) {

	cli();
	wdt_enable(WDTO_500MS);
	while(1);
	sei();

}
