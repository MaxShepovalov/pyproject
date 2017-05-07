from PIL import Image, ImageDraw

outname = "gif.lua"
out = "GIFOS!"

#open image
im = Image.open('news.gif')
rgb_im = im.convert('RGB')
w, h = im.size

##analyze background
background = '0x'
hist = dict()
for x in range(w):
    for y in range(h):
        r, g, b = rgb_im.getpixel((x, y))
        clr = ""
        clr += "{0:#0{1}x}".format(r,4)[2:]
        clr += "{0:#0{1}x}".format(g,4)[2:]
        clr += "{0:#0{1}x}".format(b,4)[2:]
        clr = "0x"+clr.upper()
        if clr in hist.keys():
            hist[clr] += 1
        else:
            hist[clr] = 1
import operator
background = max(hist.iteritems(), key=operator.itemgetter(1))[0]
out +=','
out += background
#out += chr((int(background[2],16)<<4)+int(background[3],16))
#out += chr((int(background[4],16)<<4)+int(background[5],16))
#out += chr((int(background[6],16)<<4)+int(background[7],16))

#fill colors
out +=','
colors = hist.keys()
print 'write ',len(colors),' colors'
for i in colors:
    #print 'Process: ',i
    out += i[2:]
    #out += chr((int(i[2],16)<<4)+int(i[3],16))
    #out += chr((int(i[4],16)<<4)+int(i[5],16))
    #out += chr((int(i[6],16)<<4)+int(i[7],16))

#fill items
out +=','
x,y = 0,0
i = 1
lastcolor = '0x'
lastx, lasty = 0, 0
cntr = 0
while x in range(w):
    while y in range(h):
        r, g, b = rgb_im.getpixel((x, y))
        clr = ""
        clr += "{0:#0{1}x}".format(r,4)[2:]
        clr += "{0:#0{1}x}".format(g,4)[2:]
        clr += "{0:#0{1}x}".format(b,4)[2:]
        clr = "0x"+clr.upper()
        #if clr!=background:
        if lastcolor == '0x':
            lastcolor = clr
        if lastcolor != clr or (x == w-1 and y == h-1):
            #out+='map['+str(i)+']={'+str(x/2)+','+str(y/2)+','+lastcolor+', '+str(cntr)+'}\n'
            out += "{0:#0{1}x}".format(cntr,6)[2:]
            clrind = colors.index(lastcolor)
            out += "{0:#0{1}x}".format(clrind,4)[2:]
            i += 1
            cntr = 1
            lastx = x
            lasty = y
            lastcolor = clr
        else:
            cntr += 1
        #end of if
        y += 2
    y = 0
    out+='-'
    x += 2
if cntr!=1:
    print 'EXIT ERROR'

file = open(outname, 'w')
file.write(out)
file.close()
print 'done'