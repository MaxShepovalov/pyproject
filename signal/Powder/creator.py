import bson
import bz2
import sys

#############################################

#SETUP
gravEnabled = False
AirMode = 0
gravMode = 0
paused = False
legacy = False
heat = False

#version
VERSION = 91
ver2 = 5
buildN = 330
modN = 0

#geometry
CELL = 4
bW = 1
bH = 1

#############################################

if len(sys.argv)<2:
	print "give me a name of file to write"
	exit()

Fname = sys.argv[1]
if Fname[-4:]!=".stm":
	Fname += ".stm"
if len(Fname)>14:
	Fname = Fname[:10] + ".stm"
while len(Fname)<14:
	Fname = "0"+Fname


def pos(x,y):
	if y>bH*CELL:
		print("asced for Y position outside of world. (%d:%d)" % (x,y))
		exit()
	if x>bW*CELL:
		print("asced for X position outside of world. (%d:%d)" % (x,y))
		exit()
	return y*bW*CELL+x

#real data
rdata = dict()
rdata[u'origin'] = dict()
rdata[u'origin'][u'majorVersion'] = VERSION
rdata[u'origin'][u'minorVersion'] = ver2
rdata[u'origin'][u'builtType'] = u'SSE2'
rdata[u'origin'][u'builtNum'] = buildN
rdata[u'origin'][u'releaseType'] = u'R'
rdata[u'origin'][u'platform'] = u'MACOSX'
rdata[u'origin'][u'snapshotId'] = 0
rdata[u'origin'][u'modId'] = modN
rdata[u'partsPos'] = ""
rdata[u'gravityEnable'] = gravEnabled
rdata[u'legacyEnable'] = legacy
rdata[u'airMode'] = AirMode
rdata[u'paused'] = paused
rdata[u'parts'] = ""
rdata[u'waterEEnabled'] = False
rdata[u'aheat_enable'] = heat
rdata[u'gravityMode'] = gravMode
rdata[u'edgeMode'] = 256
rdata[u'minimumVersion'] = dict()
rdata[u'minimumVersion'][u'major'] = 90
rdata[u'minimumVersion'][u'minor'] = 2

#fill blank place
#for i in range(bW*bH*CELL*CELL):
#for i in range(bW*CELL):
#	rdata["partsPos"] += '\x00'
#	rdata["partsPos"] += '\x00'
#	rdata["partsPos"] += '\x00'

#put data
MATERIAL = 0x7d
Temp = 0x20
#fill exact particles
ctype = 1
print "create box %dx%d" % (bW,bH)
for i in range(bH*bW*CELL*CELL):
	rdata["partsPos"] += '\x00'
	rdata["partsPos"] += '\x00'
	rdata["partsPos"] += '\x01'
	rdata["parts"] += '\x7d'
	rdata["parts"] += '\x00'
	rdata["parts"] += '\x00'
	rdata["parts"] += '\x01'
	#rdata["parts"] += chr(Temp)
	#if ctype <= 0xff:
	#	rdata["parts"] += '\x00'
	#	rdata["parts"] += '\x01'
	#	rdata["parts"] += chr(ctype)
	#else:
	#	rdata["parts"] += '\x02'
	#	rdata["parts"] += '\x01'
	#	#rdata["parts"] += chr( ctype&0xff)
	#	#rdata["parts"] += chr((ctype>>24)&0xff)
	#	#rdata["parts"] += chr((ctype>>16)&0xff)
	#	#rdata["parts"] += chr((ctype>>8)&0xff)
	#ctype *= 2

#for i in range(2*bW*CELL+2):
#	rdata["partsPos"] += '\x00'
#	rdata["partsPos"] += '\x00'
#	rdata["partsPos"] += '\x00'


#calc uncompressed data
udata = bson.dumps(rdata)

#calc data
data = bz2.compress(udata)

#calc flags
FLAG = 0
if gravEnabled:
	FLAG |= 1<<7
if paused:
	FLAG |= 1<<1
if legacy:
	FLAG |= 1
FLAG |= AirMode<<4
FLAG |= gravMode<<2

#output to the file
output = "OPS"					#0,1,2
output += chr(0x31)				#3
output += chr(VERSION)			#4
output += chr(CELL)				#5
output += chr(bW)				#6
output += chr(bH)				#7
size = len(udata)
output += chr(size&0xff)		#8
output += chr((size>>8)&0xff)	#9
output += chr((size>>16)&0xff)	#10
output += chr((size>>24)&0xff)	#11
output += data					#12-eof

f1 = open(Fname, 'w')
f1.write(output)
f1.close()




