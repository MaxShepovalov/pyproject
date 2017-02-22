import matplotlib.pyplot as plt
import math
import sys

arg = ["-n", "-no-plot", "-r", "-real"]

SHOW_PLOT = True
SHOW_STAT = False
for cmd in sys.argv:
	if cmd==arg[0] or cmd==arg[1]:
		SHOW_PLOT = False
	if cmd==arg[2] or cmd==arg[3]:
		SHOW_STAT = True

#orbit speed, m/s
v = (450,0)
#GM = 65.14*pow(10, 10)
GM = 5.886*pow(10, 10)
#body radius, m
R = 200000.0
#Sphere of Influence
SOI = 2*R
#Initial position
p = (0, R+112000.0)
#time incrementation
T = 0.005

#ALTITUDE, AT WHICH STAGE 3 SHOULD START
ST3_FIRE = R + 10000.0 # m

#air drag
zone1 = [0, R + 3000]
zone2 = [R + 3000, R + 22000]
zone3 = [R + 22000, R + 45000]
zone4 = [R + 45000, R + 70000]
def inZone(pos, zone):
	out = False
	alt = ampl(pos)
	if alt >= zone[0] and alt < zone[1]:
		out = True
	return out

def air(pos, vel):
	v = (0,0)
	if inZone(pos, zone1):
		v = add(0,(0,0),-0.00003,vel)
	elif inZone(pos, zone2):
		v = add(0,(0,0),-0.000015,vel)
	elif inZone(pos, zone3):
		v = add(0,(0,0),-0.000005,vel)
	elif inZone(pos, zone4):
		v = add(0,(0,0),-0.0001,vel)
	return v

#vector addition
def add(A,a,B,b):
	return (A*a[0]+B*b[0],A*a[1]+B*b[1])
#amplitude of the vector
def ampl(t):
	return pow( pow(t[0],2)+pow(t[1],2),0.5)
#calculate change of the speed
def calcDv():
	return add(0,(0,0), -GM/ pow(ampl(p),3), p)

#angle of the vector
def angle(vect):
	a = math.degrees(math.atan2(float(vect[1]),float(vect[0])))
	if a<0:
		a += 360.0
	return a

#Check if position [vect] is closer than [eps] meters from [trg]
def inArea(vect, trg, eps):
	ret = False
	dVect = add(1, vect, -1, trg)
	dist = ampl(dVect)
	if dist <= eps:
		ret = True
	return ret

#provide thrust
class engine:
	def __init__(self):
		self.force = 360000.0	#N
		self.thrs = 0.0 	#0.0..1.0
		self.gas = 10*1000.0	#fuel
		self.cons = 0.12*1000	#ton/s
		self.vect = (0,1) #opposit global v
		self.ison = False

	def setOppositeVector(self, Nvect):
		des_angle = math.radians(angle(Nvect)+180)
		self.vect = (math.cos(des_angle), math.sin(des_angle))

	def turnOn(self):
		self.ison = True

	def run(self):
		dV = (0,0)
		if self.thrs>1.0:
			print "thrs is more than 1.0 (100%)"
		if self.thrs<0.0:
			print "thrs is less than 0.0 (0%)"
		if self.ison:
			if self.gas>0:
				acc = self.thrs*self.force/(mass+self.gas)
				dV = add(0,(0,0),acc/ampl(self.vect),self.vect)
				self.gas -= self.thrs*self.cons*T
			else:
				print "Out of gas"
				self.ison = False
		return dV

	def turnOff(self):
		self.ison = False

############################################################

Pstart = p
ExcPos = 20*T #meters
Vstart = v
ExcVel = T #m/sec
traceX = []
traceY = []
Astart = angle(p)
ExcAng = 0.1*T

gravity = []

velH = []
velV = []
velA = []
velAmp = []

#Raw mass of craft [tons]
mass = 8000.0

minH = ampl(p)
maxH = ampl(p)
minV = ampl(v)
maxV = ampl(v)


print 'start'
mTime = 1000000

E = engine()
E.thrs = 1.0
E.setOppositeVector(v)
Gas_start = E.gas
engA = []
engforce = []
stage = 0

#######################################################################
#SIMULATION
#######################################################################

for i in range(mTime):
	####Apply speed
	p = add(1,p,T,v)
	####Trace
	traceX.append(p[0])
	traceY.append(p[1])
	####Change current speed vector
	v = add(1,v,T,calcDv())
	####Check thrust
	dVeng = E.run()
	####Add thrust influence
	v = add(1,v,T,dVeng)
	####Add air influence
	v = add(1,v,1,air(p,v))
	####analys
	hshift = ampl(v)*math.cos(math.radians(angle(p)+angle(v)-90.0))
	vshift = (ampl(add(1,p,T,v))-ampl(p))/T
	velH.append(hshift)
	velV.append(vshift)
	velA.append(angle(v)-angle(p)+90)
	velAmp.append(ampl(v))
	engA.append(angle(E.vect))
	gravity.append(GM/pow(ampl(p),2))
	engforce.append(ampl(dVeng))
	#check max vals (that is a part of analysis, isn't it?)
	if maxH<ampl(p):
		maxH = ampl(p)
	if minH>ampl(p):
		minH = ampl(p)
	if maxV<ampl(v):
		maxV = ampl(v)
	if minV>ampl(v):
		minV = ampl(v)

	####PRINT CURRENT STATS
	if SHOW_STAT:
		statline = "P:"+str(int(p[0]))+":"+str(int(p[1]))+"\t Alt:"+str(ampl(p)-R)+"\t Spd:"+str(ampl(v))+"\t Vspd:"+str(vshift)+"\t Fuel:"+str(int(E.gas*100.0/Gas_start))+"  "
		sys.stdout.write(statline + "\r")
		sys.stdout.flush()

	####FLIGHT LOGIC

	##IF ALTITUDE (AMPLIDUE OF POSITION) IS LESS THAN BODY RADIUS => CRAFT IS ON THE GROUND
	if ampl(p)<=R:
		print "\nFallen after " + str((i*T)) + " seconds impactV = " + str(round(ampl(v), 3)) + " m/sec" + " horiz.shift = " + str(round(hshift, 3))
	###IF VELOSITY IS MORE THAN 30m/s - SMASHED, IF >15m/s LANDED AND POSSIBLY  DAMAGED
	###IF < 15m/s SAVE LANDING
		if ampl(v)>15:
			if ampl(v)>30:
				print "  FULL DESTRUCTION"
			else:
				print "  MINOR CRASH"
		else:
			print "  SAFE LANDING"
		break

	###FLEW AWAY IF NOT IN SPHERE OF INFLUENCE
	if ampl(p)>SOI:
		print "\nFlew away after " + str((i*T)) + " seconds"
		break

	####IF APPEARED NEAR START POINT => PERHAPS ORBITING
	if inArea(p, Pstart, ExcPos):
		print "\nAt start point after " + str((i*T)) + " seconds"
		print "  Distance = " + str(ampl(add(1, Pstart, -1, p)))
	##IF VELOCITY IS LIKE AT THE START => DEFINETLY ORBITING, NO NEED TO LOOP FURTHER
		if inArea(v, Vstart, ExcVel):
			print "  Full cycle"
			print "  dV = " + str(ampl(add(1, Vstart, -1, v)))
			break

	##PRINT OUT MORE INFO
	if abs(angle(p)-Astart)<=ExcAng:
		print "\nNear start angle after " + str((i*T)) + " seconds"
		print "  P=" + str(p) + " v=" + str(v)
		print "  Distance = " + str(ampl(add(1, Pstart, -1, p)))
		print "  dV = " + str(ampl(add(1, Vstart, -1, v)))
		print "  angle = " + str(angle(p))
		print "  stage: " + str(stage) + " gas: " + str(E.gas)

	##PRINT TIME PROGRESS
	if i%(mTime/10)==0:
		print "\n"+str(100*i/mTime)+"%\n"

	########STAGES
	#======================
	##STAGE 0. FLY ON ORBIT FOR SOME TIME
	if stage==0 and abs(angle(p)-80.0)<=ExcAng:
		E.setOppositeVector(v)
		E.turnOn()
		stage = 1
		print "\nSTAGE 1 on " + str(i) + " iteration"

	##STAGE 1. DEORBITING (HORISONTAL SPEED = 0)
	if stage==1:
		#E.setOppositeVector(v)
		if abs(hshift-0)<=0.1:# or abs(angle(v)+angle(p)-180)<0.1:
			E.thrs = 0.0
			stage = 2
			print "\nSTAGE 2 on " + str(i) + " iteration"

	##STAGE 2. DECELERATE FALLING SPEED (MAINTAIN VERTICAL VELOCITY NORMAL)
	##STAGE 2.1 FREE FALL
	if stage==2:
		E.thrs = 0.0
		#E.setOppositeVector(v)
		#if ampl(v) > 100.0:
		#	E.thrs = 1.0
		#elif ampl(v) >= 50.0:
		#	E.thrs = (-50.0+ampl(v))/50.0
		#	if E.thrs>1.0:
		#		E.thrs = 1.0
		#	if E.thrs<0.0:
		#		E.thrs = 0.0
		#else:
		#	E.thrs = 0.0
	##TURN ON ST3 AT ST3_FIRE ALTITUDE
		if ampl(p) < ST3_FIRE:
			stage = 3
			print "\nSTAGE 3 on " + str(i) + " iteration"
	
	##STAGE 3. LANDING SKYLIFT (DECREASE VERTICAL VELOCITY)
	if stage==3:
		E.vect = p
		if vshift < -10.0:
			E.thrs = -(10.0+vshift)
			if E.thrs>1.0:
				E.thrs = 1.0
			if E.thrs<0.0:
				E.thrs = 0.0
		else:
			E.thrs = 0.0
	## ACTIVATE LANDING
		if ampl(p) < R+100:
			stage = 4
			print "\nSTAGE = 4 on " + str(i) + " iteration"

	##STAGE 4. LANDING (LOW VERTICAL SPEED)
	if stage==4:
		E.setOppositeVector(v)
		if ampl(v)>0.5:
			E.thrs = -(0.5+vshift)/5
			if E.thrs>1.0:
				E.thrs = 1.0
			if E.thrs<0.0:
				E.thrs = 0.0
		else:
			E.thrs = 0.0

#PRINT FINAL DATA
print "\nAltitude: " + str(minH) + ".." + str(maxH) + "\nVelocity: " + str(minV) + ".." + str(maxV)
print "Left " + str(E.gas/1000.0) + " tonns of gas. It is " + str(int(E.gas*100.0/Gas_start)) + "% of initial " + str(Gas_start/1000.0) + " tons"

#PRINT PLOTS
if SHOW_PLOT:
	groundX = []
	groundY = []
	for i in range(360*4):
		groundX.append(R*math.cos(math.radians(i/4.0)))
		groundY.append(R*math.sin(math.radians(i/4.0)))
	
	minX = int(round(min(traceX)))-5000
	if minX<-SOI:
		minX = -SOI
	maxX = int(round(max(traceX)))+5000
	if maxX>SOI:
		maxX = SOI
	minY = int(round(min(traceY)))-5000
	if minY<-SOI:
		minY = -SOI
	maxY = int(round(max(traceY)))+5000
	if maxY>SOI:
		maxY = SOI
	
	plt.subplot(442)
	plt.plot(traceX, traceY, "b", groundX, groundY, "k")
	#plt.axis([minX, maxX, minY, maxY])
	plt.axis('equal')
	plt.ylabel('blue-Trace\nblack-ground')
	
	plt.subplot(412)
	plt.plot(engforce, 'k', gravity, 'g')
	plt.ylim([-0.5,2])
	plt.ylabel('black-thrust\ngreen-gravity')
	
	plt.subplot(413)
	plt.plot(velH, 'r', velV, 'b', velAmp, 'k')
	plt.ylabel('Velocity\nred-Horizontal\nblue-Vertical\nblack-Amplitude')
	
	plt.subplot(414)
	plt.plot(velA, 'b', engA, 'r')
	plt.ylabel('Angle\nblue-Velocity\nred-Engine')
	plt.show()
	