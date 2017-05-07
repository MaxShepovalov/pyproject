def translate(txt):
	bn = ''
	for ch in txt:
		num = ord(ch)
		bn += bin(num)[2:]
	return bn

def compress(btxt):
	tkn = btxt[0]
	out = 'start="'+tkn+'"'
	ctr = 1
	for ch in btxt[1:]:
		if ch==tkn:
			ctr+=1
		else:
			tkn = ch
			out += ','+str(ctr)
			ctr = 1
	return out

text = raw_input("write message> ")
bin_text = translate(text)
print "Result: ",bin_text
print "length ",len(bin_text)
cmp_txt = compress(bin_text)
print "compressed: ",cmp_txt
