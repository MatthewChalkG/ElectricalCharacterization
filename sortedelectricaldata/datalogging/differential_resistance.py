from SR2124 import SR2124
import time
import serial
import numpy as np


LIA = SR2124('COM4')
    
x, y, r, theta = LIA.readall()
#BION
print(x,y,r,theta)

f = 10.123
v = 10**-2 # Minimum v necessary to get full range of DC bias: Why: bias values can be set up to 1000 the reference amplitude
b = 0

LIA.setv(v)
LIA.setf(f)
LIA.setb(0)
LIA.onb(1)

flog = open("DiffRes.txt", "w")
flog.write("f,b,v,x,y,r, theta\n")



for b in np.linspace(0, 10, 40):
    b =  round(b,2) # lock in wont take values with more decimal places then it holds
    
    LIA.setb(b)
    time.sleep(1)
    

    x, y, r, theta = LIA.readall()
    print()
    print(f,b,v,x,y,r,theta)


    flog.write(str(f)+","+str(b) + ',' +str(v)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")

for b in np.linspace(10, 0, 40):
    b =  round(b,2) # lock in wont take values with more decimal places then it holds
    
    LIA.setb(b)
    time.sleep(1)
    

    x, y, r, theta = LIA.readall()
    print()
    print(f,b,v,x,y,r,theta)


    flog.write(str(f)+","+str(b) + ',' +str(v)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")


flog.close()
