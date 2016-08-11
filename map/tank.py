import curses
import time
import sys
from random import random as rand
from curses import panel

score = 0
plr_marks = ['^','>','V','<']

class Obj:
    def __init__(self, y, x, a, objtype):
        self.x = x
        self.y = y
        self.a = a
        self.parent = 'sys'
        self.objtype = objtype
        self.mark = '?'
        self.live = 0
        if objtype=='':
            self.mark = '#'
            self.live = 0
        elif objtype=='bot':
            self.mark = plr_marks[a]
            self.live = 3
        elif objtype=='plr':
            self.mark = plr_marks[a]
            self.live = 3
        elif objtype=='blt':
            self.mark = '.'
            self.live = 30
        elif objtype=='bwall':
            self.mark = 'H'
            self.live = 0
        self.act = True

    def hitPos(self, y, x):
        if self.y==y and self.x==x:
            return True
        else:
            return False

    def hitObj(self, o):
        if self.y==o.y and self.x==o.x:
            return True
        else:
            return False

def getObjID(y, x):
    out = -1
    for i in range(0,len(objects)):
        if objects[i].x==x and objects[i].y==y:
            out = i
            break
    return out

def checkType(name):
    out = 0
    for i in objects:
        if i.objtype==name:
            out += 1
    return out

def killobj(list, obj):
    i = 0
    while i < len(list):
        if list[i]==obj:
            del list[i]
        else:
            i += 1

def inframe(y, x):
    out = True
    if y<0 or y>my-2 or x<0 or x>mx-2:
        out = False
    return out

def collision(list, y, x):
    out = False
    for i in list:
        out = i.hitPos(y, x)
        if out:
            break
    return out

def collisionObj(list, obj):
    out = False
    for i in list:
        out = i.hitObj(obj)
        if out:
            break
    return out

objects = []
GAP = 1

def randmap(active):
    global plr    
    if not active:
        objects.append(Obj(5,7,0,'plr'))
        plr = objects[0]
        #plr.mark = plr_marks[0]
        #plr.live = 3
        objects.append(Obj(6 ,1 ,0,''))
        objects.append(Obj(2 ,2 ,0,''))
        objects.append(Obj(3 ,2 ,0,''))
        objects.append(Obj(4 ,2 ,0,''))
        objects.append(Obj(6 ,2 ,0,''))
        objects.append(Obj(8 ,2 ,0,''))
        objects.append(Obj(9 ,2 ,0,'bwall'))
        objects.append(Obj(10,2 ,0,''))
        objects.append(Obj(11,2 ,0,''))
        objects.append(Obj(13,2 ,0,''))
        objects.append(Obj(4 ,3 ,0,''))
        objects.append(Obj(8 ,3 ,0,''))
        objects.append(Obj(2 ,4 ,0,''))
        objects.append(Obj(4 ,4 ,0,''))
        objects.append(Obj(6 ,4 ,0,''))
        objects.append(Obj(7 ,4 ,0,''))
        objects.append(Obj(8 ,4 ,0,''))
        objects.append(Obj(10,4 ,0,''))
        objects.append(Obj(12,4 ,0,''))
        objects.append(Obj(13,4 ,0,''))
        objects.append(Obj(14,4 ,0,''))
        objects.append(Obj(2 ,5 ,0,''))
        objects.append(Obj(2 ,6 ,0,''))
        objects.append(Obj(4 ,6 ,0,''))
        objects.append(Obj(5 ,6 ,0,''))
        objects.append(Obj(6 ,6 ,0,''))
        objects.append(Obj(7 ,6 ,0,''))
        objects.append(Obj(8 ,6 ,0,''))
        objects.append(Obj(10,6 ,0,''))
        objects.append(Obj(12,6 ,0,''))
        objects.append(Obj(13,6 ,0,''))
        objects.append(Obj(2 ,7 ,0,''))
        objects.append(Obj(6 ,7 ,0,'bwall'))
        objects.append(Obj(8 ,7 ,0,''))
        objects.append(Obj(10,7 ,0,''))
        objects.append(Obj(12,7 ,0,''))
        objects.append(Obj(13,7 ,0,'bwall'))
        objects.append(Obj(6 ,8 ,0,'bwall'))
        objects.append(Obj(10,8 ,0,''))
        objects.append(Obj(13,8 ,0,''))
        objects.append(Obj(2 ,9 ,0,''))
        objects.append(Obj(4 ,9 ,0,''))
        objects.append(Obj(6 ,9 ,0,''))
        objects.append(Obj(7 ,9 ,0,''))
        objects.append(Obj(8 ,9 ,0,''))
        objects.append(Obj(9 ,9 ,0,''))
        objects.append(Obj(10,9 ,0,''))
        objects.append(Obj(13,9 ,0,''))
        objects.append(Obj(2 ,10,0,'bwall'))
        objects.append(Obj(4 ,10,0,'bwall'))
        objects.append(Obj(2 ,11,0,''))
        objects.append(Obj(4 ,11,0,''))
        objects.append(Obj(5 ,11,0,''))
        objects.append(Obj(6 ,11,0,''))
        objects.append(Obj(7 ,11,0,''))
        objects.append(Obj(8 ,11,0,''))
        objects.append(Obj(2 ,12,0,''))
        objects.append(Obj(5 ,12,0,'bwall'))
        objects.append(Obj(8 ,12,0,'bwall'))
        objects.append(Obj(2 ,13,0,''))
        objects.append(Obj(3 ,13,0,''))
        objects.append(Obj(5 ,13,0,''))
        objects.append(Obj(6 ,13,0,''))
        objects.append(Obj(7 ,13,0,''))
        objects.append(Obj(8 ,13,0,''))
        #bots
        objects.append(Obj(12,3,0,'bot'))
        objects.append(Obj(11,7,3,'bot'))
        objects.append(Obj(3,11,2,'bot'))
        objects.append(Obj(11,13,1,'bot'))
    else:
        #fill map randomly
        bool_plr = False
        objtypes = ['bwall','plr','bot']
        for rx in range(1,14):
            for ry in range(1,14):
                dirN = int(10*rand()%4)
                botN = int(10*rand()%len(objtypes))
                while (objtypes[botN]=='plr') and bool_plr:
                    botN = int(10*rand()%len(objtypes))
                objects.append(Obj(ry,rx,dirN,objtypes[botN]))
                if objtypes[botN]=='plr':
                    bool_plr = True
                    plr = objects[getObjID(ry,rx)]
    #walls
    for i in range(0,15):
        objects.append(Obj(0,i,0,''))
        objects.append(Obj(15-i,0,0,''))
        objects.append(Obj(15,15-i,0,''))
        objects.append(Obj(i,15,0,''))

if __name__ == "__main__":
    if len(sys.argv)==2:
        randmap(sys.argv[1])
    else:
        randmap(False)

scr = curses.initscr()
my, mx = scr.getmaxyx()
curses.noecho()
curses.curs_set(False)
scr.keypad(1)
curses.halfdelay(GAP)
blast = curses.newwin(1,1,16,16)
blast.bkgd('X')
blast.box()
#obj = curses.newwin(1,2,plr.y,plr.x)
walls = curses.newwin(my-2,mx-2,3,3)

curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_RED)

#obj_panel = panel.new_panel(obj)
#blast.addstr(0,0,'.')
wall_panel = panel.new_panel(walls)
blast_panel = panel.new_panel(blast)
#obj_panel.show()
#fire_panel.show()

def draw():
    walls.erase()
    #obj.erase()
    for i in objects:
        if i.objtype=='effect':
            if i.live==0:
                killobj(objects, i)
                continue
            else:
                i.live -= 1
        if inframe(i.y,i.x):
            if i.objtype=='plr':
                walls.addch(i.y,i.x,i.mark, curses.A_REVERSE+curses.color_pair(1))
            elif i.objtype=='bot':
                walls.addch(i.y,i.x,i.mark, curses.A_REVERSE+curses.color_pair(2))
            elif i.objtype=='blt':
                walls.addch(i.y,i.x,i.mark, curses.A_REVERSE+curses.color_pair(3))
            elif i.objtype=='effect':
                walls.addch(i.y,i.x,i.mark, curses.A_REVERSE+curses.color_pair(4))
            else:
                walls.addch(i.y,i.x,i.mark)
    panel.update_panels()
    curses.doupdate()
    if not blast_panel.hidden():
        blast_panel.hide()

def Fire(parent): #creates new bullet
    if parent in objects:
        bull = Obj(parent.y, parent.x, parent.a, 'blt')
        bull.act = True
        bull.live = 30
        bull.mark = '.'
        bull.parent = parent.objtype
        objects.append(bull)
        del bull

def addEffect(y,x,mark,time):
    dot = Obj(y, x, 0, 'effect')
    dot.mark = mark
    dot.live = time
    dot.act = True
    objects.append(dot)
    del dot

def Move(): #moves the bullet
    global score
    for i in objects:
        if i.objtype == 'blt':
            newx = i.x
            newy = i.y
            if i.a==0:
                newy -= 1
            elif i.a==1:
                newx += 1
            elif i.a==2:
                newy += 1
            elif i.a==3:
                newx -= 1
            if not inframe(newy, newx):
                killobj(objects, i)
            elif collision(objects, newy, newx) or i.live==0:
                #create explosion
                addEffect(i.y,i.x,'X',1)
                #reduce HP
                target = getObjID(newy, newx)
                if target != -1:
                    if objects[target].objtype == 'blt':
                        objects[target].live -= 30
                    elif objects[target].objtype != '':
                        objects[target].live -= 1
                        if i.parent == 'plr':
                            score += 1
                    if objects[target].live<=0 and objects[target].objtype != '':
                        del objects[target]
                if blast_panel.hidden():
                    blast_panel.show()
                killobj(objects, i)
            else:
                i.x = newx
                i.y = newy
                i.live -= 1

def Forw(doll, move): #moves tank forward
    if doll.objtype == 'bot' or doll.objtype == 'plr':
        newy = doll.y
        newx = doll.x
        if doll.a==0:
            newy -= move
        elif doll.a==1:
            newx += move
        elif doll.a==2:
            newy += move
        elif doll.a==3:
            newx -= move
        if not collision(objects, newy, newx) and inframe(newy, newx):
            doll.x = newx
            doll.y = newy

def Right(doll):
    if doll.objtype == 'bot' or doll.objtype == 'plr':
        doll.a += 1
        if doll.a > 3:
            doll.a -= 4
        doll.mark = plr_marks[doll.a]

def Left(doll):
    if doll.objtype == 'bot' or doll.objtype == 'plr':
        doll.a -= 1
        if doll.a < 0:
            doll.a += 4
        doll.mark = plr_marks[doll.a]

def log(msg):
    scr.move(0,0)
    scr.erase()
    scr.addstr(0,0,msg)
    draw()

def act():
    for i in objects:
        if i.objtype=='bot':
            val = rand()
            if val>0.8:
                Forw(i,1)
            elif val>0.6:
                Left(i)
            elif val>0.4:
                Right(i)
            elif val>0.2:
                Forw(i,-1)
            else:
                Fire(i)

key = -1
ai = True
iteration = 0
advanced = True
while key != ord('q'):
    if not plr in objects:
        log("your tank is destroyed! score: %d" % score)
        time.sleep(2)
        break

    if checkType('bot')==0:
        log("Win! score: %d" % score)
        time.sleep(2)
        break

    iteration += 1
    Move()

    log("(%d,%d) borders(%d,%d) objects:%d live:%d AI:%s Iteration:%d" % (plr.x,plr.y,mx,my,len(objects),plr.live,str(ai),iteration))
    key = scr.getch()

    if iteration % 4 ==0 and ai:
        act()

    if advanced:
        if key==259: #UP
            Forw(plr,1)
        elif key==260: #LEFT
            Left(plr)
        elif key==261: #RIGHT
            Right(plr)
        elif key==258: #DOWN
            Forw(plr,-1)
        elif key==10: #RETURN
            Fire(plr)
        elif key==ord('r'):
            ai = not ai
        elif key==ord('e'):
            advanced = False
    else:
        if key==259: #UP
            if plr.a==0:
                Forw(plr,1)
            else: 
                plr.a = 0
                plr.mark = plr_marks[0]
        elif key==260: #LEFT
            if plr.a==3:
                Forw(plr,1)
            else: 
                plr.a = 3
                plr.mark = plr_marks[3]
        elif key==261: #RIGHT
            if plr.a==1:
                Forw(plr,1)
            else: 
                plr.a = 1
                plr.mark = plr_marks[1]
        elif key==258: #DOWN
            if plr.a==2:
                Forw(plr,1)
            else: 
                plr.a = 2
                plr.mark = plr_marks[2]
        elif key==10: #RETURN
            Fire(plr)
        elif key==ord('r'):
            ai = not ai
        elif key==ord('e'):
            advanced = True

    if key!=-1:
        time.sleep(GAP/10.0)

curses.echo()
curses.curs_set(True)
curses.endwin()
