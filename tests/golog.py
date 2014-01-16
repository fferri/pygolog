#!/usr/bin/env python3.3

from strips import *
from golog_condition import *
from golog_program import *

x = Variable('x')
y = Variable('y')

exists = Fluent('exists', Object)

a = Object('a')
b = Object('b')
c = Object('c')

s = State(exists(a), exists(b), exists(c))

class Remove(Action):
    def execute(self, s, obj: Object):
        if not s.holds(exists(obj)): raise UnsatisfiedPreconditions()
        return s.remove(exists(obj))

remove = Remove()

p = If(Holds(exists(x)), Pick(x, Object, Exec(remove(x))))

for p1, s1, a1 in trans_star(p, s, []):
    print('p\' = %s' % p1)
    print('s\' = %s' % s1)
    print('a\' = %s' % a1)
