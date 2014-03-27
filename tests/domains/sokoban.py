#!/usr/bin/env python3

from collections import defaultdict
from strips import *

class Locatable(Object): pass
class Dude(Locatable): pass
class Block(Locatable): pass
class Space(Object): pass

class SokobanState(State):
    def __init__(self):
        self.at = dict()
        self.has_dude = defaultdict(bool)
        self.has_block = defaultdict(bool)

    @Action
    def move(self, dude: Dude, start: Space, end: Space):
        if not (start != end
                and adjacent(start, end)
                and self.at[dude] == start
                and self.has_dude[start]
                and not self.has_dude[end]
                and not self.has_block[end]
                and not self.has_block[start]):
            raise UnsatisfiedPreconditions()
        self.at[dude] = end
        self.has_dude[end] = True
        del self.has_dude[start]

    @Action
    def move_block(self, dude: Dude, block: Block, dude_start: Space, block_start: Space, block_end: Space):
        if not (dude_start != block_start
                and block_start != block_end
                and dude_start != block_end
                and self.has_dude[dude_start]
                and not self.has_dude[block_start]
                and not self.has_dude[block_end]
                and self.has_block[block_start]
                and not self.has_block[dude_start]
                and not self.has_block[block_end]
                and inline(dude_start, block_start, block_end)
                and self.at[dude] == dude_start
                and self.at[block] == block_start):
            raise UnsatisfiedPreconditions()
        self.at[dude] = block_start
        self.has_dude[block_start] = True
        self.at[block] = block_end
        self.has_block[block_end] = True
        del self.has_dude[dude_start]
        del self.has_block[block_start]
#
#    def has_dude(self, space):
#        return any(self.pos[o] == space for o in get_objects_of_type(Dude))
#
#    def has_block(self, space):
#        return any(self.pos[o] == space for o in get_objects_of_type(Block))

player = Dude('player')
a = Block('a')
p = list(Space('p%d' % i) for i in range(14))

# static relations:
is_left = defaultdict(bool, {p: True for p in [(p[1], p[2]), (p[4], p[5]), (p[5], p[6]), (p[6], p[7]), (p[8], p[9]), (p[9], p[10]), (p[10], p[11]), (p[12], p[13])]})
is_above = defaultdict(bool, {p: True for p in [(p[4], p[8]), (p[8], p[12]), (p[9], p[13]), (p[5], p[9]), (p[3], p[5]), (p[2], p[3]), (p[6], p[10]), (p[7], p[11])]})

def adjacent(s1, s2):
    return is_left[(s1, s2)] or is_left[(s2, s1)] or is_above[(s1, s2)] or is_above[(s2, s1)]

def inline(s1, s2, s3):
    return ((is_above[(s2, s1)] and is_above[(s3, s2)]) or
            (is_above[(s1, s2)] and is_above[(s2, s3)]) or
            (is_left[(s2, s1)] and is_left[(s3, s2)]) or
            (is_left[(s1, s2)] and is_left[(s2, s3)]))

s = SokobanState()
s.at[player] = p[5]
s.has_dude[p[5]] = True
s.at[a] = p[10]
s.has_block[p[10]] = True

goal = lambda s: s.at[a] == p[13] and s.has_block[p[13]]

