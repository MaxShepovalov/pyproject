from random import random as rand
import curses
import time
import sys

SIZE_X = 30
SIZE_Y = 10
MINE_NUM = 30
mines = []
opened = []
marks = []
screen = ""

scr = curses.initscr()
scr.keypad(1)
curses.noecho()
curses.curs_set(False)
square = curses.newwin(SIZE_Y+3,SIZE_X+3,1,1)
square.keypad(1)

def haveArg(line):
	found = False
	for cmd in sys.argv:
		if cmd == line:
			found = True
			break
	return found

for cmd in sys.argv:
	if cmd not in ["main.py","-h","--help","-n","--no-color"]:
		curses.echo()
		curses.curs_set(True)
		curses.endwin()
		print("miner/main.py: miner game on python language with interface on \"curses\"")
		print("run:\tpython main.py [params]\n")
		print("\t-h --help: show this page")
		print("\t-n --no-color: force standard \"white on black\" style")
		print("####\nUnknown argument: %s" % cmd)
		exit()		

if haveArg("--help") or haveArg("-h"):
	curses.echo()
	curses.curs_set(True)
	curses.endwin()
	print("miner/main.py: miner game on python language with interface on \"curses\"")
	print("run:\tpython main.py [params]\n")
	print("\t-h --help: show this page")
	print("\t-n --no-color: force standard \"white on black\" style")
	exit()
curses.start_color()
if haveArg("--no-color") or haveArg("-n"):
	for i in range(1,11):
		curses.init_pair(i, curses.COLOR_WHITE, curses.COLOR_BLACK)
else:
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_BLACK)

logs = "=================\nNEW STARTED\n=================\n"

class Mine:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.mode = 0

def setup():
	global K_UP
	global K_DW
	global K_LF
	global K_RG
	scr.clear()
	scr.addstr(0,0,"press UP key (press Q for exit)")
	scr.refresh()
	K_UP = scr.getch()
	scr.addstr(0,0,"press DOWN key (press Q for exit)")
	scr.refresh()
	K_DW = scr.getch()
	scr.addstr(0,0,"press LEFT key (press Q for exit)")
	scr.refresh()
	K_LF = scr.getch()
	scr.addstr(0,0,"press RIGHT key (press Q for exit)")
	scr.refresh()
	K_RG = scr.getch()
	log("controls: LEFT %d; RIGHT %d; UP %d; DOWN %d;" % (K_LF, K_RG, K_UP, K_DW))
	scr.clear()
	scr.addstr(0,0,"to reset controls, press R")
	scr.refresh()

def log(msg):
	global logs
	if msg[len(msg)-1]=='\n':
		logs += msg
	else:
		logs += msg+'\n'

def logArray(arr, msg):
	log("\nlogArray [%s]:" % msg)
	for i in range(0,len(arr)):
		log("%d: (%d,%d)" % (i, arr[i].x, arr[i].y))

def terminate():
	try:
		curses.echo()
		curses.curs_set(True)
		curses.endwin()
	except NameError:
		log("curses not initialysed yet. exit anyway")
		pass
	#logArray(mines, "mines")
	#logArray(marks, "marks")
	#logArray(opened,"opened tiles")
	print(logs)
	exit()

def printWin(lines):
	log("print screen:\n%s" % screen)
	square.clear()
	x=0
	y=0
	square.addstr(0,0,"mines %d" % (MINE_NUM - len(marks)))
	for i in screen:
		if ord(i) in range(48,58):
			square.addch(y+1,x,i,curses.color_pair(int(i)))
		elif i == '~':
			square.addch(y+1,x,i,curses.color_pair(9))
		elif i == 'x' or i == '@':
			if not play:
				square.addch(y+1,x,i,curses.color_pair(9)+curses.A_BLINK)
			else:
				square.addch(y+1,x,i,curses.color_pair(5)+curses.A_BLINK)
		elif i == ' ' or i == '!' or i == '?':
			square.addch(y+1,x,i)
		else:
			continue
		x+=1
		if x==SIZE_X:
			x=0
			y+=1
	square.refresh()

def drawCursor(x,y):
	log("add cursor at %d:%d (character %d from %d)" % (x,y, 1+x+(SIZE_X+3)*y, len(screen)))
	if (1+x+(SIZE_X+3)*y)<len(screen):
		tile = screen[1+x+(SIZE_X+3)*y]
	else:
		log("   out of border")
		tile = "E"
	printWin(screen)
	if ord(tile) in range(48,58):
		square.addch(y+1,x,tile, curses.color_pair(int(tile))+curses.A_REVERSE)
	elif tile == '~':
		square.addch(y+1,x,tile, curses.color_pair(9)+curses.A_REVERSE)
	elif tile == 'x' or tile == 'E' or tile == '@':
		square.addch(y+1,x,tile, curses.color_pair(5)+curses.A_BLINK+curses.A_REVERSE)
	elif tile == ' ' or tile == '!' or tile == '?':
		square.addch(y+1,x,tile, curses.A_REVERSE)
	square.refresh()

def arraySearch(arr, x,y):
	for i in range(0,len(arr)):
		if arr[i].x==x and arr[i].y==y:
			return i
	return -1

def addMine(x,y):
	log("new mine at %d:%d" % (x,y))
	global mines
	if not haveMine(x,y):
		mines.append(Mine(x,y))
	else:
		log("mine already exists")

def addMark(x,y):
	log("new mark at %d:%d" % (x,y))
	if openedTile(x,y):
		log("   can't mark opened tile")
	else:
		global marks
		found = False
		i = 0
		while i < len(marks):
			log("   checking mark#%d (%d:%d)" % (i, marks[i].x, marks[i].y))
			if marks[i].x==x and marks[i].y==y:
				log("   this mark exists. Upgrading to mode 1")
				if marks[i].mode == 0:
					marks[i].mode = 1
				else:
					log("   already have mode 1. deleting # %d / %d" % (i, len(marks)))
					del marks[i]
					i-=1
				found = True
			i+=1
		if not found:
			marks.append(Mine(x,y))

def haveMine(x,y):
	return arraySearch(mines, x, y) != -1;

def openedTile(x,y):
	return arraySearch(opened, x, y) != -1;

def markedTile(x,y):
	return arraySearch(marks, x, y) != -1;

def countNum(x,y):
	num = 0
	if not openedTile(x,y):
		if markedTile(x,y):
			num = -2
	else:
		if haveMine(x,y):
			num = -1
		else:
			for i in range(x-1,x+2):
				for j in range(y-1,y+2):
					if haveMine(i,j):
						num += 1
	return num

def showMap():
	log("prepare screen string")
	global screen
	screen = ""
	for i in range(0,SIZE_Y):
		screen = screen + "|"
		for j in range(0,SIZE_X):
			val = countNum(j,i)
			if openedTile(j,i):
				if val==-1:
					screen = screen + "x"
				elif val==0:
					screen = screen + " "
				elif val in range(0,10):
					screen = screen + str(val)
				else:
					log("ERROR: wrong num at %d:%d [%d]" % (j,i,val))
					screen = screen + '@'
			else:
				if val==-2:
					if marks[arraySearch(marks, j,i)].mode == 0:
						screen = screen + "!"
					if marks[arraySearch(marks, j,i)].mode == 1:
						screen = screen + "?"
				else:
					screen = screen + '~'
		screen = screen + "|\n"
	printWin(screen)

def showMines():
	global opened
	log("uncover mines")
	for i in mines:
		if not openedTile(i.x,i.y):
			opened.append(Mine(i.x,i.y))
	printWin(screen)

def hideMines():
	global opened
	log("cover mines")
	for i in mines:
		trg = arraySearch(opened, i.x, i.y)
		if trg != -1:
			del opened[trg]
			

def openTile(x,y):
	if x>=0 and x<SIZE_X and y>=0 and y<SIZE_Y:
		if not haveMine(x,y):
			if not openedTile(x,y):
				if markedTile(x,y):
					try:
						addMark(x,y)
					except IndexError:
						log("INDEX ERROR OCCURED terminating")
						terminate();
				opened.append(Mine(x,y))
				if countNum(x,y)==0:
					openTile(x-1,y-1)
					openTile(x-1,y)
					openTile(x-1,y+1)
					openTile(x,y-1)
					openTile(x,y+1)
					openTile(x+1,y-1)
					openTile(x+1,y)
					openTile(x+1,y+1)

def step(x,y):
	log("step at %d:%d" % (x,y))
	global opened
	if not markedTile(x,y):
		openTile(x,y)
		onmine = haveMine(x,y)
		if onmine:
			log("mine is touched")
		return not onmine
	else:
		return True

filled = False
def fillMap(x,y,num):
	log("filling %d mines from %d:%d" % (num, x,y))
	global filled
	global mines
	while len(mines) < num:
	#for i in range(0,30):
		mx = int(SIZE_X*rand())
		my = int(SIZE_Y*rand())
		if mx!=x or my!=y:
			addMine(mx, my)
		else:
			log("attempt to add mine on start vector")
	filled = True

def checkWinner():
	log("checking if won")
	win = True
	for i in range(0,SIZE_Y):
		for j in range(0,SIZE_X):
			if openedTile(j,i):
				if haveMine(j,i):
					log("mined tile (%d:%d) was opened" % (j,i))
					win = False
					break
			else:
				if not haveMine(j,i):
					log("clear tile (%d:%d) is closed" % (j,i))
					win = False
					break
		if win==False:
			break
	return win

#####setup
K_UP = 259
K_DW = 258
K_LF = 260
K_RG = 261

if (MINE_NUM+1 > SIZE_X*SIZE_Y):
	log("Filed %dx%d is too small for %d mines" % (SIZE_X, SIZE_Y, MINE_NUM))
	terminate()

play = True
curX = 0
curY = 0
showMap()
scr.clear()
scr.addstr(0,0,"to reset controls, press R")
scr.refresh()
TIME_start = time.time()
while play:
	showMap()
	drawCursor(curX,curY)
	key = square.getch()
	if key == 10:
		log("ENTER pressed at %d:%d" % (curX, curY))
		if filled:
			if not openedTile(curX, curY):
				play = step(curX, curY)
			else:
				#check marks
				Mnum = 0
				for i in range(curY-1,curY+2):
					for j in range(curX-1,curX+2):
						if markedTile(j,i):
							Mnum += 1
				if Mnum == countNum(curX,curY):
					play = play and step(curX-1,curY-1)
					play = play and step(curX  ,curY-1)
					play = play and step(curX+1,curY-1)
					play = play and step(curX-1,curY)
					play = play and step(curX+1,curY)
					play = play and step(curX-1,curY+1)
					play = play and step(curX  ,curY+1)
					play = play and step(curX+1,curY+1)
		else:
			fillMap(curX, curY, MINE_NUM)
			step(curX, curY)
	elif key == ord('q'):
		log("exit (Q) pressed")
		play = False
	elif key == K_UP:
		log("UP pressed at %d:%d" % (curX, curY))
		if curY > 0:
			curY -= 1
	elif key == K_DW:
		log("DOWN pressed at %d:%d" % (curX, curY))
		if curY < SIZE_Y-1:
			curY += 1
	elif key == K_LF:
		log("LEFT pressed at %d:%d" % (curX, curY))
		if curX > 0:
			curX -= 1
	elif key == K_RG:
		log("RIGHT pressed at %d:%d" % (curX, curY))
		if curX < SIZE_X-1:
			curX += 1
	elif key == 32:
		log("MARK pressed at %d:%d" % (curX, curY))
		addMark(curX, curY)
	elif key == ord('r') or key == ord('R'):
		setup()
	else:
		log("%d pressed" % key)

	if key==ord('p'):
		log("cheat applied")
		showMines()
	else:
		hideMines()

	if checkWinner():
		log("All mines found")
		play = False

#game ended

scr.clear()
scr.addstr(0,0,"Game ended, press 1 to see logs. Any key to close")
scr.refresh()

if checkWinner():
	TIME_spend = time.time() - TIME_start
	showMines()
	showMap()
	scrwin = 0
	scrYwin = int(SIZE_Y/2)
	if SIZE_X >= 8:
		scrwin = int((SIZE_X - 7)/2)
		square.addstr(scrYwin-1,scrwin,"#######", curses.color_pair(10)+curses.A_REVERSE)
		square.addstr(scrYwin,scrwin,"# WIN #", curses.color_pair(10)+curses.A_REVERSE)
		square.addstr(scrYwin+1,scrwin,"#######", curses.color_pair(10)+curses.A_REVERSE)
		if TIME_spend > 999:
			square.addstr(scrYwin+2,scrwin,"slowpoke" % int(TIME_spend), curses.color_pair(10)+curses.A_REVERSE)
		else:
			square.addstr(scrYwin+2,scrwin,"%d secs" % int(TIME_spend), curses.color_pair(10)+curses.A_REVERSE)
	else:
		square.addstr(scrYwin,scrwin,"WIN", curses.color_pair(10)+curses.A_REVERSE)
		if TIME_spend > 999:
			square.addstr(scrYwin+1,scrwin,"---", curses.color_pair(10)+curses.A_REVERSE)
		else:
			square.addstr(scrYwin+1,scrwin,"%d" % int(TIME_spend), curses.color_pair(10)+curses.A_REVERSE)

	square.refresh()
else:
	play = True
	showMines()
	showMap()
	scr.clear()
	scr.addstr(0,0,"You loose! Game ended, press 1 to see logs. Any key to close")
	scr.refresh()
	showMap()

key = square.getch()

curses.echo()
curses.curs_set(True)
curses.endwin()

if key==ord('1'):
	log("request to print logs")
	print(logs)
