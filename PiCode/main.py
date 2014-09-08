#!/usr/bin/python
# main.py
# Interfaces with Arduino via ardial data stream
# Steven Rofrano
# 2014-07-28

import time
import threading
from data import ArdData 	# subclass of pySerial deals specifically with Arduino needs


# Initialize communications
ard = ArdData(115200, 'A02')
outfile = open('log.txt', 'w')

ard.resetARD()

print "Firing up the Arduino"


print "ready"

cnt = 0
lastTime1 = 0
lastTime2 = 0
while ard.isOpen() :

	try :
		
		ard.msgRequest()

		if ard.inWaiting() :

			# lst = ard.readline()
			# if lst[0] != 'A' :
			# 	print lst

			print ard.readline()

			# ard.msgToList()		# reads the stream from the Arduino into a list

			# ard.parseValues()

			
			# # dataline = "PI,N,%d,MS,%d,PS,%d,NL,%d,CHA,%d,CHB,%d,\n" % (ard.receivedMsgs, 
			# 		# ard.millis, ard.photoState, ard.numLaps, ard.chA, ard.chB)

			

			# # if ard.receivedMsgs < 1000 :
			# 	# outfile.write(dataline)
			# # elif ard.receivedMsgs == 1000 :
			# 	# outfile.close()

			# if (time.clock() - lastTime1 > 1) and (ard.index > 1) :
			
			# print ard.msg
			# print 'time:             ', ard.time[ard.index - 1]	
			# if (ard.index > 1) :						
			# 	print 'received to date: ', ard.index
			# 	print 'velocity:         ', ard.velocity[ard.index - 1]
			# 	print 'displacement:     ', ard.displacement[ard.index - 1]
			# 	print 'position:         ', ard.position[ard.index - 1]
			# 	print 'acceleration:     ', ard.acceleration[ard.index - 1]
			# 	print 'numLaps:          ', ard.numLaps, '\n'
			# 	lastTime1 = time.clock()

			ard.sendMsg = True
			

		# print 'yo'
		
		# if time.clock() - lastTime2 > 1 :
		if ard.laps[ard.index - 1] > ard.laps[ard.index - 2] :

			
			ard.valveOpen(300)
			# lastTime2 = time.clock()

		cnt += 1

		

	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
		time.sleep(2)
	
	except IOError :

		print "Plug the Arduino back in"
		time.sleep(2)

