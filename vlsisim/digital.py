#digital devices
import notify
import task
import wire
import globalvars as GLOB

# logic[device] = dict[input]->output
from preset_devices import logic, active

def giveNames():
    return logic.keys()

def giveLogic(dtype):
    notify.say(logic[dtype]['help'])

def printNames():
    out = 'digital:\n'
    for k in logic.keys():
        out += '    '+k+'\n'
    notify.say(out)

# inset,outset = [(wire, id)]
def process(dtype, inset, outset):
    #read data
    inpt = ''
    for pair in inset:
        wireName, i = pair
        if wireName=='grd' or wireName=='ground':
            inpt += '0'
        else:
            pin = wire.readV(wireName)[i]
            if pin > GLOB.digital_thr:
                inpt += '1'
            else:
                inpt += '0'
    #process
    outp = '0'
    if dtype in logic.keys():
        outp = logic[dtype][inpt]
    notify.debug('Logic '+dtype+' input='+inpt+' output='+outp)
    #write data
    #wires = [] #wire names
    values = dict() #wire data (lists)
    for i in range(len(outp)):
        val = 0.0
        if outp[i]=='1':
            val = GLOB.digital_high
        else:
            val = GLOB.digital_low
        wireName, p = outset[i]
        if wireName in values.keys():
            values[wireName][p] = val
        else:
            values[wireName] = wire.readV(wireName)
            values[wireName][p] = val
    notify.debug('values: '+str(values))
    for i in values.keys():
        wire.setV(i, values[i])

def help():
    out += 'Digital devices\n'
    out += '    giveNames() - returns types of known devices\n'
    out += '    printNames() - print types of known devices\n'
    out += '    process(dtype, input set, output set) - simulate chip\n'
    out += '    giveLogic(dtype) - shows help for given device type\n'
    out += '\n'
    notify.say(out)
