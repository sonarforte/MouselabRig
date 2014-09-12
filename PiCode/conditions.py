#!/usr/bin/python
# conditions.py
# Defines the Experiment class for setting and implementing conditional reward system
# Steven Rofrano
# 2014-09-12

import random
from parameters import Cons, Vars


def probability( p = 1 ):
	'''Returns true p * 100 percent of the time.

	Uses a pseudo-random probability distribution to determine probabalistic experiments. 
	0 <= p <= 1'''

	
	if p >= 1 :
		return True
	if p < 0 : 
		return False

	value = random.random()
	if value <= p :
		return True
	else :
		return False 



class Positional:

	'''Defines the different experiments and parameters that can be run on the rig.

	Each experiment is a standalone method that instructs Arduino to open valve after some
	condition has been met.'''

	def __init__( self, dataObject ):

		self.data = dataObject
		self.lastTime = 0
		self.randTime = random.randrange(Vars.randTimeLower, Vars.randTimeUpper)
		self.lastDisp = 0
		self.randDisp = random.randrange(Vars.randDispLower, Vars.randDispUpper)


	def none( self ):
		'''Returns true.

		When used as the positional condition, main will skip right to the 
		behavior condition check with every iteration.'''

		return True


	def timeElapsed( self ):
		'''Returns true after Vars.timeInterval seconds have elapsed.

		Uses Vars.timeInterval parameter to set the interval for which
		the method returns true.'''

		if self.data.time[-1] - self.lastTime > Vars.elapsedTime:
			
			self.lastTime = self.data.time[-1]
			return True

		return False


	def randomTimeElapsed( self ):
		'''Returns true if a random time in a given interval has elapsed.

		Set the interval from which to find the random time in the paramter 
		file.'''

		if self.data.time[-1] - self.lastTime > self.randTime:
			self.lastTime = self.data.time[-1]
			self.randTime = random.randrange(Vars.randLowerBound, \
				            Vars.randUpperBound)
			return True

		return False


	def newLap( self ):
		'''Returns true if a new lap has been completed.

		If virtual laps are set, the function tests for a new virtual lap.
		Otherwise, real laps will be tested.'''
		if self.data.index < 2:
			return False
		if Vars.virtualLaps:
			if self.data.virtualLaps[-1] > self.data.virtualLaps[-2]:
				return True
			return False
		else:
			if self.data.realLaps[-1] > self.data.realLaps[-2]:
				return True
			return False
	

	def randomDisplacement( self ):
		'''Returns true if a random distance has been travelled.

		Set the interval in which to find a random distance in the parameter 
		file.'''

		if self.data.displacement[-1] - self.lastDisp > self.randDisp:
			self.lastDisp = self.data.displacement[-1]
			self.randDisp = random.randrange(Vars.randDispLower, \
							Vars.randDispUpper)
			return True
		return False

	



class Behavioral:
	

	def __init__( self, dataObject ):

		self.data = dataObject

	def none( self ):
		'''Returns true.

		When used as the positional condition, main will skip right to the 
		behavior condition check with every iteration.'''

		return True

	def isAboveVelocity( self ):
		pass


	def isBelowVelocity( self ):
		pass


	def isAboveAcceleration( self ):
		pass


	def isBelowAcceleration( self ):
		pass