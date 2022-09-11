import matplotlib.pyplot as plt
import pandas as pd

resistorRes = 10*10**3
data = pd.read_csv("DiffRes.txt")

voltAcrossResistor = abs(data["x2"])

dI = voltAcrossResistor/resistorRes
dV = abs(data["x8"])

bias = data["b"]
R = dV/dI

plt.scatter(bias, R)
plt.show()


