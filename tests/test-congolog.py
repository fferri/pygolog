#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *
from golog_program import *
from domains.math import S as S1

cond = lambda s: s.n < 8
s = S(3)
p = PConc(
    Sequence(
        Star(Exec(S.double())),
        Test(cond)
    ),
    Sequence(
        Star(Exec(S.incr())),
        Test(cond)
    )
)

maxsol=10
for pn, sn, an in trans_star(p, s, []):
    if maxsol < 0: break
    else: maxsol -= 1
    print('solution: %s' % an)
    print('resulting state: %s' % sn)

