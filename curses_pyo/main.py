import pyo
import time
import curses

def run():
    A = 440.00
    As = 466.16
    B = 493.88
    C = 523.25
    Cs = 554.37
    D = 587.33
    Ds = 622.25
    E = 659.25
    F = 698.46
    Fs = 739.99
    G = 783.99
    Gs = 830.61
    
    keys = ["q","2","w","3","e","r","5","t","6","y","7","u"]
    
    #screen server
    #scr = curses.initscr()
    #scr.keypad(1)
    
    #audio
    serv = pyo.Server().boot()
    serv.amp = 0.1
    
    Asin  = pyo.Sine(freq=A)
    ASsin = pyo.Sine(freq=As)
    Bsin  = pyo.Sine(freq=B)
    Csin  = pyo.Sine(freq=C)
    CSsin = pyo.Sine(freq=Cs)
    Dsin  = pyo.Sine(freq=D)
    DSsin = pyo.Sine(freq=Ds)
    Esin  = pyo.Sine(freq=E)
    Fsin  = pyo.Sine(freq=F)
    FSsin = pyo.Sine(freq=Fs)
    Gsin  = pyo.Sine(freq=G)
    GSsin = pyo.Sine(freq=Gs)
    
    serv.start
    #serv.gui(locals())
    #read key
    key = ''
    while key!='1':
        key = raw_input()
        if key==keys[0]:
            print("do")
            Csin.out()
        if key==keys[1]:
            print("do#")
            CSsin.out()
        if key==keys[2]:
            print("re")
            Dsin.out()
        if key==keys[3]:
            print("re#")
            DSsin.out()
        if key==keys[4]:
            print("mi")
            Esin.out()
        if key==keys[5]:
            print("fa")
            Fsin.out()
        if key==keys[6]:
            print("fa#")
            FSsin.out()
        if key==keys[7]:
            print("sol")
            Gsin.out()
        if key==keys[8]:
            print("sol#")
            GSsin.out()
        if key==keys[9]:
            print("la")
            Asin.out()
        if key==keys[10]:
            print("la#")
            ASsin.out()
        if key==keys[11]:
            print("si")
            Bsin.out()
        if key=='':
            print("clear")
            Asin.play()
            ASsin.play()
            Bsin.play()
            Csin.play()
            CSsin.play()
            Dsin.play()
            DSsin.play()
            Esin.play()
            Fsin.play()
            FSsin.play()
            Gsin.play()
            GSsin.play()
        if key=='1':
            print("exit")
    
    serv.shutdown()
    