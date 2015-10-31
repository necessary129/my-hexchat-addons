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
__module_name__ = 'Nick Ignore'
__module_version__ = '0.0.1'
__module_description__ = 'Ignores nick changes.'
__module_author__ = 'noteness'
ignores = []

def setignorer(word, word_eol, userdata):
    global ignores
    if len(word) < 2:
        hexchat.prnt("Need a host maaan")
    ignores.append(word[1])
    hexchat.prnt('host {0} successfully added to ignore list'.format(word[1]))
    return hexchat.EAT_NONE
def on_nick(word, word_eol, userdata):
    host =word[0].split('@')[1]
    if host in ignores:
        return hexchat.EAT_ALL
    return hexchat.EAT_NONE

def unset(word, word_eol, userdata):
    global ignores
    if len(word) < 2:
        hexchat.prnt("Need a host maaan")
    if word[1] not in ignores:
        hexchat.prnt('I am not ignoring that host')
        return hexchat.EAT_NONE
    ignores.remove(word[1])
    hexchat.prnt('host {0} successfully removed from ignore list'.format(word[1]))
    return hexchat.EAT_NONE
hexchat.hook_server('NICK',on_nick,priority=hexchat.PRI_HIGHEST)
hexchat.hook_command('NIGNORE',setignorer,help="/nignore <host>")
hexchat.hook_command('UNNIGNORE',unset,help="/unnignore <host>")