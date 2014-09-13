#!/usr/bin/python
# conditions.py
# Defines the Experiment class for setting and implementing conditional reward system
# Steven Rofrano
# 2014-09-12

import random
import math
from parameters import Cons, Vars


class Probability:
	'''Returns true p * 100 percent of the time.

	Uses a pseudo-random probability distribution to determine probabalistic experiments. 
	0 <= p <= 1'''

	def __init__( self ):


		self.p = Vars.probability
		if self.p >= 1:
			self.p = 1
		if self.p < 0: 
			self.p = 0

		self.timesCalled = 0
		if Vars.endAfterSuccesses:
			self.__predeterminedProb()
		

	def __randomProb( self ):

		value = random.random()
		if value <= self.p:
			return True
		else:
			return False 


	def __predeterminedProb( self ):

		rewards = int(self.p * Vars.numberOfSuccesses)
		noRewards = Vars.numberOfSuccesses - rewards
		dist = [True for x in range(rewards)]
		dist.extend([False for x in range(noRewards)])
		random.shuffle(dist)
		self.pDistribution = dist


	def probability( self ):

		if hasattr(self, 'pDistribution'):
			self.timesCalled += 1
			return self.pDistribution[self.timesCalled - 1]
		else:
			self.timesCalled += 1
			return self.__randomProb()



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


	def velocityOverTime( self ):
		'''Returns true if the average velocity over time meets the specified 
		condition.

		Finds the average velocity over a time interval starting at a specific
		time in the past, and tests if it is above, below, or equal within a 
		threshold to a specific value.
		These four parameters can be specified in parameters.py.'''
		
		testVelocity = Vars.velTime
		test = Vars.velTimeTest
		threshold = Vars.wasVelTimeThreshold
		timeToCheck = Vars.wasVelTimeAgo
		
		listToCheck = self.data.time

		startInterval = listToCheck[-1] - timeToCheck

		# Stop executing condition if the desired time doesn't exist
		if startInterval <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > startInterval:
				i -= 1
				if listToCheck[i] == startInterval:
					break
			
			velInterval = self.data.velocity[i:]
			avgVel = sum(velInterval) / len(velInterval)

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if avgVel >= testVelocity:
				return True
			return False
		elif test == Cons.test_below:
			if avgVel <= testVelocity:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(avgVel - testVelocity) <= threshold:
				return True
			return False



	def velocityOverDistance( self ):
		'''Returns true if the average velocity over distanc meets the 
		specified condition.

		Finds the average velocity over a displacement interval starting at 
		a specific distance in the past, and tests if it is above, below, or
		equal within a threshold to a specific value.
		These four parameters can be specified in parameters.py.'''
		
		testVelocity = Vars.velDist
		test = Vars.velDistTest
		threshold = Vars.velDistThreshold
		dispToCheck = Vars.velDistAgo
		
		listToCheck = self.data.displacement

		startInterval = listToCheck[-1] - dispToCheck

		# Stop executing condition if the desired time doesn't exist
		if startInterval <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > startInterval:
				i -= 1
				if listToCheck[i] == startInterval:
					break
			
			velInterval = self.data.velocity[i:]
			avgVel = sum(velInterval) / len(velInterval)

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if avgVel >= testVelocity:
				return True
			return False
		elif test == Cons.test_below:
			if avgVel <= testVelocity:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(avgVel - testVelocity) <= threshold:
				return True
			return False


	def accelerationOverTime( self ):
		'''Returns true if the average acceleration over time meets the 
		specified condition.

		Finds the average acceleration over a time interval starting at a 
		time in the past, and tests if it is above, below, or equal within a 
		threshold to a specific value.
		These four parameters can be specified in parameters.py.'''
		
		testAccel = Vars.velTime
		test = Vars.velTimeTest
		threshold = Vars.wasVelTimeThreshold
		timeToCheck = Vars.wasVelTimeAgo
		
		listToCheck = self.data.time

		startInterval = listToCheck[-1] - timeToCheck

		# Stop executing condition if the desired time doesn't exist
		if startInterval <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > startInterval:
				i -= 1
				if listToCheck[i] == startInterval:
					break
			
			accInterval = self.data.acceleration[i:]
			avgAcc = sum(accInterval) / len(accInterval)

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if avgAcc >= testAccel:
				return True
			return False
		elif test == Cons.test_below:
			if avgAcc <= testAccel:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(avgAcc - testAccel) <= threshold:
				return True
			return False


	def accelerationOverDistance( self ):
		'''Returns true if the average acceleration over distance meets the 
		specified condition.

		Finds the average acceleration over a displacement interval starting 
		at a specific distance in the past, and tests if it is above, below, 
		or equal within a threshold to a specific value.
		These four parameters can be specified in parameters.py.'''
		
		testAccel = Vars.accDist
		test = Vars.accDistTest
		threshold = Vars.accDistThreshold
		dispToCheck = Vars.accDistAgo
		
		listToCheck = self.data.displacement

		startInterval = listToCheck[-1] - dispToCheck

		# Stop executing condition if the desired time doesn't exist
		if startInterval <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > startInterval:
				i -= 1
				if listToCheck[i] == startInterval:
					break
			
			accInterval = self.data.acceleration[i:]
			avgAcc = sum(accInterval) / len(accInterval)

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if avgAcc >= testAccel:
				return True
			return False
		elif test == Cons.test_below:
			if avgAcc <= testAccel:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(avgAcc - testAccel) <= threshold:
				return True
			return False


	def isVelocity( self ):
		'''Returns true if the current velocity meets the specified condition.

		Tests if the velocity is above, below, or equal within a threshold to
		a specific value. These three parameters can be specified in 
		parameters.py.'''

		testVelocity = Vars.isVel
		test = Vars.isVelTest
		threshold = Vars.isVelThreshold


		# Use an average velocity from five consecutive values to reduce the 
		# effect of anomalies
		if self.data.index > 3:
			avgVel = sum(self.data.velocity[-3:])
			avgVel = avgVel / 3.0
			if test == Cons.test_above:
				if avgVel >= testVelocity:
					return True
				return False
			if test == Cons.test_below:
				if avgVel <= testVelocity:
					return True
				return False
			if test == Cons.test_equal:
				if abs(avgVel - testVelocity) <= threshold:
					return True
				return False
		
		# Reduce trials which were incremented when positional returned true
		self.data.trials -= 1 	
		return False


	def wasVelocityTimeAgo( self ):
		'''Returns true if a past velocity meets the specified condition.

		Finds the velocity at a specific time in the past, and tests if 
		it is above, below, or equal within a threshold to a specific value.
		These four parameters can be specified in parameters.py.'''

		testVelocity = Vars.wasVelTime
		test = Vars.wasVelTimeTest
		threshold = Vars.wasVelTimeThreshold
		timeToCheck = Vars.wasVelTimeAgo
		
		listToCheck = self.data.time

		pastTime = listToCheck[-1] - timeToCheck

		# Stop executing condition if the desired time doesn't exist
		if pastTime <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > pastTime:
				i -= 1
				if listToCheck[i] == pastTime:
					break
			
			oldVel = sum(self.data.velocity[i - 1:i + 2])
			oldVel = oldVel / 3.0

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if oldVel >= testVelocity:
				return True
			return False
		elif test == Cons.test_below:
			if oldVel <= testVelocity:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(oldVel - testVelocity) <= threshold:
				return True
			return False


	def wasVelocityDistanceAgo( self ):
		'''Returns true if a past velocity meets the specified condition.

		Finds the velocity at a specific distance in the past, and tests if 
		it is above, below, or equal within a threshold to a specific value.
		These four parameters can be specified in parameters.py.'''

		testVelocity = Vars.wasVelDist
		test = Vars.wasVelDistTest
		threshold = Vars.wasVelDistThreshold
		dispToCheck = Vars.wasVelDistAgo
		
		listToCheck = self.data.displacement

		pastDisp = listToCheck[-1] - dispToCheck

		# Stop executing condition if the desired time doesn't exist
		if pastDisp <= 0: 
			self.data.trials -= 1
			return False

		try: 
			i = -1
			while listToCheck[i] > pastDisp:
				i -= 1
				if listToCheck[i] == pastDisp:
					break
			
			oldVel = sum(self.data.velocity[i - 1:i + 2])
			oldVel = oldVel / 3.0

		except IndexError:
			self.data.trials -= 1
			return False

		if test == Cons.test_above:
			if oldVel >= testVelocity:
				return True
			return False
		elif test == Cons.test_below:
			if oldVel <= testVelocity:
				return True
			return False
		elif test == Cons.test_equal:
			if abs(oldVel - testVelocity) <= threshold:
				return True
			return False