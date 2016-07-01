import time
import sys
from window import *

CANV_X = 16
CANV_Y = 9

can = canvas(CANV_X, CANV_Y)

#env
devices = ['Input', 'Delay', 'Disto', 'MonoToStereo', 'Out']

#read pattern
device_setup = [0, 1, 2, 3, 4]
device_num = len(device_setup)

#Device counter
start_num = 0
def deviceNtext(start_num):
    s = ''
    for i in range(start_num, start_num + CANV_Y):
        if i < 10:
            s = s + '%d ' % i
        else:
            s = s + '%d' % i
    return s
deviceN = textbox(deviceNtext(start_num), 2, CANV_Y)

#Buttons
s = ''
for i in range(start_num, start_num + CANV_Y):
    s = s + '<'
btnL = textbox(s, 1, CANV_Y)
s = ''
for i in range(start_num, start_num + CANV_Y):
    s = s + '>'
btnR = textbox(s, 1, CANV_Y)

#write device list on the screen
#first is selected
select = 0
def deviceList(start_num):
    print('[dev list] start %d, select %d' % (start_num, select))
    devList = []
    sel = ' '
    for i in range(0, CANV_Y):
        devN = i + start_num
        if devN == select:
            sel = '*'
        else:
            sel = ' '
        if devN < device_num:
            devList.append(textbox(sel+devices[device_setup[devN]], CANV_X - 4, 1))
        else:
            devList.append(textbox(sel+'none', CANV_X - 4, 1))
    return devList

showDev = deviceList(start_num)



#prepare screen
def screen_update(scrn):
    scrn.clear()
    scrn.set_cursor(0, 0)
    deviceN.project(scrn)
    can.set_cursor(2, 0)
    btnL.project(scrn)
    can.set_cursor(CANV_X - 1, 0)
    btnR.project(scrn)
    for i in range(0,CANV_Y):
        can.set_cursor(3, i)
        showDev[i].project(scrn)
    scrn.draw()

screen_update(can)

def listMove(amnt):
    global select
    global start_num
    global showDev
    select = select + amnt
    if select > start_num + CANV_Y - 1:
        start_num = start_num + 1
    if select == start_num - 1:
        start_num = start_num - 1
    showDev = deviceList(start_num)
    deviceN.write(deviceNtext(start_num))
    screen_update(can)
    time.sleep(0.2)

run = True
while run:
    pkey = sys.stdin.read(1)
    if pkey == 'q':
        run = False
    if pkey == 'w':
        listMove(-1)
    if pkey == 's':
        listMove(1)
    if pkey == 'a':
        device_setup[start_num + select] = device_setup[start_num + select] - 1
        if device_setup[start_num + select] == -1:
            device_setup[start_num + select] = device_setup[start_num + select] + len(devices)
        listMove(0)
    if pkey == 'd':
        device_setup[start_num + select] = device_setup[start_num + select] + 1
        if device_setup[start_num + select] == -1:
            device_setup[start_num + select] = device_setup[start_num + select] + len(devices)
        listMove(0)