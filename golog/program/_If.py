#!/usr/bin/env python

from ._Program import *

class If(Program):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __str__(self):
        return 'if %s then %s else %s endIf' % (self.condition, self.then_branch, self.else_branch)

    def replace(self, var, obj):
        return If(self.condition.replace(var, obj), self.then_branch.replace(var, obj), self.else_branch.replace(var, obj))

    def trans(self, s):
        if self.condition.holds(s):
            yield from self.then_branch.trans(s)
        else:
            yield from self.else_branch.trans(s)

    def final(self, s):
        if self.condition.holds(s):
            return self.then_branch.final(s)
        else:
            return self.else_branch.final(s)
