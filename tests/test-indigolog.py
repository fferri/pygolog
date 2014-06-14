#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *
from golog_program import *

class S(State):
    def __init__(self, n=1):
        self.n = n

    @Action
    def incr(self):
        self.n += 1

    @Action
    def double(self):
        self.n *= 2

goal = lambda s: s.n == 4
s = S(3)
p = Sequence(
        Choose(Exec(S.double()), Exec(S.incr())),
        Test(goal))

#for pn, sn, an in trans_star(p, s, []):
#    print('solution: %s' % an)
#    print('resulting state: %s' % sn)

def print_exec(a):
    print('executing %s' % a)

print('following one should fail:')
if indigolog(p, s, [], exec_cb=print_exec): print('Succeeded')
else: print('Failed')
print('following one should pass:')
if indigolog(Search(p), s, [], exec_cb=print_exec): print('Succeeded')
else: print('Failed')

