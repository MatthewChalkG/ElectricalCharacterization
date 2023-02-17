from MachineCode.SR2124 import SR2124
from MachineCode.SR830 import SR830
import time
import serial
import numpy as np


SR2 = SR2124('COM3')
SR8 = SR830('COM4')

x2, y2, r2, theta2 = SR2.readall()

print(x2,y2,r2,theta2)

f2 = 92.16
v2 = 10**-1 # Minimum v necessary to get full range of DC bias: Why: bias values can be set up to 1000 the reference amplitude
b2 = 0
steps = 20

SR2.setv(v2)
SR2.setf(f2)
SR2.setb(0)
SR2.onb(1)



flog = open("DiffRes.txt", "w")
flog.write("f2,b2,v2,x2,y2,r2,theta2,x8,y8,r8, theta8 \n")



for b2 in np.linspace(0, 10, steps):
    b2 =  round(b2,2) # lock in wont take values with more decimal places then it holds
    
    SR2.setb(b2)
    time.sleep(1.5)
    

    x2, y2, r2, theta2 = SR2.readall()
    x8, y8, r8, theta8 = SR8.readall()

    print()
    print(f2,b2,v2,x2,y2,r2,theta2, x8, y8, r8, theta8)


    flog.write(str(f2)+","+str(b2) + ',' +str(v2)+","+str(x2)+","+str(y2)+","+str(r2)+","+str(theta2)+','+str(x8)+','+str(y8)+','+str(r8)+','+str(theta8)+"\n")

for b2 in np.linspace(10, 0, steps):
    b2 =  round(b2,2) # lock in wont take values with more decimal places then it holds
    
    SR2.setb(b2)
    time.sleep(1)
    

    x2, y2, r2, theta2 = SR2.readall()
    x8, y8, r8, theta8 = SR8.readall()

    print()
    print(f2,b2,v2,x2,y2,r2,theta2)


    flog.write(str(f2)+","+str(b2) + ',' +str(v2)+","+str(x2)+","+str(y2)+","+str(r2)+","+str(theta2)+','+str(x8)+','+str(y8)+','+str(r8)+','+str(theta8)+"\n")

for b2 in np.linspace(0, -10, steps):
    b2 =  round(b2,2) # lock in wont take values with more decimal places then it holds
    
    SR2.setb(b2)
    time.sleep(1)
    

    x2, y2, r2, theta2 = SR2.readall()
    x8, y8, r8, theta8 = SR8.readall()

    print()
    print(f2,b2,v2,x2,y2,r2,theta2)


    flog.write(str(f2)+","+str(b2) + ',' +str(v2)+","+str(x2)+","+str(y2)+","+str(r2)+","+str(theta2)+','+str(x8)+','+str(y8)+','+str(r8)+','+str(theta8)+"\n")

for b2 in np.linspace(-10, 0, steps):
    b2 =  round(b2,2) # lock in wont take values with more decimal places then it holds
    
    SR2.setb(b2)
    time.sleep(1)
    

    x2, y2, r2, theta2 = SR2.readall()
    x8, y8, r8, theta8 = SR8.readall()

    print()
    print(f2,b2,v2,x2,y2,r2,theta2)


    flog.write(str(f2)+","+str(b2) + ',' +str(v2)+","+str(x2)+","+str(y2)+","+str(r2)+","+str(theta2)+','+str(x8)+','+str(y8)+','+str(r8)+','+str(theta8)+"\n")



flog.close()
