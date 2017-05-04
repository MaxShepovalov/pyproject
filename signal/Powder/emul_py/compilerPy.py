#python compiler for Powder CPU

class variable(object):
	"""docstring for variable"""
	def __init__(self):
		self.addr = 0
		self.size = 0

	def alloc(self, sz):
		self.size = sz

	def define(self, adr):
		self.addr = adr

vars = dict()

def cutter(line):
	strng = 0
	quots = ' '
	N = len(line)
	i = 0
	while i < N:
		if line[i]=='\"':
			if line[i-1:i+1]!='\\"':
				if quots[0]=='\"':
					strng-=1
					quots = quots[1:]
				else:
					strng+=1
					quots = '\"' + quots
		if line[i]=='\'':
			if line[i-1:i+1]!="\\'":
				if quots[0]=='\'':
					strng-=1
					quots = quots[1:]
				else:
					strng+=1
					quots = '\'' + quots
		print str(i) + ' - \'' + line[i] + '\' _' + str(strng) + '_ <' + quots + '>'
		if line[i]==' ' and strng==0:
			line = line[:i] + line[i+1:]
			print 'deleted ' + str(i) + '-> line=' + line
			N-=1
		else:
			i+=1
	return line


		
		