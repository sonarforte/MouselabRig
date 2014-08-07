#!/usr/bin/python
# main.py
# Interfaces with Arduino via serial data stream
# Steven Rofrano
# 2014-07-28

import serial
import time
import threading

received = 0
numLaps = 0
prevPhotoState = 0


# Initialize serial communications
ser = serial.Serial()	
ser.baudrate = 115200

# Identify valid serial port
portNo = 0
while True :
	# Loops through serial ports until connection found
	try :
		ser.port = '/dev/ttyACM' + str(portNo)
		ser.open()
		break

	except serial.SerialException :
		portNo += 1

	if portNo > 8 :
		print "Please connect the Arduino"
		break

print "ready"

ser.flushInput()

while True :

	# print "begin loop"

	try :

		while ser.isOpen() :

		

			if ser.inWaiting() :

				received += 1

				ardMsg = ser.readline()
				ardMsg = ardMsg.split(",")

				print ardMsg

				# Assign important values from Ard to their variables
				if (ardMsg[0] == 'ARD') and (ardMsg[1:len(ardMsg)] != 'ARD'):  
				
					for i in range(1, len(ardMsg) - 1) : 

						if ardMsg[i] == 'MS' :

							millis = ardMsg[i + 1]

						elif ardMsg[i] == 'PHOTO_STATE' :

							photoState = ardMsg[i + 1]


					
					
					print 'millis: ' + str(millis)
					print 'photoState: ' + str(photoState)

					# if photoState != 0 :

					# 	if photoState != prevPhotoState :

					# 		numLaps += 1
					# 		prevPhotoState = photoState
					# 		ser.write(100)



				# print 'numlaps: ' + str(numLaps)


				
			
			# print "Pi: still ser isOpen" + str(ser.inWaiting())


	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
	
	except IOError :

		print "Plug the Arduino back in"

print "end loop"