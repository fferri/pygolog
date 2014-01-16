#!/usr/bin/env python

from copy import copy, deepcopy

from ._GroundAction import *
from ._GroundFluent import *
from ._Variable import *

def unify(a, b, sigma={}):
    if isinstance(a, GroundFluent) and isinstance(b, GroundFluent):
        return len(a.args) == len(b.args) and a.fluent.name == b.fluent.name \
                and all(unify(x, y, sigma) for x, y in zip(a.args, b.args))
    elif isinstance(a, GroundAction) and isinstance(b, GroundAction):
        return len(a.args) == len(b.args) and a.action.name == b.action.name \
                and all(unify(x, y, sigma) for x, y in zip(a.args, b.args))
    elif isinstance(a, Variable):
        if a in sigma and sigma[a] != b: return None
        sigma[a] = b
        return sigma
    elif isinstance(b, Variable):
        if b in sigma and sigma[b] != a: return None
        sigma[b] = a
        return sigma
    else:
        return a == b

class State(object):
    def __init__(self, *contents):
        self.contents = contents[0] if isinstance(contents[0], set) else set(contents)

    def query(self, q):
        for fact in self.contents:
            sigma = dict()
            if unify(fact, q, sigma):
                yield fact

    def holds(self, *qs):
        return all(any(self.query(q)) for q in qs)

    def add(self, *qs):
        return State(self.contents | set(qs))

    def remove(self, *qs):
        return State(self.contents - set(qs))

    def __str__(self):
        return str(self.contents)

    def __repr__(self):
        return self.__str__()
