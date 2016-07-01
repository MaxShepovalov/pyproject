import time
from window import *

can = canvas(6,5)

number = box()
number.size(3,1)

letter = box()
letter.size(3,1)
letter.pos(0,2)

slide = textbox('||#||', 1, 5)

num = 888
msg = '???'
number.tbox.write('%d' % num)
letter.tbox.write(msg)

can.set_cursor(0,0)
number.project(can)
letter.project(can)
can.set_cursor(5,0)
slide.project(can)	
can.draw()

time.sleep(2)

for i in range(100,125):
	can.clear()

	number.tbox.write('%d' % i)
	letter.tbox.write(chr(i))

	if i < 105:
		slide.write('#||||')
	elif i < 110:
		slide.write('|#|||')
	elif i < 115:
		slide.write('||#||')
	elif i < 120:
		slide.write('|||#|')
	else:
		slide.write('||||#')

	can.set_cursor(0,0)
	number.project(can)
	letter.project(can)
	can.set_cursor(5,0)
	slide.project(can)	
	can.draw()

	time.sleep(0.1)
