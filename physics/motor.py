#rocket imitation
import math

class engine():
	def __init__(self, tank, thr, attr, tdir, fuel):
		self.isOn = False
		self.Gas = tank
		self.mGas = tank
		self.threshold = thr
		self.a_max = attr # m/s2
		self.thrust_dir = tdir # -1 or 1 # 1 - move up, -1 - move down
		self.fuel_consmp = fuel # Liter # fuel consumption per iteration

	def turnON(self):
		self.isOn = True

	def thrust(self):
		a = 0.0 # attraction
		if self.isOn:
			if self.Gas > self.threshold:
				a = self.a_max
				self.Gas -= self.fuel_consmp
				if self.Gas < 0:
					self.Gas = 0.0
			else:
				a = self.a_max * self.Gas / self.threshold
				self.Gas -= self.fuel_consmp
				if self.Gas < 0:
					self.Gas = 0.0
		return self.thrust_dir * a

	def getTank(self):
		return int(100 * self.Gas / self.mGas)

#engine    (Gas, THRS, ATTR, D,FUEL)
E1 = engine(40.0, 5.0, 20.0, 1, 0.2)
E2 = engine( 6.0, 0.1, 9.45, 1, 0.2)

X = 0.0 # m # vertical position
V = 0.0 # m/s # vertical speed
A = 0.0 # m/s2 # vertical attraction

g = 9.8 # m/s2 # gravity

def air():
	AIR_COEF = 0.15
	MAX_AIR_PRESENCE = 60000.0
	air_coef = AIR_COEF - X / (MAX_AIR_PRESENCE / AIR_COEF)
	if X > MAX_AIR_PRESENCE:
		air_coef = 0
	return V*air_coef

def grav():
	RADIUS = 6000000.0
	return g*pow(RADIUS, 2)/pow(RADIUS+X, 2)

log_line = ""
def log_t(title):
	global log_line
	log_line += "%s," % title

def log(data):
	global log_line
	log_line += "%f," % data

def log_new():
	global log_line
	log_line += "\n"

def log_out(file):
	f = open(file, 'w')
	f.write(log_line)
	f.close()

log_t("X")
log_t("V")
log_t("A")
log_t("dA")
log_t("thrust1")
log_t("thrust2")
log_t("tank2")
log_t("gravity")
log_t("air_drag")

run = True
ticks = 500
E1.turnON()
dAm = 0
while run:
	if E1.getTank() <= 0:
		if ticks <= 0:
			run = False
			print("time end")
		else:
			ticks -= 1
	oldA = A
	Thr1 = E1.thrust()
	Thr2 = E2.thrust()
	#apply softlanding engine
	if V < -5 and X < 500:
		E2.turnON()
	Gf = grav()
	Ar = air()
	A = Thr1 + Thr2 - Gf - Ar
	V += A
	X += V
	if X < 0:
		print("Fallen")
		X = 0
		print("dV = %f" % -V)
		if dAm < abs(A):
			dAm = abs(A)
		print("dAm = %f" % dAm)
		V = 0
		A = 0
		run = False
	log_new()
	log(X)
	log(V)
	log(A)
	log(A - oldA)
	if dAm < abs(A - oldA):
		dAm = abs(A - oldA)
	log(Thr1)
	log(Thr2)
	log(E2.getTank())
	log(-Gf)
	log(-Ar)

log_out("output_kinetic.csv")