import task
import wire
import devices


wire.addBus('bus01', 3)

wire.addBus('result',1)
wire.addBus('carry',1)
wire.addBus('test',1)

wire.printReport()


#       res
#  A-[ ]->[ ]
#  B-[+]  [&]-> tst
#  C-[ ]->[ ]
#       car

#register adder 3:2+
print('REGISTER==============================')
inset = [('bus01', 2), ('bus01', 1), ('bus01', 0)]
outset = [('carry',0), ('result',0)]
devices.addDevice('adder', '3:2+', inset, outset)
task.doAll()
inset = [('result',0),('carry',0)]
outset = [('test',0)]
devices.addDevice('And', 'and', inset, outset)
task.doAll()


#set input
print('INPUT 0==============================')
wire.setBinary('bus01', 3)
task.doAll()
wire.printReport()

#set input
print('INPUT 3==============================')
wire.setBinary('bus01', 7)
task.doAll()
wire.printReport()