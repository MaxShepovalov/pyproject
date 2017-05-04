import sys

if sys.version[:3]!='2.7':
	print 'this version is for Python 2.7.11, not '+sys.version[:3]
	exit()

#0-0000 > no command
#1-0001 > LDAA <addr>	- load to A from addr
#2-0010 > LDAB <addr>	- load to B from addr
#3-0011 > STAA <addr>	- save from A to addr
#4-0100 > STAB <addr>	- save from A to addr
#5-0101 > ADDA			- A = A + B
#6-0110 > MULT			- AB = A * B
#7-0111 > XOR 			- A = A xor B
#8-1000 > AND			- A = A & B
#9-1001 > OR			- A = A | B
#a-1010 > SETA <num>	- A := num
#b-1011 > SETB <num>	- B := num
#c-1100 > JUMP <addr>	- goto addr
#d-1101 > BREQ <addr>	- goto addr if A==B
#e-1110 > SWAP         - swap A and B
#f-1111 > STOP 		- clear RAM, stop clock
#
#	$00 - hex addres
#	0x00 - hex number
#	&00 - hex shift from the start of a programm
#	&d000 - decimal shift from the start of a program
#	0b00000000 - binary number
#	000 - decimal number
#	#0,00 - block and pixel addres

def addr(num):
	loc = num%7
	glo = (num/7)<<3
	if glo < 16:
		return '0'+ hex(glo+loc)[2:]
	return hex(glo+loc)[2:]

def num(adr):
	loc = int(adr,16)&0b00000111
	glo = (int(adr,16)&0b11111000)>>3
	return glo*7+loc

CodesWithAddr = ['LDAA','LDAB','STAA','STAB','JUMP','BREQ']
CodesWithParam = ['SETA','SETB']

codeword = dict()
codeword["LDAA"]=0x1
codeword["LDAB"]=0x2
codeword["STAA"]=0x3
codeword["STAB"]=0x4
codeword["ADDA"]=0x5
codeword["MULT"]=0x6
codeword["XOR"]=0x7
codeword["AND"]=0x8
codeword["OR"]=0x9
codeword["SETA"]=0xa
codeword["SETB"]=0xb
codeword["JUMP"]=0xc
codeword["BREQ"]=0xd
codeword["SWAP"]=0xe
codeword["STOP"]=0xf

#varmap = dict()
#add [addr, len, type]

#open file

start = 14
if addr(start)<'10':
	print 'cannot start at first pixel'
	exit()
fl = []
if len(sys.argv)<2:
	fl = ["LDAA $00", "STAB 0x00", "BREQ &00", "SETA 0x00", "STAA &21"]
else:
	f1 = open(sys.argv[1],'r')
	for line in f1:
		fl.append(line)

def transform(cmdline):
	par = cmdline.split()
	line = hex(codeword[par[0]])[2:]
	if par[0] in CodesWithParam or par[0] in CodesWithAddr:
		if par[1][:2]=='0x' or par[1][:1]=='$':
			line += par[1][-2:]
		elif par[1][:1]=='&':
			if par[1][1:2]=='d':
				line += addr(start+int(par[1][2:]))
			else:
				line += addr(start+int(par[1][-2:],16))
		elif par[1][:2]=='0b':
			while len(par[1])<10:
				par[1] = '0b0'+ par[1][2:]
			line += hex(int(par[1][2:6],2))[2:]
			line += hex(int(par[1][6:10],2))[2:]
		elif par[1][:1]=='#' and par[1][2,3]==',':
			block = int(par[1][1:2],8)
			pixel = int(par[1][3:5],16)<<3
			line += hex(pixel+block)[2:]
		elif int(par[1])<256:
			line += addr(int(par[1]))
		else:
			print "Unsupported address/data format: " + cmdline
	return line

program = ""
FILT = []

if start>15:
	program = transform('JUMP $'+addr(start))
else:
	program = transform('JUMP $0'+addr(start))
i = 3
while i<start:
	program += '0'
	i+=1
for l in fl:
	program += transform(l)

print program

shift = 0
pixel = ''
for i in range(len(program)):
	pixel = program[i] + pixel
	if i%7==6:
		FILT.append(pixel)
		shift += 1
		pixel = ''
	#print "added "+program[i]+" to "+str(shift)+" pixel"
if pixel!='':
	while len(pixel)<7:
		pixel = '0'+pixel
		#print "added 0 to "+str(shift)+" pixel"
	FILT.append(pixel)
print FILT
for f in FILT:
	print "0x2" + f + "    " + bin(int('0x2'+f,16))




