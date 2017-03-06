LOG = ""
def log(msg):
	global LOG
	LOG += str(msg)+"\n"

def offset(i,j):
	return 8*i+2*j

def find(needle, haystack):
	needle_obj = None
	for i in range(len(haystack)):
		if haystack[i]==needle:
			needle_obj = i
			break
	return needle_obj

def checkmiss(obj):
	global miscount
	global hitcount
	miss_hit = "miss"
	if obj[:2] in cache:
		miss_hit = "hit"
		hitcount += 1
	else:
		miscount += 1
	return miss_hit

#fully associative
def use(obj):
	trg = find(-2, LRU)
	if not trg:
		trg = find(max(LRU), LRU)
	if obj[:2] not in cache:
		cache[trg] = obj[:2]
		LRU[trg] = -1
	#if getLRU()==obj[:2]:
	else:
		rst = find(obj[:2], cache)
		LRU[rst] = -1
	for k in range(len(LRU)):
		if LRU[k]!=-2:
			LRU[k]+=1
def getLRU():
	trg = find(max(LRU), LRU)
	return cache[trg]

#direct mapped
def load(obj):
	row = int(obj[1])
	col = int(obj[2])
	start = int("0x1000",16)
	if obj[0]=="B":
		start = int("0x2000",16)
	start += offset(row-1,col-1)
	index = (start>>3)&0x3
	cache[index] = obj[:2]

log("DIRECT MAPPED CACHE ____ NON BLOCKED")
cache = ["--","--","--","--"]
LRU = [-2,-2,-2,-2]
miscount = 0
hitcount = 0
for i in range(4):
	for j in range(4):
		#read A
		obj = "A"+str(i+1)+str(j+1)
		log(str(cache) + "\t\t" + "Read " + obj + "\t" + checkmiss(obj))
		load(obj)
		#write B
		obj = "B"+str(j+1)+str(i+1)
		log(str(cache) + "\t\t" + "Write " + obj + "\t" + checkmiss(obj))
		load(obj)
log("Hits: " + str(hitcount) + "; Misses: " + str(miscount))

log("FULLY ASSOCIATIVE CACHE ____ NON BLOCKED")
cache = ["--","--","--","--"]
LRU = [-2,-2,-2,-2]
miscount = 0
hitcount = 0
for i in range(4):
	for j in range(4):
		#read A
		obj = "A"+str(i+1)+str(j+1)
		log(str(cache) + "\t\t" + "Read " + obj + "\t" + getLRU() + "\t" + checkmiss(obj))
		use(obj)
		#write B
		obj = "B"+str(j+1)+str(i+1)
		log(str(cache) + "\t\t" + "Write " + obj + "\t" + getLRU() + "\t" + checkmiss(obj))
		use(obj)
log("Hits: " + str(hitcount) + "; Misses: " + str(miscount))

log("DIRECT MAPPED CACHE ____ BLOCKED")
cache = ["--","--","--","--"]
LRU = [-2,-2,-2,-2]
miscount = 0
hitcount = 0
for i in [0,2]:
	for j in [0,2]:
		for ii in [i,i+1]:
			for jj in [j,j+1]:
				#read A
				obj = "A"+str(ii+1)+str(jj+1)
				log(str(cache) + "\t\t" + "Read " + obj + "\t" + checkmiss(obj))
				load(obj)
				#write B
				obj = "B"+str(jj+1)+str(ii+1)
				log(str(cache) + "\t\t" + "Write " + obj + "\t" + checkmiss(obj))
				load(obj)
log("Hits: " + str(hitcount) + "; Misses: " + str(miscount))

log("FULLY ASSOCIATIVE CACHE ____ BLOCKED")
cache = ["--","--","--","--"]
LRU = [-2,-2,-2,-2]
miscount = 0
hitcount = 0
for i in [0,2]:
	for j in [0,2]:
		for ii in [i,i+1]:
			for jj in [j,j+1]:
				#read A
				obj = "A"+str(ii+1)+str(jj+1)
				log(str(cache) + "\t\t" + "Read " + obj + "\t" + getLRU() + "\t" + checkmiss(obj))
				use(obj)
				#write B
				obj = "B"+str(jj+1)+str(ii+1)
				log(str(cache) + "\t\t" + "Write " + obj + "\t" + getLRU() + "\t" + checkmiss(obj))
				use(obj)
log("Hits: " + str(hitcount) + "; Misses: " + str(miscount))

print LOG