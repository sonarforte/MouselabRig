// devices.h
// Header file for devices.c 
// Steven Rofrano
// 2014-07-28



#ifndef DEVICES_H_	// continues only if the header has not yet been included
#define DEVICES_H_

#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/io.h>

#define photoPin 	5
#define valvePin 	6
#define optCh1Pin	4
#define optChAPin	2
#define optChBPin	3
#define ledPin 		13		// built-in LED on pin 13		

// Opens valve for ms milliseconds
void valveOpen( int ms );

// Returns state of input pin i from 0 to 7
int pinDRead( int i );

#endif