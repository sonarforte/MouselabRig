# parameters.py
# contains all the settings that should be changed and confirmed before each experiment
# Steven Rofrano
# 2014-09-09

class Cons :

	'''Defines numerical constants for use as parameters and arguments in MouselabRig.

	Do not modify unless you know what you are doing, as these will affect calculation accuracy
	and changing them may result in useless data''' 
	
	# Constants
	encoder_model_A02 = 500		# pulses per revolution for HEDS-5540-A02
	encoder_model_C02 = 100		# pulses per revolution for HEDS-5540-C02
	wheel_radius = 5 			# radius of rig wheel (cm)
	belt_length = 137 			# circumfrence of belt (cm)


class Vars :

	'''Defines all the variables that determine the conditional reward system.

	Comment out '''

	# def __init__( self ) :
	
	

	# Multiple-Choice Variables
	# Comment out (CTRL-/ on Linux/Mac) all but one line from each group
	
	# Set True if you want the experiment to be run with a virtual lap (define length below)
	virtualLaps = False
	# virtualLaps = True

	# Look on the left side of the encoder for the last three characters and 
	# pick the one you have (A02 has a better resolution)
	encoderPPR = Cons.encoder_model_A02
	# encoderPPR = Cons.encoder_model_C02
	

	# Which computer are you running Mouselabrig from?
	computerType = 'Linux'
	# computerType = 'Pi'
	# computerType = 'Mac'
	
	
	# Variable-Choice Variables
	# Update each variable with your preferred value 
	
	experimenterInitials = 'SR'						# your initials (as a string)			
	mouseName = 'Jerry'								# name of your mouse (as a string)
	virtualLapLength = 140							# length of virtual lap (cm)
	valveOpenMillis = 100							# amount of time to open valve (ms)
	# Path to save log files on different computers
	logPathPi = '/home/pi/'				 
	logPathLinux = '/home/mouselab/Dropbox/Repository/MouselabRig/'
	




