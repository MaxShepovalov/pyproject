import bz2
import bson
import sys

def printhex(pref, seq):
	k = 0
	pline = pref
	if type(seq)==str:
		while k < len(seq):
			num = hex(ord(seq[k]))[2:]
			if len(num)==1:
				num = "0" + num
			pline += num
			k += 1
			if not k%15:
				pline += "\n" + pref
			elif not k%3:
				pline += " "
	else:
		pline += str(seq)
	return pline

if len(sys.argv)<2:
	print 'give me an \'stm\' file'
	exit()
name = sys.argv[1]
nl = len(name)
if name[-4:]!=".stm":
	print 'given file is \''+name[-4:]+'\' not stm'
	exit()

f1 = open(name, 'r')
d = f1.read()
f1.close()
name = name[:-4]
data = d[12:]
udata = bz2.decompress(data)
rdata = bson.loads(udata)
KEYS = rdata.keys()

#parsing
output = ""
if d[:3]=="OPS":
	output += "Type: OPS\n"
elif d[:3]=="PSv":
	output += "Type: PSv\n"
else:
	output += "Type: unknown %s" + d[:3]

flags = ord(d[3])
output += "gravEnabled "
if flags&0x80:
	output += "+ , "
else:
	output += "- , "
output += "AirMode "
output += "%d, " % ((flags&0x70)>>4)
output += "gravMode "
output += "%d, " % ((flags&0x0c)>>2)
output += "paused "
if flags&0x02:
	output += "+ , "
else:
	output += "- , "
output += "legasyEnabled "
if flags&0x01:
	output += "+\n"
else:
	output += "-\n"

output += "VERSION = %d\n" % (ord(d[4]))

output += "CELL = %d\n" % (ord(d[5]))

output += "blockW = %d\n" % (ord(d[6]))
output += "blockH = %d\n" % (ord(d[7]))

size = ord(d[8])
size += ord(d[9])<<8
size += ord(d[10])<<16
size += ord(d[11])<<24
output += "BSON length = %d\n" % (size)

output += "\nBSON KEYS: " + str(KEYS) + "\n"

for i in KEYS:
	output += "\n" + i + "\n"
	output += printhex("   ", rdata[i])
	output += "\n"

f2 = open(name+".txt", 'w')
f2.write(output)
f2.close()

