# PhotoSensorListen.py
# Displays data from Arduino
# Steven Rofrano
# 2014-07-23

import serial
import ConditionalRewards


ser = serial.Serial('/dev/ttyACM0', 9600);




while True :
	
	while ser.inWaiting > 0 :

		line = ser.readline()
		line = line.split(",")

		for i in range(0, len(line)):

			print "entry " + str(i) + " is " + str(line[i])


	

ser.close()

print "Reconnect Serial Port"