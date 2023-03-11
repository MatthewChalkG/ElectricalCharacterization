from  MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino


timeStamp = str(time.time())[3:10]
fn = "hallVoltageSweep{}.txt".format(timeStamp)
f = open("Data/"+fn, "a")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc\n")
f.close()

LIA = SR2124.SR2124('COM5')
SPD3303x = spd3303x()
relay = Arduino("COM3")

SPD3303x.set_voltage(5)
SPD3303x.set_current(0)


while True:
    for direction in [(0, 3.2), (3.2, 0), (0, -3.2), (-3.2,0)]: 
        for i in np.linspace(direction[0], direction[1], 20):
            if direction[0] > -1 and direction[1] > -1:
                relay.enable_P1()
            else:
                relay.enable_P2()
            
            SPD3303x.set_current(abs(i))
            time.sleep(.7)
            x, y, r, theta = LIA.readall() 

            lockstatus = LIA.readlock()
            xK = 0
            f = open("Data/"+fn, "a")

            print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i, x, y, r, theta, xK))
            f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
            f.close()


SPD3303x.set_current(0)

    
