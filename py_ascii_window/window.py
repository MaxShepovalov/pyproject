class canvas:
    def __init__(self, width, height):
        self.xcur = 0
        self.ycur = 0
        self.X = width
        self.Y = height
        self.clear()

    def set_cursor(self, xc, yc):
        self.xcur = xc
        self.ycur = yc

    def move_cursor(self, xc, yc):
        self.xcur = self.xcur + xc
        self.ycur = self.ycur + yc

    def draw(self):
        lines = 'NEW CANVAS\n'
        for i in range (0, self.Y):
            line = ''.join(self.dots[i])
            lines = lines + line + '|\n'
        del line
        print(lines)
        del lines

    def write(self, line):
        for i in line:
            if self.xcur in range(0,self.X)\
            and self.ycur in range(0,self.Y):
            #if self.xcur < self.X\
            #and self.ycur < self.Y\
            #and self.xcur >= 0\
            #and self.ycur >= 0:
                self.dots[self.ycur][self.xcur] = i
                self.move_cursor(1, 0)

    def clear(self):
        self.dots = []
        for line in range(0, self.Y):
            self.dots.append([])
            for row in range(0, self.X):
                self.dots[line].append(' ')

class box:

    def __init__(self):
        self.symbH = '='
        self.symbV = '|'
        self.symbC = '#'
        self.xpos=0
        self.ypos=0
        self.xsize = 1
        self.ysize = 1
        self.tbox = textbox("", 1, 1)

    def pos(self, nx, ny):
        self.xpos = nx
        self.ypos = ny

    def size(self, nx, ny):
        self.xsize = nx
        self.ysize = ny
        self.tbox.xsize = nx
        self.tbox.ysize = ny

    def project(self, screen):
        lineC = []
        lineM = []
        lineC.append(self.symbC)
        lineM.append(self.symbV)
        for i in range(0, self.xsize):
            lineC.append(self.symbH)
            lineM.append(' ')
        lineC.append(self.symbC)
        lineM.append(self.symbV)
        screen.set_cursor(self.xpos, self.ypos)
        screen.write(lineC)
        for i in range(0, self.ysize):
            screen.set_cursor(self.xpos, self.ypos + 1 + i)
            screen.write(lineM)
        screen.move_cursor(- self.xsize - 2, 1)
        screen.write(lineC)
        screen.set_cursor(self.xpos + 1, self.ypos + 1)
        self.tbox.project(screen)

class textbox:
    def __init__(self, text, xs, ys):
        self.xoff = 0
        self.yoff = 0
        self.text = text
        self.xsize = xs
        self.ysize = ys

    def project(self, screen):
        num = 0
        for i in self.text:
            screen.write(i)
            num = num + 1
            if num >= self.xsize:
                screen.move_cursor(-self.xsize, 1)
                num = 0
        del num

    def write(self, text):
        if len(text)>self.xsize*self.ysize:
            print('[ERROR] text is too big')
        else:
            self.text = text
