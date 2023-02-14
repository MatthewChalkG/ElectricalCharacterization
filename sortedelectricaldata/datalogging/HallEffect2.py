import SR2124
from SPD3303X import spd3303x
import numpy as np
import time
import os
from keithley2110tc import keithley2110tc
from arduinorelayinterface import Arduino
import time

fn = "hallVoltage.txt"
startTime = time.time() 

try:
    os.remove(fn)
except:
    pass
LIA = SR2124.SR2124('COM4')
SPD3303x = spd3303x()
f = open(fn, "a")
f.write("i,x,y,r,theta,xK\n")
f.close()
SPD3303x.set_voltage(5)
SPD3303x.set_current(0)
keith = keithley2110tc()
relay = Arduino("COM3")

while True:
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
        xK = keith.voltage()
        f = open(fn, "a")
        t = time.time() - startTime
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(t, i*direction, x, y, r, theta, xK))
        f.write("{}, {}, {}, {}, {}, {}, {}"+ "\n".format(t, i*direction, x, y, r, theta, xK))
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

    
