#!/usr/bin/env python

from ._Program import *

class Pick(Program):
    def __init__(self, var, domain, prog):
        self.var = var
        self.domain = domain
        self.prog = prog

    def __str__(self):
        return 'pi %s from %s . %s' % (self.var, self.domain, self.prog)

    def replace(self, var, obj):
        if var == self.var: return self
        else: return Pick(self.var, self.domain, self.prog.replace(var, obj))

    def trans(self, s):
        for obj in objects[self.domain]:
            yield from self.prog.replace(self.var, obj).trans(s)

    def final(self, s):
        for obj in objects[self.domain]:
            if self.prog.replace(self.var, obj).final(s): return True
        return False
