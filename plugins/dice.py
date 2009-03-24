#!/usr/bin/env python
"""
dice.py written by Scaevolus 2008, updated 2009
simulates dicerolls
"""
import re
import random

import hook

whitespace_re = re.compile(r'\s+')
valid_diceroll_re = re.compile(r'^[+-]?(\d+|\d*d\d+)([+-](\d+|\d*d\d+))*$')
sign_re = re.compile(r'[+-]?(?:\d*d)?\d+')
split_re = re.compile(r'([\d+-]*)d?(\d*)')

def nrolls(count, n):
    "roll an n-sided die count times"
    if n < 2: #it's a coin
        if count < 5000:
            return sum(random.randint(0,1) for x in xrange(count))
        else: #fake it
            return int(random.normalvariate(.5*count,(.75*count)**.5))
    else:
        if count < 5000:
            return sum(random.randint(1,n) for x in xrange(count))
        else: #fake it
            return int(random.normalvariate(.5*(1+n)*count,
                (((n+1)*(2*n+1)/6.-(.5*(1+n))**2)*count)**.5))

@hook.command
def dice(input):
    ".dice <diceroll> - simulates dicerolls, e.g. .dice 2d20-d5+4 roll 2 " \
        "D20s, subtract 1D5, add 4"
    if not input.strip():
        return dice.__doc__

    spec = whitespace_re.sub('', input)
    if not valid_diceroll_re.match(spec):
        return "Invalid diceroll"
    sum = 0
    groups = sign_re.findall(spec)
    for roll in groups:
        count, side = split_re.match(roll).groups()
        if side == "":
            sum += int(count)
        else:
            count = int(count) if count not in  " +-" else 1
            side = int(side)
            try:
                if count > 0:
                    sum += nrolls(count, side)
                else:
                    sum -= nrolls(abs(count), side)
            except OverflowError:
                return "Thanks for overflowing a float, jerk >:["
    
    return str(sum)