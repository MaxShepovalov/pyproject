import globalvars as GLOB
#notify_errors = True
#notify_warnings = True
#notify_info = True

buff = ''

def flush():
    global buff
    buff = ''

def say(msg):
    print msg

def error(msg):
    print 'ERROR ',msg

def warn(msg):
    print 'WARNING ',msg

def info(msg):
    print 'INFO ',msg

def debug(msg):
    print '\nDEBUG ',msg,'\n'