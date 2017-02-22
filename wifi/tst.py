import gui

gui.start()

for i in range(0,15):
	gui.print_to_scr("This is a line %d on screen" % i)

gui.print_to_stat("This is a status")

gui.print_to_input("This is input")

run = True
while run:
	cmd = gui.getline()
	if cmd == None:
		continue
	gui.print_to_scr("got: " + cmd)
	if cmd == 'exit':
		gui.stop()
		run = False

gui.stop()
