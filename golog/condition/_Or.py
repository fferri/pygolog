#!/usr/bin/env python

from ._Condition import *

class Or(Condition):
    def __init__(self, c1, c2, *cs):
        self.c1 = c1
        if len(cs) > 0:
            self.c2 = And(c2, cs[0], *cs[1:])
        else:
            self.c2 = c2

    def __str__(self):
        return '%s or %s' % (self.c1, self.c2)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return self.c1.holds(s) or self.c2.holds(s)
