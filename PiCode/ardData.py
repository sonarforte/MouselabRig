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


	'''Returns true if the incoming data stream adheres to message protocol'''

	def msgCheck( self ) :

		if (self.msg[0] == 'ARD') and (self.msg[1:len(self.msg)] != 'ARD') : 
			return True


	'''Parses the incoming stream and assigns the values to class variables'''

	def parseValues( self ) :

		self.msg = self.readline().split(',')


		if self.msgCheck() :  

			if 'MS' in self.msg :
				i = self.msg.index('MS') + 1
				ms = int(self.msg[i])

				if self.receivedMsgs == 0 :
					self.startTime = ms

				self.millis = ms - self.startTime

			if 'PHOTO_STATE' in self.msg :
				
				i = self.msg.index('PHOTO_STATE') + 1
				self.photoState = int(self.msg[i])

			self.receivedMsgs += 1



		# for now... come up with a better way to handle this after implementation of experiments
		else : 
			pass 	# !!	

