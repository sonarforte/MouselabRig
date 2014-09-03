  // devices.c
// Defines device interface functions 
// Steven Rofrano
// 2014-07-28

#include "devices.h"


// Can't import "HIGH"?
// Opens valve for ms milliseconds
// Should use timer interrupt here or else Arduino does nothing useful while we're waiting
void valveOpen( int ms ) {

	unsigned long startTime = millis();
	digitalWrite(VALVE_PIN, HIGH);

	while  (millis() - startTime < ms) {
		
		// Wait it out until ms time has passed 
	
	}
	
	digitalWrite(VALVE_PIN, LOW);

}

// // Returns state of specified digital pin
// int pinDRead( int i ) {

// 	return bitRead(PIND, i);

// }

// int pinDWrite( int i, int b ) {

// 	if (b != 0) b = 1;
// 	bitWrite(PIND, i, b); 

// }