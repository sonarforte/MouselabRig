# parameters.py
# contains all the settings that should be changed and confirmed before each experiment
# Steven Rofrano
# 2014-09-09

class Cons:

	'''Defines numerical constants for use as parameters and arguments in MouselabRig.

	Do not modify unless you know what you are doing, as these will affect calculation accuracy
	and changing them may result in useless data''' 
	
	# Constants
	encoder_model_A02 = 500		# pulses per revolution for HEDS-5540-A02
	encoder_model_C02 = 100		# pulses per revolution for HEDS-5540-C02
	wheel_radius = 5 			# radius of rig wheel (cm)
	belt_length = 137 			# circumfrence of belt (cm)
	baud_rate = 115200

class Vars:

	'''Defines all the variables that determine the conditional reward system.

	Comment out '''
	

	# Multiple-Choice Variables
	# Comment out (CTRL-/ on Linux) all but one line from each group
	
	# Set True if you want the experiment to be run with a virtual lap (define length below)
	# virtualLaps = False
	virtualLaps = True

	# Look on the left side of the encoder for the last three characters and 
	# pick the one you have (A02 has a better resolution)
	encoderPPR = Cons.encoder_model_A02
	# encoderPPR = Cons.encoder_model_C02
	

	# Which computer are you running Mouselabrig from?
	computerType = 'Linux'
	# computerType = 'Pi'
	# computerType = 'Mac'


	# Do you want to log data for this experiment?
	wantToLog = True
	# wantToLog = False
	
	
	# Variable-Choice Variables
	# Update each variable with your preferred value 
	
	yourInitials = 'SR'						# your initials (as a string)			
	mouseName = 'Jerry'								# name of your mouse (as a string)
	virtualLapLength = 50							# length of virtual lap (cm)
	valveOpenMillis = 100							# amount of time to open valve (ms)
	# Path to save log files on different computers
	logFilePi = '/home/pi/log.txt'				 
	logFileLinux = '/home/mouselab/Dropbox/Repository/MouselabRig/log.txt'
	logFileMac = '/Users/name/Documents/log.txt'
	

	# Params gets printed to the log file once at the beginning of each 
	# experiment. Include information from this file that you would like
	# to have for later reference. For info about the syntax, look at python's
	# string.format() documentation	
	params = 'Run by {0} with mouse {1} and virtual lap {2} cm and valve open for {3} ms.\n' \
			 .format(yourInitials, mouseName, virtualLapLength, valveOpenMillis)


	# Conditions
	# The parameters in this section determine the behavior of the 
	# conditional reward system. The condition block will be tested once for 
	# every iteration of the main loop. The conditions are tested in order; 
	# if a condition fails, execution of the condition block will cease and the 
	# program will continue to run. 
	# The test will be considered passed if and only if all the conditions are 
	# satisfied. Even a passed test may fail to result in water reward, as is 
	# deetermined by the result of the probability value specified below.
	# To find out more information about the individual conditions, open 
	# conditions.py and read the comments there.

	# Positional Conditions
	# Define the parameter below as the positional requirement to be tested.
	# (written as a string).
	# A successful test of this condition will result in the 'trials' 
	# counter being incremented by one.
	# positional = 'timeElapsed'
	positional = 'newLap'


	# Specify the behavioral conditions to be tested. They will execute in 
	# order. If you do not want all conditions to be tested, define them as
	# <none> in this list. E.g. condition3 = none
	# These conditions test mouse behavior and are called only if the 
	# positional requirement from the positonal condition specified above is 
	# met. A successful complettion of these conditions will result in the 
	# 'successes' variable to be incremented. 
	# Whether the water is released at this point, however, is determined by 
	# the probability set for the experiment (below). 
	# behavioral1 = none
	# behavioral2 = none
	# behavioral3

	# After the test has been passed, the release of water is determined with
	# the probability defined below. Set to 1 for water to always be released.
	probability = 1 		# 0 <= p <= 1


	# Arguments for conditions
	# The methods for testing conditions can't directly accept arguments.
	# Set the relevent parameters for each condition method below

	# parameters for Conditions.timeElapsed()
	timeInterval = 1000		# interval for timeElapsed() to return true (ms)
