import curses
from curses import panel
import threading
import time

print("GUI LOADED")

READY = False
cmd_line = []
old_cmd = ['']

K_UP = 259
K_DW = 258
K_LF = 260
K_RG = 261
K_BCK = 127

#this is for thread
thr = 0
thr_active = True

#screens
scr = None
win_input = None
pan_input = None
win_status = None
pan_status = None
win_msg = None
pan_msg = None

def print_to_scr(msg):
	#print ">" + msg to win_msg
	if READY:
		win_msg.scroll(1)
		win_msg.move(10,0)
		win_msg.addstr(msg)
		panel.update_panels()
		curses.doupdate()
	else:
		print("GUI_subsys > GUI is not ready")
		print(msg)

def print_to_stat(msg):
	#print ">" + msg to win_status
	if READY:
		win_status.clear()
		win_status.addstr(0, 0, msg[:50])
		panel.update_panels()
		curses.doupdate()
	else:
		print_to_scr(msg)

def print_to_input(msg):
	#print ">" + msg to win_input
	if READY:
		win_input.clear()
		print("GUI GOT : {" + msg + "}")
		win_input.addstr(0, 0, msg[:50])
		panel.update_panels()
		curses.doupdate()

def getline():
	global cmd_line
	ret_line = None
	if len(cmd_line) != 0:
		ret_line = cmd_line[0]
		cmd_line = cmd_line[1:]
	return ret_line

def reading_thread():
	global cmd_line
	cur_line = ""
	cur_pos = len(cur_line)
	cur_cmd = 0
	pre_l = cur_line[0:cur_pos]
	pos_l = cur_line[cur_pos:]
	while thr_active:
		key = scr.getch()
		if key in range(32,127):
			pre_l += chr(key)
			cur_line = pre_l + pos_l
			cur_pos += 1
		elif key == 10:
			cmd_line.append(cur_line)
			old_cmd.insert(1, cur_line)
			old_cmd[0] = ''
			cur_cmd = 0
			cur_line = ""
			cur_pos = 0
			pre_l = ''
			pos_l = ''
		elif key == K_UP:
			old_cmd[cur_cmd] = cur_line
			if cur_cmd < len(old_cmd)-1:
				cur_cmd += 1
			cur_line = old_cmd[cur_cmd]
			cur_pos = len(cur_line)
			pre_l = cur_line
			pos_l = ''
		elif key == K_DW:
			old_cmd[cur_cmd] = cur_line
			if cur_cmd > 0:
				cur_cmd -= 1
			cur_line = old_cmd[cur_cmd]
			cur_pos = len(cur_line)
			pre_l = cur_line
			pos_l = ''
		elif key == K_LF:
			if cur_pos > 0:
				cur_pos -= 1
				pre_l = cur_line[0:cur_pos]
				pos_l = cur_line[cur_pos:]
		elif key == K_RG:
			if cur_pos < len(cur_line):
				cur_pos += 1
				pre_l = cur_line[0:cur_pos]
				pos_l = cur_line[cur_pos:]
		elif key == K_BCK:
			pre_l = pre_l[:-1]
			cur_line = pre_l + pos_l
			if cur_pos > 0:
				cur_pos -= 1
		print_to_input(cur_line)

def start():
	global READY
	global thr
	global scr
	global win_input
	global pan_input
	global win_status
	global pan_status
	global win_msg
	global pan_msg
	if not READY:
		scr = curses.initscr()
		scr.keypad(1)
		curses.noecho()
		curses.halfdelay(1)

		win_msg = curses.newwin(11,53,0,0)
		win_msg.scrollok(1)
		pan_msg = panel.new_panel(win_msg)
		pan_msg.show()
		win_input = curses.newwin(3,53,12,0)
		pan_input = panel.new_panel(win_input)
		pan_input.show()
		win_status = curses.newwin(3,53,14,0)
		pan_status = panel.new_panel(win_status)
		pan_status.show()
		READY = True

		thr = threading.Thread(target=reading_thread)
		thr.start()

def stop():
	global READY
	global thr_active
	thr_active = False
	if thr != 0:
		while thr.is_alive():
			time.sleep(1)
	READY = False
	curses.echo()
	curses.curs_set(True)
	curses.endwin()