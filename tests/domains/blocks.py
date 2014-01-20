#!/usr/bin/env python3.3

from collections import defaultdict
from copy import copy
from strips import *

class Block(Object):
    pass

class BlocksState(State):
    def __init__(self):
        self.on = defaultdict(bool)
        self.clear = defaultdict(bool)

    @Action
    def move(self, obj: Block, objfrom: Object, objto: Object):
        if objfrom == objto or obj == objto:
            raise UnsatisfiedPreconditions()
        if not self.on[obj] == objfrom or not self.clear[obj] or not (self.clear[objto] or objto == table):
            raise UnsatisfiedPreconditions()
        self.on[obj] = objto
        self.clear[objfrom] = True
        del self.clear[objto]

a = Block('a')
b = Block('b')
c = Block('c')
d = Block('d')
table = Object('table')

s = BlocksState()
s.clear[b] = True
s.on[b] = d
s.on[d] = a
s.on[a] = table
s.clear[c] = True
s.on[c] = table

goal = lambda s: s.clear[a] and s.on[a] == b and s.on[b] == c and s.on[c] == d and s.on[d] == table

