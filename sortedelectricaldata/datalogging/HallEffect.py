import MachineCode.SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino

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
    for direction in [(0, 3.2), (3.2, 0), (0, -3.2), (-3.2,0)]: 
        for i in np.linspace(direction[0], direction[1], 20):
            if direction[0] > -1 and direction[1] > -1:
                relay.enable_P1()
            else:
                relay.enable_P2()
            
            SPD3303x.set_current(abs(i))
            time.sleep(1)
            x, y, r, theta = LIA.readall() 

            lockstatus = LIA.readlock()
            xK = keith.voltage()
            f = open(fn, "a")

            print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, sens: {}".format(i, x, y, r, theta, xK))
            f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
            f.close()


SPD3303x.set_current(0)

    
