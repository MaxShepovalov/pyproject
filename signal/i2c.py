#SDA--\__<===x===x===x===x===x===x===x===>_____/---
#SCL----\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/--------
#	  S    0   1   2   3   4   5   6   7       P

class bus():
	def __init__(self):
		self.sda = 1
		self.scl = 1
	def setSDA(self, bn):
		if bn in range(1):
			self.sda = bn
		else:
			print "SDA: Can set only 1 or 0"
	def setSCL(self, bn):
		if bn in range(1):
			self.scl = bn
		else:
			print "SCL: Can set only 1 or 0"
	def read(self):
		return [self.sda, self.scl]

class device(object):
	def __init__(self, d_id):
		self.id = d_id
		self.bus = None
		self.inputs = [[1,1],[1,1]]
		self.mode = "idle"
		self.submode = 1
		self.in3b = ""
		self.out3b = ""
	def fetch(self):
		self.inputs = [ self.inputs[1], self.bus.read()]
	def calc(self):
		if self.mode=="idle":
			#look for SDA -\_
			if self.inputs[1][1]==1:
				SDA_dyn = str(self.inputs[0][0])+str(self.inputs[1][0])
				if SDA_dyn == "10":
					self.submode = 1
					self.mode = "reading"
		elif self.mode=="reading":
			#look for SCL _/-
			SCL_dyn = str(self.inputs[0][1])+str(self.inputs[1][1])
			if SCL_dyn == "01":
				if self.submode%9==0:
					setSDA(1)
				else:
					self.in3b += str(self.inputs[1][0])
				self.submode += 1
			elif:

		elif self.mode=="process":
			self.mode = "idle"
		elif self.mode=="sendback":
			self.mode = "idle"
	def getData(self):
		return self.out3b[0:8], self.out3b[8:16]

#         .       .       .       .          . .  
#---|---|---|---|---|---|---|---|---|---|---|---|---|
#---|---|---|---|---|---|---|---|---|---|---|---|---|
#---|---|---|---|---|---|---|---|---|---|---|---|---|
#---|---|---|---|---|---|---|---|---|---|---|---|---|
#---|---|---|---|---|---|---|---|---|---|---|---|---|
#---|---|---|---|---|---|---|---|---|---|---|---|---|