#!/usr/bin/env python3.3

from strips import *
from golog_program import *
from domains.sokoban import *

def nearBlock(b):
    bx = Variable('bx')
    px = Variable('px')
    return Pick(px, Space, Pick(bx, Space, Test(And(Holds(has_dude(px)), Holds(at(player, px)), Or(Holds(is_left(px, bx)), Holds(is_left(bx, px)), Holds(is_above(px, bx)), Holds(is_above(bx, px))), Holds(has_block(bx)), Holds(at(b, bx))))))

def approachOneBlock():
    x = Variable('x')
    y = Variable('y')
    w = Variable('w')
    return Pick(w, Block, Sequence(Star(Pick(x, Space, Pick(y, Space, Exec(move(player, x, y))))), nearBlock(w)))

p = approachOneBlock()
print('initial state: %s' % s)
print('program: %s' % p)
for pn, sn, an in trans_star(p, s, []):
    print('solution: %s' % an)
    print('resulting state: %s' % sn)
