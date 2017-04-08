"""
simple circuit (2 poles)

-[c]-...-[c]-  type 0

 *-[c]-*
-* ... *-      type 1
 *-[c]-*

c = [tp, ... ]

c = [0,[1,10,100,1000],330,[0,5100,100,10]]

c = [0,[0,x,x,x]] === [0,x,x,x]
c = [1,[1,x,x,x]] === [1,x,x,x]
c = []

"""
res_base = [
        10.0,		#0
        100.0,		#1
        220.0,		#2
        330.0,		#3
        1000.0,		#4
        2000.0,		#5
        5100.0,		#6
        10000.0,	#7
        100000.0,	#8
        1000000.0	#9
]
res_pics = [
		"-[ 10]-",	#0
        "-[100]-",	#1
        "-[220]-",	#2
        "-[330]-",	#3
        "-[ 1k]-",	#4
        "-[ 2k]-",	#5
        "-[5.1]-",	#6
        "-[10k]-",	#7
        "-[.1M]-",	#8
        "-[1.M]-"	#9
]

INF = 1e+999

def calc(c):
	if type(c)==type([]):
		tp = c[0]
		res = 0.0
		if tp==0:   #series
			for part in c[1:]:
				res+=calc(part)
		elif tp==1: #parallel
			for part in c[1:]:
				out = calc(part)
				if out==0:
					res+=INF
				else:
					res+=1.0/calc(part)
			res = 1./res
		else:
			print "Unknown node: ",c[0]
			return INF
		return res
	elif type(c)==type(1.1):
		return c
	elif type(c)==type(1):
		return res_base[c]
	else:
		print "Unsupported type: ",type(c)
		return INF

def count_size(c):
	ln,wd = 0,0
	if type(c)==type([]):
		tp = c[0]

def draw(c):
	lenX = 0
	lenY = 0
	pict = [""]
	
	return lenX, lenY, pict

def find(val):
	#loop though resistance
	maxdepth=10
	deep = 1
	tp = 0
