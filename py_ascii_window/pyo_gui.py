import curses
import time

#buttons
KEY_UP = 65 #curses.KEY_UP
KEY_DOWN = 66 #curses.KEY_DOWN
KEY_LEFT = 68 #curses.KEY_LEFT
KEY_RIGHT = 67 #curses.KEY_RIGHT
KEY_RETURN = 10

scr = curses.initscr()
curses.cbreak()
curses.noecho()
#scr.keypad(1)

W_X = 20
W_Y = 7

def PlainWin(num):
    win = scr.subwin(W_Y, W_X, (num-1)*W_Y, 0)
    return win

devName = ['Input', 'Delay', 'Disto', 'MonoToStereo', 'Out']
maxdev = len(devName)

schema = [-1]

w = []
w.append(PlainWin(1))
devN = 1
select = 0

scr.refresh()

key = ''
while key != ord('q'):
    key = scr.getch()
    if key == KEY_UP and select > 0:
        select = select - 1
    elif key == KEY_DOWN and select < devN - 1:
        select = select + 1
    elif key == KEY_LEFT and schema[select] > 0:
        schema[select] = schema[select] - 1
    elif key == KEY_RIGHT and schema[select] != -1 and schema[select] < maxdev - 1:
        schema[select] = schema[select] + 1
    elif key == KEY_RETURN:
        if schema[select] == -1:
            schema[select] = 0
            w.append(PlainWin(devN+1))
            schema.append(-1)
            devN = devN + 1

    #print('%d presed, %d selected, device %s' % (key, select, devName[schema[select]]))

    for wnum in range(0, devN):
        w[wnum].erase()
        w[wnum].border()
        w[wnum].refresh()
        txt = w[wnum].derwin(W_Y - 2, W_X - 2, 1, 1)
        if wnum == select:
            txt.border()
        if schema[wnum] == -1:
            txt.addstr(1,1,'add device')
        else:
            txt.addstr(1,1, devName[schema[wnum]])
        txt.refresh()

curses.echo()
curses.endwin()