from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import time


timeStamp = str(time.time())[3:10]
fn = "resistivity{}.txt".format(timeStamp)

f = open("Data/"+fn, "a")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc\n")
f.close()

startTime = time.time() 
biasD = -1

LIA = SR2124.SR2124('COM5')
SPD3303x = spd3303x()
relay = Arduino("COM3")


SPD3303x.set_voltage(5)
SPD3303x.set_current(0)

SPD3303x.set_current(.25, channel = 2) # safety control
SPD3303x.set_voltage(0, channel = 2) # safety control

for dc in np.linspace(0,30, 151):
    SPD3303x.set_voltage(dc, channel = 2)
    time.sleep(1.5)
    LIA.overloadDetect()


    x, y, r, theta =LIA.readall() 
    lockstatus = LIA.readlock()
    # xK = keith.voltage() * LIA.readsens()/10
    xK = 0
    # tc = keith.thermoCoupleTemp()
    i = 0
    tc = 0
    #therm = keith.resistance()
    therm = 0
    #temp = 0
    f = open("Data/"+fn, "a")
    t = time.time() # - startTime
    print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm, dc*biasD))
    f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, xK, tc, therm, dc*biasD) + "\n")
    f.close()

for dc in np.linspace(30,0, 151):
    SPD3303x.set_voltage(dc, channel = 2)
    time.sleep(1.5)
    LIA.overloadDetect()


    x, y, r, theta =LIA.readall() 
    lockstatus = LIA.readlock()
    # xK = keith.voltage() * LIA.readsens()/10
    xK = 0
    # tc = keith.thermoCoupleTemp()
    i = 0
    tc = 0
    #therm = keith.resistance()
    therm = 0
    #temp = 0
    f = open("Data/"+fn, "a")
    t = time.time() # - startTime
    print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm, dc*biasD))
    f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, xK, tc, therm, dc*biasD) + "\n")
    f.close()



    
#SPD3303x.set_voltage(0, channel = 2)
#SPD3303x.set_current(0, channel = 2)    

    

LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()

def voltage_stepDown(inst, channel):
    current_voltage = inst.read_voltage(channel)
    #while 