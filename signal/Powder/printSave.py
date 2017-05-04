import sys

if len(sys.argv)<4:
	print "Usage: printSave [-hex] <length> <file1> <file2>"
	exit()

try:
	l = int(sys.argv[1])
except ValueError:
	print sys.argv[1] + " - is not a number"
	print "Usage: printSave [-hex] <length> <file1> <file2>"
	exit()

f1 = open(sys.argv[2],'r')
d1 = f1.read()
f1.close()

f1 = open(sys.argv[3],'r')
d2 = f1.read()
f1.close()

d1p = d1
d2p = d2
if '-hex' in sys.argv:
	d1p = ""
	d2p = ""
	for i in range(l):
		num = ord(d1[i])
		num2 = ord(d2[i])
		if num <= 15:
			d1p += "0"
		if num2 <= 15:
			d2p += "0"
		d1p += hex(num)[2:] + " "
		d2p += hex(num2)[2:] + " "

print "1>> len: " + str(len(d1)) + " <start>" + d1p[:l] + "<end>"
print "2>> len: " + str(len(d2)) + " <start>" + d2p[:l] + "<end>"