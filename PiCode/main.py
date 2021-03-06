#!/usr/bin/python
# main.py
# Interfaces with arduino via arduinoial data stream
# Steven John 
# 2014-07-28

import time
import sys
from arduino import Arduino 	# subclass of pySerial deals specifically with arduino needs
from data import Data
from parameters import Cons, Vars
from conditions import Positional, Behavioral, Probability


# Initialize communications
arduino = Arduino(Cons.baud_rate)

if Vars.computerType == 'Linux':
	data = Data(arduino, Vars.logFileLinux)
elif Vars.computerType == 'Pi':
	data = Data(arduino, Vars.logFilePi)
elif Vars.computerType == 'Mac':
	data = Data(arduino, Vars.logFileMac)

posit = Positional(data)
behave = Behavioral(data)
prob = Probability()

try:
	print '\nThank you for choosing MouselabRig. We hope you find this experience' \
	 'enjoyable.\nIf you didn\'t update the parameters for this experiment, quit ' \
	 '(CTRL-C) and do so now.\n'
	begin = raw_input('Ready to begin? (Y/N) ')
	if (begin == 'Y') or (begin == 'y'):
		pass
	else: 
		sys.exit('Have a nice day.')
except KeyboardInterrupt:
	sys.exit('\nBe back soon!')


print "Firing up the arduino"

arduino.resetArd()

print "ready"


try:
	while arduino.isOpen():
		
		arduino.requestMsg()

		if arduino.inWaiting():

			data.parseMsg()

			data.displayData()
			arduino.sendMsg = True
			data.logData()
		
			if data.index > 0:
				if getattr(posit, Vars.positional)():
					data.trials += 1
					if getattr(behave, Vars.behavioral1)():
						if getattr(behave, Vars.behavioral2)():
							if getattr(behave, Vars.behavioral3)():
								data.successes += 1
								if prob.probability():
									data.rewards += 1
									arduino.openValve(Vars.valveOpenMillis)
		
		if data.endExperiment():
			raise KeyboardInterrupt
		

except OSError:

	print "Why is there an OSError? Possibly because you reset the arduino?"
	time.sleep(2)

except IOError:

	print "Plug the arduino back in"
	time.sleep(2)

except KeyboardInterrupt:

	data.outFile.close()
	sys.exit('\nExperiment concluded. Have fun analyzing all that data.')
