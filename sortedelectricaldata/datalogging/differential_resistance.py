from MachineCode.SR2124 import SR2124
from MachineCode.SR830 import SR830
import time
import serial
import numpy as np

######################
# Sweep parameters
f2 = 92.16
v2 = .1 # Minimum v necessary to get full range of DC bias: Why: bias values can be set up to 1000 the reference amplitude
steps = 20
maxV = 10 # max bias voltage
#######################


SR2.setv(v2)
SR2.setf(f2)
SR2.setb(0)
SR2.onb(1)


SR2124 = SR2124('COM3')
SR830 = SR830('COM4')


timeStamp = str(time.time())
fn = "differential_resistance_{}.txt".format(timeStamp)

f = open("Data/Differential_Resistance/"+fn, "a")
f.write("t,f2,b2,v2,x2,y2,r2,theta2,x8,y8,r8,theta8\n")
f.close()



a = [np.linspace(0, maxV, steps), np.linspace(maxV, 0, steps), np.linspace(0, -maxV, steps), np.linspace(-maxV, 0, steps)]

for sweepSpace in a:
    for bias in sweepSpace:
        bias =  round(bias, 2) # lock in wont take values with more decimal places then it holds
        
        SR2124.setb(bias)
        time.sleep(1.5)
        

        x2, y2, r2, theta2 = SR2.readall()
        x8, y8, r8, theta8 = SR8.readall()

        print(f2,b2,v2,x2,y2,r2,theta2, x8, y8, r8, theta8)
        t = time.time()
        f = open("Data/Differential_Resistance/"+fn, "a")
        f.write(("{},"*11 + '{}\n').format(t,f2,b2,v2,x2,y2,r2,theta2, x8, y8, r8, theta8))
        f.close()

