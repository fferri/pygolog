#!/usr/bin/env python

from ._Condition import *

class Holds(Condition):
    def __init__(self, ground_fluent):
        self.ground_fluent = ground_fluent

    def __str__(self):
        return '%s' % (self.ground_fluent)

    def replace(self, var, obj):
        new_args = []
        for arg in self.ground_fluent.args:
            if arg == var: new_args.append(obj)
            else: new_args.append(arg)
        return Holds(GroundFluent(self.ground_fluent.fluent, *new_args))

    def holds(self, s):
        return holds(s, self.ground_fluent)
