###
import curses

scr = 0
SIZE_Y = 20
SIZE_X = 40
window = 0

KEY_UP = 259
KEY_DOWN = 258
KEY_LEFT = 260
KEY_RIGHT = 261

def start_code():
	global scr
	global window
	scr = curses.initscr()
	curses.noecho()
	curses.curs_set(True)
	window = curses.newwin(SIZE_Y,SIZE_X,1,1)
	window.keypad(1)

def exit_code():
	curses.echo()
	curses.curs_set(True)
	curses.endwin()

def edit(line):
	prevline = str(line)
	nextline = ""
	start_code()
	window.addstr(0,0, "press ctrl-x to exit")
	window.addstr(1,0, prevline)
	key = 0
	while key != 24 and key != 10:
		key = window.getch()
		if key == 127:
			prevline = prevline[:-1]
		elif key == 330:
			nextline = nextline[1:]
		elif key == KEY_LEFT:
			if prevline != "":
				c = prevline[len(prevline)-1]
				prevline = prevline[:-1]
				nextline = c + nextline
		elif key == KEY_RIGHT:
			if nextline != "":
				c = nextline[0]
				nextline = nextline[1:]
				prevline += c
		elif key != 24 and key != 10 and not key in [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP]:
			prevline += chr(key)
		window.erase()
		#window.addstr(2,0,"%d pressed" % key)
		window.addstr(0,0,"press ctrl-x to exit")
		window.addstr(1,0, prevline + nextline)
		curposX = len(prevline) % SIZE_X
		curposY = len(prevline) / SIZE_X
		window.move(curposY + 1, curposX)
		window.refresh()
	exit_code()
	return prevline + nextline
