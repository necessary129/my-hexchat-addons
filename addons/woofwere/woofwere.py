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
__module_version__ = '0.0.6'
__module_description__ = 'Werewolf game helper.'
__module_author__ = 'noteness'

safes = []
commands = {}


######################### Formatter - Made by skizzerz ################################
import re
import string

""" Custom formatter mimicing str.format() with additional capabilities.

A format string can now additionally take the form:
    {literal|:format_spec}
This form will treat the text "literal" as the text to be formatted
instead of attempting to get the value from the passed-in arguments.

Furthermore, the built-in format_spec mini language has been expanded.
The following may now appear as the "type":
    plural[(int)] - converts the value to plural form
    num(int) - converts the value to plural form and prefixes with int
    list[(sep=", ")] - converts value to list separated by sep
    is - returns "is" if value is 1 or "are" otherwise (value must be an int)
    was - returns "was" if value is 1 or "were" otherwise
    an - prefixes value with "a" or "an"

If the # specifier is used with num or an, it will cause the prefix
to be bolded. If it is used with list, it will omit the "and" prior to
the last list item and will not special-case the two-item form.
"""

# Note: {0:is} is simply shorthand for {is|:plural({0})}, same with {0:was}

# https://docs.python.org/3/library/string.html#format-specification-mini-language
# (enhanced with the above additional types)
FORMAT = re.compile(
    r"^(?:(?P<fill>.?)(?P<align>[<>^=]))?(?P<sign>[+\- ]?)(?P<alt>#?)(?P<zero>0?)"
    r"(?P<width>[1-9]+|0+|0[oO][1-7]+|0[xX][0-9a-fA-F]+|0[bB][01]+)?(?P<comma>,?)"
    r"(?P<precision>\.(?:[1-9]+|0+|0[oO][1-7]+|0[xX][0-9a-fA-F]+|0[bB][01]+))?"
    r"(?P<type>[bcdeEfFgGnosxX%]|plural|num|list|is|was|an)(?:\((?P<arg>.*)\))?$"
    )

class CustomFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        if not isinstance(key, int) and key[-1] == "|":
            return key[:-1]
        return super(CustomFormatter, self).get_value(key, args, kwargs)

    def format_field(self, value, format_spec):
        if format_spec:
            m = FORMAT.match(format_spec)
            if m:
                fill = m.group("fill") or ""
                align = m.group("align") or ""
                sign = m.group("sign") or ""
                alt = m.group("alt") == "#" # we don't pass alt through
                zero = m.group("zero") or ""
                width = m.group("width") or ""
                comma = m.group("comma") or ""
                precision = m.group("precision") or ""
                ty = m.group("type")
                arg = m.group("arg") # may be None
                if ty in ("plural", "num", "list", "is", "was", "an"):
                    format_spec = fill + align + sign + zero + width + comma + precision + "s"
                if ty == "plural":
                    arg = int(arg, 0) if arg else 2
                    value = self.plural(value, arg)
                elif ty == "num":
                    if arg is None:
                        raise ValueError("num() format requires an argument")
                    arg = int(arg, 0)
                    prefix = str(arg) if arg > 0 else "no"
                    if alt:
                        prefix = "\u0002" + prefix + "\u0002"
                    value = prefix + " " + self.plural(value, arg)
                elif ty == "an":
                    prefix = "an" if value[0] in ("a", "e", "i", "o", "u") else "a"
                    if alt:
                        prefix = "\u0002" + prefix + "\u0002"
                    value = prefix + " " + value
                elif ty == "is":
                    if not isinstance(value, int):
                        value = int(value, 0)
                    value = "is" if value == 1 else "are"
                elif ty == "was":
                    if not isinstance(value, int):
                        value = int(value, 0)
                    value = "was" if value == 1 else "were"
                elif ty == "list":
                    sep = arg or ", "
                    lv = len(value)
                    if alt:
                        value = sep.join(value)
                    elif lv == 0:
                        value = ""
                    elif lv == 1:
                        value = value[0]
                    elif lv == 2:
                        value = value[0] + " and " + value[1]
                    else:
                        value = sep.join(value[:-1]) + sep + "and " + value[-1]

        return super(CustomFormatter, self).format_field(value, format_spec)

    def plural(self, value, count=2):
        if count == 1:
            return value
        bits = value.split()
        if bits[-1][-2:] == "'s":
            bits[-1] = self.plural(bits[-1][:-2], count)
            bits[-1] += "'" if bits[-1][-1] == "s" else "'s"
        else:
            bits[-1] = {"person": "people",
                        "wolf": "wolves",
                        "has": "have",
                        "is": "are",
                        "was": "were",
                        "succubus": "succubi"}.get(bits[-1], bits[-1] + "s")
        return " ".join(bits)

################################ End Formatter ######################################
cf = CustomFormatter()


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
    if not safes:
        print("There are no current safes.")
        return
    print(cf.vformat("Saved {safe|:plural({0})} {0:is}: {1:list}", (len(safes), safes), {}))

@command("safe add", args=1)
def sadd(*nsafe):
    aye = []
    nye = []
    global safes
    for safe in nsafe:
        if safe in safes:
            nye.append(safe)
            continue
        safes.append(safe)
        aye.append(safe)
    if nye:
        print(cf.vformat("{0:list} {1:is} already in safes.", (nye, len(nye)), {}))
    save_safe()
    if aye:
        print(cf.vformat("{0:list} {1:is} added to safes.", (aye, len(aye)), {}))


@command("safe del", args=1)
def sadd(*nsafe):
    global safes
    aye = []
    nye = []
    for safe in nsafe:
        if safe not in safes:
            nye.append(safe)
            continue
        safes.remove(safe)
        aye.append(safe)
    if nye:
        print(cf.vformat("{0:list} {1:is} not in safes.", (nye, len(nye)), {}))
    save_safe()
    if aye:
        print(cf.vformat("{0:list} {1:is} removed from safes.", (aye, len(aye)), {}))

hexchat.hook_command("", notice_override)
hexchat.hook_command("WW", ww, help="AA")
load_safe()
