def logprint(msg):
	print "log>" + msg

class Traincart:
	def __init__(self, path, node, pict):
		self.path = path
		self.node = node
		self.icon = pict
	#def moveR():
		#if tracks[path][node+1]!=-1:



# -1 = stop
#  0 = simple way
# [X,Y,side] = intersection
# [id,X,Y,side] = fork #id to track X, that goes to node Y in track X
# track:  [shift, ... path ...]
tracks = [[0,-1,0,0,0,0,0,[0,2,3,1],0,0,-1], [3,[3,3,1],0,0,[1,6,0]], [0,-1,0,0,[1,2,0,0],0,0,0,0,0,0,-1]]
forks = [True, True]
trains = [Traincart(0,2,'A')]

def hasTrain(path, node):
	o = None
	for t in trains:
		if t.path==path and t.node==t.node:
			print "has train at "+str(path)+":"+str(node)
			o = t
			break
	return o

def draw():
	out = ""
	for ti in range(len(tracks)):
		tr = tracks[ti]
		for i in range(tr[0]):
			out += " "
		for i in range(1,len(tr)):
			trn = hasTrain(ti,i+1)
			if trn:
				out+=trn.icon
			elif tr[i]==0:
				out+="="
			elif tr[i]==-1:
				out+="#"
			elif len(tr[i])==3:
				if tr[i][0]-1<ti:
					if tr[i][2]==1:
						out+="\\"
					else:
						out+="/"
				else:
					if tr[i][2]==1:
						out+="/"
					else:
						out+="\\"
			elif len(tr[i])==4:
				if forks[tr[i][0]]:
					if tr[i][1]-1<ti:
						if tr[i][3]==1:
							out+="\\"
						else:
							out+="/"
					else:
						if tr[i][3]==1:
							out+="/"
						else:
							out+="\\"
				else:
					out+="-"
		out += "\n"
	print out

################################

draw()
