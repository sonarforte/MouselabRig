#!/usr/bin/python
# main.py
# Interfaces with Arduino via ardial data stream
# Steven Rofrano
# 2014-07-28

# import ardial
import time
import threading
from ardData import ArdData 	# subclass of pySerial deals specifically with Arduino needs


numLaps = 0
prevPhotoState = 0


# Initialize communications
ard = ArdData(115200)

print "ready"



while True :

	# print "begin loop"

	try :

		while ard.isOpen() :

			if ard.inWaiting() :

				ard.parseValues()

				print ard.msg	
				print 'millis: ', ard.millis
				print 'photoState: ', ard.photoState
				print 'received to date: ', ard.receivedMsgs



	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
	
	except IOError :

		print "Plug the Arduino back in"

print "end loop"