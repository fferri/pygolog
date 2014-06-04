#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *
from golog_program import *
from domains.math1 import S

s = S(0)
p = Sequence(
        Choose(
                Exec(S.incr()),
                Exec(S.double())
        ),
        Choose(
                Exec(S.incr()),
                Exec(S.double())
        ),
        Test(lambda s: s.n == 1)
)

def debug(p, s, a=[], depth=0):
    print('  '*depth+'%s' % a)
    print('  '*depth+'s: %s' % s)
    print('  '*depth+'p: %s%s' % (p, ' (final)' if p.final(s) else ''))
    i = input('> [c=creep, other=skip] ')
    if i != 'c': return
    for pn, sn, an in p.trans(s):
        debug(pn, sn, an[len(a):], depth+1)

debug(p, s)
