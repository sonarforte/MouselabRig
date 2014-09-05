// devices.h
// Header file for devices.c 
// Steven Rofrano
// 2014-07-28



#ifndef DEVICES_H_	// continues only if the header has not yet been included
#define DEVICES_H_

#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include "digitalWriteFast.h"

#define PHOTO_PIN 	5
#define VALVE_PIN 	6
#define OPT_CH1_PIN	4
#define OPT_CHA_PIN	2
#define OPT_CHB_PIN	3
#define LED_PIN 	13		// built-in LED on pin 13		

#define A02			500
#define C02			100






// Opens valve and sets closing time ms milliseconds later
int valveOpen( int ms );

// Closes the valve (called from main() after valveOff time has expired)
void valveClose( void ); 

// Resets the Arduino from software (should only be called from Pi at program start)
void reset( void );



#endif