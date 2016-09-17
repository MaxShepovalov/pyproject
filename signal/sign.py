#   SYNC -----------#-----------------#
#                   |                 |
#  *----------* *---V--* *-------* *--V---* *--------*
#  | launcher |=| sync |=| wires |=| sync |=| module |
#  *----------* *------* *-------* *------* *--------*
#                        <------->
#                         sgn_del (delay of wire connection. aka distance)
#
#  line ______------______
#             <----> - sgn_len (length of signal)
#
#  sync_del - delay between syncroniser signal and output of [sync]
#
#  module_calc - delay, required for module calculations
#
#  tempo - way how sync works (missed ticks)
#  if sgn_len = 1
#  tempo 0 = -------- (always ON)
#  tempo 1 = _-_-_-_- ()
#  tempo 2 = __-__-__
#  tempo 3 = ___-___-
#            01234567

sgn_len = 4     #length of signal
sgn_del = 3     #delay between input and output for wires
sync_del = 1    #delay between sync and action
tempo = 1       #number of OFF sync ticks
module_calc = 10 #time for calculation

counts = 50	#number of counts to iterate. Not used if = -1
cycles = 6      #sync cycles for iterating

def set_vals(sgn_l, sgn_d, sync_d, temp, mod_c, cnts, cycle):
	global sgn_len
	global sgn_del
	global sync_del
	global tempo
	global module_calc
	global counts
	global cycles
	sgn_len = sgn_l
	sgn_del = sgn_d
	sync_del = sync_d
	tempo = temp
	module_calc = mod_c
	counts = cnts
	cycles = cycle

def get_vals():
	return sgn_len, sgn_del, sync_del, tempo, module_calc, counts, cycles

class syncroniser:
    def __init__(self, name):
        self.name = name
        self.number = 0
        if len(devices) >= 1:
            self.number = len(devices)
        self.memory = 0
        self.syncDelay = -1
        self.out = 0
        self.logM = ""
        self.logO = ""

    def tick(self, sync_val):
        inp = devices[self.number - 1].getOutput()
        if inp != 0:
            self.memory = 1
        #check sync
        if sync_val == sgn_len and self.syncDelay == -1:
            self.syncDelay = sync_del
        #check output signal
        if self.out > 0:
            self.out -= 1
        #check sync waiter
        if self.syncDelay >= 0:
            if self.syncDelay == 0:
                if self.memory != 0:
                    self.out = sgn_len
                    self.memory = 0
            self.syncDelay -= 1
        if self.memory == 0:
            self.logM += "_"
        else:
            self.logM += "-"

    def doOutput():
        writeout("ERR Syncroniser cannot do output on denand. Sync only")

    def getOutput(self):
        val = self.out
        if val == 0:
            self.logO += "_"
        else:
            self.logO += "-"
        return val

    def printlog(self):
        #line = "\n inp   "
        #line += self.logI
        line = "\n mem   "
        line += self.logM
        line += "\n out   "
        line += self.logO
        return line

    def reset(self):
        self.memory = 0
        self.syncDelay = -1
        self.out = 0
        self.logM = ""
        self.logO = ""

class module:
    def __init__(self, name, delay):
        self.name = name
        self.number = 0
        if len(devices) >= 1:
            self.number = len(devices)
        self.lastinp = 0
        self.log = ""
        self.state = []
        self.delay = delay
        for i in range(0, self.delay):
            self.state.append(0)

    def tick(self, sync_val):
        #check input
        if self.number > 0:
            inp = devices[self.number - 1].getOutput()
            self.state.append(inp)
        else:
            if self.lastinp > 0:
                self.lastinp -= 1
            self.state.append(self.lastinp)

    def doOutput(self):
        self.lastinp = sgn_len + 1

    def getOutput(self):
        val = 0
        if len(self.state) > 0:
            val = self.state.pop(0)
        #else:
        #    writeout("ERR %s: Output buffer is empty" % self.name)
        if val == 0:
            self.log += "_"
        else:
            self.log += "-"
            #self.log += str(val)
        return val

    def printlog(self):
        return self.log

    def reset(self):
        self.lastinp = 0
        self.log = ""
        self.state = []
        for i in range(0, self.delay):
            self.state.append(0)

# lncher > sync > delay > sync > calc(delay) > sync > delay > sync > lncher
# LNCH_O > LO_S > WIRE1 > MI_S > MODULE      > MO_S > WIRE2 > LI_S > LNCH_I 

devices = []
devices.append( module("LNCH_O", 0))            #0
devices.append( syncroniser("LO_S  "))          #1
devices.append( module("WIRE1 ", sgn_del))      #2
devices.append( syncroniser("MI_S  "))          #3
devices.append( module("MODULE", module_calc))  #4
devices.append( syncroniser("MO_S  "))          #5
devices.append( module("WIRE2 ", sgn_del))      #6
devices.append( syncroniser("LI_S  "))          #7
devices.append( module("LNCH_I", 0))            #8

#global sync
sync_log = ""
def calcsync(it):
    state = 0
    signals = it / sgn_len
    if (signals % (tempo + 1))==tempo:
        state = (signals+1)*sgn_len - it
    return state

output = ""
def writeout(msg):
    global output
    output += str(msg) + "\n"

def info_head():
    outline = ""
    outline += str("signal length: %d" % sgn_len) + "\n"
    outline += str("Wire delay: %d" % sgn_del) + "\n"
    sncline = ""
    for i in range(0, tempo):
        sncline += "_"
    outline += str("Sync strobe: %d: %s-" % (tempo, sncline)) + "\n"
    outline += str("Time for calculations in Module: %d" % module_calc) + "\n"
    outline += str("Cycles to calc: %d" % cycles) + "\n"
    return outline

def scheme_head():
    outline = ""    
    #writeout scheme
    outline += str("*----------*          *----*           *----*   *--------*") + "\n"
    outline += str("|         >> LNCH_0 > |LO_S| > WIRE1 > |MI_S| > > MODULE > >") + "\n"
    outline += str("| Launcher |          |    |           |  | |   *--------*  V") + "\n"
    outline += str("|         << LNCH_I < |LI_S| < WIRE2 < |MO_S| < < < < < < < ") + "\n"
    outline += str("*----------*          *--:-*           *--:-*") + "\n"
    outline += str("                         |                |") + "\n"
    outline += str("__sync strob_____________#________________#") + "\n"
    return outline

def main_loop():
    global output
    global sync_log
    #clear output
    output = ""
    sync_log = ""
    for i in devices:
        i.reset()
    devices[0].delay = 0
    devices[2].delay = sgn_del
    devices[4].delay = module_calc
    devices[6].delay = sgn_del
    devices[8].delay = 0
    #prerun
    Tstart = 3
    for i in range(0,Tstart):
        sync_log += "_"
        for dev in devices:
            dev.tick(0)
        devices[8].getOutput()
    
    #initiate output
    devices[0].doOutput()
    
    #run simulation
    N = counts
    if N==-1:
    	N = (tempo + 1) * sgn_len
    	N *= cycles
    writeout(N)
    Tend = Tstart
    for i in range(0, N):
        #read sync
        sync = calcsync(i)
        if sync == 0:
            sync_log += "_"
        else:
            sync_log += "-"
        #update devices
        out = devices[8].getOutput()
        for dev in range(len(devices)):
            devices[len(devices) - 1 - dev].tick(sync)
        #for dev in devices:
        #    dev.tick(sync)
        if out == sgn_len and Tend == Tstart:
            Tend = i+2

    if __name__ == "__main__":
        writeout(info_head())
        writeout(scheme_head())

    #writeout graph
    writeout("sync   %s" % sync_log)
    for dev in devices:
        writeout("%s %s" % (dev.name, dev.printlog()))
    
    #show signal time
    timer = "       "
    for i in range(0, Tstart):
        timer += " "
    timer += "/"
    for i in range(0, Tend - Tstart):
        timer += " "
    timer += "\\"
    writeout("%s\nsignal time: %d" % (timer, Tend - Tstart))

if __name__ == "__main__":
    #default vals
    set_vals(4,3,1,1,10,50,6)
    main_loop()
    print(output)