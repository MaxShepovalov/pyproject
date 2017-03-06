class object:
	def __init__(self, name, data):
		self.name = name
		self.data = data
		self.type = "file"

	def getSize(self):
		return 0 #retrun 0 as it is not a folder

	def getName(self):
		return self.name

class folder:
	def __init__(self, name):
		self.name = name
		self.data = []
		self.type = "folder"

	def getName(self):
		return self.name

	def getSize(self):
		val = len(data)
		for i in self.data:
			val += i.getSize()
		return val

	def newObject(self, nobj):
		for k in self.data:
			if k.name == nobj.name:
				print str(nobj.name) + " already exist!"
				return
		self.data.append(nobj)
		return self.data[len(self.data)-1]

	def getItem(self, iname):
		if iname == "":
			retrun self
		for k in self.data:
			if k.name == iname:
				return k
		print "No such item: " + str(iname)

	def getList(self):
		out = []
		for i in self.data:
			out.append(i.name)
		return out

class server:
	def __init__(self, publ_name):
		self.commands = ["getlist", "stop", "getfile"]
		self.state = False
		self.name = publ_name
		self.data = folder("")

	def find(self, path):
		#"/f1/f2/fl.txt"
		obj = path.split("/")
		pntr = self.data
		for p in obj:
			nptr = pntr.getItem(p)
			pntr = nptr
			if pntr == None:
				break
		return pntr

	def getList(self, path):
		ptr = self.find(path)
		if ptr != None:
			return ptr.getList()
		return

	def uploadItem(self, obj):
		run = True
		ptr = obj
		while run:
			if ptr.type == "file":
				

FS1 = folder("test")
FS1_f = FS1.newObject(folder("subfodler"))
FS1_f.newObject(object("example.txt", "This is a text"))
FS1.newObject(object("test.txt", "done well"))
