import time
import serial
import numpy as np

class SR2124:
    # configure the serial connections
    def __init__(self, comport):
        self.ser = serial.Serial(
            port=comport,
            baudrate=9600
        )
        self.ser.close()
        self.ser.open()
        self.ser.isOpen()

    def readval(self, command, parse=True):
        #\r\n is for device terminators set to CR LF
        self.ser.write((command+'\r\n').encode('utf-8'))
        #wait one second before reading output.
        time.sleep(0.5)
        out=''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode('utf-8')
        if out != '':
            out=out.rstrip()
            if parse: return float(out)
            else: return out

    def readx(self):
        return self.readval("OUTX?")
    
    def ready(self):
        return self.readval("OUTY?")

    def readr(self):
        return self.readval("MAGI?")

    def readtheta(self):
        return self.readval("ATAN?")

    def readf(self):
        return self.readval("FREQ?")

    def readv(self):
        return self.readval("SLVL?")

    def readsens(self):
        return self.readval("SENS?")

    def readall(self):
        csv = [self.readx(), self.ready(), self.readr(), self.readtheta(), self.readsens()]
        try:
            x = float(csv[0])*float(csv[4])/10
            y = float(csv[1])*float(csv[4])/10
            r = float(csv[2])*float(csv[4])/10
            theta = float(csv[3])
        except:
            print('read error')
            x,y,r,theta = [0]*4
        return x,y,r,theta

    def readlock(self):
        lockbit = self.readval("LOCK?")
        print("UNLOCK STATUS",lockbit)
        return(lockbit)
        # 0: unlocked
        # 1: locked
        # 2: notpll (wut is this?)

    def setf(self, f):
        self.ser.write(("FREQ"+str(f)+'\r\n').encode('utf-8'))

    def setv(self, v):
        self.ser.write(("SLVL"+str(v)+'\r\n').encode('utf-8'))
    
    def setb(self, b):
        self.ser.write(("BIAS"+str(b)+'\r\n').encode('utf-8'))

    def onb(self, yn):
        self.ser.write(("BION"+str(yn)+'\r\n').encode('utf-8'))
    

