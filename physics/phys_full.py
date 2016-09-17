import math
#constants
ITERATE = 300 # number of iteration to calculate
IPS	= 100		# number of iterations per second
g = 9.8			# gravity

path = ""
doLog = True
def log_path_vel(obj):
	global path
	if doLog:
		if path=="":
			path += "X       ,Y       ,,Vel\n"
					#0.000000,0.000000,,0.000000
		path += "%f,%f,,%f\n" % (obj.Px, obj.Py, obj.getV())

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

FILE = "output_full.csv"
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
		self.maxY = 0.0 # m

	def set_V(self, x, y):
		self.Vx = float(x)
		self.Vy = float(y)

	def set_P(self, x, y):
		self.Px = float(x)
		self.Py = float(y)
		if self.Py > self.maxY:
			self.maxY = self.Py

	#def report(self):
	#	global chart
	#	chart.append(self.name)
	#	chart.append(self.Px)
	#	self.flying = False

	def applyV(self):
		NewX = float(self.Px + self.Vx / IPS)
		NewY = float(self.Py + self.Vy / IPS)
		NewVX = float(self.Vx)
		NewVY = float(self.Vy - g / IPS)

		if NewY < 0:
			#self.report()
			NewY = 0
			NewVY = (-0.5)*NewVY
		if self.flying:
			self.set_P(NewX, NewY)
			self.set_V(NewVX, NewVY)

	def applyAir(self):
		AIR_CONST = 0.001 # m/s2
		WIND_DIR = -180 # degrees
		WIND_FORSE = 1 # m/s
		NewVY = self.Vy*(1 - AIR_CONST) + WIND_FORSE * math.sin(math.radians(WIND_DIR))
		NewVX = self.Vx*(1 - AIR_CONST) + WIND_FORSE * math.cos(math.radians(WIND_DIR))
		self.set_V(NewVX, NewVY)

	def getV(self):
		return pow( pow(self.Vx,2)+pow(self.Vy,2) , 0.5)

	def set_Vangle(self, ang):
		self.Vx = self.getV() * math.cos(math.radians(ang))
		self.Vy = self.getV() * math.sin(math.radians(ang))

#start velosity
Boxes = []
def addBox(speed, ang):
	Boxes.append(Pbody("%d" % ang))
	Boxes[len(Boxes)-1].set_P(0,0)
	Boxes[len(Boxes)-1].set_V(speed,0)
	Boxes[len(Boxes)-1].set_Vangle(ang)

#for i in range(0,100):
#	addBox(3.0, 44+i/100)
addBox(10.0, 30)
#addBox(3.0, 45)	

#log_path(Boxes)
log_path_vel(Boxes[0])

ITER_M = ITERATE
while ITERATE > 0:
	for obj in Boxes:
		obj.applyAir()
		obj.applyV()
	#log_path(Boxes)
	log_path_vel(Boxes[0])
	perc = 100 * (1 - float(ITERATE) / float(ITER_M))
	if perc % 10 == 0:
		print("%d%c" % (int(perc), chr(37)))
	ITERATE -= 1

print("maximum altitude was %f" % Boxes[0].maxY)

safeGraph()