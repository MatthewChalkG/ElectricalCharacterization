from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import time

fn = "hallDCBias.txt"
startTime = time.time() 

try:
    os.remove(fn)
except:
    pass

LIA = SR2124.SR2124('COM5')
SPD3303x = spd3303x()
f = open(fn, "a")
f.write("t,i,x,y,r,theta,xK,tc, therm, dc\n")
f.close()
SPD3303x.set_voltage(5)
SPD3303x.set_current(0)

SPD3303x.set_current(.05, channel = 2) # safety control
SPD3303x.set_voltage(0, channel = 2) # safety control


#keith = keithley2110tc(1)
relay = Arduino("COM3")

for dc in np.linspace(0, 12, 37):
    SPD3303x.set_voltage(dc, channel = 2)

    for direction in [1, -1]:
        SPD3303x.set_current(0)
        time.sleep(1)
        if direction == 1:
            relay.enable_P1()
        else:
            relay.enable_P2()
        time.sleep(.5)


        i = 3.2
        
        SPD3303x.set_current(i)
        time.sleep(.5)
        x, y, r, theta =LIA.readall() 
        lockstatus = LIA.readlock()
        # xK = keith.voltage() * LIA.readsens()/10
        xK = 0
        # tc = keith.thermoCoupleTemp()
        tc = 0
        #therm = keith.resistance()
        therm = 0
        #temp = 0
        f = open(fn, "a")
        t = time.time() # - startTime
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}".format(t-startTime, i*direction, x, y, r, theta, xK, tc, therm, dc))
        f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i*direction, x, y, r, theta, xK, tc, therm, dc) + "\n")
        f.close()

    """i = 0
    SPD3303x.set_current(i)
    time.sleep(3)
    x, y, r, theta =LIA.readall() 
    lockstatus = LIA.readlock()
    xK = keith.voltage()
    f = open(fn, "a")

    print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i, x, y, r, theta, xK))
    f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
    f.close()"""
    
SPD3303x.set_current(0)

    
