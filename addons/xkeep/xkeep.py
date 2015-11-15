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
from datetime import timedelta
import time
__module_name__ = 'xkeep'
__module_version__ = '0.1-dev'
__module_description__ = 'Keeps your account in xshellz.'
__module_author__ = 'noteness'

week = 604800
now = time.time()
lastkeep = 1


#YOU SHOULD SET THIS
username ="your xshellz username"

hook = None

def getlstkeep():
    global lastkeep
    kp = hexchat.get_pluginpref('xkeep__lastkeep')
    if kp:
        lastkeep = float(kp)

def savk():
    global lastkeep
    hexchat.set_pluginpref('xkeep__lastkeep', str(lastkeep))

def update():
    global lastkeep
    lastkeep = time.time()
    savk()

getlstkeep()
diff = timedelta(seconds=now) - timedelta(seconds=lastkeep)
diff = (diff.days *60*60) + (diff.seconds)

def time_cb(_):
    global week
    global hook
    channel = hexchat.find_context(channel='#xshellz')
    channel.command('say !keep {0}'.format(username))
    update()
    if hook:
        hexchat.unhook(hook)
    hook = hexchat.hook_timer((week*1000),time_cb)

def unload_cb(_):
    hexchat.prnt("{0} module v{1} unloaded".format(__module_name__, __module_version__))

if diff >= week:
    time_cb(None)
else:
    dif = week - diff
    hook = hexchat.hook_timer((dif*1000),time_cb)
hexchat.prnt("{0} module v{1} loaded".format(__module_name__, __module_version__))
hexchat.hook_unload(unload_cb)