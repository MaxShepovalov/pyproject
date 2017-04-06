#FFT in python
import math
PI = math.pi

#vectors ops
def Vadd(in1, in2):
	return (in1[0]+in2[0], in1[1]+in2[1])

def Smul(in1, m):
	return (in1[0]*m, in1[1]*m)
def Vmul(in1, in2):
	A,B=in1
	C,D=in2
	#print "MULTIPTY 1=",in1," 2=",in2," out",(A*(C-D), A*D+B*C)
	return (A*(C-D), A*D+B*C)

#parameter
#(real, imaginary)
def W(n,k):
	return (round(math.cos(2*PI*n/k),9), -round(math.sin(2*PI*n/k),9))

W8 = []
for i in range(8):
	W8.append(W(i,8))
print "W8=",W8

def L2DFT(in1, in2, mult):
	out1 = Vadd(in1, Vmul(in2, mult))
	out2 = Vadd(in1, Vmul(in2, Smul(mult,-1)))
	return out1, out2

def butterfly(inA, inB, C):
	if len(inA)!=len(inB) or 2*len(inA)!=len(C):
		print "lengths of INA, INB, or half length of C ARE NOT THE SAME"
		exit()
	out = [0]*(2*len(inA))
	for i in range(len(out)):
		if i < len(out)/2:
			out[i]=Vadd(inA[i], Vmul( inB[i], C[i]))
		else:
			out[i]=Vadd(inA[i-out/2], Vmul( inB[i-out/2], Smul(C[i], -1)))

def L8FFT(inp_arr):
	#DFT
	STAGE0 = []
	STAGE0 += L2DFT(inp_arr[0], inp_arr[1])
	STAGE0 += L2DFT(inp_arr[2], inp_arr[3])
	STAGE0 += L2DFT(inp_arr[4], inp_arr[5])
	STAGE0 += L2DFT(inp_arr[6], inp_arr[7])
	#print "\nSTAGE 0:",STAGE0
	STAGE1 = []
	STAGE1 += [Vadd(STAGE0[0], Vmul(STAGE0[2], W8[0]))]
	STAGE1 += [Vadd(STAGE0[1], Vmul(STAGE0[3], W8[2]))]
	STAGE1 += [Vadd(STAGE0[0], Vmul(STAGE0[2], W8[4]))]
	STAGE1 += [Vadd(STAGE0[1], Vmul(STAGE0[3], W8[6]))]
	STAGE1 += [Vadd(STAGE0[4], Vmul(STAGE0[6], W8[0]))]
	STAGE1 += [Vadd(STAGE0[5], Vmul(STAGE0[7], W8[2]))]
	STAGE1 += [Vadd(STAGE0[4], Vmul(STAGE0[6], W8[4]))]
	STAGE1 += [Vadd(STAGE0[5], Vmul(STAGE0[7], W8[6]))]
	#print "\nSTAGE 1",STAGE1
	STAGE2 = []
	STAGE2 += [Vadd(STAGE1[0], Vmul(STAGE1[4], W8[0]))]
	STAGE2 += [Vadd(STAGE1[1], Vmul(STAGE1[5], W8[1]))]
	STAGE2 += [Vadd(STAGE1[2], Vmul(STAGE1[6], W8[2]))]
	STAGE2 += [Vadd(STAGE1[3], Vmul(STAGE1[7], W8[3]))]
	STAGE2 += [Vadd(STAGE1[0], Vmul(STAGE1[4], W8[4]))]
	STAGE2 += [Vadd(STAGE1[1], Vmul(STAGE1[5], W8[5]))]
	STAGE2 += [Vadd(STAGE1[2], Vmul(STAGE1[6], W8[6]))]
	STAGE2 += [Vadd(STAGE1[3], Vmul(STAGE1[7], W8[7]))]
	#print "\nSTAGE 2:",STAGE2
	return STAGE2

STAGEpR = [0,2,0,-2,-4,4,2,4]
#STAGEpR = [1,0,0,0,0,0,0,0]
#STAGEpR = [1,0,-1,0,1,0,-1,0]
#STAGEpR = [0,1,2,3,4,5,6,7]
#make imaginary_compatible
STAGEp0 = []
for i in STAGEpR:
	STAGEp0.append((i, 0)) 
print "\nSTAGE -2:",STAGEp0
#remake
#STAGEp1 = [ STAGEp0[0], STAGEp0[2], STAGEp0[4], STAGEp0[6], STAGEp0[1], STAGEp0[3], STAGEp0[5], STAGEp0[7]]
STAGEp1 = []
for i in range(len(STAGEp0)):
	#reverse bit
	b = bin(i)[2:]
	while len(b)<len(bin(len(STAGEp0)-1)[2:]):
		b = '0'+b
	d = int(b[::-1],2)
	STAGEp1.append(STAGEp0[d])
print "\nSTAGE -1:",STAGEp1
############################
#STAGE2 = L8FFT(STAGEp1)
############################

x = STAGEp1

ST0 = [0,0,0,0,0,0,0,0]
ST1 = [0,0,0,0,0,0,0,0]
ST2 = [0,0,0,0,0,0,0,0]
#STAGE 0

ST0[0],ST0[1] = L2DFT(x[0], x[1], W8[0])
ST0[2],ST0[3] = L2DFT(x[2], x[3], W8[0])
ST0[4],ST0[5] = L2DFT(x[4], x[5], W8[0])
ST0[6],ST0[7] = L2DFT(x[6], x[7], W8[0])
print ST0

#STAGE 1
ST1[0],ST1[2] = L2DFT(ST0[0],ST0[2], W8[0])
ST1[1],ST1[3] = L2DFT(ST0[1],ST0[3], W8[2])
ST1[4],ST1[6] = L2DFT(ST0[4],ST0[6], W8[0])
ST1[5],ST1[7] = L2DFT(ST0[5],ST0[7], W8[2])
print ST1

#STAGE 2
ST2[0], ST2[4] = L2DFT(ST1[0],ST1[4],W8[0])
ST2[1], ST2[5] = L2DFT(ST1[1],ST1[5],W8[1])
ST2[2], ST2[6] = L2DFT(ST1[2],ST1[6],W8[2])
ST2[3], ST2[7] = L2DFT(ST1[3],ST1[7],W8[3])
print ST2

output = ST2

############################

#amplitude
amp = []
for i in output:
	amp.append(pow((pow(i[0],2)+pow(i[1],2)),0.5))
print "\nAMPL :",amp
import matplotlib.pyplot as plt
plt.plot(amp)
plt.show()