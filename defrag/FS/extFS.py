FILES = []
NAME = "memfs"

#read files
def get_file(filename):
	if 

def descr(fsname, memclass):
	mem = []
	k = get_file(fsname)


def send(fsname, memclass, memory):
	fl_txt = ""
	fl_txt += len(memory) + ";"
	for C in memory:
		fl_txt += C.dmem + " "
		fl_txt += C.addr + " "
		fl_txt += C.type + ";"
	