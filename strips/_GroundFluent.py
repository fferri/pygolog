#!/usr/bin/env python

class GroundFluent(object):
    def __init__(self, fluent, *args):
        self.fluent = fluent
        self.args = args

    def __str__(self):
        return '%s(%s)' % (self.fluent.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.fluent.name == other.fluent.name and self.args == other.args

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.fluent.name) + sum(hash(arg) for arg in self.args)
