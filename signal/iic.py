#SDA--\__<===x===x===x===x===x===x===x===>_____/---
#SCL----\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/--------
#	  S    0   1   2   3   4   5   6   7       P

#aaaaaaaabbbbbbbbdddddddd
import datetime
import time

def byte(int_val):
	b = bin(int_val)[2:]
	while len(b)<8:
		b = "0"+b
	return b

def printDevLog(dev, name_l):
	line = dev.log
	for i in range(name_l):
		line = " " + line
	print line

class bus:
	def __init__(self, name):
		self.name = name
		self.backtr = ""
		self.cDev = []
	def getTrace(self):
		return self.name, self.backtr
	def clockTrace(self):
		self.backtr += str(self.getVal())
	def addDev(self, dev):
		self.cDev.append(dev)
	def delDev(self, dev):
		for k in range(len(self.cDev)):
			if self.cDev[k]==dev:
				del self.cDev[k]
				break
	def getVal(self):
		for i in self.cDev:
			if i.getV(self.name) == 0:
				return 0
		return 1
	def setVal(self, nval):
		for i in self.cDev:
			i.setV(self.name, nval)

class device(object):
	def __init__(self, id):
		self.id = id
		self.sda = 1
		self.sda_wire = ""
		self.scl = 1
		self.scl_wire = ""
		self.state = 0
		self.state_str = ["idle", "warmup", "ID", "address", "data", "processing", "done", "upload", "ignore"]
		self.buffer = ""
		self.trg = 8
		self.addr = 0
		self.data = 0
		self.out = 0
		self.log = " "
		self.needUpload = False

	def setState(self, nstt):
		for i in range(len(self.state_str)):
			if self.state_str[i] == nstt:
				self.state = i
				return
		print "no such state:"+str(nstt)

	def getState(self):
		return self.state_str[self.state]

	def setWire(self, pin, wire):
		if pin=="SDA":
			self.sda_wire = wire.name
			wire.addDev(self)
		if pin=="SCL":
			self.scl_wire = wire.name
			wire.addDev(self)

	def cutWire(self, pin):
		if pin=="SDA":
			self.sda_wire = ""
			wire.delDev(self)
		if pin=="SCL":
			self.scl_wire = ""
			wire.delDev(self)

	def getV(self, wname):
		if wname == self.sda_wire:
			return self.sda
		if wname == self.scl_wire:
			return self.scl
		print "Wire "+wname+" not connected"

	def setV(self, wname, nval):
		if wname == self.sda_wire:
			if self.sda!=nval:
				self.sda = nval
				if self.getState()!="upload":
					self.recalc()
			return
		if wname == self.scl_wire:
			if self.scl!=nval:
				self.scl = nval
				if self.getState()!="upload":
					self.recalc()
			return
		print "Wire "+wname+" not connected"

	def main_func(self, addr, data):
		print "Device "+str(self.id)+" got at "+str(addr)+", data: "+str(data)
		self.setState("done")
		return self.trg, addr, data

	def recalc(self):

		#try:
			if self.getState()=="idle":
				#search for start bit
				if self.sda==0 and self.scl==1:
					self.setState("warmup")
			
			elif self.getState()=="warmup":
				#wait for first bit
				if self.sda==0 and self.scl==0:
					self.setState("ID")
					self.buffer = ""
			
			elif self.getState()=="ID":
				if self.scl == 1:
					self.buffer += str(self.sda)
					if len(self.buffer)==8:
						if self.id == int(self.buffer, 2):
							self.setState("address")
						else:
							#print "Wrong ID "+self.buffer+"="+str(int(self.buffer,2))+"!="+str(self.id)
							self.data = 16
							self.setState("ignore")
						self.buffer = ""
			
			elif self.getState()=="address":
				if self.scl == 1:
					self.buffer += str(self.sda)
					if len(self.buffer)==8:
						self.addr = int(self.buffer, 2)
						self.buffer = ""
						self.setState("data")
			
			elif self.getState()=="data":
				if self.scl == 1:
					self.buffer += str(self.sda)
					if len(self.buffer)==8:
						self.data = int(self.buffer, 2)
						self.buffer = ""
						self.setState("processing")
			
			elif self.getState()=="processing":
				self.trg, self.addr, self.data = self.main_func(self.addr, self.data)
			
			elif self.getState()=="upload":
				trg_bn = byte(self.trg)
				adr_bn = byte(self.addr)
				dat_bn = byte(self.data)
				Ctrl.sendInit()
				Ctrl.sendByte(trg_bn)
				Ctrl.sendByte(adr_bn)
				Ctrl.sendByte(dat_bn)
				Ctrl.sendStop()
				self.needUpload = False
				self.setState("idle")

			elif self.getState()=="done":
				if self.sda==1 and self.scl == 1:
					if self.needUpload:
						self.setState("upload")
						Ctrl.sendStop()
						self.recalc()
					else:
						self.setState("idle")

			elif self.getState()=="ignore":
				if self.scl == 1:
					if self.data > 0:
						self.data -= 1
					else:
						self.setState("idle")

		#except:
		#	print "Error in '"+self.getState()+"' state"

	def clockTrace(self):
		if self.getState()=="ID" or self.getState()=="address" or self.getState()=="data":
			if self.scl==1:
				self.log += str(self.sda)
			else:
				self.log += " "
		elif self.getState()=="processing":
			self.log += "~"
		elif self.getState()=="ignore":
			self.log += "!"
		elif self.getState()=="idle":
			self.log += " "
		elif self.getState()=="warmup":
			self.log += "."
		elif self.getState()=="done":
			self.log += "+"
		elif self.getState()=="upload":
			self.log += "M"

class controller:
	def __init__(self):
		self.SDA = bus("SDA")
		self.SCL = bus("SCL")
		self.SDA.setVal(1)
		self.SCL.setVal(1)
		self.clockTrace()
	def sendInit(self):
		self.SCL.setVal(1)
		self.SDA.setVal(0)
		self.clockTrace()
	def sendByte(self, val_bn):
		self.SCL.setVal(0)
		self.clockTrace()
		for b in range(8):
			self.SDA.setVal(int(val_bn[b],2))
			self.clockTrace()
			self.SCL.setVal(1)
			self.clockTrace()
			self.SCL.setVal(0)
			self.clockTrace()
		self.SDA.setVal(0)
		self.clockTrace()
	def sendStop(self):
		self.SCL.setVal(1)
		self.clockTrace()
		self.SDA.setVal(1)
		
	def getTrace(self):
		dn, d = self.SDA.getTrace()
		cn, c = self.SCL.getTrace()
		name_l = max(len(dn), len(cn))
		while len(dn)<name_l:
			dn += " "
		while len(cn)<name_l:
			cn += " "
		return name_l, dn+d+"\n"+cn+c

	def wait(self, n):
		for i in range(n):
			self.SDA.setVal(1)
			self.SCL.setVal(1)
			self.clockTrace()

	def clockTrace(self):
		self.SDA.clockTrace()
		self.SCL.clockTrace()
		for i in self.SDA.cDev:
			i.clockTrace()

	def resetTrace(self):
		self.SDA.backtr = ""
		self.SCL.backtr = ""
		for i in self.SDA.cDev:
			i.log = " "

class timer(device):
	def main_func(self, addr, data):
		k = datetime.datetime.now()
		self.needUpload = True
		self.setState("done")
		return addr, data, k.second

scr_buffer = [' ']*16*9
class screen(device):
	def main_func(self, addr, data):
		global scr_buffer
		for i in range(8):
			if addr+i in range(len(scr_buffer)):
				dt = byte(data)
				if dt[i]=="0":
					scr_buffer[addr+i] = " "
				else:
					scr_buffer[addr+i] = "#"
		prep_line = ""
		for i in range(len(scr_buffer)):
			if i%16==0 and i!=1:
				prep_line += "\n"
			prep_line += scr_buffer[i]
		print "screen:\n----\n"+prep_line+"\n----"
		self.setState("done")
		return 8, 0, 0

class filler(device):
	def main_function(self, addr, data):
		self.needUpload = True
		self.setState("done")
		return addr, data, 0xFF

out_number = ""
class numtoscr(device):
	def __init__(self, id):
		super (numtoscr, self).__init__(id)
		self.mem=[0]*10
		self.mem[0]=["00001100","00110011","00110011","00001100"]
		self.mem[1]=["00001100","00111100","00001100","00111111"]
		self.mem[2]=["00011100","00000011","00011100","00111111"]
		self.mem[3]=["00011111","00000111","00000011","00111110"]
		self.mem[4]=["00110011","00111111","00000011","00000011"]
		self.mem[5]=["00111111","00110000","00001111","00111111"]
		self.mem[6]=["00011111","00110011","00110011","00111111"]
		self.mem[7]=["00111111","00000011","00000011","00000011"]
		self.mem[8]=["00111111","00111111","00110011","00111111"]
		self.mem[9]=["00111111","00111111","00000011","00111111"]
	def main_func(self, addr, data):
		global out_number
		dec = int(data)/10
		num = int(data)%10
		out = self.mem[dec][0]
		out += self.mem[num][0]
		out += self.mem[dec][1]
		out += self.mem[num][1]
		out += self.mem[dec][2]
		out += self.mem[num][2]
		out += self.mem[dec][3]
		out += self.mem[num][3]
		self.setState("done")
		out_number = out
		return addr, data, out

Ctrl = controller()

A = timer(0x16)
B = screen(0x73)
C = numtoscr(0x40)
A.setWire("SDA", Ctrl.SDA)
A.setWire("SCL", Ctrl.SCL)
B.setWire("SDA", Ctrl.SDA)
B.setWire("SCL", Ctrl.SCL)
C.setWire("SDA", Ctrl.SDA)
C.setWire("SCL", Ctrl.SCL)

print_data = "0000110000001100"+\
			 "0011001100111100"+\
			 "0011001100001100"+\
			 "0000110000111111"
for i in range(1200):
	#read timer
	time.sleep(0.05)
	Ctrl.sendInit()
	Ctrl.sendByte(byte(0x16))#ID
	Ctrl.sendByte(byte(0x40))#addr
	Ctrl.sendByte(byte(0))	 #data
	Ctrl.sendStop()
	Ctrl.wait(5)
	#write to screen
	for i in range(len(out_number)/8):
		Ctrl.resetTrace()
		Ctrl.sendInit()
		Ctrl.sendByte(byte(0x73))#ID
		Ctrl.sendByte(byte(8*i))#ID
		Ctrl.sendByte(out_number[8*i:8*(i+1)])#data
		Ctrl.sendStop()
		Ctrl.wait(5)
		n_l, line = Ctrl.getTrace()
		print line
		printDevLog(A, n_l)
		printDevLog(B, n_l)
		printDevLog(C, n_l)
		print "A: "+A.getState()+" B: "+B.getState()+" C: "+C.getState()

#for i in range(16):
#	time.sleep(1)
#	Ctrl.resetTrace()
#	Ctrl.sendInit()
#	Ctrl.sendByte(byte(0x16))
#	Ctrl.sendByte(byte(0x73))
#	Ctrl.sendByte(byte(0x00))
#	Ctrl.sendStop()
#	Ctrl.wait(5)
#	n_l, line = Ctrl.getTrace()
#	print line
#	printDevLog(A, n_l)
#	printDevLog(B, n_l)
#	printDevLog(C, n_l)
#	print "A: "+A.getState()+" B: "+B.getState()+" C: "+C.getState()
