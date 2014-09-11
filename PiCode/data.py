#!/usr/bin/python
# data.py
# Defines the comm class for communications with Arduino
# Steven Rofrano
# 2014-08-07


import math
import datetime
from parameters import Cons, Vars


class Data:
	
	
	 
	def __init__( self, arduinoObj, filePath ):
		
		self.arduino = arduinoObj
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
		
		self.displacement = []			# list contains linear displacement (time component in millis)
		self.velocity = []			# list contains linear velocity
		self.acceleration = []
		self.valveState = 0
		self.latency = []
		self.revs = 0
		self.index = 0			# number of messages received

		self.trials = 0
		self.successes = 0

		if Vars.wantToLog:
			self.outFile = open(filePath, 'w')
			t = str(datetime.datetime.today())
			self.outFile.write(t + '\n')
			self.outFile.write(Vars.params + '\n')
			ref = 'Index, Time, Displacement, Velocity, Acceleration, ' \
				  'Real_Position, Real_Laps, Virtual_Position, ' \
				  'Virtual_Laps, Valve_State\n'
			self.outFile.write(ref)


	def checkMsg( self ):
		'''Returns true if the incoming data stream adheres to message protocol'''

		for x in self.incoming[1:]:
			if x == 'ARD':
				return False

		if (self.incoming[0] == 'ARD') and  (self.incoming[-1] == '\n'):
			return True 
		return False

	def parseMsg( self ):
		'''Parses the incoming stream and assigns the values to instance variables'''
		
		self.incoming = self.arduino.readMsg()
		

		if self.checkMsg():  

			# update timer value
			if 'MS' in self.incoming:
				self.__getMS()

			if ('TKS') in self.incoming:
				self.__getENC()

			# Update photo sensor value 
			if 'PS' in self.incoming:
				self.__getPS()

			if 'VAL' in self.incoming:
				self.__getVAL()

			self.index += 1			# update message index number


		# for now... come up with a better way to handle this after implementation of experiments
		else: 
			print 'msg didnt parse'
			pass 	# !!	


	def __getMS( self ):
		'''Pulls MS from data stream, normalizes the time and keeps a timer in self.millis'''

		k = self.incoming.index('MS') + 1
		self.millis = int(self.incoming[k])

		if self.index == 0:
			self.startTime = self.millis

		self.millis -= self.startTime		# normalize timer to start at 0

		self.time.append(self.millis)
		if len(self.time) > 0:
			deltaT = self.millis - self.time[self.index - 1]
			self.latency.append(deltaT)


	def __getENC( self ):
		'''Does math on net encoder ticks. 

		Finds revolutions, total displacement, instantaneous velocity, and acceleration'''
		k = self.incoming.index('TKS') + 1
		ticks = float(self.incoming[k])
		i = self.index
		self.revs = ticks / (2 * Vars.encoderPPR)
		disp = 2 * math.pi * Cons.wheel_radius * self.revs
		self.displacement.append(disp)
		self.realPosition.append(disp - self.realLapDist)
		
		if disp - self.virtualLapDist > Vars.virtualLapLength:
			self.__resetVirtualPositionMarker()
			self.numVirtualLaps += 1
		self.virtualLaps.append(self.numVirtualLaps)
		self.virtualPosition.append(disp - self.virtualLapDist)
		
		if self.time[i] == 0:
			self.velocity.append(0.0)
			self.acceleration.append(0.0)
		else:
			dt = (self.time[i] - self.time[i - 1])
			self.velocity.append(1000 * (self.displacement[i] - self.displacement[i - 1]) / dt)
			self.acceleration.append((self.velocity[i] - self.velocity[i - 1]) / dt)


	def __getPS( self ): 
		'''Pulls PHOTO_STATE from stream and keeps track of number of laps'''

		psOld = self.photoState
		k = self.incoming.index('PS') + 1
		self.photoState = int(self.incoming[k])

		# Incrememnt numLaps every time the sensor changes from 0 to 1
		if (psOld == 0) and (self.photoState == 1):			
			# Only counts a lap if the mouse has completed >80 % of a lap
			if self.realPosition[self.index] > .8 * Cons.belt_length:
				self.numRealLaps += 1
			self.__resetRealPositionMarker()

		self.realLaps.append(self.numRealLaps)


	def __getVAL( self ):
		'''Finds state of the valve.

		Pulls value from stream and appends it to a list.'''
		k = self.incoming.index('VAL') + 1
		val = int(self.incoming[k])
		self.valveState = val


	def __resetRealPositionMarker( self ):
		'''Keeps track of position within the lap.

		Resets every time numLaps is incremented. Maintains a list similar to self. displacement,
		whose contents are the total displacement from the lap origin'''

		self.realLapDist = self.displacement[self.index]


	def __resetVirtualPositionMarker( self ):
		'''Keeps track of position within the virtual lap.

		Called by __getENC every time the distance traveled increments by Vars.virtualLapLength.
		Stores current displacement so __getENC() can shift position calculations until the next 
		time a lap is completed.'''

		self.virtualLapDist = self.displacement[self.index]

	def logData( self ):
		'''Adds a line of data to the log file.

		Log file specified during __init__. Writes one line containing the most 
		recent of all calculated values. Should start logging after request for 
		new information so Arduino has time to respond in the interim.'''
		
		if not Vars.wantToLog:
			return

		n = self.index - 1

		# Format the line containing all the data to be printed
		# If this line changes, the legend line printed at the beginning
		# of the log file should be modified to reflect those changes as well
		# The code for the legend is in self.__init__() (above)
		line = 'N,{0},T,{1},X,{2},V,{3},A,{4},RP,{5},RL,{6},VP,{7},' \
			   'VL,{8},VAL,{9},TRI,{10},SUC,{11},\n'.format(n, self.time[n], 
			   self.displacement[n], self.velocity[n], self.acceleration[n],
			   self.realPosition[n], self.numRealLaps, self.virtualPosition[n],
			   self.numVirtualLaps, self.valveState, self.trials, 
			   self.successes)

		self.outFile.write(line)

	def displayData( self ):
		'''Prints values to the screen.'''
		n = self.index - 1

		print 'Time:			', data.time[n]	          
		print 'Displacement:		', data.displacement[n]
		print 'Velocity:		', data.velocity[n]
		print 'Acceleration:		', data.acceleration[n]
		print 'Real Position:		', data.realPosition[data.index - 1]
		print 'Real Lap Count:		', data.numRealLaps
		print 'Virtual Position:	', data.virtualPosition[data.index - 1]
		print 'Virtual Lap Count:		', data.numVirtualLaps
		print 'Number of Trials     ', self.trials
		print 'Number of Successes  ', self.successes
