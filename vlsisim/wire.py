#sets wire system
import task
import notify
import globalvars as GLOB 

#      str     float   int      [str]
# bus[name] = ([value], size, [outputs])

bus = dict()

#return list of wires
def giveNames():
    return bus.keys()

def printNames():
    out = 'wires:\n'
    for w in bus.keys():
        out += w+'\n'
    notify.say(out)

def giveReport(wire, full=True):
    out = ''
    if wire in bus.keys():
        V,S,output = bus[wire]
        if S==1:
            out += wire+' ['+str(V[0])+' V] '+str(len(output))+' device(s) listen\n'
        if S>1:
            out += wire+' '+str(S)+' lines '+str(len(output))+' device(s) listen\n'
            for i in range(len(V)):
                out += '        '+str(i)+':['+str(V[i])+']\n'
        if full:
            out += '    listeners:\n'
            for o in output:
                out += '        '+o+'\n'
    else:
        out = 'Not a wire: '+str(wire)+'\n'
        notify.error('wire.giveReport: Wrong wire name '+str(wire))
    return out


def printReport():
    out = 'wires:\n'
    for w in bus.keys():
        out += giveReport(w, full=False)
    notify.say(out)

def readV(wire):
    if wire in bus.keys():
        out = []
        v,_,_ = bus[wire]
        out.extend(v)
        return out
    else:
        notify.error('wire.readV: Wrong wire name '+str(wire))

def setV(wire, value):
    notify.debug('wire.setV setting '+str(wire)+' to '+str(value))
    if wire in bus.keys():
        if type(value) == type([]):
            V,S,out = bus[wire]
            if len(value) > S:
                notify.warn('wire.setV: '+str(len(value))+' bit value '+str(value)+'is to big and it will be truncaded to LSB ['+str(S)+' pin bus '+str(wire)+']')
                value = value[-S:]
            if value != V or GLOB.force_same_v_update:
                #extend MSB to value
                svalue = [0]*max(S-len(value),0)
                svalue.extend(value)
                #write out
                bus[wire] = svalue,S,out
                #add task for updating connected devices
                for dev in out:
                    task.addTask('recalc', dev)
            else:
                notify.info('wire.setV: New value is the same, no update. To ommit, set "force_same_v_update = True"')
        else:
            notify.error('wire.setV: value ['+str(value)+' '+str(type(value))+'] is not a list [bus '+str(wire)+']')
    else:
        notify.error('wire.setV: Wrong wire name '+str(wire))

def setBinary(wire, value):
    if wire in bus.keys():
        if type(value) == type(0):
            busvalue = []
            for bn in bin(value)[2:]:
                if bn=='1':
                    busvalue.append(GLOB.digital_high)
                else:
                    busvalue.append(GLOB.digital_low)
            setV(wire, busvalue)
        #if type(value) ==  type([]):
        #    setV(wire, value)
        elif type(value) == type(''):
            busvalue = []
            for bn in value:
                if bn=='1':
                    busvalue.append(GLOB.digital_high)
                else:
                    busvalue.append(GLOB.digital_low)
        else:
            notify.error('wire.setBinary: value ['+str(value)+' '+str(type(value))+'] is not an integer or a string [bus '+str(wire)+']')
    else:
        notify.error('wire.setBinary: Wrong wire name'+str(wire))

def connect(wire, device):
    if wire in bus.keys():
        V,S,out = bus[wire]
        out.add(device)
        bus[wire] = V,S,out
        task.addTask('recalc', device)
    else:
        notify.error('wire.connect: Wrong wire name '+str(wire))

def addBus(wire, size):
    size = int(size)
    bus[wire] = ([0.0]*size, size, set())

def help():
    out = ''
    out += 'Wire module. Connects devices\n'
    out += '    giveNames() - returnes wires\' names \n'
    out += '    printNames() - prints wires\' names\n'
    out += '    giveReport(name) - returns data for one wire\n'
    out += '    printReport() - prints data for wires\n'
    out += '    readV(name) - returns value of a wire\n'
    out += '    setV(name, value) - set values for wire\n'
    out += '                value is a list \n'
    out += '    setBinary(name, value) - \n'
    out += '                value can be an int (will be converted to binary)\n'
    out += '                value can be a binary string, 1 - high, else - low\n'
    out += '    connect(wire name, device name) - adds listener\n'
    out += '    addBus(name, size) - adds new bus with given size\n'
    notify.say(out)