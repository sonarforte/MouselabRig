#!/usr/bin/python
# data.py
# Defines the comm class for communications with Arduino
# Steven Rofrano
# 2014-08-07

import serial
import math
from parameters import Cons, Vars


class ArdData( serial.Serial ) :
	
	
	 
	def __init__( self, rate, enc = 'A02' ) :
		'''Finds the correct port and initializes serial communication at baudrate "rate"
		Takes the name of the encoder as a string for motion calculations'''

		self.sentMsgs = 0
		self.startTime = 0
		self.time = []
		self.photoState = 0
		self.numLaps = 0
		self.laps = []
		self.ticks = 0
		self.displacement = []			# list contains linear displacement (time component in millis)
		self.position = []				# list contains linear position in current lap
		self.velocity = []			# list contains linear velocity
		self.acceleration = []
		self.valveState = []
		self.revs = 0
		self.index = 0			# number of messages received
		self.lapDist = 0
		self.sendMsg = False
		self.valveOpenTime = 0


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

	

	def msgToList( self ) :
		'''Reads the message from Arduino and separates data by commas into a list'''

		self.msg = self.readline().split(',')
		return self.msg



	

	def msgCheck( self ) :
		'''Returns true if the incoming data stream adheres to message protocol'''

		header = bool((self.msg[0] == 'ARD') and (self.msg[1:(len(self.msg) - 1)] != 'ARD'))
		trailer = bool(self.msg[len(self.msg) - 1] == '\n')
		return header and trailer

	

	def parseValues( self ) :
		'''Parses the incoming stream and assigns the values to instance variables'''
		if not hasattr(ArdData, 'msg') :
			self.msgToList()

		lst = self.msg

		if self.msgCheck() :  

			# update timer value
			if 'MS' in lst :
				self.__getMS()

			if ('TKS') in lst :
				self.__getENC()

			# Update photo sensor value 
			if 'PS' in lst :
				self.__getPS()

			# if 'VAL' in lst :
			# 	self.__getVAL()

			

			self.index += 1			# update message index number

		# for now... come up with a better way to handle this after implementation of experiments
		else : 
			pass 	# !!	



	def __getMS( self ) :
		'''Pulls MS from data stream, normalizes the time and keeps a timer in self.millis'''

		k = self.msg.index('MS') + 1
		self.millis = int(self.msg[k])

		if self.index == 0 :
			self.startTime = self.millis

		self.millis -= self.startTime		# normalize timer to start at 0

		self.time.append(self.millis)


	

	def __getPS( self ) : 
		'''Pulls PHOTO_STATE from stream and keeps track of number of laps'''

		psOld = self.photoState
		k = self.msg.index('PS') + 1
		self.photoState = int(self.msg[k])

		# Incrememnt numLaps every time the sensor changes from 0 to 1
		if (psOld == 0) and (self.photoState == 1) :			
			# Only counts a lap if the mouse has completed >80 % of a lap
			if self.position[self.index] > .8 * Cons.belt_length :
				self.numLaps += 1
			self.__resetPosition()

		self.laps.append(self.numLaps)


	def __getENC( self ) :
		'''Does math on net encoder ticks. 

		Finds revolutions, total displacement, instantaneous velocity, and acceleration'''
		k = self.msg.index('TKS') + 1
		ticks = float(self.msg[k])
		
		i = self.index

		self.revs = ticks / (2 * Vars.encoderPPR)
		disp = 2 * math.pi * Cons.wheel_radius * self.revs
		self.displacement.append(disp)
		self.position.append(disp - self.lapDist)
		if i == 0 :
			self.velocity.append(0)
			self.acceleration.append(0)
		else :
			dt = (self.time[i] - self.time[i - 1])
			self.velocity.append(1000 * (self.displacement[i] - self.displacement[i - 1]) / dt)
			self.acceleration.append((self.velocity[i] - self.velocity[i - 1]) / dt)


	def __getVAL( self ) :
		'''Finds state of the valve.

		Pulls value from stream and appends it to a list.'''
		k = self.msg.index('VAL') + 1
		val = int(self.msg[k])
		self.valveState.append(val)


	def __resetPosition( self ) :
		'''Keeps track of position within the lap.

		Resets every time numLaps is incremented. Maintains a list similar to self. displacement,
		whose contents are the total displacement from the lap origin'''

		self.lapDist = self.displacement[self.index]





	def __sendMsg( self, valveMS = 0, moreData = 0,  reset = 0 ) :
		'''Sends a message over serial to Arduino.

		Includes Pi header, reset flag (only used once), and duration (ms) to open the valve.
		If moreData != 0, valveMS and reset flags will not be set on the Arduino. 
		Only call with moreData = 1 if no other information needs to be sent.'''

		msg = 'PI,VAL,%d,MORE,%d,RES,%d,\n' % (valveMS, moreData, reset)
		self.write(msg)
		self.sendMsg = False

	def msgRequest( self ) :
		'''Tells the Arduino to send new data.

		Sends a message over serial after the current data stream has been processed and
		the processor has been freed up for more data.'''

		self.flushOutput()
		if self.sendMsg :
			if self.valveOpenTime :
				self.__sendMsg(self.valveOpenTime, 1)
				self.valveOpenTime = 0
			
			else :
				self.__sendMsg(0, 1)



	def valveOpen( self, ms ) :
		'''Opens the water valve for MS milliseconds.

		Sends a message over serial with the length of time for the Arduino to open the valve.'''

		self.valveOpenTime = ms
		# print 'valveopen = ms'


	def resetARD( self ) :
		'''Resets the Arduino and re-initializes eeverything.

		Sends a message over serial with the reset flag set to one. Should only be called on 
		startup of the Pi code.'''

		# Emergency command-- does not need self.sendMsg to be true 
		self.__sendMsg(0, 0, 1)		


	

	