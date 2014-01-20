#!/usr/bin/env python3.3

from collections import defaultdict
from strips import *
from golog_condition import *
from golog_program import *

x = Variable('x')
y = Variable('y')

a = Object('a')
b = Object('b')
c = Object('c')

class TestState(State):
    def __init__(self):
        self.exists = defaultdict(bool)

    @Action
    def remove(self, obj):
        if not self.exists[obj]: raise UnsatisfiedPreconditions()
        del self.exists[obj]

s = TestState()
s.exists[a] = True
s.exists[b] = True
s.exists[c] = True

test_num = 1

def pr(descr, pn, sn, an=None):
    global test_num
    if descr == 'initial':
        print('\n************ TEST #%d ************' % test_num)
        test_num += 1
    print('%s state: %s' % (descr, sn))
    print('%s program: %s' % (descr, pn))
    if descr != 'initial':
        print('executed actions: %s' % an)

p = Exec(TestState.remove(a))
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)
assert sn == State(exists(b), exists(c))

p = While(Holds(exists(x)), Pick(x, Object, Exec(remove(x))))
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)
assert len(an) == 3
assert sn == State()

p = Sequence(Exec(remove(a)), Choose(Exec(remove(a)), Exec(remove(b))))
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)
assert sn == State(exists(c))

p = If(Holds(exists(a)), Exec(remove(a)), Empty())
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)
assert sn == State(exists(b), exists(c))

passed = False
p = Star(Choose(Exec(remove(a)), Exec(remove(b)), Exec(remove(c))))
pr('initial', p, s)
for pn, sn, an in trans_star(p, s, []):
    if len(an) == 3 and sn == State():
        passed = True
        break
pr('resulting', pn, sn, an)
assert passed

p = Test(Holds(exists(x)))
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, [])) # test passed if no StopIteration exception
pr('resulting', pn, sn, an)

p = Sequence(Exec(remove(a)), Exec(remove(b)), Exec(remove(c)), Test(Holds(exists(x))))
pr('initial', p, s)
assert not any(trans_star(p, s, [])) # should not have solution
print('no solutions (as expected).')

p = Sequence(Exec(remove(a)), Choose(Sequence(Test(Holds(exists(a))), Exec(remove(b))), Exec(remove(c))))
pr('initial', p, s)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)

p = Sequence(Choose(Exec(remove(a)), Exec(remove(b)), Exec(remove(c))), Test(Holds(exists(a))))
pr('initial', p, s)
for pn, sn, an in trans_star(p, s, []):
    print(pn, sn, an)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)

p = Sequence(Star(Pick(x, Object, Exec(remove(x)))), Test(Holds(exists(x))))
p = Star(Pick(x, Object, Exec(remove(x))))
p = Sequence(Star(Pick(x, Object, Exec(remove(x)))), Exec(remove(b)))
p = Sequence(Star(Pick(x, Object, Exec(remove(x)))), Test(Not(Holds(exists(x)))))
pr('initial', p, s)
for pn, sn, an in trans_star(p, s, []):
    print(pn, sn, an)
pn, sn, an = next(trans_star(p, s, []))
pr('resulting', pn, sn, an)
