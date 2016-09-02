from bin.defr import cell
from bin.defr import header

FILES = []
NAME = "memfs"

#read files
def get_file(filename):
	#if
	pass

def descr(line):
	mem = []
	head = []
	line_blocks = line.split("|")
	##read sizes
	sizes = line_blocks[0].split(" ")
	MEM_H = int(sizes[0])
	MEM_S = int(sizes[1])
	##read header
	headers = line_blocks[1].split(";")
	for H in headers:
		if H!="":
			params = H.split(" ")
			hobj = header()
			hobj.title = params[0]
			hobj.size = int(params[1])
			hobj.addr = int(params[2])
			head.append(hobj)
	##read cells
	memcells = line_blocks[2].split(";")
	for C in memcells:
		if C!="":
			params = C.split(" ")
			cobj = cell()
			if params[2]=="String":
				cobj.dmem = params[0]
			elif params[2] == "Int":
				cobj.dmem = int(params[0])
			elif params[2] == "Bool" and params[0] == "True":
				cobj.dmem = True
			elif params[2] == "Bool" and params[0] == "False":
				cobj.dmem = False
			cobj.addr = int(params[1])
			cobj.dtype = params[2]
			mem.append(cobj)
	return head, mem, len(mem)

def send(fsname, head, memory):
	fl_txt = ""
	fl_txt += str(len(head)) + " " + str(len(memory))
	fl_txt += "|"
	for F in head:
		fl_txt += F.title + " " + str(F.size) + " " + str(F.addr) + ";"
	fl_txt += "|"
	for C in memory:
		fl_txt += str(C.dmem) + " "
		fl_txt += str(C.addr) + " "
		fl_txt += C.dtype + ";"
	return fl_txt
	
######################
#FOR TEST

def makemem(size):
	mem = []
	for i in range(size):
		mem.append(cell())
	return mem

def prepare():
	mem = makemem(4)
	hd = [header(), header()]
	hd[0].title = "file"
	hd[0].addr = 0
	hd[0].size = 2
	hd[1].title = "file2"
	hd[1].size = 1
	hd[1].addr = 3
	mem[0].dmem = "Y"
	mem[0].dtype = "String"
	mem[0].addr = 1
	mem[1].dmem = "s"
	mem[1].dtype = "String"
	mem[1].addr = -1
	mem[3].dmem = True
	mem[3].addr = -1
	mem[3].dtype = "Bool"
	return hd, mem

def prepare2():
	hd, mem = prepare()
	out = send("file", hd, mem)
	return out
