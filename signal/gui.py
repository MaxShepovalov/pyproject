import sign
import curses

K_UP = 259
K_DW = 258
K_LF = 260
K_RG = 261

SCR_W = 140

l = ""
def log(msg):
    global l
    l += str(msg) + "\n"

def checker(num, sel):
    if num == sel:
        return curses.A_REVERSE
    else:
        return curses.A_NORMAL

def draw_at(y, x, array):
    lines = array.split('\n')
    dy = 0
    for ln in lines:
        if ln != "":
            if ln[0]=="E" and ln[1]=="R" and ln[2]=="R":
                log(ln)
                continue
        try:
            scr.addstr(y+dy, x, ln)
        except:
            log("Error with addstr at Y:%d X:%d STR:\"%s\"" % (y+dy, x, ln))
        dy += 1
        if y+dy > 29:
            break

scr = curses.initscr()

scr.keypad(1)
curses.noecho()
curses.curs_set(False)


key = 0
cur_sel = 0
draw_at(0, 15, sign.scheme_head())
sign.main_loop()
draw_at(8, 15, sign.output)
while key != ord('q'):
    scr.clear()
    #read state
    sgn_len, sgn_del, sync_del, tempo, module_calc, counts, cycles = sign.get_vals()
    line = "sgn_len "
    scr.addstr(0,0,"sgn_len     ")
    scr.addstr(0,12,str(sgn_len), checker(0, cur_sel))

    scr.addstr(1,0,"sgn_del     ")
    scr.addstr(1,12,str(sgn_del), checker(1, cur_sel))

    scr.addstr(2,0,"sync_del    ")
    scr.addstr(2,12,str(sync_del), checker(2, cur_sel))

    scr.addstr(3,0,"tempo       ")
    scr.addstr(3,12,str(tempo), checker(3, cur_sel))

    scr.addstr(4,0,"module_calc ")
    scr.addstr(4,12,str(module_calc), checker(4, cur_sel))

    scr.addstr(5,0,"counts      ")
    scr.addstr(5,12,str(counts), checker(5, cur_sel))

    scr.addstr(6,0,"cycles      ")
    scr.addstr(6,12,str(cycles), checker(6, cur_sel))
    
    draw_at(0, 15, sign.scheme_head())
    draw_at(8, 15, sign.output)
    scr.refresh()

    #get char
    key = scr.getch()
    change = 0
    if key == ord('q'):
        continue
    elif key == K_RG:
        change = 1
    elif key == K_LF:
        change = -1
    elif key == K_UP:
        if cur_sel > 0:
            cur_sel -= 1
    elif key == K_DW:
        if cur_sel < 6:
            cur_sel += 1

    if key == K_LF or key == K_RG:
        #change
        if cur_sel == 0:
            if sgn_len+change > 0:
                if counts > -1 or (sgn_len+change)*(tempo+1)*cycles + 3 < SCR_W:
                    sgn_len += change
        elif cur_sel == 1:
            if sgn_del+change >= 0:
                sgn_del += change
        elif cur_sel == 2:
            if sync_del+change >= 0:
                sync_del += change
        elif cur_sel == 3:
            if tempo+change >= 0:
                if counts > -1 or sgn_len*(tempo+change+1)*cycles + 3 < SCR_W:
                    tempo += change
        elif cur_sel == 4:
            if module_calc+change >= 0:
                module_calc += change
        elif cur_sel == 5:
            if counts+change >= -1 and counts+change < SCR_W:
                #if not (counts+change == -1 and sgn_len*(tempo+1)*cycles + 3 < SCR_W ):
                counts += change
        elif cur_sel == 6:
            if cycles+change >= 0:
                if counts > -1 or sgn_len*(tempo+change+1)*cycles + 3 < SCR_W:
                    cycles += change
        else:
            continue
        #write state and run
        sign.set_vals( sgn_len, sgn_del, sync_del, tempo, module_calc, counts, cycles)
        sign.main_loop()

curses.echo()
curses.curs_set(True)
curses.endwin()

if l!= "":
    print("\n\nLOG IS NOT EMPTY\n\n")
    print(l)
    print("========================")