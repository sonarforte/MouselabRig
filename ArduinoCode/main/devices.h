// devices.h
// Header file for devices.c 
// Steven Rofrano
// 2014-07-28



#ifndef DEVICES_H_	// continues only if the header has not yet been included
#define DEVICES_H_

#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/io.h>


#define photoPin 	2
#define valvePin 	3
#define optCh1Pin	4
#define optChAPin	5
#define optChBPin	6
#define ledPin 		13		// built-in LED on pin 13		


// Opens valve for ms milliseconds
void valveOpen( int ms );

// Returns state of input pin i from 0 to 7
int pinDRead( int i );

#endif