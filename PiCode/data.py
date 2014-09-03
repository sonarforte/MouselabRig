#!/usr/bin/python
# comm.py
# Defines the comm class for communications with Arduino
# Steven Rofrano
# 2014-08-07

import serial


class ArdData( serial.Serial ) :
	
	'''Finds the correct port and initializes serial communication at baudrate "rate"'''
	 
	def __init__( self, rate ) :
		
		self.receivedMsgs = 0
		self.sentMsgs = 0

		self.startTime = 0
		self.millis = 0
		self.photoState = 0
		self.numLaps = 0
		self.chA = 0
		self.chB = 0
		self.ch1 = 0

		super(ArdData, self).__init__(baudrate = rate)
		# Identify valid serial port
		portNo = 0
		while True :
			# Loops through serial ports until connection found
			try :
				self.port = '/dev/ttyACM' + str(portNo)
				self.open()
				break

			except serial.SerialException :
				portNo += 1

			if portNo > 8 :
				print "Please connect the Arduino"
				break

		self.flushInput()

	'''Reads the message from Arduino and separates data by commas into a list'''

	def getMsg( self ) :

		self.msg = self.readline().split(',')
		return self.msg



	'''Returns true if the incoming data stream adheres to message protocol'''

	def msgCheck( self ) :

		header = bool((self.msg[0] == 'ARD') and (self.msg[1:(len(self.msg) - 1)] != 'ARD'))
		trailer = bool(self.msg[len(self.msg) - 2] == 'EOL')
		return header and trailer

	'''Parses the incoming stream and assigns the values to instance variables'''

	def parseValues( self ) :

		lst = self.msg

		if self.msgCheck() :  

			# update timer value
			if 'MS' in lst :
				self.__getMS()

			# Update photo sensor value 
			if 'PS' in lst :
				self.__getPS()

			if ('CHA' and 'CHB') in lst :
				self.__getENC()

			self.receivedMsgs += 1			# keep track of total received messages

		# for now... come up with a better way to handle this after implementation of experiments
		else : 
			pass 	# !!	


	'''Pulls MS from data stream, normalizes the time and keeps a timer in self.millis'''

	def __getMS( self ) :

		i = self.msg.index('MS') + 1
		self.millis = int(self.msg[i])

		if self.receivedMsgs == 0 :
			self.startTime = self.millis

		self.millis -= self.startTime		# normalize timer to start at 0


	'''Pulls PHOTO_STATE from stream and keeps track of number of laps'''

	def __getPS( self ) : 

		psOld = self.photoState
		i = self.msg.index('PS') + 1
		self.photoState = int(self.msg[i])

		# Incrememnt numLaps every time the sensor changes from 0 to 1
		if (psOld == 0) and (self.photoState == 1) :
			self.numLaps += 1


	'''Pulls encoder values from stream'''

	def __getENC( self ) :

		i = self.msg.index('CHA') + 1
		self.chA = int(self.msg[i])

		j = self.msg.index('CHB') + 1
		self.chB = int(self.msg[j])
