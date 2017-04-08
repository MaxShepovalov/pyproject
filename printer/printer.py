MAXX = 1000.0 #mm
MAXY = 1000.0 #mm
XSCALE = 0.01  #mm
YSCALE = 0.01  #mm

import math
import matplotlib.pyplot as plt
from random import random as rand

def snaptogrid(fx,fy):
	x = XSCALE * round(fx / XSCALE)
	y = YSCALE * round(fy / YSCALE)
	return (x,y)

def func(s):
	#return (0.01*rand(),0.01*rand())
	return (s/10.0, 3.0*(s/10.0))
	#return (math.cos(s),math.sin(s))

curX = 0
curY = 0
traceX = [curX]
traceY = [curY]
traceX2 = [0]
traceY2 = [0]
traceX2[0], traceY2[0] = snaptogrid(curX, curY)
for i in range(20):
	nX, nY = func(i/20.0)
	cnX, cnY = snaptogrid(nX, nY)
	dx = round(cnX - curX, 2)
	dy = round(cnY - curY, 2)
	curX = cnX
	curY = cnY
	traceX.append(nX)
	traceY.append(nY)
	traceX2.append(cnX)
	traceY2.append(cnY)
	print str((nX,nY))+" -> "+str((cnX,cnY))+" -> d"+str((dx,dy))

plt.plot(traceX, traceY, "r", traceX2, traceY2, "b")

plt.show()