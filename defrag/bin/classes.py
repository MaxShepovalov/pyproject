class cell:
    def __init__(self):
        self.dmem = 0
        self.dtype = "Null"
        self.addr = -1

    def writeMem(self, data, tp):
        self.dmem = data
        self.dtype = tp

    def readCell(self):
        return self.dmem

    def readMem(self):
        outD = self.dmem
        if self.addr in range(MEM_SIZE):
            outD += MEM_ARR[self.addr].readMem()
        return outD

    def calcSize(self):
        itr = 1
        if self.addr in range(MEM_SIZE):
            itr += MEM_ARR[self.addr].calcSize()
        return itr

    def readType(self):
        return self.dtype

    def makeChain(self, adr):
        global ERR_STR
        err = 0
        if MEM_ARR[adr] != self:
            if adr in range(MEM_SIZE):
                self.addr = adr
            else:
                err = 1
                ERR_STR = "memory index %d out of range" % adr
        else:
            err = 1
            ERR_STR = "next cell should be different cell"
        return err

    def clearCell(self):
        self.addr = -1
        self.writeMem(0,"Null")

    def clearMem(self):
        num = 1
        if self.addr in range(MEM_SIZE):
            num += MEM_ARR[self.addr].clearMem()
        self.clearCell()
        return num

########################

class header():
    def __init__(self):
        self.title = ""
        self.size = 0
        self.addr = -1

    def makeMem(self, name, data, tp):
        global ERR_STR
        err = 0
        blocks = []
        #prepare data
        if tp == "Null":
            err = 1
            ERR_STR = "can't write Null. use \"freeMem()\" method"
        elif tp == "String":
            for i in data: # chars
                blocks.append(i)
        elif tp == "Int":
            blocks.append(data)
        elif tp == "Bool":
            blocks.append(data)
        #count empty cells
        memAddrs = []
        for c in range(MEM_SIZE):
            if MEM_ARR[c].readType() == "Null" and MEM_ARR[c].addr == -1:
                memAddrs.append(c)
        if len(memAddrs) < len(blocks):
            err = 1
            ERR_STR = "not enough space in memory %d given, %d availible" % (len(blocks), len(memAddrs))
        #write
        if err == 0:
            for blN in range(len(blocks)):
                MEM_ARR[memAddrs[blN]].writeMem(blocks[blN], tp)
                if blN != len(blocks)-1:
                    MEM_ARR[memAddrs[blN]].makeChain(memAddrs[blN+1])
                else:
                    MEM_ARR[memAddrs[blN]].makeChain(-1)
            self.title = name
            self.addr = memAddrs[0]
            self.size = MEM_ARR[self.addr].calcSize()
        return err

    def readMem(self):
        return MEM_ARR[self.addr].readMem()

    def freeMem(self):
        global ERR_STR
        err = 0
        #get size
        size = MEM_ARR[self.addr].calcSize()
        sizeDel = MEM_ARR[self.addr].clearMem()
        if size != sizeDel:
            err = 1
            ERR_STR = "File %s blocks deleted %d blocks" % (size, sizeDel)
        return err

############################
