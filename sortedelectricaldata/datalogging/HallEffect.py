import SR2124
from SPD3303X import spd3303x
import numpy as np
import time

fn = "hallVoltage.txt"

LIA = SR2124.SR2124('COM9')
SPD3303x = spd3303x()
f = open(fn, "a")
f.write("i,x,y,r,theta\n")
f.close()
SPD3303x.set_voltage(5)
SPD3303x.set_current(0)

for i in np.linspace(0, 3.2, 200):
    SPD3303x.set_current(i)
    time.sleep(2)
    x, y, r, theta =LIA.readall() 
    lockstatus = LIA.readlock()

    f = open(fn, "a")

    print("i: {}, x: {}, y: {}, r: {}, theta: {}".format(i, x, y, r, theta))
    f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + "\n")
    f.close()

    
