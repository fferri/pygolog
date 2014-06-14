#!/usr/bin/env python3

from strips import *

class Block(Object):
    pass

class BlocksState(State):
    def __init__(self, on=dict(), clear=set()):
        self.on = on
        self.clear = clear

    @Action
    def move(self, obj: Block, objfrom: Object, objto: Object):
        if objfrom == objto or obj == objto:
            raise UnsatisfiedPreconditions()
        if not self.on[obj] == objfrom or obj not in self.clear or not (objto in self.clear or objto == table):
            raise UnsatisfiedPreconditions()
        self.on[obj] = objto
        self.clear.add(objfrom)
        self.clear.discard(objto)

a = Block('a')
b = Block('b')
c = Block('c')
d = Block('d')
table = Object('table')

s = BlocksState(on = {b: d, d: a, a: table, c: table}, clear = {b, c})

goal = lambda s: a in s.clear and s.on[a] == b and s.on[b] == c and s.on[c] == d and s.on[d] == table

