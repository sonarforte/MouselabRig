#!/usr/bin/python
# arduino.py
# Subclasses pySerial to handle interactions with Arduino
# Steven Rofrano
# 2014-09-10

import serial
import time
import sys

class Arduino( serial.Serial ):

	'''Used to deal with Arduino interactions over serial.

	Meant to create an instance of an "Arduino" object that contains methods and properties
	exclusively useful to the Arduino in MouselabRig'''


	def __init__( self, rate ):
		'''Finds the correct port and initializes serial communication at baudrate "rate"
		Takes the name of the encoder as a string for motion calculations'''

		self.sentMsgs = 0
		self.sendMsg = False
		self.valveOpenTime = 0

		super(Arduino, self).__init__(baudrate = rate)
		# Identify valid serial port
		namesFailed = 0
		portNo = 0
		portName = '/dev/ttyACM'
		try:
		
			while True:
				# Loops through serial ports until connection found
				try:
					self.port =  portName + str(portNo)
					self.open()
					break

				except serial.SerialException:
					portNo += 1
				except OSError:
					portNo += 1

				if portNo > 32767:
					namesFailed += 1
					portNo = 0
					portName = '/dev/tty.usbmodem'

				if namesFailed > 1:
					msg = 'Serial Connection not found. Please connect the Arduino.\n' \
					      'Quitting now.'
					sys.exit(msg)
					
		except serial.SerialException:

			print "Please connect the Arduino"
			time.sleep(2)
		
		self.flushInput()


	def readMsg( self ):
		'''Reads the message from Arduino and separates data by commas into a list'''
	
		return self.readline().split(',')
		 

	def __sendMsg( self, valveMS = 0, moreData = 0,  reset = 0 ):
		'''Sends a message over serial to Arduino.

		Includes Pi header, reset flag (only used once), and duration (ms) to open the valve.
		If moreData != 0, valveMS and reset flags will not be set on the Arduino. 
		Only call with moreData = 1 if no other information needs to be sent.'''

		msg = 'PI,VAL,%d,MORE,%d,RES,%d,\n' % (valveMS, moreData, reset)
		self.write(msg)
		self.sendMsg = False
		self.sentMsgs += 1


	def requestMsg( self ):
		'''Tells the Arduino to send new data.

		Sends a message over serial after the current data stream has been processed and
		the processor has been freed up for more data.'''

		self.flushOutput()
		if self.sendMsg:
			self.__sendMsg(self.valveOpenTime, 1)
			self.valveOpenTime = 0
	

	def openValve( self, ms ):
		'''Opens the water valve for MS milliseconds.

		Sends a message over serial with the length of time for the Arduino to open the valve.'''

		self.valveOpenTime = ms


	def resetArd( self ):
		'''Resets the Arduino and re-initializes eeverything.

		Sends a message over serial with the reset flag set to one. Should only be called on 
		startup of the Pi code.'''

		# Emergency command-- does not need self.sendMsg to be true 
		self.__sendMsg(0, 0, 1)		