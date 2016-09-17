import math
#test of sound force

#imitation (in time) of sound sense by friquency


#inportant points
# freq     sense
#  0 Hz		0
#  30 Hz    0.01
#  440 Hz 	1
#  18 kHz 	0.5
#  22 kHz	0
def getAmpFreqMod(freq):
	mod = 0.0
	#bass
	if int(freq) in range(0,440):
		mod = math.sqrt(freq / 440.0)
	#mid
	elif int(freq) in range(441,14000):
		mod = 1.0
	#high
	elif int(freq) in range(14000, 22000):
		mod = pow(abs(freq-18000.0),1.0/3)/30
		if freq > 18000.0:
			mod = 0.5 - mod
		else:
			mod = 0.5 + mod
	#outside
	else:
		mod = 0.0
	return mod

AFC = ""

dF = 1
fr = 0.0
while fr < 22000:
	print("fr = %f" % fr)
	AFC += "%f, %f\n" % (fr, getAmpFreqMod(fr))
	fr += dF

f = open("log_sound_freq.csv", 'w')
f.write(AFC)
f.close()
