import readline
import sys
class memory:
	def __init__(self):
		self.MEM = []
		for i in range(31):
			self.MEM.append(0x30000000)
		self.addr = 0x00
		self.lastaddr = 0x00
	def next(self):
		self.addr += 1
	def savelast(self):
		self.lastaddr = self.addr
	def loadlast(self):
		self.addr = self.lastaddr
	def read(self, adr):
		self.addr = adr
		return self.rd()
	def write(self, adr, data):
		self.addr = adr
		self.wt(data)
	def rd(self):
		if self.addr&0x7==0b111:
			self.addr += 1
		file = self.addr>>3
		block = self.addr&0x7
		pixel = self.MEM[file]
		return (pixel>>4*block)&0xf
	def wt(self, data):
		if self.addr&0x7==0b111:
			self.addr += 1
		file = self.addr>>3
		block = self.addr&0x7
		pixel = self.MEM[file]
		pixel &= (0xf<<4*block)^0xffffffff
		pixel |= data<<4*block
		self.MEM[file] = pixel

def recalc(num):
	nums = "00"
	#$00 and 0x00 hex address
	if num[:1]=='$' or num[1:2]=='x':
		nums += num[-2:]
	#&00 hex shift
	elif num[:1]=='&':
		addr = start
		addr += int(num[1:],16)
		nums += hex(addr)[2:]
	#$d000 decimal shift
	elif num[:2]=="&d":
		addr = start+int(num[2:])
		nums += hex(addr)[2:]
	#0b00000000 binary
	elif num[1:2]=='b':
		addr = int(num[2:],2)
		nums += hex(addr)[2:]
	#000 decimal
	elif len(num)<=3:
		addr = int(num, 10)
		nums += hex(addr)[2:]
	elif num[:1]=="n":
		print 'block and pixel addressing is not supported'
	num1 = int(nums[-2:-1], 16)
	num2 = int(nums[-1:],16)
	print 'transform '+num+' > '+str(num1)+' '+str(num2)
	return num1, num2

def compile():
	M.addr = start
	lines = prg.split('\n')
	for l in lines:
		#print '"'+l+'"'
		if l[:1]=='#':
			continue
		arg = l.split()
		param_req = 0
		if len(arg)==0:
			continue
		if arg[0]=="LDAA":
			M.wt(0x1)
			M.next()
			param_req = 1
		elif arg[0]=="LDAB":
			M.wt(0x2)
			M.next()
			param_req = 1
		elif arg[0]=="STAA":
			M.wt(0x3)
			M.next()
			param_req = 1
		elif arg[0]=="STAB":
			M.wt(0x4)
			M.next()
			param_req = 1
		elif arg[0]=="ADDA":
			M.wt(0x5)
			M.next()
		elif arg[0]=="MULT":
			M.wt(0x6)
			M.next()
		elif arg[0]=="XOR":
			M.wt(0x7)
			M.next()
		elif arg[0]=="AND":
			M.wt(0x8)
			M.next()
		elif arg[0]=="OR":
			M.wt(0x9)
			M.next()
		elif arg[0]=="SETA":
			M.wt(0xa)
			M.next()
			param_req = 1
		elif arg[0]=="SETB":
			M.wt(0xb)
			M.next()
			param_req = 1
		elif arg[0]=="JUMP":
			M.wt(0xc)
			M.next()
			param_req = 1
		elif arg[0]=="BREQ":
			M.wt(0xd)
			M.next()
			param_req = 1
		elif arg[0]=="SWAP":
			M.wt(0xe)
			M.next()
		elif arg[0]=="STOP":
			M.wt(0xf)
			M.next()
		elif arg[0][-1:]==':':
			M.addr =  int(arg[0][:-1],16)
		else:
			print 'unsupported command ' + arg[0] + ' in "' + l + '"'
		if param_req!=0:
			if len(arg[param_req])>9:
				print 'long number ' + arg[param_req] + ' in "' + l + '"'
			else:
				num1, num2 = recalc(arg[param_req])
				if num1 == -1 or num2 == -1:
					print 'error occured: cant recalculate address/number at "'+l+'"'
					clear()
					print 'memory cleared'
					break
				#num1 = int(arg[param_req][2],16)
				#num2 = int(arg[param_req][3],16)
				M.wt(num1)
				M.next()
				M.wt(num2)
				M.next()

def show(num1, num2):
	if num1<0:
		print 'num1 should be >0'
		return 0
	if num2>31:
		print 'num2 should be <=31'
		return 0
	for i in range(num1,num2):
		print hex(M.MEM[i])

def process():
	M.addr = start
	A1 = 0x0
	A2 = 0x0
	B1 = 0x0
	B2 = 0x0
	D1 = 0x0
	D2 = 0x0
	run = True
	try:
		while run:
			cmd = M.rd()
			M.next()
			if cmd == 1:
				sys.stdout.write("LDAA")
				A1 = M.rd()
				M.next()
				A2 = M.rd()
				M.next()
				M.savelast()
				M.addr = A1*16+A2
				A1 = M.rd()
				M.next()
				A2 = M.rd()
				M.next()
				print '  A = ' + hex(A1*16+A2)
				M.loadlast()
			elif cmd == 2:
				sys.stdout.write("LDAB")
				B1 = M.rd()
				M.next()
				B2 = M.rd()
				M.next()
				M.savelast()
				M.addr = B1*16+B2
				B1 = M.rd()
				M.next()
				B2 = M.rd()
				M.next()
				print '  B = ' + hex(B1*16+B2)
				M.loadlast()
			elif cmd == 3:
				sys.stdout.write("STAA")
				D1 = M.rd()
				M.next()
				D2 = M.rd()
				M.next()
				M.savelast()
				M.addr = D1*16+D2
				M.wt(A1)
				M.next()
				M.wt(A2)
				M.next()
				M.loadlast()
				print '  addr = ' + hex(M.addr)
				print '  A (' + hex(A1*16+A2) + ') -> ' + hex(D1*16+D2)
			elif cmd == 4:
				sys.stdout.write("STAB")
				D1 = M.rd()
				M.next()
				D2 = M.rd()
				M.next()
				M.savelast()
				M.addr = D1*16+D2
				M.wt(B1)
				M.next()
				M.wt(B2)
				M.next()
				M.loadlast()
				print '  B (' + hex(B1*16+B2) + ') -> ' + hex(D1*16+D2)
			elif cmd == 5:
				sys.stdout.write("ADDA")
				A = (A1*16+A2) + (B1*16+B2)
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2) + ' A+B=' + hex(A)
				A1 = (A&0xf0)>>4
				A2 = A&0x0f
			elif cmd == 6:
				sys.stdout.write("MULT")
				D = (A1*16+A2) * (B1*16+B2)
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2) + ' A*B=' + hex(D)
				A1 = (D&0xf000)>>12
				A2 = (D&0x0f00)>>8
				B1 = (D&0x00f0)>>4
				B2 = D&0x000f
			elif cmd == 7:
				sys.stdout.write("XOR")
				A = (A1*16+A2) ^ (B1*16+B2)
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2) + ' A^B=' + hex(A)
				A1 = (A&0xf0)>>4
				A2 = A&0x0f
			elif cmd == 8:
				sys.stdout.write("AND")
				A = (A1*16+A2) & (B1*16+B2)
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2) + ' A&B=' + hex(A)
				A1 = (A&0xf0)>>4
				A2 = A&0x0f
			elif cmd == 9:
				sys.stdout.write("OR")
				A = (A1*16+A2) | (B1*16+B2)
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2) + ' A|B=' + hex(A)
				A1 = (A&0xf0)>>4
				A2 = A&0x0f
			elif cmd == 10:
				sys.stdout.write("SETA")
				A1 = M.rd()
				M.next()
				A2 = M.rd()
				M.next()
				print '  A = ' + hex(A1*16+A2)
			elif cmd == 11:
				sys.stdout.write("SETB")
				B1 = M.rd()
				M.next()
				B2 = M.rd()
				M.next()
				print '  B = ' + hex(B1*16+B2)
			elif cmd == 12:
				sys.stdout.write("JUMP")
				D1 = M.rd()
				M.next()
				D2 = M.rd()
				M.next()
				M.addr = D1*16+D2
				print '  addr = ' + hex(M.addr)
			elif cmd == 13:
				sys.stdout.write("BREQ")
				if A1==B1 and A2==B2:
					print '  taken'
					D1 = M.rd()
					M.next()
					D2 = M.rd()
					M.next()
					M.addr = D1*16+D2
					print '  addr = ' + hex(M.addr)
				else:
					print '  not taken'
					M.next()
					M.next()
					M.next()
			elif cmd == 14:
				sys.stdout.write("SWAP")
				D1 = A1
				D2 = A2
				A1 = B1
				A2 = B2
				B1 = D1
				B2 = D2
				print '  A=' + hex(A1*16+A2) + ' B=' + hex(B1*16+B2)
			elif cmd == 15:
				print "STOP"
				run = False
			else:
				print 'error cmd=' + hex(cmd) + ' at ' + str(M.addr) + '('+ hex(M.addr) + ')'
				run = False
	except KeyboardInterrupt:
		print "error KeyboardInterrupt at "+str(M.addr)
		print "  A="+hex(A1*16+A2)+" B="+hex(B1*16+B2)+" D="+hex(D1*16+D2)

M = memory()
start = 0x00

prg = ""
#compile()

#show(0,9)
#process()
#show(0,9)

if len(sys.argv)>1:
	print 'terminal mode activated'
else:
	k = open("progs/example", 'r')
	prg = k.read()
	k.close()
	compile()
	show(0,9)
	process()
	show(0,9)
	exit()

def help():
	print '"/q" or "/exit" or "/quit" to exit'
	print '"/help" this messsage\n'
	print '"LDAA <addr>" - load to A from addr'
	print '"LDAB <addr>" - load to B from addr'
	print '"STAA <addr>" - save from A to addr'
	print '"STAB <addr>" - save from A to addr'
	print '"ADDA"        - A = A + B'
	print '"MULT"        - AB = A * B'
	print '"XOR"         - A = A xor B'
	print '"AND"         - A = A & B'
	print '"OR"          - A = A | B'
	print '"SETA <num>"	 - A := num'
	print '"SETB <num>"	 - B := num'
	print '"JUMP <addr>" - goto addr'
	print '"BREQ <addr>" - goto addr if A==B'
	print '"SWAP"        - swap A and B'
	print '"STOP"        - clear RAM, stop clock'
	print '"##:"         - next commands will be"'
	print '                written from this hex address'
	print '/compile      - compile entered script'
	print '/show <1> <2> - print memory pixels from <1> to <2>'
	print '/run          - run emulation'
	print '/clear        - clear memory'
	print '/n            - empty code'
	print '/start <addr> - set start address'
	print '/code         - prints current code'
	print '/load <file>  - load code from file'
	print '/raw <array>  - enter raw memory table'
	print '\n$00 - hex addres'
	print '0x00 - hex number'
	print '&00 - hex shift from the start of a programm'
	print '&d000 - decimal shift from the start of a program'
	print '0b00000000 - binary number'
	print '000 - decimal number'
	print 'n0,00 - block and pixel addres'

def clear():
	M.addr = 0x00
	for i in range(31):
		M.MEM[i]=0x30000000

raw_cmd = ''
prg = ""
start = 0x00
while raw_cmd!='/q' or raw_cmd!='/exit' or raw_cmd!='/quit':
	raw_cmd = raw_input('>')
	if raw_cmd=="":
		continue
	if raw_cmd=='/help' or raw_cmd=='help':
		help()
	elif raw_cmd=='/q' or raw_cmd=='/exit' or raw_cmd=='/quit':
		break
	elif raw_cmd=='/clear':
		clear()
		print 'memory was cleared'
	elif raw_cmd[:5]=='/show':
		prms = raw_cmd.split(' ')
		if len(prms)<3:
			print 'Usage: "/show <num1> <num2>", where <num1> less than <num2>'
		else:
			show(int(prms[1]),int(prms[2]))
	elif raw_cmd=='/compile':
		compile()
		show(0,9)
	elif raw_cmd=='/code':
		print 'START AT '+str(start)+'('+str(hex(start))+')'
		print prg
	elif raw_cmd=='/run':
		process()
	elif raw_cmd[:4]=='/raw':
		prms = raw_cmd.split(' ')
		if len(prms)<2:
			print 'Usage: /raw [0x2???????, 0x2???????, ... ] where ? is a data'
		else:
			data = 0
			for k in prms:
				if k[0]=='[':
					data = k
			if data==0:
				print r"Can't find table"
			else:
				pxls = data[1:-1].split(',')
				clear()
				for p in range(len(pxls)):
					M.MEM[p] = int(pxls[p],16)
	elif raw_cmd[:5]=='/load':
		prms = raw_cmd.split(' ')
		if len(prms)<2:
			print 'Usage: /load <file>'
		else:
			try:
				k = open(prms[1], 'r')
				prg += k.read()
				k.close()
			except IOError:
				print "file "+str(prms[1])+" not found"
	elif raw_cmd[:6]=='/start':
		n1, n2 = recalc(raw_cmd[7:])
		start = n1*16+n2
	elif raw_cmd[:2]=='/n':
		prg = ""
	elif raw_cmd[0]!='/':
		prg += raw_cmd + '\n'
	else:
		print 'unsupported command ' + raw_cmd + '. Try /help'

