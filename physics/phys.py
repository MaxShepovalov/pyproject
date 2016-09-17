import math
#constants
ITERATE = 10000 # number of iteration to calculate
IPS	= 1000 		# number of iterations per second
g = 9.8			# gravity

path = ""
doLog = True
def log_path(x,y):
	global path
	if doLog:
		path += "%f,%f\n" % (x, y)

def log_path(obj_list):
	global path
	if doLog:
		if path=="":
			for num in range(0,len(obj_list)):
				path += "X %d   ,Y %d      ,," % (num,num)
						#0.000000,0.000000
			path += "\n"
		for obj in obj_list:
			path += "%f,%f,," % (obj.Px, obj.Py)
		path += "\n"

FILE = "output.csv"
def safeGraph():
	if doLog:
		f = open(FILE, 'w')
		f.write(path)
		f.close()
	else:
		print("position tracking is OFF. change doLog to True for saving to csv")

#object
chart = ["nobody", 0]
class Pbody:
	def __init__(self, name):
		self.name = name
		self.Px = 0.0 # m
		self.Py = 0.0 # m
		self.Vx = 0.0 # m/s
		self.Vy = 0.0 # m/s
		self.flying = True

	def set_V(self, x, y):
		self.Vx = float(x)
		self.Vy = float(y)

	def set_P(self, x, y):
		self.Px = float(x)
		self.Py = float(y)

	def report(self):
		global chart
		chart.append(self.name)
		chart.append(self.Px)
		self.flying = False

	def applyV(self):
		NewX = float(self.Px + self.Vx / IPS)
		NewY = float(self.Py + self.Vy / IPS)
		NewVX = float(self.Vx)
		NewVY = float(self.Vy - g / IPS)

		if NewY < 0:
			self.report()
			NewY = 0
			NewVY = (-0.5)*NewVY
		if self.flying:
			self.Px = NewX
			self.Py = NewY
			self.Vx = NewVX
			self.Vy = NewVY

	def set_Vangle(self, ang):
		FullV = pow( pow(self.Vx,2)+pow(self.Vy,2) , 0.5)
		self.Vx = FullV * math.cos(math.radians(ang))
		self.Vy = FullV * math.sin(math.radians(ang))

#start velosity
Boxes = []
def addBox(speed, ang):
	Boxes.append(Pbody("%d" % ang))
	Boxes[len(Boxes)-1].set_P(0,0)
	Boxes[len(Boxes)-1].set_V(speed,0)
	Boxes[len(Boxes)-1].set_Vangle(ang)

for i in range(0,100):
	addBox(3.0, 44+i/100)
#addBox(3.0, 44)
#addBox(3.0, 45)	

log_path(Boxes)

ITER_M = ITERATE
while ITERATE > 0:
	contin = False
	for obj in Boxes:
		if obj.flying:
			contin = True
		obj.applyV()
	if not contin:
		print("all boxes fell on ground. exiting")
		break
	log_path(Boxes)
	perc = 100 * (1 - float(ITERATE) / float(ITER_M))
	if perc % 10 == 0:
		print("%d%c" % (int(perc), chr(37)))
	ITERATE -= 1

#check winner
num = 1
maxN = 1
while num < len(chart):
	if chart[maxN] < chart[num]:
		maxN = num
	num += 2
print("%s on %f" % (chart[maxN-1], chart[maxN]))
print("%d boxes. Taken %d iterations" % (len(Boxes), ITER_M - ITERATE))

safeGraph()