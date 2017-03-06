tt = dict()#c1,c0,s
tt['00000']=[0,0,0]#0
tt['00001']=[0,0,1]#1
tt['00010']=[0,0,1]#1
tt['00011']=[0,1,0]#2 <
tt['00100']=[0,0,1]#1
tt['00101']=[0,1,0]#2 <
tt['00110']=[0,1,0]#2 <-
tt['00111']=[0,1,1]#3 <-
tt['01000']=[0,0,1]#1
tt['01001']=[0,1,0]#2 <
tt['01010']=[0,1,0]#2 <-
tt['01011']=[0,1,1]#3 <-
tt['01100']=[0,1,0]#2 <-
tt['01101']=[0,1,1]#3 <-
tt['01110']=[1,0,1]#3 <
tt['01111']=[1,1,0]#4
tt['10000']=[0,0,1]#1
tt['10001']=[0,1,0]#2 <
tt['10010']=[0,1,0]#2 <-
tt['10011']=[0,1,1]#3 <-
tt['10100']=[0,1,0]#2 <-
tt['10101']=[0,1,1]#3 <-
tt['10110']=[1,0,1]#3 <
tt['10111']=[1,1,0]#4
tt['11000']=[0,1,0]#2 <-
tt['11001']=[0,1,1]#3 <-
tt['11010']=[1,0,1]#3 <
tt['11011']=[1,1,0]#4
tt['11100']=[1,0,1]#3 <
tt['11101']=[1,1,0]#4
tt['11110']=[1,1,0]#4
tt['11111']=[1,1,1]#5

tt1 = dict()
tt1['0000']=[0,0,0]#0
tt1['0001']=[0,0,1]#1
tt1['0010']=[0,0,1]#1
tt1['0011']=[0,1,0]#2 <
tt1['0100']=[0,0,1]#1
tt1['0101']=[0,1,0]#2 <
tt1['0110']=[0,1,0]#2 <
tt1['0111']=[1,0,1]#3
tt1['1000']=[0,0,1]#1
tt1['1001']=[0,1,0]#2 <
tt1['1010']=[0,1,0]#2 <
tt1['1011']=[1,0,1]#3
tt1['1100']=[0,1,0]#2 <
tt1['1101']=[1,0,1]#3
tt1['1110']=[1,0,1]#3
tt1['1111']=[1,1,0]#4

tt_f = tt
tt_f['00110']=[1,0,0]#2 <-
tt_f['00111']=[1,0,1]#3 <-
tt_f['01010']=[1,0,0]#2 <-
tt_f['01011']=[1,0,1]#3 <-
tt_f['01100']=[1,0,0]#2 <-
tt_f['01101']=[1,0,1]#3 <-
tt_f['10010']=[1,0,0]#2 <-
tt_f['10011']=[1,0,0]#3 <-===
tt_f['10100']=[1,0,0]#2 <-
tt_f['10101']=[1,0,1]#3 <-
tt_f['11000']=[1,0,0]#2 <-
tt_f['11001']=[1,0,1]#3 <-

class adder53(object):
	def __init__(self):
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.ci = 0
		self.co_o = 0
		self.ci_o = 0
		self.s_o = 0

	def getinput(self):
		line = str(self.a)+str(self.b)+str(self.c)+str(self.d)+str(self.ci)

	def calc(self):
		self.ci_o, self.co_o, self.s_o = tt[self.getinput()]

	def setA(self, a):
		self.a = a
		self.calc()

	def setB(self, b):
		self.b = b
		self.calc()

	def setC(self, c):
		self.c = c
		self.calc()

	def setD(self, d):
		self.d = d
		self.calc()

	def setCi(self, ci):
		self.ci = ci
		self.calc()

	def setABCD(self, a, b, c, d):
		self.setA(a)
		self.setB(b)
		self.setC(c)
		self.setD(d)
		self.calc()

	def getC0(self):
		return self.co_o

	def getC1(self):
		return self.ci_o

	def getS(self):
		return self.s_o

class adder43(adder53):
	def __init__(self):
		super(adder43, self).__init__()
		self.ci = ""
	def getinput(self):
		line = str(self.a)+str(self.b)+str(self.c)+str(self.d)

	def calc(self):
		self.ci_o, self.co_o, self.s_o = tt1[self.getinput()]

class adder53_f(adder53):
	def calc(self):
		self.ci_o, self.co_o, self.s_o = tt_f[self.getinput()]

class megaadder5:
	def __init__(self):
		self.inputs = ['000','000','000','000']
		self.A1 = adder43()
		self.A2 = adder53_f()
		self.A3 = adder53()
		self.report = False
		self.err = []

	def do_report(self):
		self.report = True
	def no_report(self):
		self.report = False

	def setNumber(self, num, ind):
		if ind in range(4):
			if num in range(8):
				self.inputs[ind] = bin(num)[2:]
				while len(self.inputs[ind]) < 3:
					self.inputs[ind] = '0' + self.inputs[ind]
				#self.calc()
			else:
				print "number should an be integer from 0 to 7"
		else:
			print "index should be 0, 1, 2, or 3"

	def getoutput(self):
		summ = int(str(self.A3.getC0())+str(self.A3.getS())+str(self.A1.getC0())+str(self.A1.getS()),2)
		carry = int(str(self.A3.getC1())+str(self.A2.getC0())+str(self.A2.getS())+'0',2)
		return summ+carry

	def printstate(self):
		if self.report == True:
			print "====="
			print "  "+str(self.A3.a)+str(self.A2.a)+str(self.A1.a)+"="+str(int(self.inputs[0],2))
			print "  "+str(self.A3.b)+str(self.A2.b)+str(self.A1.b)+"="+str(int(self.inputs[1],2))
			print "  "+str(self.A3.c)+str(self.A2.c)+str(self.A1.c)+"="+str(int(self.inputs[2],2))
			print "  "+str(self.A3.d)+str(self.A2.d)+str(self.A1.d)+"="+str(int(self.inputs[3],2))
			print "  "+str(self.A3.ci)+str(self.A2.ci)+str(self.A1.ci)
			print "-----"
			print " "+str(self.A3.getC0())+str(self.A3.getS())+str(self.A1.getC0())+str(self.A1.getS())
			print " "+str(self.A3.getC1())+str(self.A2.getC0())+str(self.A2.getS())
			print "-----"
			out_bin = bin(self.getoutput())[2:]
			while len(out_bin)<5:
				out_bin = '0' + out_bin
			print ""+str(out_bin)+"="+str(self.getoutput())

	def calc(self):
		self.A1.setABCD(self.inputs[0][2], self.inputs[1][2], self.inputs[2][2], self.inputs[3][2])
		self.A2.setABCD(self.inputs[0][1], self.inputs[1][1], self.inputs[2][1], self.inputs[3][1])
		self.A3.setABCD(self.inputs[0][0], self.inputs[1][0], self.inputs[2][0], self.inputs[3][0])
		self.printstate()
		self.A2.setCi(self.A1.getC1())
		self.printstate()
		self.A3.setCi(self.A2.getC1())
		self.printstate()

	def collectError(self):
		self.err.append(self.A1.getinput())
		self.err.append(self.A2.getinput())
		self.err.append(self.A3.getinput())

	def getError(self):
		if len(self.err)==0:
			print "no errors"
		else:
			err_c = dict()
			for i in self.err:
				if i in err_c.keys():
					err_c[i] += 1
				else:
					err_c[i] = 1
			mx = 0
			
			val = 'no '
			for i in err_c.keys():


if __name__=="__main__":
	M = megaadder5()
	for i in range(0,8):
		M.setNumber(i,0)
		for j in range(0,8):
			M.setNumber(j,1)
			for x in range(0,8):
				M.setNumber(x,2)
				for y in range(0,8):
					M.setNumber(y,3)
					M.calc()
					out = M.getoutput()
					if i+j+x+y != out:
						print "ERROR: "
						M.do_report()
						M.collectError()
						M.printstate()
						M.no_report()
	M.setNumber(7,0)
	M.setNumber(1,1)
	M.setNumber(4,2)
	M.setNumber(2,3)
	M.calc()
	M.do_report()
	M.printstate()