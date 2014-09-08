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
for i in range(5) :
	print '.'
	time.sleep(.5)


print "ready"

while True :

	try :


		lastTime1 = 0
		lastTime2 = 0
		while ard.isOpen() :

			ard.msgRequest()

			if ard.inWaiting() :

				# print ard.readline()
				ard.msgToList()		# reads the stream from the Arduino into a list

				ard.parseValues()

				# # print 'millis: ', ard.millis
				# # print 'photoState: ', ard.photoState
				# # print 'numLaps: ', ard.numLaps
				# # print 'ChA: ', ard.chA
				# # print 'ChB: ', ard.chB

				# # dataline = "PI,N,%d,MS,%d,PS,%d,NL,%d,CHA,%d,CHB,%d,\n" % (ard.receivedMsgs, 
				# 		# ard.millis, ard.photoState, ard.numLaps, ard.chA, ard.chB)

				

				# # if ard.receivedMsgs < 1000 :
				# 	# outfile.write(dataline)
				# # elif ard.receivedMsgs == 1000 :
				# 	# outfile.close()

				# if (time.clock() - lastTime1 > 1) and (ard.index > 1) :
				if (ard.index > 1) :
					print ard.msg
					print 'time: ', ard.time[ard.index - 2], '\n'					
					print 'received to date: ', ard.index, '\n'
					print 'velocity: ', ard.velocity[ard.index - 1], '\n'
					print 'displacement: ', ard.displacement[ard.index - 1], '\n'
					print 'position:', ard.position[ard.index - 1], '\n'
					print 'numLaps: ', ard.numLaps, '\n'
					lastTime1 = time.clock()

			# if time.clock() - lastTime2 > 3 :

			# 	print 'want to open valve\n'
			# 	ard.valveOpen(1000)
			# 	lastTime2 = time.clock()

	except OSError :

		print "Why is there an OSError? Possibly because you reset the Arduino?"
	
	except IOError :

		print "Plug the Arduino back in"
		time.sleep(2)

print "end loop"