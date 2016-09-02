# adds alias to defrag

ALIAS = []
FUNC = []

PROGRAMS = ["alias", "addfile", "printfile", "delfile", "printmem", "memstat", "nano", "malloc", "free", "defrag", "ls", "exit", "help", "move", "backup"]

FILE = "bin/aly.mem"

#read file
fl = open(FILE, 'r')
for line in fl:
	wrds = line.split()
	if len(wrds) != 2:
		print("error in alias file " + line + "")
	else:
		ALIAS.append(wrds[0])
		FUNC.append(wrds[1])
fl.close()

def safeFile():
	fl = open(FILE, 'w')
	for i in range(0, len(ALIAS)):
		fl.write( ALIAS[i] + " " + FUNC[i] + "\n")
	fl.close()

def addAlias(alname, funcname):
	if not alname in ALIAS:
		if not alname in FUNC:
			add = True
			if funcname in FUNC:
				for i in range(0, len(FUNC)):
					if FUNC[i] == funcname:
						print("  Alias already exists\n " + ALIAS[i] + " -> " + FUNC[i])
						break
				ans = raw_input("Continue? (y/n) ")
				if ans == "n" or ans == "N":
					add = False
				elif ans == "y":
					add = True
			if funcname in ALIAS:
				for i in range(0, len(ALIAS)):
					if ALIAS[i] == funcname:
						print("  Given function is an alias already\n " + ALIAS[i] + " -> " + FUNC[i])
						break
				ans = raw_input("Do you really want to make alias on alias? (y/n) ")
				if ans == "n" or ans == "N":
					add = False
				elif ans == "y":
					add = True
			if add:
				ALIAS.append(alname)
				FUNC.append(funcname)
				safeFile()
		else:
			if alname in PROGRAMS:
				print("  Can't use \"" + alname + "\" as alias. It is a name of the function")
	else:
		for i in range(0, len(ALIAS)):
			if ALIAS[i] == alname:
				print("  Alias already exists\n " + ALIAS[i] + " -> " + FUNC[i])
				break

def delAlias(alname):
	if alname in ALIAS:
		for i in range(0, len(ALIAS)):
			if ALIAS[i] == alname:
				ALIAS.pop(i)
				FUNC.pop(i)
				break
		safeFile()
	else:
		print(" Alias does not exist")

def getAliasTable():
	tbl = []
	for i in range(0, len(ALIAS)):
		tbl.append( ALIAS[i] + " -> " + FUNC[i])
	return tbl

def isAlias(cmd_name):
	ans = False
	if cmd_name in ALIAS:
		ans = True
	return ans

def getAlias(cmd_name):
	retval = ""
	for i in range(0, len(ALIAS)):
		if ALIAS[i] == cmd_name:
			retval = FUNC[i]
			break
	if retval == "":
		print("Alias does not exist")
	return retval
