#!/usr/bin/env python

from strips import *

x = Object('x')
y = Object('y')
z = Object('z')

f = Fluent('f', Object)
g = Fluent('g', Object, Object)

s = State(f(x), f(y), g(z, z))

assert unify(x, Variable())
assert unify(x, x)
assert unify(f(x), f(Variable()))
assert unify(f(x), f(x))

assert len(f(x).args) == 1
assert f(x).args[0] == x

assert set(s.query(f(Variable()))) == set([f(x), f(y)])
assert set(s.query(f(z))) == set([])

assert s.holds(f(x))
assert s.holds(f(y))
assert not s.holds(f(z))
assert not s.holds(g(x, z))
assert not s.holds(g(y, z))
assert s.holds(g(z, z))

s = s.add(f(z))

assert s.holds(f(z))

s = s.remove(g(z, z))

assert not s.holds(g(z, z))

s = s.remove(f(x))

v = Variable('v')

assert set(s.query(f(v))) == set([f(y), f(z)])

assert unify(g(v, z), g(z, v))
assert not unify(g(v, z), g(y, v))

print('Tests passed successfully')
