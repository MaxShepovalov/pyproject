import top_left as TL
import curses
import time

KEY_UP = 259
KEY_DOWN = 258
KEY_LEFT = 260
KEY_RIGHT = 261
KEY_RETURN = 10
KEY_ESC = 27

layer = 0 #window selector layer

TL.draw(layer)

run = True
while run:
    key = TL.getKey(layer)
    if key == KEY_ESC:
        TL.status('pressed %d EXIT   layer %d  ' % (key, layer))
        TL.draw(layer)
        time.sleep(0.5)
        run = False
        break
    elif key == KEY_UP:
        #TL.status('pressed %d UP     layer %d  ' % (key, layer))
        TL.upEvent(layer)
    elif key == KEY_DOWN:
        #TL.status('pressed %d DOWN   layer %d  ' % (key, layer))
        TL.downEvent(layer)
    elif key == KEY_LEFT:
        #TL.status('pressed %d LEFT   layer %d  ' % (key, layer))
        TL.leftEvent(layer)
    elif key == KEY_RIGHT:
        #TL.status('pressed %d RIGHT  layer %d  ' % (key, layer))
        TL.rightEvent(layer)
    elif key == KEY_RETURN:
        #TL.status('pressed %d RETURN layer %d  ' % (key, layer))
        run, dl = TL.selectEvent(layer)
        layer += dl
    elif key != -1:
        TL.status('pressed %d        layer %d  ' % (key, layer))
    TL.draw(layer)

TL.close()