import redactor
import aly

MEM_SIZE = 20

MEM_ARR = []
HEAD_ARR = []

def isnumber(strg):
    ans = True
    for ch in strg:
        if not ch in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            ans = False
            break
    return ans

ERR_STR = ""

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

def gl_calcEmpty():
    num = 0
    for c in MEM_ARR:
        if c.addr == -1 and c.readType() == "Null":
            num += 1
    return num

def gl_memstat():
    emp = gl_calcEmpty()
    usd = MEM_SIZE - emp
    perE = int(100.0 * float(emp) / MEM_SIZE)
    perU = 100 - perE
    print("%d (%d%c)used; %d (%d%c) free; %d total" % (usd, perU, chr(37), emp, perE, chr(37), MEM_SIZE))

def gl_printmem():
    print("###Memory###")
    for c in range(MEM_SIZE):
        cl = MEM_ARR[c]
        print("%d> %s| at %d : %s" % (c, cl.readType(), cl.addr, cl.readCell() ))

def gl_showHead():
    print("###HEAD###")
    for h in range(len(HEAD_ARR)):
        hd = HEAD_ARR[h]
        print("%d> at %d | %db : %s" % (h, hd.addr, hd.size, hd.title))

def gl_getFileNames():
    names = []
    for h in HEAD_ARR:
        names.append(h.title)
    return names

def gl_addfile(title, data, tp):
    if title == "":
        print("[gl_addfile] File should have a name")
    else:
        HEAD_ARR.append(header())
        nfile = HEAD_ARR[len(HEAD_ARR)-1]
        if nfile.makeMem(title, data, tp) != 0:
            del HEAD_ARR[len(HEAD_ARR)-1]
            print(ERR_STR)

def gl_findFile(title):
    global ERR_STR
    #find file
    fileN = []
    for h in range(len(HEAD_ARR)):
        if HEAD_ARR[h].title == title:
            fileN.append(h)
            break
    if len(fileN) == 0:
        ERR_STR = "File %s not found" % title
        return -1
    elif len(fileN) > 1:
        ERR_STR = "more than one %s file found" % title
        return -2
    return fileN[0]

def gl_printfile(title):
    fileN = gl_findFile(title)
    if fileN < 0:       
        print(ERR_STR)
    else:       
        data = HEAD_ARR[fileN].readMem()
        print("\n%s:\n%s" % (title, str(data)))

def gl_delfile(title):
    fileN = gl_findFile(title)
    if fileN < 0:       
        print(ERR_STR)
    else:       
        if HEAD_ARR[fileN].freeMem() != 0:
            print(ERR_STR)
        else:
            del HEAD_ARR[fileN]

def gl_help(topic, first):
    if first:
        print("Python demo")
    if topic == "":
        gl_help("alias", False)
        gl_help("addfile", False)
        gl_help("printfile", False)
        gl_help("delfile", False)
        gl_help("printmem", False)
        gl_help("memstat", False)
        gl_help("nano", False)
        gl_help("malloc", False)
        gl_help("free", False)
        gl_help("defrag", False)
        gl_help("ls", False)
        gl_help("exit", False)
        gl_help("help", False)
    elif topic == "help":
        print(" help                         - shows all commands")
        print(" help [command]               - shows info about specific command")
    elif topic == "addfile":
        print(" addfile <Name> <data> <type> - adds file to memory")
    elif topic == "printfile":
        print(" printfile <Name>             - prints file to screen")
    elif topic == "delfile":
        print(" delfile <Name>               - deletes file from memory")
    elif topic == "nano":
        print(" nano [file]                  - easy way to create or edit files")
    elif topic == "printmem":
        print(" printmem                     - shows current memory blocks")
    elif topic == "memstat":
        print(" memstat                      - shows current memory status")
    elif topic == "defrag":
        print(" defrag [option]              - defragment memory")
        if first:
            print("   Usage: defrag [-a|-af|-f]")
            print("no option - defragment")
            print("     -a   - analyse only")
            print("     -ag  - analyse and draw defragmented memory")
            print("     -af  - analyse and print memory data")
            print("     -f   - defragment and always print memory data")
    elif topic == "ls":
        print(" ls                           - shows names of files")
    elif topic == "exit":
        print(" exit                         - exit demo")
    elif topic == "malloc":
        print(" malloc <size>                - mounts new memory")
        if first:
            print("   \"malloc\" handles sizes only from 1 to 1024")
    elif topic == "free":
        print(" free <size>                  - unmounts memory")
        if first:
            print("   Usage: free [-f] <size>\n     -f   - force unmount. Will delete any data in")
            print("            last memory cells if there was not enough\n            number of empty cells.\n")
            print("            CAN DAMAGE DATA")
            print("   \"free\" handles sizes only from 1 to 1024")
    elif topic == "alias":
        print(" alias <action> [params]      - shows, makes and deletes aliases")
        if first:
            print("   Usage: alias                        - shows all aliases")
            print("          alias add <alias> <function> - add alias")
            print("          alias del <alias>            - delete alias")
    else:
        print(" there is no such command \"%s\"" % topic)
        gl_help("help", False)

def gl_malloc(length):
    global MEM_SIZE
    for i in range(length):
        MEM_ARR.append(cell())
    MEM_SIZE = len(MEM_ARR)

def gl_free(length, force):
    global MEM_SIZE
    emp = gl_calcEmpty()
    if length > MEM_SIZE:
        print(" can't unmount %d cells. There is only %d cells in memory" % (force, MEM_SIZE))
    if emp < length and not force:
        print(" can't unmount %d cells" % force)
    else:
        i = MEM_SIZE - 1
        deleted = 0
        while i >= 0 and deleted < length:
            if MEM_ARR[i].readType() == "Null" and MEM_ARR[i].addr == -1:
                del MEM_ARR[i]
                MEM_SIZE -= 1
                deleted += 1
                i -= 1
            else:
                #search nearest empty space and move neighbour cell there
                j = i
                while MEM_ARR[j].readType() != "Null" or MEM_ARR[j].addr != -1:
                    j -= 1
                    if j == -1:
                        if not force:
                            print("Error. Can't find empty cell")
                            print("i = %d" % i)
                            return 1
                        else:
                            del MEM_ARR[i]
                            MEM_SIZE -= 1
                            deleted += 1
                            i -= 1
                print("empty cell at j=%d" % j)
                if j != -1:
                    df_doswap(j+1, j);

def gl_movefile(name, newpos):
    fNum = gl_findFile(name)
    if fNum >= 0:
        fSize = HEAD_ARR[fNum].size
        fPos = HEAD_ARR[fNum].addr
        if newpos+fSize < MEM_SIZE - 1:
            for i in range(fSize):
                df_doswap(fPos, newpos + i)
                fPos = MEM_ARR[newpos + i].addr
                if fPos == -1 and i < fSize-1:
                    print("unexpected EOF")
                    break
                #mf = df_analyse()
                #df_showFragmStat(mf, True)
        else:
            print("new position is too close to the end of the memory. File will be damaged\ntry %d, given %d" % (MEM_SIZE - 1 - fSize, newpos))
    else:
        print(ERR_STR)

########################

class frag_cell():
    def __init__(self):
        self.file = ""
        self.num = -1
        self.fragm = False

def df_calcFrag(mf):
    fN = 0
    for mem in mf:
        if mem.fragm:
            fN += 1
    return int(100 * float(fN) / len(mf))

def df_printmem():
    mem = "data:     "
    for mcell in MEM_ARR:
        if mcell.readType() == "Null":
            mem += " .."
        elif mcell.readType() == "Int":
            mem += " %02d" % mcell.readCell()
        elif mcell.readType() == "Bool":
            if mcell.readCell():
                mem += " B1"
            else:
                mem += " B0"
        elif mcell.readType() == "String":
            mem += "  %c" % mcell.readCell()
    print(mem)

def df_showFragmStat(mf, full):
    Fl = "\nfilename: "
    num = "frgm num: "
    lnk = "link to:  "
    frg = "fragment: "
    if not full:
        frg = "\nfragment: "
    Cnum = "address:  "
    Cn = 0
    for mem in mf:
        if full:
            if len(mem.file) >= 2:
                Fl += " %c%c" % (mem.file[0], mem.file[1])
            elif len(mem.file) >= 1:
                Fl += "  %c" % mem.file[0]
            else:
                Fl += " ??"
            num += " %02d" % mem.num
            frg += " "
            Cnum += " "
        if mem.fragm:
            frg += "##"
        else:
            frg += "__"
        if full:
            Cnum += "%02d" % (Cn % 100)
            Cn += 1
    for mem in MEM_ARR:
        lnk += " %02d" % mem.addr
    if full:
        print(Fl)
        print(num)
    print(frg)
    if full:
        df_printmem()
        print(lnk)
        print(Cnum)
    #count
    print("Fragmentation %d%c" % (df_calcFrag(mf), chr(37)))

def df_doswap(src, dest):
    #if gl_calcEmpty() > 0:
    #search cell that points to SRC
    #repoint it to DEST
    for i in range(MEM_SIZE):
        if MEM_ARR[i].addr == src:
            #print("cell %d points at source %d" % (i, src))
            MEM_ARR[i].addr = dest
        elif MEM_ARR[i].addr == dest:
            #print("cell %d points at destination %d" % (i, src))
            MEM_ARR[i].addr = src
    #search head that points to SRC
    #reset it to DEST
    for i in range(len(HEAD_ARR)):
        if HEAD_ARR[i].addr == src:
            #print("header \"%s\" points at source %d " % (HEAD_ARR[i].title, src))
            HEAD_ARR[i].addr = dest
        elif HEAD_ARR[i].addr == dest:
            #print("header \"%s\" points at destination %d " % (HEAD_ARR[i].title, src))
            HEAD_ARR[i].addr = src
    #move cell from src to dest
    membuff = cell()
    membuff.writeMem( MEM_ARR[dest].readCell(), MEM_ARR[dest].readType())
    membuff.addr = MEM_ARR[dest].addr

    MEM_ARR[dest].clearCell()
    MEM_ARR[dest].writeMem( MEM_ARR[src].readCell(), MEM_ARR[src].readType())
    MEM_ARR[dest].addr = MEM_ARR[src].addr

    MEM_ARR[src].clearCell()
    MEM_ARR[src].writeMem( membuff.readCell(), membuff.readType())
    MEM_ARR[src].addr = membuff.addr
    return 0
#    else:
#        print("not enough space")
#        return 1

def df_analyse():
    #creating file-mem table
    mem_f = []
    for c in range(MEM_SIZE):
        mem_f.append(frag_cell())
    #correspont files to mem
    for fl in HEAD_ARR:
        mem_pos = []
        cur_mem = fl.addr
        mem_pos.append(cur_mem)
        foc = MEM_ARR[cur_mem]
        bl = 0
        mem_f[cur_mem].file = fl.title
        mem_f[cur_mem].num = bl
        while foc.addr != -1:
            cur_mem = foc.addr
            mem_pos.append(cur_mem)
            foc = MEM_ARR[cur_mem]
            bl += 1
            mem_f[cur_mem].file = fl.title
            mem_f[cur_mem].num = bl
        #check fragmentation
        strt_pos = mem_pos[0]
        frg = False
        for i in mem_pos:
            if i != strt_pos:
                frg = True
                break
            else:
                strt_pos += 1
        if frg:
            for i in mem_pos:
                mem_f[i].fragm = True
    return mem_f

def gl_defrag(full):
    mem_f = df_analyse()
    df_showFragmStat(mem_f, full)
    fragNum = df_calcFrag(mem_f)
    if fragNum == 0:
        print("Defragmention is not necessary")
    elif gl_calcEmpty() == 0:
        print("Not enough space. Need at least 1 cell to operate. See \"memstat\"")
    else:
        print("Defragmentation...")
        ITER_NUM = 0
        while df_calcFrag(mem_f) != 0:
            ITER_NUM += 1
            mode = "Std"
            #search first fragmented file
            foc = 0
            while not mem_f[foc].fragm:
                foc += 1
                if foc >= MEM_SIZE:
                    ERR_STR("index out of memory [when locating fragmentation]")
                    return 1
            #check if first fragment is num0
            if mem_f[foc].num != 0:
                mode = "MakeFirst"
            #now foc is pointing at first fragmented file
            filename = mem_f[foc].file

            #search for cell that we need to replace (end of fragment)
            interes_p = foc
            expectNum = 0
            if mode == "Std":
                while mem_f[interes_p].file == filename and mem_f[interes_p].num == expectNum:
                    interes_p += 1
                    expectNum += 1
                    if interes_p >= MEM_SIZE:
                        ERR_STR = "index out of memory [when locating end of fragment]"
                        return 1
            elif mode == "MakeFirst":
                interes_p = foc
            else:
                ERR_STR = "Wrong mode \"%s\" when searching interes" % mode
                return 2
            
            piece_p = interes_p
            if mode == "Std":
                #search for next fragment for file
                while mem_f[piece_p].file != filename or mem_f[piece_p].num != expectNum:
                    piece_p += 1
                    if piece_p >= MEM_SIZE:
                        ERR_STR = "index out of memory [when locating next fragment]"
                        return 1
            elif mode == "MakeFirst":
                piece_p = -1
                for fl in HEAD_ARR:
                    if fl.title == filename:
                        piece_p = fl.addr
                        if mem_f[piece_p].num != 0:
                            ERR_STR = "file header %s does n't points at first fragment" % filename
                            return 3
                if piece_p == -1:
                    ERR_STR = "index out of memory [it should be the first fragment]"
                    return 1
            else:
                ERR_STR = "Wrong mode \"%s\" when searching next piece" % mode
                return 2
            #search buffer (nearest empty cell)
            buff = 0
            while MEM_ARR[buff].readType() != "Null" or MEM_ARR[buff].addr != -1:
                buff += 1
                if piece_p >= MEM_SIZE:
                    ERR_STR = "index out of memory [when locating empty cell]"
                    return 1
            #perform swap
            if df_doswap(interes_p, buff) != 0:
                break
            if df_doswap(piece_p, interes_p) != 0:
                break
            #finish iteration, update mem_f table
            mem_f = df_analyse()
            df_showFragmStat(mem_f, full)
        if df_calcFrag(mem_f) == 0:
            print("Defragmented by %d iterations" % ITER_NUM)
        else:
            print("Error occured")
    return 0

########################

def run_command(cmd_words):
    global run
    global HEAD_ARR
    global MEM_ARR
    global MEM_SIZE

    retval = -1
    if cmd_words[0] == "exit":
        run = False
        print("exit...")
        retval = 0

    elif cmd_words[0] == "ls":
        gl_showHead()
        retval = 0

    elif cmd_words[0] == "help":
        if len(cmd_words) > 1 and cmd_words[1]!="":
            gl_help(cmd_words[1], True)
        else:
            gl_help("", True)
        retval = 0

    elif cmd_words[0] == "addfile":
        if len(cmd_words) >= 4 and cmd_words[1]!="" and cmd_words[2]!="" and cmd_words[3]!="":
            gl_addfile(cmd_words[1], cmd_words[2], cmd_words[3])
        else:
            print("[gl_addfile] not enought elements! See \"help addfile\"")
        retval = 0

    elif cmd_words[0] == "nano":
        file = ""
        line = ""
        if len(cmd_words) > 1 and cmd_words[1] != "":
            file = cmd_words[1]
            fileN = gl_findFile(file)
            if fileN == -1:
                pass
            elif fileN == -2:
                print("there is more than one file")
            elif fileN >= 0 and fileN < len(HEAD_ARR):
                line = HEAD_ARR[fileN].readMem()
            else:
                print("Error with file: fileN = %d" % fileN)
                return
        line = redactor.edit(line)
        if file == "":
            print("new file\nto cancel just hit Enter")
            file = "."
            while file != "":
                print("Name: ")
                file = raw_input()
                if file == "":
                    continue
                else:
                    HEAD_ARR.append(header())
                    nfile = HEAD_ARR[len(HEAD_ARR)-1]
                    if nfile.makeMem(file, line, "String") != 0:
                        del HEAD_ARR[len(HEAD_ARR)-1]
                        print(ERR_STR)
                    else:
                        break
        else:
            if gl_findFile(file) == 0:
                gl_delfile(file)
            gl_addfile(file, line, "String")
        retval = 0

    elif cmd_words[0] == "printfile":
        if len(cmd_words) == 2 and cmd_words[1]!="":
            gl_printfile(cmd_words[1])
        else:
            print("[gl_addfile] not enought elements! See \"help printfile\"")
        retval = 0

    elif cmd_words[0] == "delfile":
        if len(cmd_words) == 2 and cmd_words[1]!="":
            gl_delfile(cmd_words[1])
        else:
            print("[gl_addfile] not enought elements! See \"help delfile\"")
        retval = 0

    elif cmd_words[0] == "printmem":
        df_printmem()
        retval = 0

    elif cmd_words[0] == "memstat":
        gl_memstat()
        retval = 0

    elif cmd_words[0] == "defrag":
        if len(cmd_words) == 1:
            out = gl_defrag(False)
            if out != 0:
                print(ERR_STR)
                print("[defrag] exit: %d" % out)
        elif len(cmd_words) == 2 and cmd_words[1] == "-a":
            memf = df_analyse()
            defr = df_calcFrag(memf)
            print("Fragmented %d%c of memory" % (defr, chr(37)))
        elif len(cmd_words) == 2 and cmd_words[1] == "-ag":
            memf = df_analyse()
            df_showFragmStat(memf, False)
        elif len(cmd_words) == 2 and cmd_words[1] == "-af":
            memf = df_analyse()
            df_showFragmStat(memf, True)
        elif len(cmd_words) == 2 and cmd_words[1] == "-f":
            out = gl_defrag(True)
            if out != 0:
                print(ERR_STR)
                print("[defrag] exit: %d" % out)
        else:
            gl_help("defrag", True)
        retval = 0

    elif cmd_words[0] == "malloc":
        if len(cmd_words) == 2 and cmd_words[1] != "":
            if int(cmd_words[1]) in range(1024):
                gl_malloc(int(cmd_words[1]))
            else:
                gl_help("malloc", True)
        else:
            gl_help("malloc", True)
        retval = 0

    elif cmd_words[0] == "free":
        if len(cmd_words) == 2 and cmd_words[1] != "":
            if int(cmd_words[1]) in range(1024):
                gl_free( int(cmd_words[1]), False)
            else:
                gl_help("free", True)
        elif len(cmd_words) == 3 and cmd_words[2] != "":
            if cmd_words[1] != "-f":
                print("unknown option %s" % cmd_words[1])
            else:
                if int(cmd_words[2]) in range(1024):
                    gl_free( int(cmd_words[2]), True)
                else:
                    gl_help("free", True)
        else:
            gl_help("free", True)
        retval = 0

    elif cmd_words[0] == "preset":
        filenames = []
        for file in HEAD_ARR:
            filenames.append(file.title)
        for name in filenames:
            gl_delfile(name)
        line = ""
        number = (MEM_SIZE - 1) / 4
        for i in range(number):
            line += chr(i%26 + 97)
        #make files
        HEAD_ARR.append(header())
        HEAD_ARR.append(header())
        HEAD_ARR.append(header())
        HEAD_ARR.append(header())
        HEAD_ARR[0].addr = 0
        HEAD_ARR[0].title = "file0"
        HEAD_ARR[0].size = number
        HEAD_ARR[1].addr = 1 
        HEAD_ARR[1].title = "file1"
        HEAD_ARR[1].size = number
        HEAD_ARR[2].addr = 2 
        HEAD_ARR[2].title = "file2"
        HEAD_ARR[2].size = number
        HEAD_ARR[3].addr = 3 
        HEAD_ARR[3].title = "file3"
        HEAD_ARR[3].size = number
        for i in range(number):
            MEM_ARR[4*i+0].writeMem(line[i], "String")
            MEM_ARR[4*i+1].writeMem(line[i], "String")
            MEM_ARR[4*i+2].writeMem(line[i], "String")
            MEM_ARR[4*i+3].writeMem(line[i], "String")
            if i != number-1:
                MEM_ARR[4*i+0].makeChain(4*i+0+4)
                MEM_ARR[4*i+1].makeChain(4*i+1+4)
                MEM_ARR[4*i+2].makeChain(4*i+2+4)
                MEM_ARR[4*i+3].makeChain(4*i+3+4)
        retval = 0

    elif cmd_words[0] == "move":
        if len(cmd_words) == 3:
            if isnumber(cmd_words[2]):
                gl_movefile(cmd_words[1], int(cmd_words[2]))
            else:
                print("  parameter 2: <new memory position> should be integer")
        else:
            print("  Usage: move <filename> <new memory position>")
        retval = 0

    elif cmd_words[0] == "alias":
        if len(cmd_words) == 1:
            for al in aly.getAliasTable():
                print(al)
        elif len(cmd_words) == 3:
            if cmd_words[1] == "del":
                aly.delAlias(cmd_words[2])
            else:
                gl_help("alias", True)
        elif len(cmd_words) == 4:
            if cmd_words[1] == "add":
                aly.addAlias(cmd_words[2], cmd_words[3])
            else:
                gl_help("alias", True)
        else:
            gl_help("alias", True)
        retval = 0

    elif cmd_words[0] == "printpart":
        if len(cmd_words) == 3:
            if isnumber(cmd_words[1]):
                if isnumber(cmd_words[2]):
                    data = ""
                    num = ""
                    for i in range(int(cmd_words[1]), int(cmd_words[2])):
                        cell = MEM_ARR[i]
                        if cell.dtype == "Null":
                            data += " .."
                        else:
                            data += "  %c" % cell.dmem
                        num += " %02d" % i
                    print(data)
                    print(num)
                else:
                    print("  End position should be integer")
            else:
                print("  Start position should be integer")
        else:
            print("  Usage: printpart <from> <where> - print part of memory")

    elif cmd_words[0] == "compress":
        for i in range(MEM_SIZE):
            if MEM_ARR[i].dtype=="Null":
                #find nearest file
                dist = MEM_SIZE
                flname = ""
                for f in HEAD_ARR:
                    if f.addr > i and f.addr-i < dist:
                        dist = f.addr - i
                        flname = f.title
                #print("Moving file %s at %d" % (flname, i))
                if flname != "":
                    gl_movefile(flname, i)

    elif cmd_words[0] == "backup":
	import FS.extFS as fs
        if len(cmd_words) > 1:
            if cmd_words[1] == "save":
                print("not ready yet")
            elif cmd_words[1] == "restore":
                #open file
                f_line = fs.prepare2()
                HEAD_ARR, MEM_ARR, MEM_SIZE = fs.descr(f_line)

    else:
        #check alias
        if aly.isAlias(cmd_words[0]):
            cmd_words[0] = aly.getAlias(cmd_words[0])
            retval = run_command(cmd_words)
        else:
            print("function \"%s\" not found" % cmd_words[0])

    return retval

###############################
for i in range(MEM_SIZE):
    MEM_ARR.append(cell())

print("Python memory demo")

run = True
while run:
    cmd = raw_input(">")
    command_w = cmd.split(' ')
    run_command(command_w)
