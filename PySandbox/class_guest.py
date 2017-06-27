#class of live being

class guest(object):
	def __init__(self, x, y, z):
		self.hp = 1
		self.att = 1
		self.pic = None
		self.items = []
		self.pos = (x, y, z)
	def giveItem(self, itemclass, amount):
		for k in range(amount):
			self.items.append(itemclass())
	def hurt(self, att):
		self.hp -= att
	def ai(self, param):
		pass

#predefined

class player(guest):
	def __init__(self, x, y, z):
		super.__init__(x, y, z)
		self.hp = 20
	def ai(self, param):
		#check for pressed button
		pass