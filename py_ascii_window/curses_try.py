import curses as cs
from curses import panel as pnl

#init screen
scr = cs.initscr()
scr.keypad(1)
cs.noecho()
cs.curs_set(False)

cs.start_color()
cs.init_pair( 1, cs.COLOR_BLACK, cs.COLOR_GREEN)

window = cs.newwin(5,5,3,5)
window.box()
panel = pnl.new_panel(window)

window2 = cs.newwin(15,15,2,4)
window2.box()
window2.addstr(1,1,'Back window')
panel2 = pnl.new_panel(window2)

running = True
while running:
    pnl.update_panels()
    cs.doupdate()
    key = scr.getch()
    if key == 27:
        running = False
    if key == ord('w'):
        window.bkgd(' ', cs.color_pair(1))
    if key == ord('s'):
        window.bkgd(' ', cs.color_pair(1) + cs.A_REVERSE)
    if key == ord('1'):
        panel.move(1,1)
        panel.top()
    if key == ord('2'):
        panel.move(3,5)
        panel.top()
    if key == ord('3'):
        panel2.top()

scr.addstr(0,0,'EXITING...')
cs.endwin()
