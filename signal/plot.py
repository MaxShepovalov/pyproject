import matplotlib.pyplot as plt
import math


gm = 0.00122
r2 = 5671.0
r = range(30,120)
for i in range(len(r)):
	r[i] *= 100.0

p = []

for i in range(len(r)):
	p.append(gm*(r2*r[i])/(r[i]+r2))

plt.plot(r,p)
plt.show()