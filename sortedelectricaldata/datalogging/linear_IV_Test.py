from MachineCode import SR830
import numpy as np
import time
import os
from MachineCode.Keithley2400 import Keithley2400
import time

######################
# Sweep parameters
stepV = .1      #size of incriment increase in mV
minV = .1       # starting voltage in mV
maxV = .5       #final voltage to reach in mV
speed = 1       #time it takes to move up a step (in seconds)
trig = (maxV - minV)/stepV
#######################

timeStamp = str(time.time())[:10]

startTime = time.time()

keith = Keithley2400('COM10')

keith.reset()
keith.beeperOff()
keith.setComplianceCurrent()
keith.sendValue(":SOUR:FUNC VOLT")
keith.sendValue(":SENS:FUNC 'CURR'")
keith.sendValue(":SOUR:VOLT:START " + str(minV)+ "E-3")
keith.sendValue(":SOUR:VOLT:STOP " + str(maxV) + "E-3")
keith.sendValue(":SOUR:VOLT:STEP " + str(stepV) + "E-3")
keith.sendValue(":SOUR:VOLT:MODE SWE")
keith.sendValue(":SOUR:SWE:RANG AUTO")
keith.sendValue(":SOUR:SWE:SPAC LIN")
keith.sendValue(":TRIG:COUN " + str(trig))
keith.sendValue(":SOUR:DEL " + str(speed))
keith.sendValue(":SOUR:SWE:DIR UP")
keith.sendValue(":SOUR:SWE:CAB EARL")
keith.sendValue(":OUTP ON")
print(keith.readValue(":READ?"))
keith.sendValue(":OUTP OFF")