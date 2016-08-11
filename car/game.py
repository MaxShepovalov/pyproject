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
curGas = 100.0

frame = 1

NAME = "map1.m"

tiles = []
links = []
#def safeFile(patt, name):
#	file = open(name, 'w')
#	for i in patt:
#		file.write("%d\n" % i)

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
		log("No such file or directory: %s." % name)
		tiles.append(25)
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
		out = "#/ /[ ]%d#" % lnk#new road
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
		out = "#%d|   |%d#" % (lnk, lnk)
	elif num==16:
		out = "#%d| | |%d#" % (lnk, lnk)
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
		out = "#%d     %d#" % (lnk, lnk) #intersection mid1
	else:
		out = "empty"
	return out

def log(msg):
    scr.move(0,0)
    scr.erase()
    scr.addstr(0,0,msg)

def getDGas():
	x = curSpeed - 4
	return 0.04 + (x*(x*x-4))/3500

scr = curses.initscr()
scr.keypad(1)
curses.noecho()
curses.curs_set(False)
curses.halfdelay(frame)
road = curses.newwin(16,16,1,1)
road_panel = panel.new_panel(road)
road_panel.show()

run = True
if __name__ == "__main__":
	if len(sys.argv)==2:
		NAME = sys.argv[1]

openFile(NAME)
curTile = 0
curLine = 4
itr = 0
next_move = 1
while run:
	road.erase()
	#load new location if necessary
	if tiles[curTile]==15 or tiles[curTile]==16:
		if curLine==0 or curLine==6:
			if links[curTile]!=0:
				NAME = "map%d.m" % links[curTile]
				openFile(NAME)
				curLine = 6
				curTile = 0
	elif tiles[curTile]==24 and (curLine==0 or curLine==6):
		if links[curTile]!=0:
			oldMap = int(NAME[3])
			NAME = "map%d.m" % links[curTile]
			openFile(NAME)
			curLine = 4
			for inter in range(0,len(tiles)):
				if tiles[inter]==24 and links[inter]==oldMap:
					curTile=inter+2
					break
	#calculate gas
	if curGas > 0:
		curGas += getDGas()
	#apply speed (vertical)
	if itr==next_move and curGas > 0:
		next_move = (next_move+(11-curSpeed)) % 100
		if curSpeed > 0:
			if curTile < len(tiles) - 1:
				curTile += 1
			else:
				curTile = 0
	#apply roadways (horizontal)
	if tiles[curTile]==14:
		curLine = 6
	elif tiles[curTile]==13:
		curLine = 5
	elif tiles[curTile]==12 or tiles[curTile]==11 or tiles[curTile]==10:
		curLine = 4
	#draw dashboard
	log("Spd: %d Gas: %d Mtr:%d/%d iter: %d next: %d" %(curSpeed, int(curGas), curTile, len(tiles), itr, next_move))
	#draw road
	for i in range(0,15):
		t = 7 + curTile - i
		if t<len(tiles) and t>=0:
			road.addstr(i+1,2,getDrawing(tiles[t], links[t]))
			if t==curTile:
				road.addch(i+1,3+curLine,"A",curses.A_REVERSE)
	panel.update_panels()
	curses.doupdate()
	#change parameters if necessary
	key = road.getch()
	if key == ord('q'):
		run = False
	elif key == 260 or key == 68: #left
		itr = (itr+1) % 100
		if curLine > 0:
			curLine -=1
	elif key == 261 or key == 67: #right
		itr = (itr+1) % 100
		if curLine < 6:
			curLine +=1
	elif key == 259 or key == 65: #up
		if curSpeed < 10 and curGas > 0:
			curSpeed += 1
			next_move -= 1
	elif key == 258 or key == 66: #down
		if curSpeed > 0:
			curSpeed -= 1
			next_move += 1
	else:
		itr = (itr+1) % 100

curses.echo()
curses.curs_set(True)
curses.endwin()
