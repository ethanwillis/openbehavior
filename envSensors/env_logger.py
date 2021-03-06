'''
	Author: Ethan Willis, Hao Chen
	Description: This program will log temperature, humidity, and barometric pressure
	and luminosity to a log file with a given frequency.
        The seonsor are MCP9808 for temperature, HTU21DF for humidity, MPL3115A2 for  
        barometric pressure, TSL2561 for luminosity. These are all connected using 
        the I2C protocol. 
	
	As well log times are recorded using the Adafruit DS-1307 Real Time Clock. System time is synchronized using this clock at device startup so that the system clock can be used.
		
	The log will have the following structure per entry.
	"date\ttime\ttemperature (C)\thumidity(%)\tbarometric pressure (hPa)\tLuminosity (Lux)\n"

	Usage:
		python env_logger.py
'''
import time
from time import strftime
import datetime
import HTU21DF
import sys
import MPL3115A2
import TSL2561
import Adafruit_MCP9808.MCP9808 as MCP9808
from multiprocessing import Process, Lock

tempsensor = MCP9808.MCP9808()
tempsensor.begin()
LightSensor = TSL2561.Adafruit_TSL2561()
LightSensor.enableAutoGain(True)
HTU21DF.htu_reset
  

'''
	Writes data to the logfile located at the location specified
	by the filename variable.
'''
def write_to_log(filename, data):
	with open(filename, "a") as logfile:
		datastring = str(data[0]) + "\t" + str(data[1]) + "\t" + str(data[2]) + "\t" + str(data[3]) + "\t" + str(data[4])+"\n"
		logfile.write(datastring)
		print datastring

'''
	Reads light levels from the light sensor
'''
def readLux():
	count=0
	luxTotal=0
	while True:
 		if (count <=100):
				 luxTotal=LightSensor.calculateLux() + luxTotal 
 				 count+=1
 		else:
     		 lux=round(luxTotal/100)
    	 	 break
	return lux


''' 
    This function reads and logs all of our sensor data
'''
def sensorReadingProcess(logfileLock, filename, sleeptime):
    while True:
        # reset sensor and collect data for next log entry.
        # TODO: Make this section of code resistant to hardware failures by inserting "nil" values for missing data when appropriate
	temp = tempsensor.readTempC()
	humidity = HTU21DF.read_humidity()
	tempPres = MPL3115A2.pressure()
        lux = readLux()
        ## calculate average lux for 100 readings
    	datetime = strftime("%Y-%m-%d\t%H:%M:%S") 
	data = [datetime, temp, humidity, tempPres[1], lux]
	
	# save new data entry, blocking I/O operation
        logfileLock.acquire()
	write_to_log(filename, data)
        logfileLock.release()
    	# sleep until ready to collect next measurements.
	time.sleep(sleeptime)

''' 
    This function copies our current logfile to USB storage
    devices that are attached to the system.

    @param sleeptime - The sleeptime parameter determines
    how long to wait between checking for new USB devices.
'''
def usbLoggerProcess(logfileLock, sleeptime=2):
    while True:
        # TODO: Implement getting usb attched and mounting it and whatnot
        time.sleep(sleeptime)

'''
	Collects environmental data on the time period
	specified by the sleeptime variable.
'''
def prog(filename="/home/pi/behaviorRoomEnv.log", sleeptime=30):
    logfileLock = Lock()
    sensorP = Process(target=sensorReadingProcess, args=(logfileLock, filename, sleeptime))
    #usbLogP = Process(target=usbLoggerProcess, args=())
    sensorP.start()
    #usbLogP.start()

prog()

