#TOP LEFT WINDOW OF THE SCREEN
import curses
import time
from curses import panel

select = 0
selectM = 0
selectS = 0

SIZE_X = 30
SIZE_Y = 10

MENU_X = 10
MENU_Y = 7

SUBMENU_X = 20
SUBMENU_Y = 5

#number of cycles for status appearing
STAT_MAX = 5

scr = curses.initscr()
scr.keypad(1)
curses.noecho()
curses.curs_set(False)
curses.halfdelay(5)

window = curses.newwin(SIZE_Y, SIZE_X, 1, 0)
update = curses.newwin(SIZE_Y, SIZE_X, 1, 0)
menu = curses.newwin(MENU_Y, MENU_X, 2, 1)
submenu = curses.newwin(SUBMENU_Y, SUBMENU_X, 3, 2)
info = curses.newwin(SIZE_Y - 2, SIZE_X - 2, 1, 1)

update.bkgd(" ", curses.A_REVERSE)
main_panel = panel.new_panel(window)
menu_panel = panel.new_panel(menu)
subm_panel = panel.new_panel(submenu)
info_panel = panel.new_panel(info)
update_panel = panel.new_panel(update)
main_panel.show()
menu_panel.hide()
subm_panel.hide()
update_panel.hide()
info_panel.hide()

window_data = ["variables","set variable","exit"]
window_act = ["info", "menu", "stop"]
menu_data = ["var A","var B","close"]
menu_act = ["chng", "chng", "back"]

pa_type = dict()
params = dict()
params["var A"] = 0
pa_type["var A"] = "int"
params["var B"] = 1
pa_type["var B"] = "varBlist"
params["varBlist"] = ["Input", "Delay", "Disto", "Output"]

subm_name = "var A"
subm_val = 0
info_on = False
stat_time = 0

def draw(layer): 
    if layer == 0:
        window.bkgd(" ", curses.A_REVERSE)
    else:
        window.bkgd(" ")

    for i in range(0,len(window_data)):
        if select == i and layer == 1:
            window.addstr(i+1,1,window_data[i], curses.A_REVERSE)
        else:
            window.addstr(i+1,1,window_data[i])

    for i in range(0,len(menu_data)):
        if selectM == i and layer == 2:
            menu.addstr(i+1,1,menu_data[i], curses.A_REVERSE)
        else:
            menu.addstr(i+1,1,menu_data[i])
    menu.addstr(0,1,"MENU:")

    info.clear()
    for i in range(0,len(menu_data)):
        if layer == 3 and menu_data[i] != "close":
            try:
                if pa_type[menu_data[i]] == "int":
                    line = "%s = %d" % (menu_data[i], params[menu_data[i]])
                else:
                    line = "%s = %s" % (menu_data[i], str(params[pa_type[menu_data[i]]][params[menu_data[i]]]))
            except KeyError:
                line = "no such key (%s) in dict (pa_type)" % menu_data[i]
            except TypeError:
                line = "dict error: data: %s." % menu_data[i]
            info.addstr(i+1,1,line)

    submenu.clear()
    submenu.addstr(1,3,subm_name)
    submenu.addstr(2,1,"<")
    submenu.addstr(2,SUBMENU_X - 2,">")
    if selectS == 0:
        try:
            if pa_type[subm_name] == "int":
                submenu.addstr(2,3,str(subm_val), curses.A_REVERSE)
            else:
                submenu.addstr(2,3,str(params[pa_type[subm_name]][subm_val]), curses.A_REVERSE)
        except KeyError:
            status("no such key (%s) in dict (pa_type)" % subm_name)
        submenu.addstr(3,3,"OK")
    elif selectS == 1:
        try:
            if pa_type[subm_name] == "int":
                submenu.addstr(2,3,str(subm_val))
            else:
                submenu.addstr(2,3,str(params[pa_type[subm_name]][subm_val]))
        except KeyError:
            status("no such key (%s) in dict (pa_type)" % subm_name)
        submenu.addstr(3,3,"OK", curses.A_REVERSE)
    window.box()
    menu.box()
    submenu.box()
    info.box()
    time.sleep(0.01)
    if not update_panel.hidden():
        update_panel.hide()
    panel.update_panels()
    curses.doupdate()

def status(msg):
    global stat_time
    scr.move(0,0)
    scr.erase()
    scr.addstr(0,0,msg)
    stat_time = STAT_MAX

def upEvent(layer):
    global select
    global selectM
    global selectS
    if layer == 1: #inside window
        if select > 0:
            select -= 1
    elif layer == 2: #inside menu
        if selectM > 0:
            selectM -= 1
    elif layer == 3 and not info_on: #submenu
        if selectS == 1:
            selectS = 0

def leftEvent(layer):
    global subm_val
    global params
    if layer == 3 and selectS == 0 and not info_on: # submenu
        if pa_type[subm_name] == "int":
            subm_val -= 1
            status("wrote %d to %s" % (subm_val, subm_name));
        else:
            if subm_val > 0:
                subm_val -= 1
                status("new value for %s is %d [%s]" % (subm_name, subm_val, params[pa_type[subm_name]][subm_val]));
            else:
                status("value is on edge")
    else:
        status("layer: %s,selectS: %s ,info: %s" % (str(layer==3),str(selectS==0),str(not info_on)))

def rightEvent(layer):
    global subm_val
    global params
    if layer == 3 and selectS == 0 and not info_on: # submenu
        if pa_type[subm_name] == "int":
            subm_val += 1
            status("new value for %s is %d" % (subm_name, subm_val));
        else:
            if subm_val < len(params[pa_type[subm_name]]) - 1:
                subm_val += 1
                status("new value for %s is %d [%s]" % (subm_name, subm_val, params[pa_type[subm_name]][subm_val]));
            else:
                status("value is on edge")

def downEvent(layer):
    global select
    global selectM
    global selectS
    if layer == 1: #inside window
        if select < len(window_data) - 1:
            select += 1
    elif layer == 2: #inside menu
        if selectM < len(menu_data) - 1:
            selectM += 1
    elif layer == 3 and not info_on: #submenu
        if selectS == 0:
            selectS = 1

def selectEvent(layer):
    try:
        update_panel.show()
        panel.update_panels()
        curses.doupdate()
    except NameError:
        status("update_panel do not exist")

    global subm_name
    global subm_val
    global selectS
    global info_on
    if layer == 0: #root
        act = "root"
    elif layer == 1: #window
        act = window_act[select]
    elif layer == 2: #menu
        act = menu_act[selectM]
    elif layer == 3 and not info_on: #submenu
        if selectS == 1:
            act = "save"
        else:
            act = "none"
    elif layer == 3 and info_on: #info window
        act = "no info"
    else:
        act = "none"

    if act == "none":
        return True, 0
    elif act == "root":
        return True, 1
    elif act == "menu":
        menu_panel.show()
        return True, 1
    elif act == "back":
        menu_panel.hide()
        return True, -1
    elif act == "chng":
        selectS = 0
        subm_name = menu_data[selectM]
        subm_val = params[subm_name]
        subm_panel.show()
        return True, 1
    elif act == "save":
        params[subm_name] = subm_val
        subm_panel.hide()
        status("%s saved to %s" % (str(subm_val), subm_name))
        return True, -1
    elif act == "stop":
        return False, 0
    elif act == "info":
        info_on = True
        info_panel.show()
        return True, 2
    elif act == "no info":
        info_on = False
        info_panel.hide()
        return True, -2
    else:
        return False, 0

def close():
    curses.echo()
    curses.curs_set(True)
    curses.endwin()

def getKey(layer):
    global stat_time
    if stat_time > 0:
        stat_time -= 1
    if stat_time == 0:
        scr.move(0,0)
        scr.erase()
        draw(layer)
    scr.addstr(12,0,"stat_time: %d, selectS %s, info %s" % (stat_time, selectS, str(info_on)))
    return scr.getch()