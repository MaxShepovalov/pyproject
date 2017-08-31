#task system
import notify
import devices
import globalvars as GLOB 

task = []

def addTask(command, target):
    task.append((command, target))
    if GLOB.notify_new_task:
        notify.say('INFO new task: \''+str(command)+'\' on \''+str(target)+'\'')

def stopTask():
    global task
    task = []

def doAll():
    while len(task) != 0: 
        doTask()

def doTask():
    cmd, trg = task.pop(0)
    if cmd == 'recalc':
        devices.update(trg)
    else:
        notify.error('task.doTask: Unknown command '+str(cmd))
    notify.info('task.doTask: '+str(len(task))+' tasks left')