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

print '\nThank you for choosing MouselabRig. We hope you find this experience enjoyable.\n'
print 'If you didn\'t update the parameters for this experiment, quit (CTRL-Z) and do so now.\n'
begin = raw_input('Ready to begin? (Y/N) ')
if (begin == 'Y') or (begin == 'y'):
	pass
else: 
	sys.exit('Fine. Have a nice day.')


print "Firing up the arduino"

arduino.resetArd()

print "ready"

lastTime1 = 0
lastTime2 = 0
while arduino.isOpen():

	try:
		
		arduino.requestMsg()

		if arduino.inWaiting():
			# print "INWAITING"
			# lst = arduino.readline()
			# if lst[0] != 'A':
			# 	print lst

			# print arduino.readline()

			# arduino.msgToList()		# reads the stream from the arduino into a list

			data.parseMsg()

			
			

			

			# # if arduino.receivedMsgs < 1000:
			# 	# outfile.write(dataline)
			# # elif arduino.receivedMsgs == 1000:
			# 	# outfile.close()

			# if (time.clock() - lastTime1 > 1) and (data.index > 1):
			
			# print arduino.msg
			print 'time:			', data.time[data.index - 1]	
			print 'index:			', data.index            
			# if (data.index > 0):						
				# print 'received to date: ', data.index
			print 'acceleration:		', data.acceleration[data.index - 1]
			print 'velocity:		', data.velocity[data.index - 1]
			print 'displacement:		', data.displacement[data.index - 1]
			print 'real position:		', data.realPosition[data.index - 1]
			print 'real laps:		', data.numRealLaps
			print 'virtual position:	', data.virtualPosition[data.index - 1]
			print 'virtual laps:		', data.numVirtualLaps
			print 'valve:			', data.valveState
			print 'latency:		', data.latency[data.index - 1], '\n'
			# 	lastTime1 = time.clock()

			arduino.sendMsg = True
			data.logData()
			

		# print 'yo'
		
		# if time.clock() - lastTime2 > 2:
		if (data.index > 1):
			if (data.realLaps[data.index - 1] > data.realLaps[data.index - 2]):
				if data.realPosition[data.index - 1] > 100:
					arduino.openValve(100)
			# lastTime2 = time.clock()


		

	except OSError:

		print "Why is there an OSError? Possibly because you reset the arduino?"
		time.sleep(2)
	
	except IOError:

		print "Plug the arduino back in"
		time.sleep(2)

	except KeyboardInterrupt:

		data.outFile.close()
		sys.exit('Experiment concluded. Now have fun analyzing all that data!')