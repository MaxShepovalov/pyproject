import sys

#value base
res_base = [
	10.0,
	100.0,
	220.0,
	330.0,
	1000.0,
	2000.0,
	5100.0,
	10000.0,
	100000.0,
	1000000.0
]

#dictionary base
res = dict()
res["10R"] = 10.0
res["100R"] = 100.0
res["220R"] = 220.0
res["330R"] = 330.0
res["1K"] = 1000.0
res["2K"] = 2000.0
res["5K1"] = 5100.0
res["10K"] = 10000.0
res["100K"] = 100000.0
res["1M"] = 1000000.0

def getName(r):
	names = res.keys()
	for i in names:
		if res[i]==r:
			while len(i)<4:
				i += " "
			return i
	print "No such resistor in base for "+str(r)+" Ohm"
	return "--"

class resistor:
	def __init__(self, res):
		self.value = res
		self.ctype = "posled"
def draw_circ(circ):
	lines = ["",""]
	for i in circ:
		elem = "-*-["+getName(i.value)+"]"
		#elem = "-*-[????]"
		if i.ctype == "posled":
			lines[0] += elem
		elif i.ctype == "parall":
			while len(lines[1]) < len(lines[0]) - 8:
				lines[1] += " "
			lines[0] += "-*"
			lines[1] += elem[1:] + "-* "
	#end
	lines[0] += "-*-"
	for i in lines:
		print i

def calc_circ(circ):
	out = int_calc_circ(circ, 0, "add")

def int_calc_circ(circ, val, mode):
	for i in range(len(circ)):
		ind = len(circ)-1-i
		if circ[ind].ctype == "posled":
			pass
	return val

def ex_circ():
	c = []
	c.append(resistor(10.0))
	c.append(resistor(220.0))
	c[1].ctype = "parall"
	c.append(resistor(100.0))
	c.append(resistor(330.0))
	c[3].ctype = "parall"
	c.append(resistor(5100.0))
	return c

def par(R1, R2):
	return 1.0/( 1.0/R1 + 1.0/R2)

def cpar(r1, r2):
	return par(r1.value, r2.value)

def pos(R1, R2):
	return R1+R2

def cpos(r1, r2):
	return pos(r1.value, r2.value)

def getcomb():
	out = []
	combination = []
	for i in range(len(res_base)):
		for j in range(len(res_base)):
			val1 = par(res_base[i],res_base[j])
			if val1 not in out:
				out.append(val1)
				combination.append([i,j])
	return out, combination

def find(val):
	circuit = []
	#search all resistors until delta R < minimum resistance
	minres = min(res_base)
	delt_r = float(val)
	#loop thru base until found resistor
		#found = False
	for i in range(len(res_base)):
		trg_res = res_base[len(res_base)-1-i]
		sys.stdout.write("check "+str(trg_res)+" ")
		if delt_r >= trg_res:
			sys.stdout.write("match!")
			circuit.append(resistor(trg_res))
			delt_r -= trg_res
		sys.stdout.write(" .\n")
		if delt_r < minres:
			print("Can't append more resistors consequently")
			break
	if delt_r != 0.0:
		par_vals, hint = getcomb()
		#find minimum difference
		mindiff = minres + 1
		comb = [0,0]
		for i in range(len(par_vals)):
			diff = abs(delt_r - par_vals[i])
			if diff < mindiff:
				mindiff = diff
				comb = hint[i]
		delt_r = mindiff
		circuit.append(resistor(res_base[comb[0]]))
		circuit.append(resistor(res_base[comb[1]]))
		circuit[len(circuit)-1].ctype = "parall"
	print " final delt_r = "+str(delt_r)+"\n"
	return circuit