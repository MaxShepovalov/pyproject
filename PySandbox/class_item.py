#Player holds an item in hand or in a pocket

#Item has one main function, that operates on other instance in the world

#notifications
from class_base import notify

class item_dummy(object):
	pic = None
	name = 'Generic Item'
	def action(self, target, player):
		notify('this thing does nothing')

#predefined Items:

class item_changer(item_dummy):
	pic = None
	name = 'Changer'
	import io_notepad
	def action(self, target, player):
		if target!=None:
			#open notepad if target was selected
			io_notepad.openApp(target)
		else:
			notify('Target is not selected')