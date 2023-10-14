import pyvisa as visa
import matplotlib.pyplot as plt
import time
import numpy as np

#fn_gen = rm.open_resource("ASRL10::INSTR")
#lia = rm.open_resource("GPIB0::8::INSTR")
#print(lia.query("*IDN?"))

rm = visa.ResourceManager()
lia = rm.open_resource("GPIB0::8::INSTR")
print(lia.query("OUTP?3"))

freq_array = np.concatenate((np.linspace(10, 1e5, 50), np.logspace(1, 5, 40)))
r_array = []
new_freq_array = []

for i in range(len(freq_array)):
    freq_array[i] = int(freq_array[i])

for f in freq_array:
    lia.write("FREQ"+str(f)) 
     
    for i in range(10):
        time.sleep(1/f*3)  
        time.sleep(.1)
        r_array += [lia.query("OUTP?3")]
        new_freq_array += [f]
        




import pandas as pd
df = pd.DataFrame()
df['Frequency'] = new_freq_array
df["Voltage"] = r_array
print(r_array[1])

from pathlib import Path  
filepath = Path('56K_filter_x.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)  