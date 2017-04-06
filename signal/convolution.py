import time
def convol(a1,a2,sh):
	o = []
	for a in range(len(a1)):
		indB = a-sh
		if indB in range(len(a2)):
			o.append(a1[a]*a2[indB])
		else:
			o.append(0)
	return o
def mult(a,num):
	b = []
	for k in a:
		b.append(k*num)
	return b
def inverse(a):
	b = []
	for k in a:
		b.append(1.0/k)
	return b

#k = [10,9,8,7,6,5,4,3,2,2,3,4,5,4,4,5,4,3,2,2,3,4,3,3,4,3,2,2,3,2,1]
k = [1,3,-4,5,7,5,-4,3,1]
#l = inverse(k)
l = [0,2,0,-2,0,2,0,-2,0]

#print k
#print l
print convol(k,l,0)