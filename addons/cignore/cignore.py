# Copyright (c) 2015 noteness
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
import hexchat
import sys
import fnmatch
__module_name__ = 'CIgnore'
__module_version__ = '0.1.0'
__module_description__ = 'Strips color codes from a specific nick'
__module_author__ = 'noteness'
ignores = []
hook = None

def saveconf():
    global ignores
    hexchat.set_pluginpref(__module_name__+'_ignores', ",".join(ignores))

def loadconf():
    global ignores
    ign = hexchat.get_pluginpref(__module_name__+'_ignores')
    if ign:
        ignores = ign.split(',')
    else:
        ignores = []

def setignorer(word, word_eol, userdata):
    global ignores
    if len(word) !=  2:
        hexchat.command('HELP '+ word[0])
        return 
    ignores.append(word[1])
    hexchat.prnt('user {0} successfully added to ignore list'.format(word[1]))
    saveconf()

def unset(word, word_eol, userdata):
    global ignores
    if len(word)  != 2 :
        hexchat.command('HELP '+ word[0])
        return
    num =int(word[1])
    if  not len(ignores) >= num:
        hexchat.prnt('Are you sure that a such index is there?')
        return hexchat.EAT_NONE
    temp = ignores[num]
    del ignores[num]
    hexchat.prnt('user {0} successfully removed from ignore list'.format(temp))
    saveconf()


def listi(word, word_eol, userdata):
    global ignores
    allo = []
    for x in ignores:
        num = str(ignores.index(x)) + ": " + x
        allo.append(num)
    alli = ", ".join(allo)
    toprnt = "Ignored users are: "+alli if ignores else "No hosts are ignored"
    hexchat.prnt(toprnt)
def on_privmsg(word, word_eol, userdata):
    global ignores
    host =word[0]
    for x in ignores:
        if fnmatch.fnmatch(host, x):
            pass
