#!/usr/bin/env python3.3

from strips import *

class Block(Object):
    pass

a = Block('a')
b = Block('b')
c = Block('c')
d = Block('d')
table = Object('table')

on = Fluent('on', Block, Object)
clear = Fluent('clear', Object)

s = State(
    clear(b),
    on(b, d),
    on(d, a),
    on(a, table),
    clear(c),
    on(c, table)
)

class Move(Action):
    def execute(self, s, obj: Block, objfrom: Object, objto: Object):
        if objfrom == objto or obj == objto:
            raise UnsatisfiedPreconditions()
        if not s.holds(on(obj, objfrom), clear(obj)):
            raise UnsatisfiedPreconditions()
        if not s.holds(clear(objto)) and objto != table:
            raise UnsatisfiedPreconditions()
        return s.add(on(obj, objto), clear(objfrom)).remove(on(obj, objfrom), clear(objto))

move = Move()

goal = lambda s: s.holds(clear(a), on(a, b), on(b, c), on(c, d), on(d, table))

