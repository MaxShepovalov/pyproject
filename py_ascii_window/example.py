import time
from window import *

can = canvas(190,40)

bx = box()
bx.size(10,5)
bx.symbH = '*'
bx.symbV = '*'
bx.symbC = '*'

txt = textbox('Some text and line', 9, 2)
bx.tbox.write('This is some text in a box on multiple lines')


for i in range(0,40):
	can.clear()
	can.set_cursor(0,0)
	if i < 10:
		bx.pos(i,i)
	elif i < 20:
		bx.size(i,i)
	else:
		bx.tbox.write('New text. Iteration %d' % i)
	txt.project(can)
	bx.project(can)

	can.draw()
	time.sleep(0.05)
