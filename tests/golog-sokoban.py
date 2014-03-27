#!/usr/bin/env python3

from strips import *
from golog_program import *
from domains.sokoban import *

move = lambda *args: Exec(SokobanState.move(*args))
move_block = lambda *args: Exec(SokobanState.move_block(*args))

def nearBlock(b):
    return Pick(Space, lambda px:
            Pick(Space, lambda bx:
                Test(lambda s: s.has_dude[px] and s.at[player] == px and adjacent(px, bx) and s.has_block[bx] and s.at[b] == bx)))

def approachOneBlock():
    return Pick(Block, lambda w:
            Sequence(Star(Pick(Space, lambda x: Pick(Space, lambda y: move(player, x, y)))),
                nearBlock(w)))

p = approachOneBlock()
print('initial state: %s' % s)
print('program: %s' % p)
numSolutions = 0
for pn, sn, an in trans_star(p, s, []):
    print('solution: %s' % an)
    print('resulting state: %s' % sn)
    numSolutions += 1
print('%d solutions found.' % numSolutions)

