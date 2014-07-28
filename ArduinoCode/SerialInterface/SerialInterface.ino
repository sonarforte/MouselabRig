// SerialInterface.ino
// Communicates directly with all sensor and device hardware
// Sends data to RPi
// Steven Rofrano
// 2014-07-28


// Define pin numbers
#define photoPin 2				// use pin number 2 for the photo sensor

#define sensorCycle 10

unsigned long lastCycleMillis = 0;



// Helper functions

// cycleCheck - returns true if "cycle" time has elapsed since "lastMillis"
boolean cycleCheck( unsigned long *lastMillis, unsigned int cycle )
{
	unsigned long currentMillis = millis();
	if (currentMillis - *lastMillis >= cycle)
	{

		*lastMillis = currentMillis;
		return true;

	}
	else
	{

		return false;

	}
}



// Define data output functions

// numLaps - Returns int value of total laps completed
int lastLap = 0, lastPhotoState = 0;
int numLaps( int *lastState ) {
	
	int currentState;
	currentState = digitalRead(photoPin);
	if (currentState != 0) {

		if (currentState != *lastState) {

			lastLap++;
		
		}

	}

	*lastState = currentState;
	return lastLap;

}



// sendSensorData - Prints sensor information to serial data stream 
// Initialized with "DATA" and terminated with newline
void sendSensorData() {

	if (cycleCheck(&lastCycleMillis, sensorCycle)) {
		
		Serial.print("DATA:,");						// entry 1 - data header
		Serial.print("milliSeconds:,");
		Serial.print(millis());						// entry 2 - number of ms since runtime
		Serial.print(",");
		Serial.print("laps:,");
		Serial.print(numLaps(&lastPhotoState));		// entry 3 - total number of laps completed
		Serial.print(",");			
		Serial.print("photoState:,");
		Serial.print(digitalRead(photoPin));		// entry 4 - state of photoPin
		Serial.print("\n");							// EOL

	}

}


void setup() 
{

	pinMode(photoPin, INPUT);			// open pin for reading input
	Serial.begin(9600);					// initialize serial data stream

}


// Main loop - Prints sensor data. Rinse and repeat
void loop() 
{
	int prevPhotoState = digitalRead(photoPin);
	delay(200);
	if (digitalRead(photoPin) != prevPhotoState) {

		sendSensorData();
	}

}