#device registry
import globalvars as GLOB
from preset_devices import logic
import notify
import wire
import digital

devices = dict()

def addDevice(dname, dtype, inset, outset):
	clear = True
	typein,typeout = logic[dtype]['data']
	if len(inset)!=typein:
		notify.error('devices.addDevice: Asked for '+str(len(inset))+' inputs in inset, when '+dtype+' has only '+str(typein))
		clear = False
	if len(outset)!=typeout:
		notify.error('devices.addDevice: Asked for '+str(len(outset))+' inputs in outset, when '+dtype+' has only '+str(typeout))
		clear = False
	if dname in devices.keys():
		notify.error('devices.addDevice: Device '+dtype+' already exists')
		clear = False
	if clear:
		devices[dname] = (dtype, inset, outset)
		notify.info('Device '+dname+' of type '+dtype+' added')
		if GLOB.autoconnect:
			#connect mentioned input buses
			wires = set()
			for w,i in inset:
				wires.add(w)
			for w in wires:
				wire.connect(w, dname)
	else:
		notify.error('Can\'t add device '+dname+' of type '+dtype)

def update(dname):
	dtype, ins, outs = devices[dname]
	digital.process(dtype, ins, outs)