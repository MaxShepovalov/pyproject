from random import random as rand
import time

def game_playcard(pcard):
	global table
	global num_fuse
	global issue
	column = pcard.get_color() - 1
	added = False
	if column in range(0,4):
		if table[column].get_number() == pcard.get_number() - 1:
			table[column].update( 0, pcard.get_number() )
			added = True
		else:
			notification("Wrong card [%s,%d]! Erasing..." % (pcard.get_color_string(), pcard.get_number()))
	else:
		issue = "[game_playcard] no such color on table: %d" % column
	if not added:
		num_fuse -= 1
		if num_fuse <= 0:
			issue = "fuse is empty. game over"
	if issue!="":
		notification(issue)
	return added

def drawTable():
	line1 = "*-**-**-**-*"
	line2 = ""
	line3 = ""
	for i in table:
		if i.get_number()==0:
			line2+="| |"
			line3+="| |"
		else:
			if i.get_color()==1:
				line2 += "|r|"
			elif i.get_color()==2:
				line2 += "|g|"
			elif i.get_color()==3:
				line2 += "|b|"
			elif i.get_color()==4:
				line2 += "|y|"
			line3 += "|%d|" % i.get_number()
	line = "%s\n%s\n%s\n%s" % (line1, line2, line3, line1)
	print(line)


def check_winner():
	win = True
	for i in table:
		if i.get_number() != 5:
			win = False
	return win

def notification(msg):
	width = len(msg)
	if width > 30:
		width = 30
	line = ""
	for i in range(0, width+2):
		line += "#"
	line += "\n#"
	words = msg.split(" ")
	pos = 0
	for w in words:
		if len(w) > width:
			line += " "
			pos += 1
		else:
			if pos+len(w) > width:
				while pos < width:
					line += " "
					pos += 1
				line += "#\n#"
				pos = 0
			elif line[len(line)-1]!="#":
				line += " "
				pos += 1
		posW = 0
		while posW < len(w):
			if pos >= width:
				line += "#\n#"
				pos = 0
			if w[posW]=="\n":
				while pos < width:
					line += " "
					pos += 1
				line += "#\n#"
				pos = 0
			else:
				line += w[posW]
				pos += 1
			posW += 1
	while pos < width:
		line += " "
		pos += 1
	line += "#\n"
	for i in range(0, width+2):
		line += "#"
	print(line)
	time.sleep(0.7)



class Player:
	def __init__(self, name, use_ai):
		self.name = name
		self.cards = [takecard(),takecard(),takecard(),takecard()]
		self.known = [Card(0,0),Card(0,0),Card(0,0),Card(0,0)]
		self.ai = use_ai
		notification("New Player \"%s\" joined" % name)

	def makeHint(self, plr, cardI, color_value):
		global num_hints
		global steps
		if num_hints > 0:
			if color_value:
				plr.known[cardI].update(plr.cards[cardI].get_color(), 0)
				notification("%s hinted %s: card %d is \"%s\"" % (self.name, plr.name, cardI, plr.cards[cardI].get_color_string()))
			else:
				plr.known[cardI].update(0, plr.cards[cardI].get_number())
				notification("%s hinted %s: card %d is %s" % (self.name, plr.name, cardI, plr.cards[cardI].get_number()))
			num_hints -= 1
			steps += 1
		else:
			notification("To %s > No hint points! Can't make a hint" % self.name)

	def eraseCard(self, cardI):
		global num_hints
		notification("card [%s,%d] was deleted from %s" % (self.cards[cardI].get_color_string(), self.cards[cardI].get_number(), self.name))
		del self.cards[cardI]
		del self.known[cardI]
		if num_hints < 6:
			num_hints += 1
		newcard = takecard()
		if newcard != None:
			self.cards.append(newcard)
			self.known.append(Card(0,0))

	def playcard(self, cardI):
		if game_playcard(self.cards[cardI]):
			notification("%s played card [%s,%s]" % (self.name, self.cards[cardI].get_color_string(), self.cards[cardI].get_number()))
		self.eraseCard(cardI)

	def drawCards(self):
		line1 = ""
		line2 = ""
		line3 = ""
		line4 = ""
		if self.ai:
			cardN = 1
			for i in range(0, len(self.cards)):
				line1 += "%d-*" % cardN
				known = "|"
				if self.known[i].get_color() != 0:
					known = ">"
				if self.cards[i].get_color()==1:
					line2 += "%sr|" % known
				elif self.cards[i].get_color()==2:
					line2 += "%sg|" % known
				elif self.cards[i].get_color()==3:
					line2 += "%sb|" % known
				elif self.cards[i].get_color()==4:
					line2 += "%sy|" % known
				known = "|"
				if self.known[i].get_number() != 0:
					known = ">"
				line3 += "%s%d|" % (known, self.cards[i].get_number())
				line4 += "*-*"
				cardN += 1
		else:
			cardN = 1
			for i in self.known:
				line1 += "%d-------*" % cardN
				line2 += "|%s|" % i.get_color_string()
				line3 += "|%s|" % i.get_number_string()
				line4 += "*-------*"
				cardN += 1
		line = "%s\n%s\n%s\n%s" % (line1, line2, line3, line4)
		print(line)

class Card:
	def __init__(self, col, num):
		self.color = col
		self.number = num

	def get_color(self):
		return self.color

	def get_color_string(self):
		line = "color #%d" % self.color
		if self.color == 1:
			line = "  red  "
		elif self.color == 2:
			line = " green "
		elif self.color == 3:
			line = " blue  "
		elif self.color == 4:
			line = "yellow "
		elif self.color == 0:
			line = "unknown"
		return line

	def get_number(self):
		return self.number

	def get_number_string(self):
		line = "number %d" % self.number
		if self.number == 0:
			line = "unknown"
		else:
			line = "   %d   " % self.number
		return line

	def update(self, col, num):
		if col!= 0:
			self.color = col
		if num!= 0:
			self.number = num

def debug_print_cards(arr):
	print("===CARD=ARRAY===")
	for i in arr:
		print("*-------*\n|%s|\n|%s|\n*-------*" % (i.get_color_string(), i.get_number_string()))

def randomize(arr):
	b = []
	for i in range(0, len(arr)):
		num = int(len(arr)*rand())
		b.append(arr.pop(num))
	return b

stack = []
for col in range(0,4): #color
	for num in range(0,5): #number
		stack.append(Card(col+1, num+1))
		stack.append(Card(col+1, num+1))
		if num < 5:
			stack.append(Card(col+1, num+1))
			if num < 3:
				stack.append(Card(col+1, num+1))

def takecard():
	if len(stack) > 0:
		return stack.pop()
	else:
		return

def drawScr():
	print("\n===========\n")
	for i in players:
		if i.ai:
			i.drawCards()
	print("TABLE:")
	drawTable()
	print("Your:")
	players[0].drawCards()
	print("Hints: %d Fuse: %d Stack: %d" % (num_hints, num_fuse, len(stack)))

def in_list(arr, card):
	for crd in arr:
		if crd.color == card.color:
			if crd.number == card.number:
				return True
	return False

def color_in_list(arr, color):
	for crd in arr:
		if crd.color == color:
				return True
	return False

def number_in_list(arr, numb):
	for crd in arr:
		if crd.number == numb:
				return True
	return False

ai_dis = False
def run_AI():
	global steps
	if not ai_dis:
		for bot in players:
			if bot.ai:
				move_done = False
				#___check desirable cards")
				wanted_cards = []
				for i in range(0,4):
					if table[i].get_number() != 5:
						wanted_cards.append(Card(table[i].get_color(), table[i].get_number() + 1))
				#___check min val on table")
				minval = 6
				for i in table:
					if minval > i.get_number():
						minval = i.get_number()
				#___bot should have cards")
				if len(bot.known) > 0:
					#___check the card")
					for kcard in range(0,len(bot.known)):
						#___make info easy to use")
						col = bot.known[kcard].get_color()
						val = bot.known[kcard].get_number()
						#___if the number too small, erase it")
						if val !=0 and val < minval:
							bot.eraseCard(kcard)
							move_done = True
							break
						#___if the number too small for color, erase it")
						if val !=0 and col!=0:
							if val <= table[col-1].get_number():
								bot.eraseCard(kcard)
								move_done = True
								break
						#___if the color is full (no desirable cards with that color)")
						if col!=0 and not color_in_list(wanted_cards, col):
							bot.eraseCard(kcard)
							move_done = True
							break
						#___if the card is desirable")
						if in_list(wanted_cards, bot.known[kcard]):
							bot.playcard(kcard)
							move_done = True
							break
						
				#___check dublicates")
				if not move_done:
					for i in range(0,len(bot.cards) - 1):
						if bot.known[i].color != 0 and bot.known[i].number != 0 and not move_done:
							for j in range(i+1, len(bot.cards)):
								if bot.known[j].color != 0 and bot.known[j].number != 0:
									if bot.known[i].color == bot.known[j].color and not move_done:
										if bot.known[i].number == bot.known[j].number:
											bot.eraseCard(i)
											move_done = True
											break
				#___finding cards for hint")
				if not move_done and num_hints > 0:
					#___check next players")
					for receiver in players:
						if receiver != bot and not move_done:
							for crdN in range(0,len(receiver.cards)):
								if in_list(wanted_cards, receiver.cards[crdN]):
									#___found good card")
									if receiver.known[crdN].get_number() == 0:
										bot.makeHint(receiver, crdN, False)
										move_done = True
										break
									elif receiver.known[crdN].get_color() == 0:
										bot.makeHint(receiver, crdN, True)
										move_done = True
										break
				#___try to find old cards")
				if not move_done and num_hints > 0:
					for receiver in players:
						if receiver != bot and not move_done:
							for crdN in range(0,len(receiver.cards)):
								if not color_in_list(wanted_cards, receiver.cards[crdN].get_color()):
									#___color is full")
									bot.makeHint(receiver, crdN, True)
									move_done = True
									break
								elif receiver.cards[crdN].get_number() < minval:
									#___all colors with that number were played")
									bot.makeHint(receiver, crdN, False)
									move_done = True
									break
				#___notify about important card")
				if not move_done and num_hints > 0:
					for receiver in players:
						if receiver != bot:
							for i in range(0,5):
								Dnum = 5 - i
								for crdN in range(0,len(receiver.cards)):
									if receiver.cards[crdN].get_number() == Dnum and not move_done:
										#___found card with max number:")
										if receiver.known[crdN].get_number() == 0:
											bot.makeHint(receiver, crdN, False)
											move_done = True
											break
										elif receiver.known[crdN].get_color() == 0:
											bot.makeHint(receiver, crdN, True)
											move_done = True
											break
				if not move_done:
					notification("%s missed turn" % bot.name)
				else:
					steps += 1
	else:
		notification("AI disabled")
	drawScr()

steps = 0
stack = randomize(stack)
num_players = 2 #2...5
players = []
players.append(Player("Player", False))
players.append(Player("Bot1", True))
players.append(Player("Bot2", True))
players.append(Player("Bot3", True))

num_hints = 6
num_fuse = 3
table = [Card(1,0), Card(2,0), Card(3,0), Card(4,0)]
issue = ""

play = True
drawScr()
while play and issue=="":
	############################################################
	cmd = raw_input()
	cmd_w = cmd.split(' ')
	if cmd_w[0] == 'help':
		print("Availible commands:\nhint1 [player#] [card#] color\nhint1 [player#] [card#] number\nhint [player#] [color/number] <cards0123>\nplay [card#]\ndrop [card#]\nmiss\nhelp\ncheat\ntoggle_ai\nexit")
	elif cmd_w[0]=='miss':
		notification("player missed turn")
		run_AI()
	elif cmd_w[0]=="toggle_ai":
		ai_dis = not ai_dis
	elif cmd_w[0]=='hint1':
		if len(cmd_w) == 4:
			if int(cmd_w[1]) < len(players):
				plrN = int(cmd_w[1])
				if int(cmd_w[2]) < len(players[plrN].cards) + 1:
					crdN = int(cmd_w[2]) - 1
					if cmd_w[3] == "color":
						players[0].makeHint(players[plrN], crdN, True)
						run_AI()
					elif cmd_w[3] == "number":
						players[0].makeHint(players[plrN], crdN, False)
						run_AI()
					else:
						notification("can give a hint only as color or number, not %s" % cmd_w[3])
				else:
					notification("player %d have only %d cards!" % (plrN, len(players[plrN].cards)))
			else:
				notification("there are only %d players!" % len(players))
		else:
			notification("not enought parameters. got %d, need 4" % len(cmd_w))
	elif cmd_w[0]=='hint':
		if len(cmd_w) == 4:
			if int(cmd_w[1]) < len(players):
				plrN = int(cmd_w[1])
				if int(max(cmd_w[3])) <= 4 and int(min(cmd_w[3])) >= 1:
					if cmd_w[2] in ["yellow", "red", "green", "blue", "y", "Y", "r", "R", "g", "G", "b", "B"]:
						col = 0
						if cmd_w[2] in ["red", "r", "R"]:
							col = 1
						elif cmd_w[2] in ["green", "g", "G"]:
							col = 2
						elif cmd_w[2] in ["blue", "b", "B"]:
							col = 3
						elif cmd_w[2] in ["yellow", "y", "Y"]:
							col = 4
						permit = True
						for P in range(0,len(cmd_w[3])):
							if players[plrN].cards[int(cmd_w[3][P])-1].get_color() != col:
								permit = False
						if permit:
							for P in range(0,len(cmd_w[3])):
								players[0].makeHint(players[plrN], int(cmd_w[3][P])-1, True)
								num_hints += 1
							num_hints -= 1
							run_AI()
						else:
							notification("not all mentioned cards have the same color")
					elif int(cmd_w[2]) in range(1,6):
						permit = True
						for P in range(0,len(cmd_w[3])):
							if players[plrN].cards[int(cmd_w[3][P])-1].get_number() != int(cmd_w[2]):
								permit = False
						if permit:
							for P in range(0,len(cmd_w[3])):
								players[0].makeHint(players[plrN], int(cmd_w[3][P])-1, False)
								num_hints += 1
							num_hints -= 1
							run_AI()
						else:
							notification("not all mentioned cards have the same number")
					else:
						notification("use color word or number only, not %s" % cmd_w[2])
				else:
					notification("card numbers can only be 1, 2, 3, and 4")
			else:
				notification("there are only %d players" % len(players))
		else:
			notification("not enought parameters. got %d, need 4" % len(cmd_w))
	elif cmd_w[0]=='play':
		if len(cmd_w) == 2:
			if int(cmd_w[1]) - 1 < len(players[0].cards):
				crdN = int(cmd_w[1]) - 1
				players[0].playcard(crdN)
				run_AI()
			else:
				notification("you have only %d cards!" % len(players[0].cards))
		else:
			notification("not enought parameters. got %d, need 2" % len(cmd_w))
	elif cmd_w[0]=='exit':
		play = False
	elif cmd_w[0]=='cheat':
		for i in range(0,len(players[0].cards)):
			col = players[0].cards[i].get_color()
			num = players[0].cards[i].get_number()
			players[0].known[i].update(col, num)
		num_hints = 6
		num_fuse = 3
		drawScr()
	elif cmd_w[0]=='drop':
		if len(cmd_w) == 2:
			if int(cmd_w[1]) - 1 < len(players[0].cards):
				crdN = int(cmd_w[1]) - 1
				players[0].eraseCard(crdN)
				run_AI()
			else:
				notification("you have only %d cards" % len(players[0].cards))
		else:
			notification("not enought parameters. got %d, need 2" % len(cmd_w))
	else:
		notification("%s command not supported" % cmd_w[0])

	if check_winner():
		play = False
	############################################################

if issue!="":
	print("ERROR: %s" % issue)

if check_winner():
	print("Team win!")
	print("Steps done: %d" % steps)
