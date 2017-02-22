#tt abcdci  c0,c1,s
tt = dict()
tt['00000']=[0,0,0]
tt['00001']=[0,0,1]
tt['00010']=[0,0,1]
tt['00011']=[1,0,0]
tt['00100']=[0,0,1]
tt['00101']=[1,0,0]
tt['00110']=[1,0,0]
tt['00111']=[1,0,1]
tt['01000']=[0,0,1]
tt['01001']=[1,0,0]
tt['01010']=[1,0,0]
tt['01011']=[1,0,1]
tt['01100']=[1,0,0]
tt['01101']=[1,0,1]
tt['01110']=[0,1,1]
tt['01111']=[1,1,0]
tt['10000']=[0,0,1]
tt['10001']=[1,0,1]
tt['10010']=[1,0,0]
tt['10011']=[1,0,1]
tt['10100']=[1,0,0]
tt['10101']=[1,0,1]
tt['10110']=[0,1,1]
tt['10111']=[1,1,0]
tt['11000']=[1,0,0]
tt['11001']=[1,0,1]
tt['11010']=[0,1,1]
tt['11011']=[1,1,0]
tt['11100']=[0,1,1]
tt['11101']=[1,1,0]
tt['11110']=[1,1,0]
tt['11111']=[1,1,1]

#c0 = 0 if 00000, 00001, 00010, 00100, 01000, 10000, 11100, 11010

def calc(a,b,c,d,ci):
	line = str(a)+str(b)+str(c)+str(d)+str(ci)
	return tt[line]

def add(num1, num2, num3, num4):
	width = max(len(num1), len(num2), len(num3), len(num4))
	#append numbers with 0
	while len(num1) < width:
		num1 = '0' + num1
	while len(num2) < width:
		num2 = '0' + num2
	while len(num3) < width:
		num3 = '0' + num3
	while len(num4) < width:
		num4 = '0' + num4
	print "1: "+num1+"\
	     \n2: "+num2+"\
	     \n3: "+num3+"\
	     \n4: "+num4
	c1 = 0
	carry = ''
	summ = ''
	for bn in range(width):
		ind = width - bn -1
		a = num1[ind]
		b = num2[ind]
		c = num3[ind]
		d = num4[ind]
		c0, c1, s = calc(a,b,c,d,c1)
		carry = str(c0) + carry
		summ = str(s) + summ
	print "summ   "+summ+"\
		 \ncarry "+carry+"0"
	#CPA
	sum_i = int(summ, 2)
	carry_i = int(carry+'0', 2)
	output = sum_i+carry_i
	return output