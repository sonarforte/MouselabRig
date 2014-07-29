// devices.h
// Header file for devices.c 
// Steven Rofrano
// 2014-07-28

#ifndef DEVICES_H_	// continues only if the header has not yet been included
#define DEVICES_H_

#define photoPin 2


// Opens valve for ms milliseconds
void valveOpen( int ms );

// Returns state of photo sensor
int photoState( void );

#endif