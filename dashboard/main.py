import curses
from curses import panel
import devices

class interface():
    def __init__(self):
        self.device = None
        self.meth_n = 1
        self.meth = ["Attach"]
        self.select = 0
        self.window = None
        self.panel = None
    def add(self, obj):
        self.device = obj
        self.meth = self.device.get_methods()
        self.meth_n = len(self.meth)
        self.select = 0
    def select_down(self):
        if self.select < self.meth_n - 1:
            self.select += 1
    def select_up(self):
        if self.select > 0:
            self.select -= 1
    def act(self):
        if self.device == None:
            return -2
        else:
            action = self.meth[self.select]
            self.device.do(action)
    def get_report(self):
        if self.device == None:
            return "no device"
        else:
            return self.device.report
    def device_type(self):
        if self.device == None:
            return "None"
        else:
            return self.device.get_type()

scr = None
panels = [interface(), interface(), interface()]
objects = []
log = ""

def init_screen():
    global scr
    scr = curses.initscr()
    curses.noecho()
    curses.curs_set(False)
    scr.keypad(1)
    runloop()

def update(sel_panel):
    global log
    for i in range(len(panels)):
        if panels[i].window == None:
            panels[i].window = curses.newwin(7,30,0,30*i)
            panels[i].panel = panel.new_panel(panels[i].window)
        panels[i].window.erase()
        panels[i].window.addstr(0,2,panels[i].device_type()[:27])
        log += "\n>window "+str(i)+" device type: "+panels[i].device_type()[:27]+"\n"
        panels[i].window.addstr(1,0,panels[i].get_report()[:29])
        log += ">window "+str(i)+" device report: "+panels[i].get_report()[:29]+"\n"
        for j in range(panels[i].meth_n):
            if j == panels[i].select:
                if i == sel_panel:
                    panels[i].window.addstr(2+j, 0, panels[i].meth[j], curses.A_REVERSE)
                    log += ">window "+str(i)+" "+panels[i].meth[j]+" [selected]\n"
                else:
                    panels[i].window.addstr(2+j, 0, panels[i].meth[j], curses.A_BOLD)
                    log += ">window "+str(i)+" "+panels[i].meth[j]+" [highlighted]\n"
            else:
                panels[i].window.addstr(2+j, 0, panels[i].meth[j])
                log += ">window "+str(i)+" "+panels[i].meth[j]+"\n"
    panel.update_panels()
    curses.doupdate()
    log += ">update exits\n"

def deinit_screen():
    global scr
    curses.echo()
    curses.curs_set(True)
    curses.endwin()
    scr = None

def add_panel():
    if len(panels) < 5:
        panels.append(interface())

def new_obj_window(panel_offset):
    obj = None
    window = curses.newwin(10, 50, 1, 30*panel_offset)
    pan = panel.new_panel(window)
    run2 = True
    sel = 0
    while run2:
        window.erase()
        window.addstr(0,0,"What device to add?")
        for i in range(len(devices.dev_class)):
            if sel == i:
                window.addstr(1+i,0,devices.dev_class[i],curses.A_REVERSE)
            else:
                window.addstr(1+i,0,devices.dev_class[i])
        panel.update_panels()
        curses.doupdate()
        key2 = scr.getch()
        if key2==259: #UP
            if sel > 0:
                sel -= 1
        elif key2==258: #DOWN
            if sel < len(devices.dev_class)-1:
                sel += 1
        elif key2==10: #RETURN
            obj = devices.make(devices.dev_class[sel])
            run2 = False
    return obj

def runloop():
    run = True
    selected = 0
    while run:
        update(selected)
        key = scr.getch()
        if key==259: #UP
            panels[selected].select_up()
        elif key==260: #LEFT
            if selected > 0:
                selected -= 1
        elif key==261: #RIGHT
            if selected < len(panels)-1:
                selected += 1
        elif key==258: #DOWN
            panels[selected].select_down()
        elif key==10: #RETURN
            retval = panels[selected].act()
            if retval == -2:
                obj = new_obj_window(selected)
                if obj != None:
                    objects.append(obj)
                else:
                    deinit_screen()
                    run = False
                    break
                objID = len(objects)-1
                panels[selected].add(objects[objID])
            elif retval == -1:
                run = False
                break
        elif key==ord("q") or key==27: #ESCAPE
            deinit_screen()
            run = False
            break