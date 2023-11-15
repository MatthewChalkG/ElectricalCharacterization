import pyvisa as visa
import MachineCode.SR830 as SR830
import time

rm = visa.ResourceManager()
temp = rm.open_resource("GPIB::1::INSTR")


startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "temp_scan{}.txt".format(timeStamp)

f = open("Data"+fn+"laser, 12b", "w+")
f.write("t,x,y,r,theta,temp_val\n")
f.close()


LIA = rm.open_resource("GPIB::8::INSTR")

while True:
    temp_str = temp.query("")
    temp_val = ""
    for i in temp_str:
        if i != " ":
            temp_val += i
        if temp_val != "" and i == " ":
            break


    x = float(LIA.query("OUTP?1"))
    y = float(LIA.query("OUTP?2"))
    r = float(LIA.query("OUTP?3"))
    theta = float(LIA.query("OUTP?4"))

    f = open("Data/"+fn, "a")
    t = time.time() # - startTime
    print("t: {}, x: {}, y: {}, r: {}, theta: {}, temp: {}".format(t-startTime, x, y, r, theta, temp_val))
    f.write("{}, {}, {}, {}, {}, {}".format(t, x, y, r, theta, temp_val) + "\n")
    f.close()

    time.sleep(1)


    print(float(temp_val))

