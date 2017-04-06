import pickle
import os
FILE = 'morze_dict.pickle'
d = None
if os.path.isfile(FILE):
	d = pickle.load(open(FILE, 'r'))
else:
	d = dict()

def add(mcode, cval):
	d[mcode]=cval
	d[cval]=mcode

def gettuple(key):
	#return LETTER,MORZE
	try:
		k2 = d[key]
	except KeyError:
		return None
	if len(k2)==1:
		return k2, key
	else:
		return key, k2

def save(file=FILE):
	pickle.dump(d, open(file, 'w'))