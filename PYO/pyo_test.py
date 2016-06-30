from pyo import *
s = Server().boot()

#Main amp
s.amp = 0.3

#signal stack
stk = ['Input', 'Delay', 'Disto', 'MonoToStereo', 'Out']
#signal memory
ch = []

#read pattern
for i in stk:
    if i == 'Input':
        ch.append(1)
        ind = len(ch) - 1
        ch[ind] = Input(chnl=0)
    if i == 'Delay':
        ch.append(1)
        ind = len(ch) - 1
        ch[ind] = Delay( ch[ind - 1])
    if i == 'Disto':
        ch.append(1)
        ind = len(ch) - 1
        ch[ind] = Disto( ch[ind - 1])
    if i =='Out':
        ind = len(ch) - 1
        ch[ind].out()
    if i =='MonoToStereo':
        ch.append(1)
        ind = len(ch) - 1
        ch[ind] = ch[ind-1].mix(2)

#start server
s.start()
s.gui(locals())
