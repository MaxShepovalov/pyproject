class encoder:
	def __init__(self):
		#params
		self.angle = 0.0
		self.pressed = False
		#pins
		self.clk = 0.0  #pinA
		self.dt = 0.0   #pinB
		self.sw = 0.0   #button
		self.plus = 3.3 #vcc
		self.grd = 0.0  #ground
		self.tick(0)
	def getCLK(self):
		return self.clk > 1.5
	def getDT(self):
		return self.dt > 1.5
	def getSW(self):
		return self.sw > 1.5
	def setVcc(self,vcc):
		self.plus = vcc
		self.tick(0)
	def tick(self, dangl):
		self.angle += dangl
		langl = self.angle%20.0  #period 20 degrees
		if self.pressed:
			self.sw = self.plus
		else:
			self.sw = self.grd
		if langl <= 6.0 or langl >= 16.0:
			self.clk = self.plus
		else:
			self.clk = self.grd
		if langl >= 4.0 and langl <= 14.0:
			self.dt = self.plus
		else:
			self.dt = self.grd
	def press(self):
		self.pressed = True
	def release(self):
		self.pressed = False
	def getAngle(self):
		ang = self.angle
		while ang > 360.0:
			ang -= 360
		while ang < 0:
			ang += 360
		return ang

#rotary direction matrix
## old 00 01 10 11
#new
# 00   -- >> << ??
# 01   << -- ?? >>
# 10   >> ?? -- << 
# 11   ?? << >> --
RDM = [["--",">>","<<","??"],["<<","--","??",">>"],[">>","??","--","<<"],["??","<<",">>","--"]]
def getDir(oldN, newN):
	return RDM[newN][oldN]

if __name__ == "__main__":
	#enviroment
	timescale = 0.001 #seconds
	rotaryspd = 60.0 #cycles/min
	
	da = 360.0*(rotaryspd/60.0)*timescale #delta angle
	
	E = encoder()
	
	oldA = int(E.getCLK())
	oldB = int(E.getDT())
	
	realtime = 0.0
	
	max_x = 10.9
	x_sel = 0.0
	sensivity = 0.1
	
	while realtime < 2.0:
		if realtime >= 30*timescale and realtime < 35*timescale:
			E.press()
			E.tick(0)
		elif round(realtime,3) == round(35*timescale,3):
			E.release()
			E.tick(0)
		else:
			if realtime > 50*timescale:
				E.tick(-da)
			else:
				E.tick(da)
		newA = int(E.getCLK())
		newB = int(E.getDT())
		move = "move:??"
		btn = "btn:??"
		if E.getSW():
			btn = "|pressed|"
		else:
			btn = "|~ ~ ~ ~|"
		move = getDir(oldA*2+oldB, newA*2+newB)
		if move==">>":
			x_sel += sensivity
			if x_sel > max_x:
				x_sel -= max_x
		if move=="<<":
			x_sel -= sensivity
			if x_sel < 0:
				x_sel += max_x
		print "|"+str(realtime)+"| "+str(E.getAngle())+" degrees -> A:"+str(newA)+" B:"+str(newB)+" "+move+" "+btn+" x="+str(x_sel)+"[item "+str(int(x_sel))+"]"
		realtime += timescale
		oldA = newA
		oldB = newB
