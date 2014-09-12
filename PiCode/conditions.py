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

	def timeElapsed( self ):
		'''Returns true after Vars.timeInterval seconds have elapsed.

		Uses Vars.timeInterval parameter to set the interval for which
		the method returns true.'''

		if self.data.time[-1] - self.lastTime > Vars.timeInterval:
			
			self.lastTime = self.data.time[-1]
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
	




class Behavioral:
	

	def __init__( self, dataObject ):

		self.data = dataObject