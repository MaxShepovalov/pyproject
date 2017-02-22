import socket
import sys
#import json
import threading
try:
   import gui
except ImportError:
   print("GUI is not found")

gui = None
EXIT_STR = "{{cmd}}::exit"

#get input
def read_keyboard():
    line = ''
    try:
        line = gui.getline()
    except AttributeError, NameError:
        line = raw_input(">")
    return line

#print function
def print_to_screen(msg):
    try:
        gui.print_to_scr(msg)
    except AttributeError, NameError:
        print(msg)

#print status
show_status = True
def print_stat(msg):
    try:
        gui.print_to_stat(msg)
    except AttributeError, NameError:
        if show_status:
            print("status: " + msg)

#log
log = ''
def print_log(msg):
    global log
    log += msg
    print_stat(msg[:-1])

def show_log():
    print_log("log printout requested\n")
    log_lines = log[:-1].split('\n')
    for line in log_lines:
        print_to_screen("log> " + line)

#exit function
#for threading
t = None
def shutdown():
    global recloop
    global run
    try:
        conn.close()
    except AttributeError, NameError:
        pass
    try:
        s.close()
    except AttributeError, NameError:
        pass
    try:
        gui.stop()
    except AttributeError, NameError:
        print_log("Can't stop GUI\n")
    k = raw_input("Press Q to see log, any other to exit")
    if k=='Q' or k=='q':
        show_log()
    exit()

#start gui
try:
    gui.start()
except AttributeError, NameError:
    print_log("Can't start GUI\n")

#check role
CLIENT = False
cl_ip = None
if 'client' in sys.argv:
    CLIENT = True
    print_log("Run as client\n")
    if len(sys.argv) == 3:
        cl_ip = sys.argv[2]
        print_log("IP for connect: " + cl_ip + "\n")
elif len(sys.argv) == 1:
    CLIENT = False
    print_log("Run as server\n")
else:
    print_to_screen("SYS> Wrong argument list: " + repr(sys.argv))
    print_to_screen("SYS> Use 'python serv.py client [ip]' to start client")
    print_to_screen("SYS> Use 'python serv.py'             to start server")
    print_to_screen("SYS> Server should be started first")
    shutdown()

#setup connection
conn = None
addr = ''
s = socket.socket()
s.settimeout(5)
if CLIENT:
    do_attempt = True
    while do_attempt:
        if cl_ip == None:
            print_log("client ip was no provided or connection failed. Asking\n")
            print_to_screen("SYS> Write an IP to connect or '/exit' to exit")
            while cl_ip==None or cl_ip == '':
                cl_ip = read_keyboard()
                if cl_ip != None:
                    print_to_screen("SYS> got ip: " + str(cl_ip))
            if cl_ip == '/exit':
                print_log("user exit\n")
                do_attempt = False
                cl_ip = None
                break
        attempt = 5
        while attempt > 0:
            try:
                s.connect((cl_ip,8602))
                conn = s
                do_attempt = False
                break
            except socket.error:
                print_log("socket error")
                do_attempt = False
                break
            except TypeError:
                print_log("ip is not a str\n")
                do_attempt = False
                break
            except socket.timeout:
                attempt -= 1
                print_log("setup failed. " + str(attempt) + " attempts left\n")
                print_to_screen("SYS> Connection attempt failed")
                s.close()
                s = socket.socket()
                s.settimeout(5)
    if cl_ip == None:
        print_log("setup failed. exit\n")
        shutdown()
    addr = cl_ip
else:
    s.bind(('', 8602))
    s.listen(1)
    print_log("ip = " + repr(s.getsockname()) + "\n")
    attempt = 5
    while attempt > 0:
        try:
            conn, addr = s.accept()
            if conn != None:
                print_log("connect established (" + repr(addr) + ")\n")
                print_to_screen("SYS> link with (" + repr(addr) + ")")
                break
        except socket.timeout:
            attempt -= 1
            print_log("setup failed. " + str(attempt) + " attempts left\n")
if conn == None:
    print_to_screen("SYS> Connection not established. Exit")
    shutdown()


#data parcer
def computeline(msg):
    return msg

#setup reading thread
recloop = True
bufsize = 1024
def receiveloop():
    global recloop
    global conn
    conn.settimeout(1)
    print_log("receiveloop started\n")
    while recloop:
        try:
            data = conn.recv(bufsize)
        except socket.timeout:
            continue
        print_log("received " + str(len(data)) + " bytes from " + repr(addr) + "\n")

        print_to_screen(repr(addr) + "> " + repr(data))
        #termination
        if data == EXIT_STR:
            recloop = False
            print_log(repr(addr) + " disconnected. stop thread\n")
            conn.close()
            print_to_screen("SYS> connection closed")
    print_log("receiveloop ended\n")

t = threading.Thread(target=receiveloop)
t.start()

#main loop
run = True
while run:
    cmd = read_keyboard()
    if cmd == "":
        continue
    elif cmd == "/help":#_123456789_123456789_123456789_123456789_123456789_
        print_to_screen("SYShelper> just line without '/' = your message")
        print_to_screen("SYShelper> /echo = print status")
        print_to_screen("SYShelper> /exit = exit from messenger")
        print_to_screen("SYShelper> /help = this helper")
        print_to_screen("SYShelper> /log = print log")
        print_to_screen("SYShelper> /noecho = hide status")
        #print_to_screen("SYShelper> /")
        #print_to_screen("SYShelper> /")
        #print_to_screen("SYShelper> /")
        #print_to_screen("SYShelper> /")
    elif cmd == "/exit" or cmd == EXIT_STR:
        run = False
        recloop = False
        print_log("user exit\n")
        try:
            conn.send(EXIT_STR)
            print_log("sended " + str(len(EXIT_STR)) + " bytes to " + repr(addr) + "\n")
        except socket.error:
            print_log("Can't send to socket\n")
            print_to_screen("SYS> Connection error")
    elif cmd == "/noecho":
        print_log("status echo is off\n")
        print_stat("")
        show_status = False
    elif cmd == "/echo":
        show_status = True
        print_log("status echo is on\n")
    elif cmd == "/log":
        show_log()
    elif cmd[0] == "/":
        print_to_screen("SYS> unknown command: '" + str(cmd) + "'")
    else:
        print_to_screen("me> " + str(cmd))
        try:
            conn.send(cmd)
            print_log("sended " + str(len(cmd)) + " bytes to " + repr(addr) + "\n")
        except socket.error:
            print_log("Can't send to socket\n")
            print_to_screen("SYS> Connection error")

#    # Get the data
#    request_data = conn.recv(10 * 1024)
#    val = ""
#    try:
#        val = json.loads(request_data)
#    except ValueError:
#        print "Not a json: '" + str(request_data) + "'"
#        continue
#
#    try:
#        if val["dir"] == '"exit"':
#            run = False
#    except KeyError:
#        pass
#
#    try:
#        if val["msg"]:
#            print val["msg"]
#    except KeyError:
#        pass
#
#    # Get the json object
#    try:
#        conn.sendall("received")
#    except Exception as e:
#        print e
#    # Close the connection
#    conn.close()

shutdown()
