#!/usr/bin/env python

from ._Program import *

class Choose(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        if len(ps) > 0:
            self.p2 = Choose(p2, ps[0], *ps[1:])
        else:
            self.p2 = p2

    def __str__(self):
        return '%s | %s' % (self.p1, self.p2)

    def replace(self, var, obj):
        return Choose(self.p1.replace(var, obj), self.p2.replace(var, obj))

    def trans(self, s):
        yield from self.p1.trans(s)
        yield from self.p2.trans(s)

    def final(self, s):
        pass
