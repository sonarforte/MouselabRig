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
	digitalWrite(valvePin, HIGH);

	while  (millis() - startTime < ms) {
		
		// Wait it out until ms time has passed 
	
	}
	
	digitalWrite(valvePin, LOW);

}

// Returns state of photo sensor
int photoState( void ) {

	return digitalRead(photoPin);

}

