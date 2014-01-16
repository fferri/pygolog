#!/usr/bin/env python

class GroundAction(object):
    def __init__(self, action, *args):
        self.action = action
        self.args = args

    def __str__(self):
        return '%s(%s)' % (self.action.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def execute(self, s):
        return self.action.execute(s, *self.args)
