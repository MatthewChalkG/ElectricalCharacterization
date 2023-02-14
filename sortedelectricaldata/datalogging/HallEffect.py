import SR2124
from SPD3303X import spd3303x
import numpy as np
import time
import os
from keithley2110tc import keithley2110tc
from arduinorelayinterface import Arduino

fn = "hallVoltage.txt"
os.remove(fn)
LIA = SR2124.SR2124('COM9')
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
        for i in np.linspace(0, 3.2*direction, 20):
            if direction == 1:
                relay.enable_P1()
            else:
                relay.enable_P2()
            
            SPD3303x.set_current(i)
            time.sleep(1)
            x, y, r, theta =LIA.readall() 
            lockstatus = LIA.readlock()
            xK = keith.voltage()
            f = open(fn, "a")

            print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i, x, y, r, theta, xK))
            f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
            f.close()

        for i in np.linspace(3.2*direction, 0, 20):
            if direction == 1:
                relay.enable_P1()
            else:
                relay.enable_P2()
            SPD3303x.set_current(i)
            time.sleep(1)
            x, y, r, theta =LIA.readall() 
            lockstatus = LIA.readlock()
            xK = keith.voltage()
            f = open(fn, "a")

            print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i, x, y, r, theta, xK))
            f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
            f.close()

SPD3303x.set_current(0)

    
