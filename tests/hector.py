#!/usr/bin/env python3

from strips import *
from golog_program import *

class HectorState(State):
    def __init__(self, a=0, b=0):
        self.a, self.b = a, b

    @Action
    def bump_a(self):
        self.a += 1

    @Action
    def bump_b(self):
        self.b += 1

bump_a = lambda: Exec(HectorState.bump_a())
bump_b = lambda: Exec(HectorState.bump_b())

def hector_test():
    return Sequence(
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()), Choose(bump_a(), bump_b()),
            Choose(bump_a(), bump_b()),
            Test(lambda s: s.a == 0)
        )

s = HectorState()
p = hector_test()
print('initial state: %s' % s)
print('program: %s' % p)
numSolutions = 0
for pn, sn, an in trans_star(p, s, []):
    print('solution: %s' % an)
    print('resulting state: %s' % sn)
numSolutions += 1
print('%d solutions found.' % numSolutions)

