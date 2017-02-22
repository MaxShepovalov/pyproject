from random import random as rand
class Node:
	def __init__(self):
		key1 = int(rand()*100)+1
		self.key = (key1, key1 + int(rand()*100)+1)
		self.keyP = (1.0/self.key[0], -(1.0*self.key[1])/self.key[0])
	def read(self, msg):
		ret_val = ""
		rmsg = []
		fmsg = []
		valid = True
		#envelope
		for k in msg:
			rmsg.append(self.keyP[0]*k+self.keyP[1])
		#pub key
		otherkey = rmsg[-2:]
		for k in rmsg[:-2]:
			fmsg.append(otherkey[0]*k+otherkey[1])
			if valid and (round(fmsg[-1:][0]) not in range(32,127)):
				ret_val += "not valid "
				valid = False
		if valid:
			pmsg = ""
			for n in fmsg:
				pmsg += chr(int(round(n)))
			ret_val += pmsg
		else:
			ret_val += str(fmsg[:-2])
		return ret_val
	def send(self, msg, key):
		pmsg = []
		#self.key
		for k in msg:
			pmsg.append(self.keyP[0]*ord(k)+self.keyP[1])
		pmsg.append(self.key[0])
		pmsg.append(self.key[1])
		for k in range(len(pmsg)):
			pmsg[k] = (key[0]*pmsg[k]+key[1])
		return pmsg

A = Node()
B = Node()
C = Node()
if True:
	print "A <- " + str(A.key)
	print "B <- " + str(B.key)
	print "C <- " + str(C.key)

def send(txt, trg):
	msg = A.send(txt, trg.key)
	print "A: " + A.read(msg)
	print "B: " + B.read(msg)
	print "C: " + C.read(msg)
	return msg

msg = send("test", A)