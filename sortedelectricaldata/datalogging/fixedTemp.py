from simple_pid import PID
import time
import matplotlib.pyplot as plt
from MachineCode.SPD3303X import spd3303x
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode import arduinorelayinterface
import sys


######################
# Sweep parameters
desiredTemp = 25
#######################

timeStamp = str(time.time())[:10]
fn = "fixedTemp{}.txt".format(timeStamp)
f = open("Data/tempControl/"+fn, "w+")
f.write("t,i,temp_desired,temp_tc\n")
f.close()

def main(desired_temp = desiredTemp, p= 0.5, i = .02 , d = 0): # i = .02
    supply = spd3303x(1)
    keithley = keithley2110tc(2)
    relays = arduinorelayinterface.Arduino('COM8')
    pid = PID(p, i, d, setpoint = desired_temp) 
    pid.output_limits = (0, 2) 
    supply.set_voltage(12, channel = 2)

    


    while True:
        if desired_temp < 22:
            heat = -1
            relays.enable_P1()
        else:
            heat = 1
            relays.enable_P2()

        tc_temp = keithley.thermoCoupleTemp()
        kill_function(tc_temp)
        

        pid.setpoint = desired_temp * heat
        current = pid(tc_temp*heat)

        supply.set_current(current, channel = 2)

        current_time = time.time()


        print("desired_temp = " + str(desired_temp), "current = " + str(current), "tc_temp = " +  str(tc_temp))

        f = open("Data/tempControl/"+fn, "a")
        f.write("{},{},{},{}\n".format(current_time, desired_temp, current, tc_temp))
        f.close()

        time.sleep(.6)


def kill_function(tc_temp):
    """ kills if temp above 70 C"""

    if tc_temp > 70:
        supply = spd3303x(1, channel = 2)
        supply.set_voltage(0, channel = 2)
        supply.set_current(0, channel = 2)
        print("temp above 70C")
        print("EXITING - TEMP > 70 C")
        sys.exit()

main()