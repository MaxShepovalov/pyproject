class delay:
	def __init__(self):
		self.input = None
		self.delay = 1
		self.stat1 = [0,0]
		self.stat0 = [0,0]
		self.out = 0
		self.inp = [0,0]
	def output(self):
		return self.out
	def cycle(self):
		if self.input:
			inp = self.input.output()
			self.inp = self.inp[1:2]
			self.inp.append(inp)
			if self.inp == [0,1]:
				self.stat1 = self.stat1[1:2]
				self.stat1.append(self.delay)
			else:
				new = self.stat1[1]-1
				if new < 0:
					new = 0
				self.stat1 = self.stat1[1:2]
				self.stat1.append(new)
			if self.inp == [1,0]:
				self.stat0 = self.stat0[1:2]
				self.stat0.append(self.delay)
			else:
				new = self.stat0[1]-1
				if new < 0:
					new = 0
				self.stat0 = self.stat0[1:2]
				self.stat0.append(new)
			if self.stat1 == [1,0]:
				self.out = 1
			if self.stat0 == [1,0]:
				self.out = 0

class inverter:
	def __init__(self):
		self.input = None
		self.out = 1
		self.inp = [0,0]
	def output(self):
		return self.out
	def cycle(self):
		if self.input:
			inp = self.input.output()
			self.inp = self.inp[1:2]
			self.inp.append(inp)
			if self.inp==[1,1]:
				self.out = 0
			elif self.inp==[0,0]:
				self.out = 1

class lever:
	def __init__(self):
		self.stat = 0
	def output(self):
		return self.stat
	def turnOn(self):
		self.stat = 1
	def turnOff(self):
		self.stat = 0
	def cycle(self):
		pass

class node:
	def __init__(self):
		self.inputs = []
		self.out = 0
	def output(self):
		return self.out
	def connect(self, Nnode):
		self.inputs.append(Nnode)
	def cycle(self):
		self.out = 0
		for i in self.inputs:
			if i.output()==1:
				self.out = 1
				break

class observer:
	def __init__(self):
		self.input = None
		self.out = 0
		self.inp = [0,0]
	def output(self):
		return self.out
	def cycle(self):
		if self.input:
			ninp = self.input.output()
			self.inp = self.inp[1:2]
			self.inp.append(ninp)
			if self.inp[0] != self.inp[1]:
				self.out = 1
			else:
				self.out = 0

def help():
	print "This is a module for redstone emulation"
	print "Classes:"
	print "		lever, node, inverter, delay, observer\n"
	print "		For emulating, construct a block model instead of"
	print "actual MC structure"
	print "Node does not exist in MC as a block. "
	print "Use 7 premade schemes as an example"
	print ""

###########################
def example1():
	L = lever()
	N = node()
	I = inverter()
	D = delay()
	O = observer()
	N.connect(L)
	I.input = N
	D.input = I
	N.connect(D)
	O.input = I
	D.delay = 3
	L.turnOn()
	plotLev = ""
	plotInp = ""
	plotInv = ""
	plotDly = ""
	plotObs = ""
	for i in range(50):
		L.cycle()
		N.cycle()
		I.cycle()
		D.cycle()
		O.cycle()
		plotLev += str(L.output())
		plotInp += str(N.output())
		plotInv += str(I.output())
		plotDly += str(D.output())
		plotObs += str(O.output())
		if i==10:
			L.turnOff()
	print "Generator and observer:"
	print "           node"
	print " [lever] -> + <-  <delay<  <- . -> >observer> -> output"
	print "            |                 |"
	print "            \ -> >inverter> ->/"
	print "Output:"
	print "Lever    " + plotLev
	print "Node     " + plotInp
	print "inverter " + plotInv
	print "Delay    " + plotDly
	print "Observer " + plotObs
def model1():
	print "r = redstone as a wire, NOT a redstone_block"
	print "< = repeater, arrow shows direction"
	print "o = observer, place it looking from output to input"
	print "# = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "' = redstone_torch attached to the nearest hard block\n"
	print "input at  layer1, row 0, column 0"
	print "output at layer1, row 0, column 5\n"
	print "  Layer1: Layer2:"
	print "  012345  012345\n"
	print "0 r#<ror   r"
	print "1  #'r     r"

def example2():
	L1 = lever()
	L2 = lever()
	N1 = node()
	N2 = node()
	I1 = inverter()
	I2 = inverter()
	N1.connect(L1)
	N1.connect(I1)
	N2.connect(L2)
	N2.connect(I2)
	I2.input = N1
	I1.input = N2
	plot_l1 = ""
	plot_l2 = ""
	plot_n1 = ""
	plot_n2 = ""
	#plot_i1 = ""
	#plot_i2 = ""
	for i in range(100):
		L1.cycle()
		I1.cycle()
		N1.cycle()
		L2.cycle()
		I2.cycle()
		N2.cycle()
		I1.cycle()
		N1.cycle()
		I2.cycle()
		N2.cycle()
		plot_l1 += str(L1.output())
		plot_l2 += str(L2.output())
		plot_n1 += str(N1.output())
		plot_n2 += str(N2.output())
		if i>0 and i%4==0:
			if i%8==0:
				if i%16 == 8:
					L1.turnOff()
				elif i%16 == 0:
					L2.turnOff()
			elif i%8==4:
				if i%16 == 12:
					L2.turnOn()
				elif i%16 == 4:
					L1.turnOn()
	print "Memory cell:"
	print "                               node1"
	print "             / -> >inverter1> -> + <- <lever1]"
	print "             |                   |"
	print " [lever2> -> + <- <inverter2< <- /"
	print "           node2"
	print "Output:"
	print "Lever1: " + plot_l1
	print "Lever2: " + plot_l2
	#print "Inver1: " + plot_i1
	print "Node1 : " + plot_n1
	#print "Inver2: " + plot_i2
	print "Node2 : " + plot_n2
def model2():
	print "r = redstone as a wire, NOT a redstone_block"
	print "# = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "' = redstone_torch attached to the nearest hard block\n"
	print "input1  at layer 1, row 3, column 0"
	print "input2  at layer 1, row 1, column 5"
	print "output1 at layer 1, row 4, column 2"
	print "output2 at layer 1, row 0, column 4\n"
	print "  Layer1: Layer2:"
	print "  012345  012345"
	print "0     r"
	print "1  r#'rr    r"
	print "2  r  r"
	print "3 rr'#r      r"
	print "4  r"

def example3():
	L1 = lever()
	L2 = lever()
	I1 = inverter()
	I2 = inverter()
	N = node()
	I3 = inverter()
	I1.input = L1
	I2.input = L2
	N.connect(I1)
	N.connect(I2)
	I3.input = N
	state = 0
	plot_in1 = ""
	plot_in2 = ""
	plot_out = ""
	for i in range(50):
		I1.cycle()
		I2.cycle()
		N.cycle()
		I3.cycle()
		plot_in1 += str(L1.output())
		plot_in2 += str(L2.output())
		plot_out += str(I3.output())
		if i>0 and i%6==0:
			state += 1
			vals = bin(state)[-2:]
			if vals[0]=="0":
				L1.turnOff()
			if vals[0]=="1":
				L1.turnOn()
			if vals[1]=="0":
				L2.turnOff()
			if vals[1]=="1":
				L2.turnOn()
	print "binary AND:"
	print "                       node"
	print " [lever1> >inverter1> -> \\"
	print "                         + -> >inverter3> -> output"
	print " [lever2> >inverter2> -> /"
	print ""
	print "Output:"
	print "in1 " + plot_in1
	print "in2 " + plot_in2
	print "out " + plot_out
def model3():
	print "r = redstone as a wire, NOT a redstone_block"
	print "* = redstone_torch on a ground"
	print "# = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "' = redstone_torch attached to the nearest hard block\n"
	print "input1 at layer1, row 0, column 0"
	print "input2 at layer1, row 2, column 0"
	print "output at layer1, row 1, column 3"
	print "  Layer1: Layer2:"
	print "  0123    0123\n"
	print "0 r#       *"
	print "1  #'r     r"
	print "2 r#       *"

def example4():
	L = lever()
	N = node()
	I1 = inverter()
	I2 = inverter()
	I3 = inverter()
	I4 = inverter()
	I5 = inverter()
	N.connect(L)
	N.connect(I5)
	I1.input = N
	I2.input = I1
	I3.input = I2
	I4.input = I3
	I5.input = I4
	L.turnOn()
	plot_l = ""
	plot_n = ""
	plot_i1 = ""
	plot_i2 = ""
	plot_i3 = ""
	plot_i4 = ""
	plot_i5 = ""
	for i in range(50):
		N.cycle()
		I1.cycle()
		I2.cycle()
		I3.cycle()
		I4.cycle()
		I5.cycle()
		plot_l += str(L.output())
		plot_n += str(N.output())
		plot_i1 += str(I1.output())
		plot_i2 += str(I2.output())
		plot_i3 += str(I3.output())
		plot_i4 += str(I4.output())
		plot_i5 += str(I5.output())
		if i==10:
			L.turnOff()
	print "Old style generator:"
	print "          node"
	print " [lever> -> + <---- <inverter5< <------- <inverter4< <--------\ "
	print "            |                                                 |"
	print "            \ -> >inverter1> -> >inverter2> -> >inverter3> -> /"
	print "\nOutput:"
	print "lever " + plot_l
	print "node  " + plot_n
	print "inv1  " + plot_i1
	print "inv2  " + plot_i2
	print "inv3  " + plot_i3
	print "inv4  " + plot_i4
	print "inv5  " + plot_i5
def model4():
	print "r = redstone as a wire, NOT a redstone_block"
	print "# = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "' = redstone_torch attached to the nearest hard block\n"
	print "input  at  layer 1, row 0, column 0"
	print "ioutput at layer 1, row 0, column 9\n"
	print "  Layer 1:"
	print "  0123456789\n"
	print "0 rr'#r'#rrr"
	print "1  r      r "
	print "2  #'r#'r#' "

def example5():
	L1 = lever()
	D1 = delay()
	D2 = delay()
	D3 = delay()
	D4 = delay()
	N = node()
	D1.input = L1
	D2.input = L1
	D2.delay = 4
	D3.input = L1
	D3.delay = 4
	D4.input = D3
	D4.delay = 4
	N.connect(D2)
	N.connect(D4)
	plot_in = ""
	plot_o1 = ""
	plot_o2 = ""
	for i in range(30):
		D1.cycle()
		D2.cycle()
		D3.cycle()
		D4.cycle()
		N.cycle()
		plot_in += str(L1.output())
		plot_o1 += str(D1.output())
		plot_o2 += str(N.output())
		if i==4:
			L1.turnOn()
		if i==8:
			L1.turnOff()
	print "signal strecher:"
	print "[lever1> -> . -> >delay1> ------------------> output1"
	print "            |                          node"
	print "            |--> >delay2> -------------> + -> output2"
	print "            |                            |"
	print "            \--> >delay3> -> >delay4> -> /"
	print "Output:"
	print "input    " + plot_in
	print "1 delay  " + plot_o1
	print "3 delays " + plot_o2
def model5():
	print "r = redstone as a wire, NOT a redstone_block"
	print "> = repeater, arrow shows direction\n"
	print "input   at  layer 1, row 1, column 0"
	print "output 1 at layer 1, row 0, column 4"
	print "output 2 at layer 1, row 2, column 4\n"
	print "  Layer 1:"
	print "  01234\n"
	print "0  r>rr"
	print "1 rr"
	print "2  r>rr"
	print "3  r>>r"

def example6():
	B = lever()
	N1 = node()
	I1a = inverter()
	I1b = inverter()
	N2 = node()
	In = inverter()
	I2 = inverter()
	N3 = node()
	Io = inverter()
	N1.connect(Io)
	N1.connect(B)
	I1a.input = Io
	I1b.input = B
	N2.connect(I1a)
	N2.connect(I1b)
	In.input = N1
	I2.input = N2
	N3.connect(In)
	N3.connect(I2)
	Io.input = N3
	plot_in2 = ""
	plot_out = ""
	state = 0
	for i in range(100):
		N1.cycle()
		I1a.cycle()
		I1b.cycle()
		N2.cycle()
		In.cycle()
		I2.cycle()
		N3.cycle()
		Io.cycle()
		plot_in2 += str(B.output())
		plot_out += str(Io.output())
		if i>0 and i%4==0:
			state += 1
			vals = bin(state)[-2:]
			if vals[1]=="0":
				B.turnOff()
			if vals[1]=="1":
				B.turnOn()
	print "flip-flop switcher on logic A==B:"
	print "             /-------------------------\ "
	print "             |                         |"
	print "             >---[+]->[i]>--v          |"
	print "             |    |         |          |"
	print " [leverB> ---)--->|        [+]>--[i]>--^-> output"
	print "             |    |         |"
	print "            [i]  [i]        |"
	print "             V    V         |"
	print "             \---[+]--[i]>--^"
	print "Output:"
	print "InputB " + plot_in2
	print "Output " + plot_out
def model6():
	print "# = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "r = redstone as a wire, NOT a redstone_block"
	print "v,^ = repeater, arrow shows direction"
	print "' = redstone_torch attached to the nearest hard block\n"
	print " input is at  layer 1, row 4, column 0"
	print " output is at layer 1, row 4, coulmn A\n"
	print "  Layer1:      Layer2:      Layer3:"
	print "  01234566789A 01234566789A 01234566789A\n"
	print "0  rrrrrrrrrr  "
	print "1  v v      r  "
	print "2  r rr#'r  r  "
	print "3  # ^   r  r   r"
	print "4 rrrr   rr#'r  #            r"
	print "5  # #   r      r"
	print "6  ' '   r     "
	print "7  rrrr#'r     "

def example7():
	B = lever()
	I1 = inverter()
	N1 = node()
	I2 = inverter()
	N3 = node()
	D = delay()
	I3 = inverter()
	N2 = node()
	I4 = inverter()
	I1.input = B
	N2.connect(B)
	N2.connect(I4)
	N1.connect(I1)
	N1.connect(D)
	I2.input = N1
	N3.connect(I3)
	N3.connect(I2)
	D.input = N3
	I4.input = N3
	I3.input = N2
	D.delay = 4
	plot_in2 = ""
	plot_out = ""
	state = 0
	for i in range(100):
		I1.cycle()
		N2.cycle()
		I3.cycle()
		D.cycle()
		N1.cycle()
		I2.cycle()
		N3.cycle()
		I4.cycle()
		plot_in2 += str(B.output())
		plot_out += str(I4.output())
		if i>0 and i%4==0:
			state += 1
			vals = bin(state)[-2:]
			if vals[1]=="0":
				B.turnOff()
			if vals[1]=="1":
				B.turnOn()
	print "flip-flop switcher on logic A==B: (variant 2)"
	print " [leverB> -.-------->[+]<----\ "
	print "           |          V n2   |"
	print "           |       I3[i]     |"
	print "           |          V n3   |"
	print "        I1[i] [D]<--<[+]>[i]>^-> output"
	print "           V   V      |  I4"
	print "           \--[+]>[i]>/"
	print "              n1  I2"
	print "Output:"
	print "InputB " + plot_in2
	print "Output " + plot_out
def model7():
	print "0 = any hard block (does not fall, does not have special function)"
	print "		for example: IRON_BLOCK, or WOOL, or STONE"
	print "r = redstone as a wire, NOT a redstone_block"
	print "< = repeater, arrow shows direction"
	print "' = redstone_torch attached to the nearest hard block"
	print "* = redstone_torch on a ground\n"
	print " input is at  layer 1, row 0, column 0"
	print " output is at layer 1, row 0, column 6\n"
	print "   Layer 1:    Layer 2:"
	print "   0123456     0123456\n"
	print "0  rrrr0rr         *"
	print "1  r   0 r         r"
	print "2  0 r<0'r         r"
	print "3  'rrr0           *"