#!/usr/bin/env python

import inspect, itertools
from copy import copy, deepcopy

_actions = {}
_objects = {}

# action decorator
class Action():
    def __init__(self, method):
        global _actions
        self.action = True
        self.name = method.__name__
        self.method = method
        arg_spec = inspect.getfullargspec(method)
        self.types = [arg_spec.annotations[arg] if arg in arg_spec.annotations else Object for arg in arg_spec.args[1:]]

        _actions[self.name] = self

    def apply(self, state, *args):
        cloned_state = state.copy()
        self.method(cloned_state, *args)
        return cloned_state

    def ground(self, *args):
        return GroundAction(self, *args)

    def __call__(self, *args):
        return self.ground(*args)

def pick_action(s):
    global objects
    for action_name, action in _actions.items():
        for args in itertools.product(*[get_objects_of_type(t) for t in action.types]):
            try:
                yield (action.ground(*args), action.apply(s, *args))
            except UnsatisfiedPreconditions:
                pass

def action_sequence(s, length):
    if length == 0:
        yield ([], s)
        return
    for action, s1 in pick_action(s):
        for p, s2 in action_sequence(s1, length - 1):
            yield ([action] + p, s2)

def plan_bfs(s, goal, maxlength):
    for length in range(maxlength + 1):
        for plan, s1 in action_sequence(s, length):
            if goal(s1):
                yield plan

def get_types():
    return list(_objects.keys())

def get_objects_of_type(t):
    if t in _objects: return _objects[t]
    else: return []

class GroundAction(object):
    def __init__(self, action, *args):
        self.action = action
        self.args = args
        for i, (a, t) in enumerate(zip(args, action.types)):
            if not isinstance(a, t):
                raise TypeError('%s: arg %d, got %s, expected %s' % (self, i, type(a).__name__, t.__name__))

    def __str__(self):
        return '%s(%s)' % (self.action.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.action == other.action and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def apply(self, s):
        return self.action.apply(s, *self.args)

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

class State(object):
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<State %s>' % self.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        cloned_state = copy(self)
        for k, v in self.__dict__.items():
            setattr(cloned_state, k, copy(v))
        return cloned_state

    def actions(self):
        for k in dir(self):
            if getattr(getattr(self, k), 'action', False): yield k

class UnsatisfiedPreconditions(Exception):
    pass

class Variable(object):
    auto_id = 1

    def __init__(self, name=None):
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
