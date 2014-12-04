#!/usr/bin/env python3

import inspect, itertools
from collections import defaultdict
from copy import copy, deepcopy

# action decorator
class Action():
    _actions = dict()

    def __init__(self, method):
        self.action = True
        self.name = method.__name__
        self.method = method
        arg_spec = inspect.getfullargspec(method)
        self.types = [arg_spec.annotations.get(arg, Object) for arg in arg_spec.args[1:]]
        Action._actions[self.name] = self

    def apply(self, state, *args):
        cloned_state = state.copy()
        self.method(cloned_state, *args)
        return cloned_state

    def ground(self, *args):
        return GroundAction(self, *args)

    def __call__(self, *args):
        return self.ground(*args)

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
    _objects = defaultdict(list)

    @staticmethod
    def get_types():
        return list(Object._objects.keys())

    @staticmethod
    def get_objects_of_type(t):
        return Object._objects.get(t, [])

    def __init__(self, name):
        t = type(self)
        while t is not object:
            Object._objects[t].append(self)
            t = t.__base__
        self.name = name

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self): return hash(type(self)) + hash(self.name)

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

    def pick_action(self):
        for action_name, action in Action._actions.items():
            for args in itertools.product(*[Object.get_objects_of_type(t) for t in action.types]):
                try: yield (action.ground(*args), action.apply(self, *args))
                except UnsatisfiedPreconditions: pass

    def action_sequence(self, length):
        if length == 0:
            yield ([], self)
            return
        for action, s1 in self.pick_action():
            for p, s2 in s1.action_sequence(length - 1):
                yield ([action] + p, s2)

    def plan_bfs(self, goal, cur_len=0, max_len=None):
        for plan, s1 in self.action_sequence(cur_len):
            if goal(s1):
                yield plan
        if not max_len or cur_len < max_len:
            yield from self.plan_bfs(goal, cur_len + 1, max_len)

class UnsatisfiedPreconditions(Exception):
    pass
