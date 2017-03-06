import matplotlib.pyplot as plt
from random import random as raw_rand

def rand(med,maxdisp):
	return maxdisp*((raw_rand()%100)/100.0-0.00495)+med
def test():
	median = 0
	for i in range(1000):
		median += (rand(0,1)-median)/(i+1)
	return median

def aver_speed():
	aver = 0.0
	if len(creatures)>0:
		for c in creatures:
			aver += c.speed
		aver /= len(creatures)
	return aver

glob_num = 0
class Ork:
	def __init__(self):
		global glob_num
		self.speed = rand(aver_speed(), 20)
		self.stop = rand(0, 20)
		self.number = glob_num
		glob_num += 1
	def evolve(self):
		self.speed += rand(0, 10)
		self.stop += rand(-2.5, 2.5)
	def run(self):
		return self.speed+self.stop

DES_NUM = 100
creatures = []
def fill():
	global plotMax
	global plotSpdMin
	global plotSpdMax
	global plotStpMax
	global plotStpMin
	plotMax = []
	plotSpdMin = []
	plotSpdMax = []
	plotStpMax = []
	plotStpMin = []
	num = DES_NUM - len(creatures)
	for i in range(num):
		creatures.append(Ork())

def findmin():
	min = creatures[0].run()
	k = 0
	for i in range(len(creatures)):
		if creatures[i].run()<min:
			k = i
			min = creatures[i].run()
	return k

def sort():
	global creatures
	new_arr = []
	while len(creatures)>0:
		minP = findmin()
		new_arr.append(creatures[minP])
		part1 = creatures[:minP]
		part2 = creatures[minP+1:]
		creatures = part1 + part2
	creatures = []
	for c in new_arr:
		creatures.append(c)

def cycle():
	for i in range(DES_NUM):
		if i in range(len(creatures)):
			creatures[i].evolve()
		else:
			creatures.append(Ork())

def cut():
	global creatures
	deadline = len(creatures)/2
	creatures = creatures[deadline:]

def show():
	print "Average speed: " + str(aver_speed())
	print "number, runs, speed, stop"
	for c in creatures:
		print("%d, %f, %f, %f" % (c.number, c.run(), c.speed, c.stop))
	print "Prepairing plots..."
	plt.subplot(211)
	plt.plot(plotMax)
	plt.subplot(212)
	plt.plot(plotSpdMax, 'r', plotSpdMin, 'r', plotStpMax, 'b', plotStpMin, 'b')
	plt.show()

def plotinfo():
	MaxMove = creatures[0].run()
	MaxSpeed = creatures[0].speed
	MaxStop = creatures[0].stop
	MinSpeed = creatures[0].speed
	MinStop = creatures[0].stop
	for i in creatures:
		if MaxMove<i.run():
			MaxMove = i.run()
		if MaxSpeed<i.speed:
			MaxSpeed=i.speed
		if MaxStop<i.stop:
			MaxStop=i.stop
		if MinSpeed>i.speed:
			MinSpeed=i.speed
		if MinStop>i.stop:
			MinStop=i.stop
	plotMax.append(MaxMove)
	plotSpdMin.append(MinSpeed)
	plotSpdMax.append(MaxSpeed)
	plotStpMax.append(MaxStop)
	plotStpMin.append(MinStop)

def do(Ncyc):
	for i in range(Ncyc):
		sort()
		plotinfo()
		cut()
		cycle()
	show()

#plot info
plotMax = []
plotSpdMin = []
plotSpdMax = []
plotStpMax = []
plotStpMin = []
