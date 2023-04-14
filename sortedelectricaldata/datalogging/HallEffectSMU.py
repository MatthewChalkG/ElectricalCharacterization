from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
from MachineCode.Keithley2400 import Keithley2400
import time

######################
# Sweep parameters
numPoints = 6
maxV = 200
minV = -200
#######################

timeStamp = str(time.time())[:10]
fn = "hallDCBiasSMU{}.txt".format(timeStamp)

f = open("Data/HallEffectDCBias/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc,i\n")
f.close()

startTime = time.time() 
biasD = -1

LIA = SR2124.SR2124('COM7')
keith = Keithley2400("COM10")
relay = Arduino("COM3")
SPD3303x1 = spd3303x() # sol curr

keith.slowIVMode()
keith.setComplianceCurrent(.001)# safety control
keith.setVoltage(0) # safety control
SPD3303x1.set_voltage(5)
SPD3303x1.set_current(0)

keith.outputOn()
sweepSpaceL = [[0, maxV, numPoints], [maxV, 0, numPoints], [0, minV, numPoints], [minV, 0, numPoints]]


for sweepSpaceParams in sweepSpaceL:
    sweepSpace = np.linspace(sweepSpaceParams[0], sweepSpaceParams[1], sweepSpaceParams[2])
    for dc in sweepSpace:
        keith.setVoltage(dc)
        time.sleep(2.5)
        LIA.overloadDetect()
        data = keith.read2()
        formattedData = data.decode().strip().split(',')
        trueGateDC = formattedData[0]
        trueGateI = formattedData[1]
        
        for direction in [1, -1, 1, -1, 1, -1]:
            SPD3303x1.set_current(0)
            time.sleep(1)
            if direction == 1:
                relay.enable_P1()
            else:
                relay.enable_P2()
            time.sleep(.5)


            i = 3.2
            
            SPD3303x1.set_current(i)
            

            time.sleep(1.2)
            x, y, r, theta =LIA.readall() 
            lockstatus = LIA.readlock()
            # xK = keith.voltage() * LIA.readsens()/10
            xK = 0
            # tc = keith.thermoCoupleTemp()
            tc = 0
            #therm = keith.resistance()
            therm = 0
            #temp = 0
            f = open("Data/HallEffectDCBias/"+fn, "a")
            t = time.time() # - startTime
            print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}, i: {}".format(t-startTime, i*direction, x, y, r, theta, xK, tc, therm, dc, i))
            f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i*direction, x, y, r, theta, xK, tc, therm, dc, i) + "\n")
            f.close()


keith.outputOff()
SPD3303x1.set_current(0)
SPD3303x1.set_voltage(0)

LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()