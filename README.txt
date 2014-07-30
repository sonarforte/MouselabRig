README.txt
Steven Rofrano
2014-07-28

This file describes the basic operation of the MouselabRig software package. It includes an index of files and basic functionality.


METHODOLOGY
	In the case of our lab, an experiment is simply a set of environmental rules that determine the reward for the mouse. Any experiment answers the question, "Under what conditions is the mouse given the reward?" The goal of the MouselabRig system is to allow researchers to design and implement experiments easily and effectively.

	To control an experiment, a researcher merely has to write a short Python module specifying their desire conditions using pre-defined variables and paramters, and the MouselabRig will take care of the rest. 

	There are two main aspects of the system that help control the hardware so the researcher doesn't have to. The sensors on the rig will be controlled by and interface directly with the Arduino microcontroller. The Arduino subsequently interfaces with the Raspberry Pi (RPi) microcomputer, which determines how the hardware should behave.

	In this system, the Arduino is a dummy board--its role is merely to translate the requests from the RPi into a fomrat understood by the hardware, and relate any information from the sensors back to the RPi. Once at the RPi, the data from the sensors is logged, processed, and fed into the running experiment. The RPi then sends new orders back to the Arduino should the experiment request that hardware be manipulated.

	The researchers role in all of this is to provide the conditions under which the RPi sends orders back to the Arduino. From three lines to one hundred, an experiment simply runs code based on universal parameters without changing the communication or data processing on the back end that's used to make the system actually run. For example,

		import rig
		exp = rig.run()

		while true: 

			if exp.numLaps() - exp.oldLaps() == 1:
				exp.valve(500)

	is all it takes for a researcher to run an experiment that opens the water valve for 500 ms every time the mouse completes a new lap. Of course, there is much more going on in the background that allows all this to happen, and these other processes (although they need not be changed often) are described below.


COMMUNICATION
	The Arduino and RPi communicate through a serial data connection. They are physically connected with a USB cable and using Arduino's Serial module and Python's pySerial extension, they can talk back and forth using serial data communication. The commands used for the Arduino are Serial.print() and Serial.readBytesUntil(). The RPi uses serial.readline() and serial.write() to read and write to the serial bus. The following is a summary of the functions and parameters of the serial transfer methods for both devices.

	On the Arduino,

	Serial.print(<'message'>) prints the string <'message'> to the serial port

	Serial.readBytesUntil(<'endline'>, <buffer>, <characters>) reads at most <characters> number of ASCII characters, stopping at the character<'endline'>, and writes them to a character array <buffer>.

	On the RPi,

	serial.readline() reads the incoming serial data stream until it reaches the newline ('\n') character.

	serial.write(<'message'>) writes the string <'message'> to the serial port.

	Once at the other device, the string must be split and the values from the stream extracted. This is easily accomplished if we specify a communication protocal for sending information between the two devices. The transfer protocol is simple--a header, a trailer, and a comma seperated list of keywords and values make up the transfer string: 
	
	"SENDING_DEVICE,KEYWORD_1,VALUE_1,KEYWORD_2,VALUE_2,...,\n"

	This takes the following form with a message sent from Arduino to RPi:

	"ARD,MILLIS,1345,PHOTO_STATE,1,ENC_STREAM_1,1,ENC_STREAM_2,0,\n"

	Because the read methods for both devices include a provision for the last character of a line, all communications shall end in '\n' and start with a recognizable header. This allows usto easily process an incoming stream with a simple algorithm that can be used by the Arduino, the RPi, or any MATLAB script used for processing the log files afterward. Here is the basic algorithm demonstrated in Python code:

	import serial

	msg = serial.readline.split(",")

	# Identify important keywords and values
	if msg[0] == 'SENDING_DEVICE' :  
					
	for i in range(1, len(msg) - 1) : 	# no need to count the last vale '\n'

		if msg[i] == 'KEYWORD_1' :		# identify the keyword

			keyWord1 = msg[i + 1]		# assign the next list entry to an appropriate variable

		elif msg[i] == 'KEYWORD_2' :	# keep going until you have all desired values

			keyWord2 = msg[i + 1]

		elif ...


	This bit of code is efficient and can be easily ported to other languages and used for other purposes. An obvious drawback is that it doesn't self-identify the incoming values--that is, it has to be expecting a certain keyword in order to read its corresponding value. However, in this type of system this poses no real problem because we have to be expecting the value anyway, because the rest of the code depends on that value being assigned to a specific variable. 

	To add additional values, simply follow this pattern and nothing should break.


