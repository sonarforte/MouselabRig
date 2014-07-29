# main.py
# Interfaces with Arduino via serial data stream
# Steven Rofrano
# 2014-07-28

import serial
import time
import threading



ser = serial.Serial()
ser.baudrate = 9600
portNo = 0

try :
	
	print "try " + str(portNo)
	ser.open()

except serial.SerialException :

	portNo += 1
	ser.port = '/dev/ttyACM' + str(portNo)
	print "except" + str(portNo)
	ser.open()

	# if ser.port == '/dev/ttyACM0' :
	# 	ser.port = '/dev/ttyACM1'

	# elif ser.port == '/dev/ttyACM1' :
	# 	ser.port = '/dev/ttyACM2'

	# elif ser.port == '/dev/ttyACM2' :
	# 	ser.port = '/dev/ttyACM3'

# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = '/dev/ttyACM0'

print "down here"
print ser.port
print ser.isOpen()

received = 0
numLaps = 0
prevPhotoState = 0


while True :

	# print "begin loop"

	try :

		while ser.isOpen() :

			# print "Pi: good connection"
			# ser.write('DATA,VALVE_MS,500,\n')
			# print "Pi: message sent"
			# # time.sleep(5)
			# # print "Pi: done sleeping"



			# if ser.inWaiting > 0 :

			# 	print "Ard: " + ser.readline()


			if ser.inWaiting() :

				received += 1

				ardMsg = ser.readline()
				ardMsg = ardMsg.split(",")

				print ardMsg

				# Assign important values from Ard to their variables
				if ardMsg.index('DATA') == 0 :  
				
					for i in range(1, len(ardMsg) - 1) : 

						if ardMsg[i] == 'milliseconds' :

							millis = ardMsg[i + 1]

						elif ardMsg[i] == 'photoState' :

							photoState = ardMsg[i + 1]



					
					print 'millis: ' + str(millis)
					print 'photoState: ' + str(photoState)

					# if photoState != 0 :

					# 	if photoState != prevPhotoState :

					# 		numLaps += 1
					# 		prevPhotoState = photoState
					# 		ser.write(100)



				# print 'numlaps: ' + str(numLaps)


				for i in range(0, len(ardMsg)) :

					print "entry " + str(i) + " is " + str(ardMsg[i])
			
			# print "Pi: still ser isOpen" + str(ser.inWaiting())


	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
	
	except IOError :

		print "Plug the Arduino back in"

print "end loop"