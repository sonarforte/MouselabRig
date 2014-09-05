#!/usr/bin/python
# comm.py
# Defines the comm class for communications with Arduino
# Steven Rofrano
# 2014-08-07

import serial
import math


class ArdData( serial.Serial ) :
	
	'''Finds the correct port and initializes serial communication at baudrate "rate"
	Takes the name of the encoder as a string for motion calculations'''
	 
	def __init__( self, rate, enc = 'A02' ) :
		
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
		self.radius = 5 		# wheel radius is 5 cm
		self.revs = 0
		self.index = 0			# number of messages received
		self.lapDist = 0
		if enc == 'A02' :
			self.ppr = 500
		elif enc == 'C02' :
			self.ppr = 100


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
		if (psOld == 0) and (self.photoState == 1) and (self.index > 10) :
			avgVel = 0
			for j in range(self.index - 10, self.index) :
				avgVel += self.velocity[j]
			# Only counts a lap if the belt is moving forward
			if (avgVel / 10) > 0:
				self.numLaps += 1
				self.__resetPosition()

		self.laps.append(self.numLaps)


	def __getENC( self ) :
		'''Does math on net encoder ticks. 

		Finds revolutions, total displacement, and instantaneous velocity'''
		k = self.msg.index('TKS') + 1
		ticks = float(self.msg[k])
		
		i = self.index

		self.revs = ticks / (2 * self.ppr)
		disp = 2 * math.pi * self.radius * self.revs
		self.displacement.append(disp)
		self.position.append(disp - self.lapDist)
		if i == 0 :
			self.velocity.append(0)
		else :
			self.velocity.append((1000 * (self.displacement[i] - self.displacement[i - 1]) / 
								   (self.time[i] - self.time[i - 1])))




	def __resetPosition( self ) :
		'''Keeps track of position within the lap.

		Resets every time numLaps is incremented. Maintains a list similar to self. displacement,
		whose contents are the total displacement from the lap origin'''

		self.lapDist = self.displacement[self.index]





	def __sendMsg( self, reset = 0, valveMS = 0 ) :
		'''Sends a message over serial to Arduino.

		Includes Pi header, reset flag (only used once), and duration (ms) to open the valve.'''

		msg = 'PI,RES,%d,VAL,%d,\n' % (reset, valveMS)
		self.write(msg)

	
	def resetARD( self ) :
		'''Resets the Arduino and re-initializes eeverything.

		Sends a message over serial with the reset flag set to one. Should only be called on 
		startup of the Pi code.'''

		self.__sendMsg(1)


	def valveOpen( self, ms ) :
		'''Opens the water valve for MS milliseconds.

		Sends a message over serial with the length of time for the Arduino to open the valve.'''

		self.__sendMsg(0, ms)