import curses
import sys
from curses import panel
from os.path import isfile

#global var
curRoad = 0
curTile = 0
onRoad = False
curSpeed = 0
curLine = 0

NAME = "map1.m"

tiles = []
links = []
def safeFile(patt, jump, name):
	file = open(name, 'w')
	#check links
	#for i in patt:
	#	if i==15 or i==16:
	#		print("Tile #%d", )
	for i in range(0,len(patt)):
		file.write("%d %d\n" % (patt[i], jump[i]))
	file.close()

def openFile(name):
	global tiles
	global links
	tiles = []
	links = []
	if isfile(name):
		file = open(name, 'r')
		for line in file:
			TL, LN = line.split()
			tiles.append(int(TL))
			links.append(int(LN))
		file.close()
	else:
		log("No such file or directory: %s. Will create new file." % name)
		tiles.append(1)
		links.append(0)

def getDrawing(num, lnk):
	out = "error (%d)" % num
	if num==0:
		out = "#       #"
	elif num==1:
		out = "# [   ] #"
	elif num==2:
		out = "# [ | ] #"
	elif num==3:
		out = "#/[   ]\#"
	elif num==4:
		out = "#/[ | ]\#"
	elif num==5:
		out = "#.[   ].#" #market
	elif num==6:
		out = "#.[ | ].#" #market
	elif num==7:
		out = "#\[   ]/#"
	elif num==8:
		out = "#\[ | ]/#"
	elif num==9:
		out = "#/ /[ ]%d#" % lnk #new road
	elif num==10:
		out = "# / [ ] #"
	elif num==11:
		out = "#/  [ ] #"
	elif num==12:
		out = "#   [ ] #"
	elif num==13:
		out = "#    [ ]#"
	elif num==14:
		out = "#     [ #"
	elif num==15:
		out = "#%d|   |%d#" % (lnk, lnk)#exit
	elif num==16:
		out = "#%d| | |%d#" % (lnk, lnk)#exit
	elif num==17:
		out = "#\     /#"
	elif num==18:
		out = "#\  |  /#" #intersection start
	elif num==19:
		out = "#={===}=#"
	elif num==20:
		out = "# [ | ]X#"
	elif num==21:
		out = "# [   ]X#"
	elif num==22:
		out = "#/  |  \#" #intersection end
	elif num==23:
		out = "#_     _#" #intersection mid2
	elif num==24:
		out = "#%d     %d#" % (lnk, lnk)#intersection mid1
	else:
		out = "empty"
	return out

def log(msg):
	scr.move(0,0)
	scr.erase()
	scr.addstr(0,0,msg)

scr = curses.initscr()
scr.keypad(1)
curses.noecho()
curses.curs_set(False)
road = curses.newwin(16,16,1,1)
road_panel = panel.new_panel(road)
road_panel.show()

run = True
if __name__ == "__main__":
	if len(sys.argv)==2:
		NAME = sys.argv[1]

openFile(NAME)
while run:
	road.erase()
	for i in range(0,15):
		t = 7 + curTile - i
		if t<len(tiles) and t>=0:
			if t==curTile:
				road.addstr(i+1,1,">%s" % getDrawing(tiles[t], links[t]))
			else:	
				road.addstr(i+1,2,getDrawing(tiles[t], links[t]))
	panel.update_panels()
	curses.doupdate()
	key = road.getch()
	log("%d was pressed" % key)
	if key == ord('q'):
		run = False
	elif key == 260 or key == 68: #left
		tiles[curTile] -= 1
		if tiles[curTile] < 0:
			tiles[curTile] = 24
	elif key == 261 or key == 67: #right
		tiles[curTile] += 1
		if tiles[curTile] > 24:
			tiles[curTile] = 0
	elif key == 259 or key == 65: #up
		curTile += 1
		while curTile >= len(tiles):
			tiles.append(1)
			links.append(0)
	elif key == 258 or key == 66: #down
		curTile -= 1
		if curTile < 0:
			curTile = len(tiles) - 1

curses.echo()
curses.curs_set(True)
curses.endwin()

safeFile(tiles, links, NAME)

#00#0123456
#01# [ | ]
#02#/[   ]\
#03#.[ | ]. #market
#04#\[   ]/
#05# [ | ]
#06# [ | ]
#07#/ /[ ]?	#new road
#08# / [ ]
#09#/  [ ]
#00#    [ ]
#11#     [
#12#     [ 
#13#?|   |? #driveway
#14#?| | |? #driveway
#15#?     ? #driveway
#16#?| | |? #driveway
#17#\     /
#18# [ | ]
#19#={===}=
#10# [ | ]
#21# [ | ]X
#22#/  |? \ #intersection
#23#_     _ #intersection
#24#?     ? #intersection
#25#\  |  / #intersection
#26# [ | ]
#27# [ | ]
