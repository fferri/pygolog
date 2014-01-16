#!/usr/bin/env python

from ._Program import *
from strips import UnsatisfiedPreconditions

class Exec(Program):
    def __init__(self, ground_action):
        self.ground_action = ground_action

    def __str__(self):
        return '%s' % (self.ground_action)

    def replace(self, var, obj):
        new_args = []
        for arg in self.ground_action.args:
            if arg == var: new_args.append(obj)
            else: new_args.append(arg)
        return Exec(GroundAction(self.ground_action.action, *new_args))

    def trans(self, s):
        try: yield (Empty(), self.ground_action.execute(s), self.ground_action)
        except UnsatisfiedPreconditions: pass

    def final(self, s):
        return False
