#import matplotlib.pyplot as plt
from random import random as rand

prints_are_active = False
def c_print(msg):
	if prints_are_active:
		print msg

focus_group = []
def f_print(msg, ID):
	if ID in focus_group:
		print msg
def sign(ID):
	focus_group.append(ID)
def unsign(ID):
	global focus_group
	for k in range(len(focus_group)):
		if focus_group[k]==ID:
			fg1 = focus_group[:k]
			fg2 = focus_group[k+1:]
			focus_group = fg1+fg2

def act_str(actn):
	if actn==0:
		return "\"pair\""
	elif actn==1:
		return "\"friend\""
	elif actn==2:
		return "\"partner\""
	elif actn==3:
		return "\"study\""

population = []
mainID = 0
class Member:
	def __init__(self):
		global mainID
		self.ID = mainID
		mainID += 1
		self.blgroup = int(4*rand()+1) 		 #1,2,3,4
		self.rez = 0.5>rand() 		 		 #True/False
		self.age = 0						 #age
		self.type = int(2*rand())			 #0-male, 1-female
		self.intel = 1 + 0.2*(rand()-0.5)	 #intellect base
		self.intel_rate = 0.01*rand()		 #intellect gain
		self.friend = 0.5 + 0.5*(rand()-0.5) #friendability
		self.friends = []			 		 #array if IDs
		self.ispregn = False				 #is pregnancy?
		self.pregndata = [0,0,0,0,-1]		 #pregnancy data
		self.partner = -1					 #found partner
		self.chance = 0						 #chance of death
		self.parents = [-1,-1]				 #parents IDs
		self.offspring = []
	def act(self):
		action = int(4*rand())
		f_print("Member "+str(self.ID)+" do action "+act_str(action), self.ID)
		if action==0: #pair
			if self.age>14:
				if 0.5<rand() and self.partner!=-1:
					pair(self, mID(self.partner))
				elif 0.1<rand():
					pair(self, mID((len(self.friends)+1)*rand()))
				else:
					pair(self, mID((len(population)+1)*rand()))
		if action==1: #friends
			if rand()>self.friend:
				num = int(len(population)*rand())
				num = population[num].ID
				if not num in self.friends and num!=self.ID:
					self.friends.append(num)
					f_print("now "+str(num)+" is a friend for "+str(self.ID), self.ID)
		if action==2: #partner
			if self.age>5:
				num = int(len(population)*rand())
				self.partner = population[num].ID
				f_print("now "+str(self.partner)+" is a partner for "+str(self.ID), self.ID)
		if action==3: #study
			self.intel += self.intel_rate
			f_print(str(self.ID) + " studied upto "+str(self.intel)+" intelligence", self.ID)
		#calc risk
		self.chance = 0.0001*self.age/self.intel + 0.00001
		if self.age>100:
			self.chance*=4
		if self.age<14:
			self.chance/=10
		if self.type==1 and self.ispregn:
			newMember(self, self.pregndata)
		self.age+=1

def mID(requestID):
	for m in population:
		if m.ID==int(requestID):
			return m
	return -1

def findID(rID):
	memb = -1
	memb = mID(rID)
	if memb==-1:
		for m in heav:
			if m.ID==rID:
				memb = m
				print("Found RIP Member: DAge: %d, Date: %d, %d friends %s, parents %s, %d offspring %s" % (m.age, m.ripdate, len(m.friends), m.friends, m.parents, len(m.offspring), m.offspring))
	else:
		print("Found Member: Age %d, blGrp %d, rez %s, type %d, preg %s, %d friends %s, parents %s, %d offspring %s" % (memb.age, memb.blgroup, memb.rez, memb.type, memb.ispregn, len(memb.friends), memb.friends, memb.parents, len(memb.offspring), memb.offspring))
	if memb==-1:
		print("No member with ID=" + str(rID))
	return memb

def calcGroup(gr1, gr2):
	table = [[1,1],[1,0],[0,1],[0,0]]
	back_table = [[4,3],[2,1]]
	gene1 = int(2*rand())
	gene2 = int(2*rand())
	return back_table[table[gr1-1][gene1]] [table[gr2-1][gene2]]


def pair(subjA, subjB):
	global prints_are_active
	old_prints = prints_are_active
	if subjA.ID in focus_group or subjB.ID in focus_group:
		prints_are_active = True
	c_print("A->B ")
	if subjA==-1:
		subjA=subjB
		c_print("  Member A is not accessable")
	if subjB==-1:
		subjB=subjA
		c_print("  Member B is not accessable")
	c_print(str(subjA.ID) + "->" + str(subjB.ID))
	if subjB.ID==subjA.ID:
		c_print("  Self like")
		return 1
	if subjA.age<18:
		c_print("  Age violation " + str(subjA.ID) + "(" + str(subjA.age) + ") by " + str(subjB.ID))
	if subjB.age<18:
		c_print("  Age violation " + str(subjB.ID) + "(" + str(subjB.age) + ") by " + str(subjA.ID))
	mom = -1
	dad = -1
	if subjA.type==1 and subjB.type == 0:
		mom = subjA.ID
		dad = subjB.ID
	elif subjB.type==1 and subjA.type == 0:
		mom = subjB.ID
		dad = subjA.ID
	else:
		if subjA.type==1:
			c_print("  Homo(L) found, no new Member")
		else:
			c_print("  Homo(G) found, no new Member")
		return 2
	if mID(mom).age<14:
		c_print("  No repr sys: fem (" + str(mom) + "), no new Member")
		return 3
	if mID(dad).age<14:
		c_print("  No repr sys: mal (" + str(dad) + "), no new Member")
		return 3
	if mID(mom).ispregn:
		c_print("  " + str(mom) + " is already in process")
	#pregn prob = 70%
	if 0.7>rand():
		mID(mom).ispregn = True
		mID(mom).pregndata = [mID(dad).blgroup, mID(dad).rez, mID(dad).intel, mID(dad).intel_rate, mID(dad).ID]
	prints_are_active = old_prints
	return 0


def newMember(mom, dad_data):
	baby = Member()
	baby.blgroup = calcGroup(mom.blgroup, dad_data[0])
	baby.intel = (mom.intel+dad_data[2])/1.4
	baby.intel = (mom.intel_rate+dad_data[3])/2.0
	if mom.rez==dad_data[1]:
		baby.rez = mom.rez
	else:
		baby.rez = 0.5>rand()
		baby.intel_rate /= 50.0
		baby.intel *= 0.8
	baby.parents = [mom.ID, dad_data[4]]
	population.append(baby)
	mom.ispregn = False
	mom.pregndata = [0,0,0,0,-1]
	mom.offspring.append(baby.ID)
	dad = mID(dad_data[4])
	if dad==-1:
		for i in heav:
			if i.ID==dad_data[4]:
				i.offspring.append(baby.ID)
	else:
		dad.offspring.append(baby.ID)
	f_print("New Member ID="+str(baby.ID)+" from "+str(mom.ID), mom.ID)

def add(N):
	for i in range(N):
		population.append(Member())

def allreset():
	global heav
	global population
	global mainID
	global YEAR
	YEAR = 0
	mainID = 0
	heav = []
	population = []
	add(10)

YEAR = 0
heav = []
class Past:
	def __init__(self, memb):
		self.ripdate = YEAR
		self.age = memb.age
		self.ID = memb.ID
		self.friends = memb.friends
		self.parents = memb.parents
		self.offspring = memb.offspring
		self.type = memb.type

def showAlive():
	lines = ""
	k = 1
	for i in population:
		lines += " %d"%i.ID
		if k%7==0:
			lines+="\n"
			k=0
		k+=1
	print "Alive:\n" + lines

def showDead():
	lines = ""
	k = 1
	for i in heav:
		lines += " %d"%i.ID
		if k%7==0:
			lines+="\n"
			k=0
		k+=1
	print "Dead:\n" + lines

def do(Ncycles):
	global population
	global YEAR
	c_print("\n==============   START OF LOOP\n")
	for n in range(Ncycles):
		for i in population:
			i.act()
		i = 0
		while i in range(len(population)):
			autochance = rand()
			if population[i].chance>autochance:
				f_print(" chance "+str(population[i].chance)+" was to high (>"+str(autochance)+")for "+str(population[i].ID), population[i].ID)
				heav.append(Past(population[i]))
				pop1 = population[:i]
				pop2 = population[i+1:]
				population = pop1+pop2
			i+=1
		YEAR += 1
	c_print("################   END OF LOOP")
	print("Year %d, population %d, maxID %d" % (YEAR, len(population), mainID))

def full(N):
	do(N)
	if len(population)<70:
		showAlive()
	if len(heav)<70:
		showDead()

def meanA():
	if len(population)>0:
		m = 0
		for k in range(len(population)):
			m+=(population[k].age-m)/(k+1)
		return m
	else:
		print "Empty Array"

def meanD():
	if len(heav)>0:
		m = 0
		for k in range(len(heav)):
			m+=(heav[k].age-m)/(k+1)
		return m
	else:
		print "Empty Array"

def mfan():
	g = 0
	b = 0
	for i in population:
		if i.type==1:
			g+=1
		else:
			b+=1
	print " Girls " + str(100.0*g/(g+b)) + "% Boys " + str(100.0*b/(g+b)) + "%"

def fast():
	allreset()
	showAlive()
	full(1)