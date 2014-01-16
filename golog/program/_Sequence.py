#!/usr/bin/env python

from ._Program import *

class Sequence(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        if len(ps) > 0:
            self.p2 = Sequence(p2, ps[0], *ps[1:])
        else:
            self.p2 = p2

    def __str__(self):
        return '%s; %s' % (self.p1, self.p2)

    def replace(self, var, obj):
        return Sequence(self.p1.replace(var, obj), self.p2.replace(var, obj))

    def trans(self, s):
        if self.p1.final(s):
            yield from self.p2.trans(s)
        else:
            for p1t, st, at in self.p1.trans(s):
                yield (Sequence(p1t, self.p2), st, at)

    def final(self, s):
        return self.p1.final(s) and self.p2.final(s)
