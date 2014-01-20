#!/usr/bin/env python3.3

from collections import defaultdict
from strips import *
from golog_program import *

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

remove = TestState.remove # alias

def assert_pn(s, incl, excl):
    for x in incl: assert s.exists[x]
    for x in excl: assert not s.exists[x]

def test01(s):
    p = Exec(remove(a))
    pn, sn, an = next(trans_star(p, s, []))
    assert an == [TestState.remove(a)]
    assert_pn(sn, [b, c], [a])

def test02(s):
    p = While(lambda s: s.exists, Pick(Object, lambda x: Exec(TestState.remove(x))))
    pn, sn, an = next(trans_star(p, s, []))
    assert len(an) == 3
    assert_pn(sn, [], [a, b, c])

def test03(s):
    p = Sequence(Exec(remove(a)), Choose(Exec(remove(a)), Exec(remove(b))))
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [c], [a, b])

def test04(s):
    p = If(lambda s: s.exists[a], Exec(remove(a)), Empty())
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [b, c], [a])

def test05(s):
    passed = False
    p = Star(Choose(Exec(remove(a)), Exec(remove(b)), Exec(remove(c))))
    for pn, sn, an in trans_star(p, s, []):
        if len(an) == 3 and not sn.exists:
            passed = True
            break
    assert passed

def test06(s):
    p = Test(lambda s: s.exists)
    pn, sn, an = next(trans_star(p, s, [])) # test passed if no StopIteration exception

def test07(s):
    p = Sequence(Exec(remove(a)), Exec(remove(b)), Exec(remove(c)), Test(lambda s: s.exists))
    assert not any(trans_star(p, s, [])) # should not have solution

def test08(s):
    p = Sequence(Exec(remove(a)), Choose(Sequence(Test(lambda s: s.exists[a]), Exec(remove(b))), Exec(remove(c))))
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [b], [a, c])

def test09(s):
    p = Sequence(Choose(Exec(remove(a)), Exec(remove(b)), Exec(remove(c))), Test(lambda s: s.exists[a]))
    for pn, sn, an in trans_star(p, s, []):
        assert sn.exists[a] and (not sn.exists[b] or not sn.exists[c])

def test10(s):
    p = Sequence(Star(Pick(Object, lambda x: Exec(remove(x)))), Test(lambda s: not s.exists))
    for pn, sn, an in trans_star(p, s, []):
        assert_pn(sn, [], [a, b, c])
    pn, sn, an = next(trans_star(p, s, []))

s = TestState()
s.exists[a] = True
s.exists[b] = True
s.exists[c] = True

for i in range(1,11): globals()['test%02d' % i](s)
print('All tests passed successfully')
