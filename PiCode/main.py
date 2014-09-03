#!/usr/bin/python
# main.py
# Interfaces with Arduino via ardial data stream
# Steven Rofrano
# 2014-07-28

import time
import threading
from data import ArdData 	# subclass of pySerial deals specifically with Arduino needs


# Initialize communications
ard = ArdData(115200)
outfile = open('log.txt', 'w')

print "ready"

while True :

	try :

		while ard.isOpen() :

			if ard.inWaiting() :

				print ard.getMsg()		# reads the stream from the Arduino into a list

				ard.parseValues()

				# print 'millis: ', ard.millis
				# print 'photoState: ', ard.photoState
				# print 'numLaps: ', ard.numLaps
				# print 'ChA: ', ard.chA
				# print 'ChB: ', ard.chB
				print 'received to date: ', ard.receivedMsgs, '\n'

				dataline = "PI,N,%d,MS,%d,PS,%d,NL,%d,CHA,%d,CHB,%d,\n" % (ard.receivedMsgs, 
						ard.millis, ard.photoState, ard.numLaps, ard.chA, ard.chB)

				

				if ard.receivedMsgs < 1000 :
					outfile.write(dataline)
				elif ard.receivedMsgs == 1000 :
					outfile.close()



	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
	
	except IOError :

		print "Plug the Arduino back in"
		time.sleep(2)

print "end loop"