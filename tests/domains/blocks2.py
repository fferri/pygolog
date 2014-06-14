#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *

class Block(Object):
    pass

class BlocksState(State):
    def __init__(self, on={}):
        self._on = on

    def on(self, a, b):
        return self._on[a] == b

    def clear(self, o):
        return o not in self._on.values()

    @Action
    def move(self, obj: Block, objfrom: Object, objto: Object):
        if objfrom == objto or obj == objto:
            raise UnsatisfiedPreconditions()
        if not self.on(obj, objfrom) or not self.clear(obj) or not (self.clear(objto) or objto == table):
            raise UnsatisfiedPreconditions()
        self._on[obj] = objto

a = Block('a')
b = Block('b')
c = Block('c')
d = Block('d')
table = Object('table')

s = BlocksState(on = {b: d, d: a, a: table, c: table})

goal = lambda s: s.clear(a) and s.on(a, b) and s.on(b, c) and s.on(c, d) and s.on(d, table)

