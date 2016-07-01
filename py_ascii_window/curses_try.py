import curses

#init screen
scr = curses.initscr()

#no echo for input
#cs.noecho()

#cancel Enter for input
curses.cbreak()

#allow curses to track noncharacter keys
scr.keypad(1)

#CODE START

pad = curses.newpad(100, 100)
#  These loops fill the pad with letters; this is
# explained in the next section
for y in range(0, 100):
    for x in range(0, 100):
        try:
            pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
        except curses.error:
            pass

#  Displays a section of the pad in the middle of the screen
pad.refresh(0,0, 5,5, 20,75)
pad.getch()

#CODE END
#reverse settings
#cs.echo()

#exit
curses.endwin()
