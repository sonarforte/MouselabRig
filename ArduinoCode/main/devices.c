  // devices.c
// Defines device interface functions 
// Steven Rofrano
// 2014-07-28

#include "devices.h"


volatile int valveOff;


// Opens valve and sets time to close it
int valveOpen( int ms ) {

	digitalWriteFast(VALVE_PIN, HIGH);
	int timeOff = millis() + ms;
	return timeOff;

}


void valveClose( void ) {

	digitalWriteFast(VALVE_PIN, LOW);

}

// Resets the Arduino when called through the watchdog timer
void reset( void ) {

	cli();
	wdt_enable(WDTO_500MS);
	while(1);
	sei();

}