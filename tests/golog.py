#!/usr/bin/env python3

from collections import defaultdict
from strips import *
from golog_program import *
from domains.bag import S as S
from domains.math import S as S1

def assert_pn(s, incl, excl):
    assert set(incl) <= s.exists
    assert not s.exists.intersection(set(excl))

def test01(s):
    p = Exec(S.remove(a))
    pn, sn, an = next(trans_star(p, s, []))
    assert an == [S.remove(a)]
    assert_pn(sn, [b, c], [a])

def test02(s):
    p = While(lambda s: s.exists, Pick(Object, lambda x: Exec(S.remove(x))))
    pn, sn, an = next(trans_star(p, s, []))
    assert len(an) == 3
    assert_pn(sn, [], [a, b, c])

def test03(s):
    p = Sequence(Exec(S.remove(a)), Choose(Exec(S.remove(a)), Exec(S.remove(b))))
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [c], [a, b])

def test04(s):
    p = If(lambda s: a in s.exists, Exec(S.remove(a)), Empty())
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [b, c], [a])

def test05(s):
    passed = False
    p = Star(Choose(Exec(S.remove(a)), Exec(S.remove(b)), Exec(S.remove(c))))
    for pn, sn, an in trans_star(p, s, []):
        if len(an) == 3 and not sn.exists:
            passed = True
            break
    assert passed

def test06(s):
    p = Test(lambda s: s.exists)
    pn, sn, an = next(trans_star(p, s, [])) # test passed if no StopIteration exception

def test07(s):
    p = Sequence(Exec(S.remove(a)), Exec(S.remove(b)), Exec(S.remove(c)), Test(lambda s: s.exists))
    assert not any(trans_star(p, s, [])) # should not have solution

def test08(s):
    p = Sequence(Exec(S.remove(a)), Choose(Sequence(Test(lambda s: a in s.exists), Exec(S.remove(b))), Exec(S.remove(c))))
    pn, sn, an = next(trans_star(p, s, []))
    assert_pn(sn, [b], [a, c])

def test09(s):
    p = Sequence(Choose(Exec(S.remove(a)), Exec(S.remove(b)), Exec(S.remove(c))), Test(lambda s: a in s.exists))
    for pn, sn, an in trans_star(p, s, []):
        assert a in sn.exists and (b not in sn.exists or c not in sn.exists)

def test10(s):
    p = Sequence(Star(Pick(Object, lambda x: Exec(S.remove(x)))), Test(lambda s: not s.exists))
    for pn, sn, an in trans_star(p, s, []):
        assert_pn(sn, [], [a, b, c])
    pn, sn, an = next(trans_star(p, s, []))

def test11(s):
    p = Star(Exec(S1.incr()))
    g = trans_star(p, s1, [])
    # first step will do nothing:
    pn, sn, an = next(g)
    last = sn.n
    # this has to increase in a sequence
    for k in range(10):
        pn, sn, an = next(g)
        assert last + 1 == sn.n
        last = sn.n

def test12(s):
    # like previous test, but forcing backtracking with test for even numbers:
    p = Sequence(Star(Exec(S1.incr())), Test(lambda s: s.n % 2 == 0))
    g = trans_star(p, s1, [])
    # first step will do nothing:
    pn, sn, an = next(g)
    last = sn.n
    # this has to increase in a sequence of step 2
    for k in range(10):
        pn, sn, an = next(g)
        assert last + 2 == sn.n
        last = sn.n

def test13(s):
    # use nondeterminism to find a solution:
    goal = lambda s: s.n == 123
    p = Sequence(Star(Choose(Exec(S1.incr()), Exec(S1.double()))), Test(goal))
    pn, sn, an = next(trans_star(p, s, []))
    assert goal(sn)

def run_test(n,s):
    testname = 'test%02d' % i
    print('running %s...' % testname)
    globals()[testname](s)

a = Object('a')
b = Object('b')
c = Object('c')
s = S(a, b, c)

s1 = S1(0)

for i in range(1,11): run_test(i,s)
for i in range(11,14): run_test(i,s1)

print('All tests passed successfully')
