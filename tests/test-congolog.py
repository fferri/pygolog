#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *
from golog_program import *
from domains.math2 import S

cond = lambda s: s.n < 8
s = S(3)
p = PConc(Star(Exec(S.incr())), Star(Exec(S.double())))
#p = PConc(Star(Exec(S.double())), Star(Exec(S.incr())))
#p = Star(Choose(Exec(S.incr()), Exec(S.double())))
#p = Star(Choose(Exec(S.double()), Exec(S.incr())))

maxsol=10
for pn, sn, an in trans_star(p, s, []):
    if maxsol < 0: break
    else: maxsol -= 1
    print('solution: %s' % an)
    print('resulting state: %s' % sn)

