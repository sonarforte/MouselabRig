// devices.h
// Header file for devices.c 
// Steven Rofrano
// 2014-07-28



#ifndef DEVICES_H_	// continues only if the header has not yet been included
#define DEVICES_H_

#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/io.h>

#define PHOTO_PIN 	5
#define VALVE_PIN 	6
#define OPT_CH1_PIN	4
#define OPT_CHA_PIN	2
#define OPT_CHB_PIN	3
#define LED_PIN 	13		// built-in LED on pin 13		

// Opens valve for ms milliseconds
void valveOpen( int ms );

// // Returns state of input pin i from 0 to 7
// int pinDRead( int i );

// // Writes 0 or 1 to pin i from 0 to 7
// int pinDWrite( int i, int b );

#endif