#!/usr/bin/env python

_objects = {}

def get_types():
    return list(_objects.keys())

def get_objects_of_type(t):
    if t in _objects: return _objects[t]
    else: return []

class Object(object):
    def __init__(self, name):
        global _objects
        t = type(self)
        while t is not object:
            if t not in _objects:
                _objects[t] = []
            _objects[t].append(self)
            t = t.__base__
        self.name = name

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self): return hash(self.name)
