#change NONE to None

class fuel_cell:
	def __init__(self):
		self.typename = "Fuel Cell"
		self.maxval = 10
		self.output = 1
		self.value = 0
		self.placed = False
	def fill(self,nval):
		self.value += nval
		if self.value > self.maxval:
			self.value = self.maxval
	def use(self, nval):
		if self.value > 0:
			self.value -= nval
			if self.value < 0:
				self.value = 0
			return self.output
		return 0
	def set(self):
		self.placed = True
	def eject(self):
		self.placed = False
	def name(self):
		return self.typename
	def add(self, nval):
		self.value += nval
		if self.value > self.maxval:
			self.value = self.maxval

class adv_fuel_cell(fuel_cell):
	def __init__(self):
		self.typename = "Adv Fuel Cell"
		self.maxval = 20
		self.output = 2
		self.value = 0
		self.placed = False

class machine:
	def __init__(self):
		self.fuel = None
		self.cons_fuel = 1
		self.ison = False
		self.output = None
		self.name = "Default machine"
	def turnon(self):
		self.ison = True
	def turnoff(self):
		self.ison = False
	def cycle(self):
		if self.output == None:
			print "No output container"
			return 1
		if self.fuel == None:
			print "No fuel to run"
			return 1
		e = self.fuel.use(self.cons_fuel)
		if e > 0:
			self.output.add(e/2.0)
		else:
			print "Fuel cell is empty"
			return 1
		return 0
	def name(self):
		return self.name
	def printname(self):
		print self.name
		if self.fuel == None:
			print "  no fuel"
		else:
			print "  fuel: " + self.fuel.name()
		if self.output == None:
			print "  no output"
		else:
			print "  out: " + self.output.name()
	def givefuel(self, cell):
		self.fuel = cell
	def giveout(self, obj):
		self.output = obj
