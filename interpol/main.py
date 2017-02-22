import time
from random import random as rand
import matplotlib.pyplot as plt
import math
import sys
printf = sys.stdout.write

char_flag = "|"
char_up = "\\"
char_dwn = "/"
char_path = " "

class sequence:
	def __init__(self, hz, arr):
		self.freq = hz
		self.data = arr

#makes new sequence with higher frequency
def interpol(seq, new_hz):
	B = sequence(new_hz, [])
#if seq.freq >= new_hz:
#	print "new frequency should be higer than " + str(seq.freq)
#else:
	#loop thru array
	time_val_inp = 1.0/seq.freq
	time_val_out = 1.0/new_hz
	cur_time = 0
	finish = time_val_inp * (len(seq.data))
	#print "finish: "+str(time_val_inp)+" * "+str(len(seq.data))+" = "+str(finish)
	while cur_time <= finish:
		ind = int(cur_time/time_val_inp)
		x_loc = cur_time % time_val_inp
		y1 = 0
		if ind in range(len(seq.data)):
			y1 = float(seq.data[ind])
		else:
			print "index "+str(ind)+" out of range["+str(len(seq.data))+"]"
			break
		y2 = y1
		if ind+1 in range(len(seq.data)):
			y2 = float(seq.data[ind+1])
		out = (y2 - y1) * x_loc / time_val_inp + y1
		B.data.append(out)
		cur_time += time_val_out
	return B

def show(seq, show_freq):
	m = 0
	period = 1.0 / show_freq
	last = None
	curtime = 0
	finish = (len(seq.data)-1.0) / seq.freq
	while curtime <= finish:
	#for k in range(len(seq.data)):
		k = int(curtime * seq.freq)
		if k not in range(len(seq.data)):
			k = len(seq.data)-1
		line = str(curtime)[:6]
		left = 6 - len(line)
		line += str("      ")[:left]
		line += "  " + str(seq.data[k])[:3]
		left = 12 - len(line)
		line += str("            ")[:left]
		line += " >"
		for i in range(int(seq.data[k])):
			line += char_path
		if last:
			if last < seq.data[k]:
				line += char_up
			elif last > seq.data[k]:
				line += char_dwn
			else:
				line += char_flag
		else:
			line += char_flag
		#printf(str(seq.freq) + "  " +line)
		line = str(seq.freq) + " " + line
		if m < len(line):
			m = len(line)
		printf(line)
		sys.stdout.flush()
		last = seq.data[k]
		time.sleep(period)
		printf("\r")
		for i in range(m):
			printf(" ")
		printf("\r")
		curtime += period
	print "\n"+str(seq.freq)+" done"

def rand_seq(freq, start, size):
	val = start
	out = sequence(freq, [])
	for i in range(size):
		out.data.append(int(val))
		val += (rand()-0.5) * start
		if val < 0:
			val += 2*start
		if val > 2*start:
			val -= 2*start
	return out

def sine_seq(freq, sfreq, size):
	out = sequence(freq, [])
	for i in range(size):
		val = 10 + 5 * math.sin(i*sfreq*math.pi/freq)
		out.data.append(val)
	return out

def show_graph(seq_arr):
	for seq in seq_arr:
		#prepare Y(x) array
		length = len(seq.data)
		dt = 1.0 / seq.freq
		ty = [seq.data[0]]
		last = seq.data[0]
		tx = [0.0]
		for i in range(length):
			if seq.data[i]!=last:
				tx.append(i * dt)
				ty.append(last)
				tx.append(i * dt)
				ty.append(seq.data[i])
				last = seq.data[i]
		#print("x["+str(len(tx))+"] , y["+str(len(ty))+"]")
		#apply array to plot
		#print("\n"+str(seq.freq)+"\nx:"+str(tx)+"\ny:"+str(ty))
		plt.plot(tx, ty)
	plt.show()

#A = sequence(8, [3,10,30,5,100,90,80,5])
#A = rand_seq(120, 20, 100)
A = sine_seq(240, 2, 400)
B = interpol(A, 13)
C = interpol(B, 240)
#D = interpol(C, 2)
TV_freq = 60
#print str(A.freq)+": " + str(A.data)
#print str(B.freq)+": " + str(B.data)
#print str(C.freq)+": " + str(C.data)
#print str(D.freq)+": " + str(D.data)

show(A,TV_freq)
show(B,TV_freq)
show(C,TV_freq)
#show(D,TV_freq)

#show_graph([A])
#show_graph([A,B])
show_graph([A,B,C])
#show_graph([A,B,C,D])