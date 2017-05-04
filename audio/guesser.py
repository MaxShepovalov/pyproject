#prepare chars
prep = ' zxcvbnm,./asdfghjkl;\'qwertyuiop[]\\1234567890-=ZXCVBNM<>?ASDFGHJKL:"QWERTYUIOP{}|!@#$%^&*()_+`~'
valid = []
for c in prep:
	valid.append(ord(c))
del prep

endpoints = []

class node():
	def __init__(self, v, s, parent):
		self.parent = parent
		self.siblings = []
		self.val = v
		self.shift = s
	def getval(self):
		if self.parent:
			return self.parent.getval()+self.val
		else:
			return self.val
	def find(self, orig_line):
		global endpoints
		line = orig_line[self.shift:]
		#create siblings
		for k in valid:
			c = bin(k)[2:]
			if line[:len(c)]==c:
				self.siblings.append(node(chr(k), len(c), self))
		#run siblings
		for child in self.siblings:
			child.find(line)
		#if no siblings, then it is an endpoint
		if len(self.siblings)==0:
			endpoints.append((self,line))

#start
start = node('',0,None)
#test = '10010011001111101101100000110011111011111101110110111011000011000001110010110111111000111101011100001'
test = raw_input('give binary string: ')
start.find(test)
print "\nBAD RESULTS"
for end,endline in endpoints:
	if endline!='':
		print '> "',end.getval(),'" left: "',endline,'"'
print "\nGOOD RESULTS"
good = 0
goodex = []
for end,endline in endpoints:
	if endline=='':
		good+=1
		vl = end.getval()
		goodex.append(vl)
		print '> "',vl,'" left: "',endline,'"'
if good==1:
	print 'found',len(endpoints),'variants only 1 of them is good'
elif good==0:
	print 'found',len(endpoints),'variants none of them are good'
else:
	print 'found',len(endpoints),'variants',good,'of them are good'
	import sys
	from random import random as rand
	while True:
		val = int(len(goodex)*rand())
		vl = goodex[val]
		sys.stdout.write(vl+'              \r')