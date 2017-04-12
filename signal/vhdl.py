#python 2.7
"""
         [generator]->+|cntr| 4
                       |    |-/->|cmpr4bit|
 [slow generator]-*   -|____|    |        |
                  |              |        | 1
inp  |\           |              |        |-/-*
--->+| \       *-[x]->+|cntr| 4  |        |   |
     |  )--cm--*  |    |    |-/->|________|   |
 *->-| /       *-[x]->-|____|                 |
 |   |/                                       |
 |      ret     1                   fdb       |
 *--------------/---[LPF]<--------------------*
"""
WIDTH = 5
def gener(time, period):
    ptime = time%period
    if ptime < period/2:
        return 0
    else:
        return 1

def cmpr1bit(a,b,act):
    return (act & a & (a^b)), (act & ((a^b)^1))

def cmpr4bit(a,b):
    o = [0]*WIDTH
    act = 1
    for i in range(WIDTH):
        o[i], act = cmpr1bit(a[i],b[i],act)
    fin = 0
    if o!=[0]*WIDTH:
        fin = 1
    return fin

def opamp(a,b):
    if a >= b:
        return 1
    else:
        return 0

class cntr:
    def __init__(self):
        self.MAX_VAL = pow(2,WIDTH)-1
        self.val = 0

    def add(self):
        self.val+=1
        if self.val > self.MAX_VAL:
            self.val = 0

    def sub(self):
        self.val-=1
        if self.val < 0:
            self.val = self.MAX_VAL

    def reset(self):
        self.val = 0

    def bits(self):
        b = []
        for k in bin(self.val)[2:]:
            b.append(int(k))
        while len(b) < WIDTH:
            b.insert(0,0)
        return b

    def getstr(self):
        return hex(self.val)[2:]

#input
import math
def inp(t):
    r = 0.
    if t >= 10:
        #r = 0.7
        r = 0.3+0.2*math.sin(2*math.pi*t/8000)
    return r

#counters
Cauto = cntr()
Cfind = cntr()

#comparator input
a = Cauto.bits()
b = Cfind.bits()

#LPF
ret = 0.
def LPF(ret, x):
    return ret+(x-ret)*0.008

#signals
gen1 = 0
gen2 = 0

#drawing
def sname(key):
    trg_len = 8
    while len(key)<trg_len:
        key = " "+key
    return key[:trg_len]

#simulation
#time = 0
inp_y = []
ret_y = []
dig_y = []
time_length = pow(2,14)
for time in range(time_length):
#while True:
    cm = opamp(inp(time), ret)
    if not gen1 and gener(time, 32):
        if cm:
            Cfind.add()
        else:
            Cfind.sub()
    gen1 = gener(time, 32)
    if not gen2 and gener(time, 2):
        Cauto.add()
    gen2 = gener(time, 2)
    fdb = cmpr4bit(Cfind.bits(), Cauto.bits())
    ret = LPF(ret, fdb)
    print round(inp(time),4),' ',gen1,' ',gen2,'\t',round(ret,4),'\t',fdb,'\t',Cfind.bits(),' ',Cfind.getstr(),' t:',time
    inp_y.append(round(inp(time),4))
    ret_y.append(round(ret,4))
    dig_y.append(Cfind.val*1./pow(2,WIDTH))
    #time += 1  

import matplotlib.pyplot as plt
plt.plot(range(time_length),inp_y,range(time_length),ret_y,range(time_length),dig_y)
plt.show()