#!/usr/bin/python
# arduino.py
# Subclasses pySerial to handle interactions with Arduino
# Steven Rofrano
# 2014-09-10

	import serial
	import time
	import math
	import sys
	from parameters import Cons, Vars



class Arduino( serial.Serial ):

	'''Used to deal with Arduino interactions over serial.

	Meant to create an instance of an "Arduino" object that contains methods and properties
	exclusively useful to the Arduino in MouselabRig'''


	def __init__( self, rate, enc = 'A02' ):
		'''Finds the correct port and initializes serial communication at baudrate "rate"
		Takes the name of the encoder as a string for motion calculations'''

		self.sentMsgs = 0
		self.startTime = 0
		self.time = []
		self.photoState = 0
		
		self.numRealLaps = 0
		self.realLaps = []
		self.numVirtualLaps = 0
		self.virtualLaps = []
		self.realPosition = []				# list contains linear position in current lap
		self.virtualPosition = []
		self.realLapDist = 0
		self.virtualLapDist = 0
		
		self.ticks = 0
		self.displacement = []			# list contains linear displacement (time component in millis)
		self.velocity = []			# list contains linear velocity
		self.acceleration = []
		self.valveState = []
		self.latency = []
		self.revs = 0
		self.index = 0			# number of messages received
		
		self.sendMsg = False
		self.valveOpenTime = 0


		super(ArdData, self).__init__(baudrate = rate)
		# Identify valid serial port
		portNo = 0
		try:
		
			while True:
				# Loops through serial ports until connection found
				try:
					self.port = '/dev/ttyACM' + str(portNo)
					self.open()
					break

				except serial.SerialException:
					portNo += 1
				except OSError:
					portNo += 1

				if portNo > 10:

					portNo = 0
					while True: 
						try:
							self.port = '/dev/tty.usbmodem' + str(portNo)
							self.open()
							break

						except serial.SerialException:
							portNo += 1
						except OSError:
							portNo += 1

						if portNo > 32767:
							msg = 'Seril Connection not found. ' \
							'Please connect the Arduino.\nQuitting now.'
							sys.exit(msg)
					break				
				
		except serial.SerialException:

			print "Please connect the Arduino"
			time.sleep(2)
		

		self.flushInput()

	def msgToList( self ):
		'''Reads the message from Arduino and separates data by commas into a list'''

		self.msg = self.readline().split(',')
		return self.msg

	def msgCheck( self ):
		'''Returns true if the incoming data stream adheres to message protocol'''

		header = bool((self.msg[0] == 'ARD') and (self.msg[1:(len(self.msg) - 1)] != 'ARD'))
		trailer = bool(self.msg[len(self.msg) - 1] == '\n')
		return header and trailer




def __sendMsg( self, valveMS = 0, moreData = 0,  reset = 0 ):
		'''Sends a message over serial to Arduino.

		Includes Pi header, reset flag (only used once), and duration (ms) to open the valve.
		If moreData != 0, valveMS and reset flags will not be set on the Arduino. 
		Only call with moreData = 1 if no other information needs to be sent.'''

		msg = 'PI,VAL,%d,MORE,%d,RES,%d,\n' % (valveMS, moreData, reset)
		self.write(msg)
		self.sendMsg = False

	def msgRequest( self ):
		'''Tells the Arduino to send new data.

		Sends a message over serial after the current data stream has been processed and
		the processor has been freed up for more data.'''

		self.flushOutput()
		if self.sendMsg:
			if self.valveOpenTime:
				self.__sendMsg(self.valveOpenTime, 1)
				self.valveOpenTime = 0
			
			else:
				self.__sendMsg(0, 1)



	def valveOpen( self, ms ):
		'''Opens the water valve for MS milliseconds.

		Sends a message over serial with the length of time for the Arduino to open the valve.'''

		self.valveOpenTime = ms
		# print 'valveopen = ms'


	def resetARD( self ):
		'''Resets the Arduino and re-initializes eeverything.

		Sends a message over serial with the reset flag set to one. Should only be called on 
		startup of the Pi code.'''

		# Emergency command-- does not need self.sendMsg to be true 
		self.__sendMsg(0, 0, 1)		