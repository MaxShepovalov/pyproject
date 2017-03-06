import math
import sys
import matplotlib.pyplot as plt

def sinc(x):
	if x==0:
		return 0
	return math.sin(x)/x

class fir:
	def __init__(self, depth, params):
		self.depth = depth
		self.coef = params
		self.coef.reverse()

	def run(self, signal):
		delay = [0]*self.depth + signal + [0]*self.depth
		output = [0]*len(delay)
		symb = ['-','\\','|','/']
		print "FIR: !"
		for i in range(len(output)):
			for j in range(self.depth):
				if i+j in range(len(delay)):
					output[i] += self.coef[j]*delay[i+j]
					sys.stdout.write("FIR: "+symb[(i+j)%3]+"\r")
		print "FIR: done"
		return output

f_edge = 100.0
scale = 18
length = 100
time_scale = 0.1

#params = []
#for i in range(scale):
#	params.append(2*f_edge*sinc(2*f_edge*i*time_scale))
	#params.append(1.0/(scale+1.0))
params = [
	0.0017106420472549515,
	0.0004260001201471347,
	-0.010448967060907076,
	-0.03284676688553758,
	-0.05222287470220172,
	-0.03905038327818816,
	0.02983474981723218,
	0.14402898137066716,
	0.2539179504433725,
	0.29951664215186996,
	0.2539179504433725,
	0.14402898137066716,
	0.02983474981723218,
	-0.03905038327818816,
	-0.05222287470220172,
	-0.03284676688553758,
	-0.010448967060907076,
	0.0004260001201471347,
	0.0017106420472549515
	]
scale = len(params)

line = []
for i in range(length):
	#line.append(math.sin(time_scale*i)+0.1*math.sin(time_scale*1000*i/(1+i)))
	line.append(math.sin(time_scale*200*i))
	#line.append(0.0)
#line[0] = 1.0

f = fir(scale, params)
out = f.run(line)

high = []
for i in range(len(line)):
	high.append(line[i]-out[i])

plt.plot(range(len(line)), line, 'r--', range(len(out)), out, 'b')
plt.show()