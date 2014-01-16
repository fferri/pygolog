#!/usr/bin/env python3.3

from strips import *

at = Fluent('at', int)
light = Fluent('light', int)

s = State(
    at(3),
    light(2),
    light(5)
)

def curfloor(s): return next(s.query(at(Variable()))).args[0]

class Up(Action):
    def execute(self, s):
        fl = curfloor(s)
        if fl >= 6: raise UnsatisfiedPreconditions()
        return s.add(at(fl+1)).remove(at(fl))

class Down(Action):
    def execute(self, s):
        fl = curfloor(s)
        if fl <= 1: raise UnsatisfiedPreconditions()
        return s.add(at(fl-1)).remove(at(fl))

class TurnOff(Action):
    def execute(self, s):
        fl = curfloor(s)
        if not s.holds(light(fl)): raise UnsatisfiedPreconditions()
        return s.remove(light(fl))

up = Up()
down = Down()
turnoff = TurnOff()

x = Variable('x')

goal = lambda s: s.holds(at(x)) and not s.holds(light(x))

