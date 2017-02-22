from random import random as rand

#		  0   1   2   3   4   5   6   7    8   9
image = ["_",".",",","-","~","=","'","\"","^","`"]
# 		   01   5    10      17
grease1 = "           _.,-~:+=#"
grease2 = " _.,-~:+=###########"

def ruler(leng):
	outp = ""
	for i in range(leng):
		if i%10 == 0:
			outp += " "
		else:
			outp += str(i%10)
	return outp

def draw(line):
	outp = ""
	for i in line:
		outp += image[i]
	return outp

def fill(gline):
	outp = "gr   "
	for i in gline:
		outp += grease1[i]
	outp += "\ngr   "
	for i in gline:
		outp += grease2[i]
	return outp

def show_contact(gline):
	outp = ""
	for i in range(size):
		if gline[i] == 0:
			outp += "^"
		else:
			outp += " "
	return outp

size = 32
thr = 0.5

sink = []
sink_off = 0
cpu = []

for i in range(size):
	s_v = rand() - thr
	if s_v > 0:
		sink.append(int(10*s_v))
	else:
		sink.append(5)
	c_v = rand() - thr
	if c_v > 0:
		cpu.append(int(10*c_v))
	else:
		cpu.append(5)

#move sink lower
reach = False
while not reach:
	for i in range(size):
		if 9 + sink[i] + sink_off == cpu[i]:
			reach = True
			print "Heat sink touch CPU on " + str(i)
	if not reach:
		sink_off-=1

delt = []
for i in range(size):
	delt.append(9+sink[i]+sink_off-cpu[i])

print "sink " + draw(sink)
print fill(delt)
print "cpu  " + draw(cpu)

print "     " + show_contact(delt)
print "     " + ruler(size)

all_d = 0
for i in range(size):
	all_d += delt[i]

print "averall therm resistance " + str(all_d)

