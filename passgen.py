import sys
from random import random as rand

def rchar(rng, excl):
    good = list(set(rng) - set(excl))
    num =int(rand()*len(good))
    return chr(good[num])

def nums(lst):
    out = []
    for k in lst:
        out.append(ord(k))
    return out

#check if 'line' is peresent as argument
def haveArg(line):
    for cmd in range(len(sys.argv)):
        if sys.argv[cmd] == line:
            return cmd
    return False

def dhelp(line):
    if line!="":
        print line
    print "========="
    print "Usage: python "+sys.argv[0]+" [help] [len INT] [set OPTS] [unset OPTS] [no STRING] [chr STRING]\n"
    print "Params:"
    print " help - this message"
    print " len - length of a password"
    print " set - allowed sets of characters"
    print " unset - restricted characters"
    print " no - string of restricted characters"
    print " chr - string of allowed characters"
    print "     OPTS"
    print "     a - all"
    print "     s - small characters"
    print "     l - large characters"
    print "     n - numbers"
    print "     p - all special characters"
    print "     z - special characters on near numbers"
    print "note: \"set a\" and \"set slnp\" have the same effect"

def getSets(pline):
    out = []
    if 'a' in pline:
        out += ALL
    if 's' in pline:
        out += SM_CHAR
    if 'l' in pline:
        out += LG_CHAR
    if 'n' in pline:
        out += NUM
    if 'p' in pline:
        out += SPEC
    if 'z' in pline:
        out += SPEC2
    return out

lvl = 16
psw = ""
cut = []
add = []

ALL = range(33,127)         #all characters with specsymb
SM_CHAR = range(97,123)     #small characters
LG_CHAR = range(65, 91)     #large characters
NUM = range(48, 58)         #numbers
SPEC = range(33,48)+range(58,65)+range(91,97)+range(123,128)
SPEC2 = nums("`~!@#$%^&*()_+-=")

if haveArg("help") or \
    haveArg("-h") or \
    haveArg("-help") or \
    haveArg("/h") or \
    haveArg("--h") or \
    haveArg("--help") or \
    haveArg("/?") or \
    haveArg("-?"):
    dhelp("")
    exit()

ind = haveArg("len")
if ind:
    if ind+1 < len(sys.argv):
        lvl = int(sys.argv[ind+1])
        print "set word length: "+str(lvl)
    else:
        dhelp("ERROR: not enough arguments for 'len'\n")
        exit()
else:
    lvl = 16

set_ind = haveArg("set")
if set_ind:
    if set_ind+1 < len(sys.argv):
        par = sys.argv[set_ind+1]
        add = getSets(par)
    else:
        dhelp("ERROR: not enough arguments for 'set'\n")
        exit()

ind = haveArg("unset")
if ind:
    if ind+1 < len(sys.argv):
        par = sys.argv[ind+1]
        cut = getSets(par)
    else:
        dhelp("ERROR: not enough arguments for 'unset'\n")
        exit()

ind = haveArg("no")
if ind:
    if ind+1 < len(sys.argv):
        par = sys.argv[ind+1]
        cut += nums(par)
    else:
        dhelp("ERROR: not enough arguments for 'no'\n")
        exit()

ind = haveArg("chr")
if ind:
    if ind+1 < len(sys.argv):
        par = sys.argv[ind+1]
        add += nums(par)
    else:
        dhelp("ERROR: not enough arguments for 'chr'\n")
        exit()
elif not set_ind:
    add = ALL

for i in range(lvl):
    psw+=rchar(add, cut)
print psw