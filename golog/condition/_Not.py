#!/usr/bin/env python

from ._Condition import *

class Not(Condition):
    def __init__(self, c1):
        self.c1 = c1

    def __str__(self):
        return 'not %s' % (self.c1)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return not self.c1.holds(s)
