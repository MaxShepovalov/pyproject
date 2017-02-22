import sys

log = ""

class axis:
	def __init__(self):
		self.angl = 0.0
		self.dx = 0.5    #mm per cycle
		self.x_crd = 0.0 #obj position
		self.x_cyc = 0   #current cycle
	def rotate(self, da):
		self.angl+=da
		if self.angl >= 360.0:
			self.angl -= 360.0
		elif self.angl < 0.0:
			self.angl += 360.0
	def getAng(self):
		return self.angl

class motor:
	def __init__(self, ax):
		self.ison = False
		self.spd = 1.0 # deg/clock
		self.axis = ax
	def turnOn(self, dr):
		self.ison = True
		self.spd = abs(self.spd)
		if dr < 0:
			self.spd *= -1
	def turnOff(self):
		self.ison = False
	def clock(self):
		if self.ison:
			self.axis.rotate(self.spd)

class rotor_encoder:
	def __init__(self, ax):
		self.vdd = 3.3
		self.axis = ax
		
	def getData(self):
		return self.vdd * self.axis.getAng() / 360.0

def move(x_trg):
	global log
	direct = 1
	if X.x_crd > x_trg:
		direct = -1
	Mx.turnOn(direct)
	timeout = 10000000
	Vlast = Ex.getData() / 3.3
	eps = 0.001 #target margin
	for i in range(timeout):
		Mx.clock()
		Vin = Ex.getData() / 3.3
		if Vin < Vlast and direct==1:
			X.x_cyc += 1
		elif Vin > Vlast and direct==-1:
			X.x_cyc -= 1
		X.x_crd = (X.x_cyc + Vin ) * X.dx
		if X.x_crd > x_trg:
			direct = -1
			Mx.turnOn(-1)
		elif X.x_crd < x_trg:
			direct = 1
			Mx.turnOn(1)
		pline = "X:"+str(X.x_crd)[:5]
		if direct==1:
			pline += " >> cycle: "
		else:
			pline += " << cycle: "
		longline = ""
		for i in range(int(10*X.x_crd)):
			longline += "."
		pline += str(X.x_cyc)+" pot:"+str(Vin)[:5]+"\t"+longline+"                        \r"
		sys.stdout.write(pline)
		sys.stdout.flush()
		log += pline[:-1] + "\n"
		Vlast = Vin
		if abs(X.x_crd-x_trg) < eps:
			print "\ndone on "+str(i)+" iteration!"
			break

X = axis()
Mx = motor(X)
Ex = rotor_encoder(X)

#task is to move X from 0 to 33.5 mm
#x_trg = 33.5

move(3.3)
move(1.5)
move(2.1)
print log
