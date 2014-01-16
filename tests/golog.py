#!/usr/bin/env python3.3

from strips import *
from golog import *
from domains.blocks import *

p0 = Sequence(
    If(And(Holds(clear(b)), Holds(clear(c))),
        Exec(move(c,table,b)),
        Exec(move(c,table,a))
    ),
    Exec(move(c,b,table))
)

x = Variable('x')

p = Sequence(
        Choose(
            Exec(move(b, d, table)),
            Exec(move(b, d, c))
            ),
        Choose(
            Exec(move(d, a, table)),
            Exec(move(d, a, b)),
            Exec(move(d, a, c))
            ),
        Pick(x, Block, Exec(move(b, x, table)))
        )

p3 = Sequence(
        Exec(move(b,d,table)),
        Pick(x, Object, Exec(move(d, a, x)))
        )

def trans_star(p, s, a):
    if p.final(s):
        yield (p, s, a)
    if isinstance(p, Empty):
        return
    for p1, s1, a1 in p.trans(s):
        yield from trans_star(p1, s1, a + [a1])

for p1, s1, a1 in trans_star(p, s, []):
    print('p\' = %s' % p1)
    print('s\' = %s' % s1)
    print('a\' = %s' % a1)
