from SR830 import SR830
import time
import serial
import numpy as np

LIA = SR2124('COM1')

x, y, r, theta = LIA.readall()

print(x,y,r,theta)

LIA.setv(0)
LIA.setf(10)

flog = open("DiffRes.txt", "w")
flog.write("f,b,v,x,y,r, theta\n")
v = 10^-7

LIA.setv(v)
for d in (1, -1)
    for b in np.linspace(-10, 10, 200):
        b=b*d
        LIA.setf(f+0.123)
        LIA.setb(b)
        time.sleep(1)

        x, y, r, theta = LIA.readall()

        print(f,b,v,x,y,r,theta)


        flog.write(str(f)+","+str(b) + ',' +str(v)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")

flog.close()
