# Copyright (c) 2015 Shamil K Muhammed
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

import ast

__module_name__ = 'WereHelper'
__module_version__ = '0.0.3'
__module_description__ = 'Werewolf game helper.'
__module_author__ = 'noteness'

safes = []
commands = {}

class NotEnoughArgError(TypeError):
    def __init__(self, rargs, gargs):
        self.rargs = rargs
        self.gargs = gargs

    def __str__(self):
        return "Required number of args is {}, you gave {}".format(self.rargs, self.gargs)

class CaseInStr(str):
    def __eq__(self, o):
        if not isinstance(o, str):
            raise NotImplementedError
        return self.lower() == o.lower()
    def __ne__(self, o):
        return not (self == o)
    def __hash__(self):
        return str.__hash__(self.lower())

def convl(l):
    for idx, item in enumerate(l):
        if isinstance(item, str):
            l[idx] = CaseInStr(item)


class command:
    def __init__(self, name, args=0):
        global commands
        self.name = CaseInStr(name).split()
        self.args = args
        self.func = None
        commands[tuple(CaseInStr(name).split())] = self
    def call(self, *args):
        args = list(args)
        args = args[len(self.name):]
        if len(args) < self.args:
            raise NotEnoughArgError(self.args, len(args))
        return self.func(*args)
    def __call__(self, func):
        self.func = func
        return func

def notice_override(word, word_eol, userdata):
    channel = hexchat.get_info('channel')
    if channel in safes:
        hexchat.command("NOTICE {} {}".format(channel, word_eol[0]))
        return hexchat.EAT_ALL

def load_safe():
    global safes
    srepr = hexchat.get_pluginpref('WereHelper_safes')
    if srepr:
        safes = ast.literal_eval(srepr)

def save_safe():
    global safes
    hexchat.set_pluginpref('WereHelper_safes', repr(safes))

def ww(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.command("HELP WW")
    word.pop(0)
    convl(word)
    for c, cc in commands.items():
        if len(word) < len(c):
            continue
        cm = word[:len(c)]
        if cm == list(c):
            cmd = cc
            break
    else:
        hexchat.command("HELP WW")
        return hexchat.EAT_ALL
    try:
        cmd.call(*word)
    except AttributeError as e:
        s = str(e)
        print("{}: {}".format(command, s))
        hexchat.command("HELP WW")
    return hexchat.EAT_ALL

@command("safe list")
def l():
    if not len(safes):
        print("There are no current safes.")
        return
    print("Saved safe{3}: {0}{1}{2}".format(', '.join(safes[:-1] if len(safes) > 1 else safes), 
        " and " if len(safes) > 1 else "", safes[-1] if len(safes) > 1 else "",
        " is" if len(safes) == 1 else "s are"))

@command("safe add", args=1)
def sadd(safe):
    global safes
    if safe in safes:
        print("'{}' is already in safes.".format(safe))
        return
    safes.append(safe)
    save_safe()
    print("'{}' added to safes.".format(safe))

@command("safe del", args=1)
def sadd(safe):
    global safes
    if safe not in safes:
        print("'{}' isn't in safes.".format(safe))
        return
    safes.remove(safe)
    save_safe()
    print("'{}' removed from safes.".format(safe))

hexchat.hook_command("", notice_override)
hexchat.hook_command("WW", ww, help="AA")
load_safe()