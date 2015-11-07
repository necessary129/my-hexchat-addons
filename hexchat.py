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
EAT_HEXCHAT = 2
EAT_ALL = 3
EAT_NONE = None
PRI_HIGHEST = 9
PRI_HIGH = 8
PRI_NORM = 7
PRI_LOW = 6
PRI_LOWEST = 5
import re
import traceback
import threading
import socket
import os
import os.path
locky = threading.RLock()
cmd_pattern = re.compile(r'eg: /(.+)', re.MULTILINE)

def parse(yo):
    eol = []
    tot = 0
    word = yo.split()
    for x in word:
        eol.append(yo.split(" ", tot)[-1])
        tot += 1
    return word, eol
def prnt(stri):
    q.put(pprnt(stri))
    
def pastebin(tb):
    with locky:
        try:
        
            sock = socket.socket()
            sock.connect(("termbin.com", 9999))
            if sys.version_info [0] == 3:
                sock.send(tb.encode("utf-8", "replace") + b"\n")
                url = sock.recv(1024).decode("utf-8")
            else:
                sock.send(tb+'\n')
                url = sock.recv(1024)
            sock.close()
        except socket.error:
            traceback.print_exc()
        else:
            return url
if __name__ == "__main__":
    import os
    import sys
    broken = 0
    print("HexChat addons test script.")
    print("There might be weird stuff. Don't worry. :)\n")
    for val in os.listdir("addons"):
        path = os.path.join('addons','__init__.py')
        open(path,'w').close()
        if val.startswith('__'):
            continue
        if val.endswith('.pyc'):
            continue
        if os.path.isdir(os.path.join('addons',val)):
            for x in os.listdir(os.path.join('addons',val)):
                if not x.endswith('.py'):
                    continue
                if x.startswith('__'):
                    continue
                x = x.replace('.py','')
                x = "{0}.{1}".format(val, x)
                print("Testing {0}".format(x))
                ppath = os.path.join('addons',val,'__init__.py')
                open(ppath, 'w').close()
                try:
                    __import__('addons.{0}'.format(x), globals=globals())
                    print("{0} is WORKING.".format(x))
                    os.remove(ppath)
                except Exception as err:
                    errurl = pastebin(traceback.format_exc())
                    print("{0} is FAILING. ({1}: {2})".format(x, err, errurl))
                    
                    broken = 1
        if not val.endswith('.py'):
            continue
        val = val.replace(".py", "")
        print("Testing {0}".format(val))
        try:
            __import__('addons.{0}'.format(val), globals=globals())
            print("{0} is WORKING.".format(val))
        except Exception as err:
            print("{0} is FAILING. ({1})".format(val, err))
            broken = 1
    os.remove(path)
    if broken == 1:
        print("\nThere are broken addons. :(")
        sys.exit(1)
    else:
        print("\nEverything is fine. :)")
        sys.exit(0)

def hook_command(name, function, help):
    yo = cmd_pattern.findall(help)
    for each in yo:
        word, eol = parse(each)
        function(word, eol, None)
    
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


rlines ={
    "nick": ':Slavetator!noteness@unaffiliated/nessessary129/bot/slavetator NICK :Slavetator___',
    "kick":':Slavetator!noteness@unaffiliated/nessessary129/bot/slavetator KICK noteness :You should know better',
    "priv": ':Slavetator!noteness@unaffiliated/nessessary129/bot/slavetator PRIVMSG #Slavetator-test :Hello'

}

datas = {
    
}
def hook_server(raw,func,priority):
    raw = raw.lower()
    raws = rlines.get(raw, None)
    word, eol = parse(raws)
    print('*** Server sends --> '+raws)
    data = datas.get(raw, None)
    bb = func(word, eol, data)
    if bb != EAT_ALL:
        print('*** Plugins recieves <-- '+raws)
    elif bb != EAT_HEXCHAT:
        print('*** We recieves <-- '+raws )
    elif bb == EAT_PLUGIN:
        print("*** Current Plugin stops processing")


def hook_print(name, func, priority):
    raws = rlines['priv']
    word, eol = parse(raws)
    func(word, eol, name)

def hook_timer(time, func, userdata=None):
    func(userdata)
def prnt(stri):
    print(stri)

def get_pluginpref(idk):
    pass
def set_pluginpref(_,__):
    pass
def hook_unload(_):
    pass


