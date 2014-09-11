#!/usr/bin/python
# main.py
# Interfaces with arduino via arduinoial data stream
# Steven Rofrano
# 2014-07-28

import time
import sys
from arduino import Arduino 	# subclass of pySerial deals specifically with arduino needs
from data import Data
from parameters import Cons, Vars



# Initialize communications
arduino = Arduino(Cons.baud_rate)

if Vars.computerType == 'Linux':
	data = Data(arduino, Vars.logFileLinux)
elif Vars.computerType == 'Pi':
	data = Data(arduino, Vars.logFilePi)
elif Vars.computerType == 'Mac':
	data = Data(arduino, Vars.logFileMac)
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

lastTime1 = 0
lastTime2 = 0
while arduino.isOpen():

	try:
		
		arduino.requestMsg()

		if arduino.inWaiting():

			data.parseMsg()

			data.displayData()
			arduino.sendMsg = True
			data.logData()
			

		if (data.index > 1):
			if (data.realLaps[data.index - 1] > data.realLaps[data.index - 2]):
				if data.realPosition[data.index - 1] > 100:
					arduino.openValve(100)


		

	except OSError:

		print "Why is there an OSError? Possibly because you reset the arduino?"
		time.sleep(2)
	
	except IOError:

		print "Plug the arduino back in"
		time.sleep(2)

	except KeyboardInterrupt:

		data.outFile.close()
		sys.exit('\nExperiment concluded. Now have fun analyzing all that data!')