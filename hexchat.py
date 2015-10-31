# -*- coding: utf8 -*-
#Copyright (c) 2015 noteness
#Copyright (c) 2015 Jesús "JeDa" Hernández
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

EAT_PLUGIN = 1
EAT_HEXCHAT = 1
EAT_ALL = 1
EAT_NONE = 1
PRI_HIGHEST = 1
PRI_HIGH = 1
PRI_NORM = 1
PRI_LOW = 1
PRI_LOWEST = 1
import re
cmd_pattern = re.compile(r'eg: /(.+)', re.MULTILINE)
if __name__ == "__main__":
    import os
    import sys
    broken = 0
    print("HexChat addons test script.")
    print("There might be weird stuff. Don't worry. :)\n")
    for val in os.listdir("addons"):
        if val.startswith('__'):
            continue
        if val.endswith('.pyc'):
            continue
        val = val.replace(".py", "")
        print("Testing {0}".format(val))
        try:
            __import__('addons.{0}'.format(val), globals=globals())
            print("{0} is WORKING.".format(val))
        except Exception as err:
            __import__('traceback').print_exc()
            print("{0} is FAILING. ({1})".format(val, err))
            broken = 1
    if broken == 1:
        print("\nThere are broken addons. :(")
        sys.exit(1)
    else:
        print("\nEverything is fine. :)")
        sys.exit(0)

def hook_command(name, function, help):
    yo = cmd_pattern.search(help).group(1).split()
    eol = []
    tot = 0
    for x in yo:
        eol.append(yo[tot])
        tot += 1
    function(yo, eol, None)
    
def command(command):
    split = command.replace("\x034", "").split(" ")
    if split[0] == "say":
        print("<testuser> {0}".format(command.replace(split[0] + " ", "")))
    elif split[0] == "me":
        print("* testuser {0}".format(command.replace(split[0] + " ", "")))
    elif split[0] == "msg" or split[0] == "privmsg":
        print(">{0}< {1}".format(split[1], command.replace(split[0] + " ", "").replace(split[1] + " ", "")))
    elif split[0] == "notice":
        print("->{0}<- {1}".format(split[1], command.replace(split[0] + " ", "").replace(split[1] + " ", "")))

testword = [':Slavetator!noteness@unaffiliated/nessessary129/bot/slavetator', 'NICK', ':Slavetator___']
testwordeol = [':Slavetator!noteness@unaffiliated/nessessary129/bot/slavetator NICK :Slavetator___', 'NICK :Slavetator___', ':Slavetator___']
testdata = None
def hook_server(raw,func,priority):
    if raw == 'NICK':
        func(testword,testwordeol,testdata)
def prnt(stri):
    print(stri)

def get_pluginpref(idk):
    pass
def set_pluginpref(_,__):
    pass
def hook_unload(_):
    pass


