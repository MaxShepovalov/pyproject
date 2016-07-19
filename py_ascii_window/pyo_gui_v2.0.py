import curses
import time

deviceName = ['Input', 'Delay', 'Disto', 'MonoToStereo', 'Out']
deviceMax = len(deviceName)

FRAME_X = 20

#buttons
#read setup

#open()
KEY_UP = 65 #curses.KEY_UP
KEY_DOWN = 66 #curses.KEY_DOWN
KEY_LEFT = 68 #curses.KEY_LEFT
KEY_RIGHT = 67 #curses.KEY_RIGHT
KEY_RETURN = 10

#read schema
schema = [0,2,3,4,-1]
select = 0

#init
scr = curses.initscr()
curses.cbreak()
curses.noecho()

#windows
arrowL = scr.subwin(2,2, 0,0)
arrowL.addstr(0,0,'<')
arrowR = scr.subwin(2,2, 0,FRAME_X)
arrowR.addstr(0,0,'>')
selected = scr.subwin(3,FRAME_X, 0,2)
devlist = scr.subwin(7, FRAME_X, 0, FRAME_X + 5)
params = scr.subwin(5, FRAME_X + 3, 3,0)

#functions
def screenRefresh():
	scr.refresh()
	selected.border()
	devlist.border()
	params.border()
	selected.refresh()
	devlist.refresh()
	arrowL.refresh()
	arrowR.refresh()
	params.refresh()

#code
screenRefresh()
time.sleep(2)

#end
curses.echo()
curses.endwin()