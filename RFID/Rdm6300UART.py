#!/usr/bin/python

'''
code originally obtained from raspberry pi forum: 
http://www.raspberrypi.org/forums/viewtopic.php?t=59025&p=501603
'''

import serial
import sys
import time
from operator import xor 
# UART
ID = ""
Ze = 0
Checksum = 0
Day = 0
# Flags
Startflag = "\x02"
Endflag = "\x03"
# UART open
UART = serial.Serial("/dev/ttyAMA0", 9600) 
UART.close();
UART.open()
while True:
    # Variablen loeschen
	Checksum = 0
	Checksum_Day = 0
	ID = ""
	# signal read
	signal = UART.read()
	# Is transfer start signaled??
	if signal == Startflag:
	    # put IDs togethern
		for Counter in range(13):
			signal = UART.read()
			ID = ID + str(signal)
		# Remove endflag from string.
		ID = ID.replace(Endflag, "" ) # Checksum calculation
		for I in range(0, 9, 2):
			Checksum = Checksum ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
		Checksum = hex(Checksum)
		# Filter out day
		Day = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0) 
                Day = hex(Tag)
		# Output data
		print "------------------------------------------"
		print "Record: ", ID
		print "Day: ", Day
		print "ID: ", ID[4:10], " - ", int(ID[4:10], 16)
		print "Checksum: ", Checksum
		print "------------------------------------------"
