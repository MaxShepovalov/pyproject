import socket

ip = "0.0.0.0"

hi = ['hi','hello','Hi','Hello','Greetings','greetings']

s = socket.socket()
s.connect((ip, 8602))

EXIT_STR = "{{cmd}}::exit"

run = True
while run:
	ans = '0000'
	data = s.recv(1024)
	print("remote > " + repr(data))
	if data in hi:
		ans = 'Hi'

	elif data == 'Ahoy':
		ans = "How r ya doin' matey?"

	elif data == EXIT_STR:
		ans = EXIT_STR
		run = False

	elif data == "Who am I?":
		ans = "You are '" + str(ip) + "'"

	else:
		ans = 'What is it?'
	print("ans    > " + str(ans))
	s.send(ans)