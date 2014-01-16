#!/usr/bin/env python

auto_id = 1

class Variable(object):
    def __init__(self, name=None):
        global auto_id
        if name is None:
            name = '?_x%d' % auto_id
            auto_id += 1
        self.name = name

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self): return hash(self.name)
