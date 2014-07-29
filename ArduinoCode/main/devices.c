// devices.c
// Defines device interface functions 
// Steven Rofrano
// 2014-07-28

#include "devices.h"

// Opens valve for ms milliseconds
void valveOpen( int ms ) {



}

// Returns state of photo sensor
int photoState( void ) {

	int currentState = digitalRead(photoPin);
	return currentState;

}

