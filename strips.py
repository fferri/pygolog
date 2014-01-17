#!/usr/bin/env python

import inspect, itertools
from copy import copy, deepcopy

_actions = {}
_objects = {}

def unify(a, b, sigma={}):
    if isinstance(a, GroundFluent) and isinstance(b, GroundFluent):
        return len(a.args) == len(b.args) and a.fluent.name == b.fluent.name \
                and all(unify(x, y, sigma) for x, y in zip(a.args, b.args))
    elif isinstance(a, GroundAction) and isinstance(b, GroundAction):
        return len(a.args) == len(b.args) and a.action.name == b.action.name \
                and all(unify(x, y, sigma) for x, y in zip(a.args, b.args))
    elif isinstance(a, Variable):
        if a in sigma and sigma[a] != b: return None
        sigma[a] = b
        return sigma
    elif isinstance(b, Variable):
        if b in sigma and sigma[b] != a: return None
        sigma[b] = a
        return sigma
    else:
        return a == b

def get_action_by_name(n):
    return _actions[n]

def pick_action(s):
    global actions, objects
    for action in actions.values():
        arg_domains = list(get_objects_of_type(t) for t in action.types)
        for args in itertools.product(*arg_domains):
            ground_action = action(*args)
            try:
                s1 = ground_action.execute(s)
                yield (ground_action, s1)
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

class Action(object):
    def __init__(self):
        global actions
        if 'actions' not in globals():
            actions = {}
        self.name = self.__class__.__name__
        if self.name not in actions:
            actions[self.name] = self

        if not hasattr(self, 'execute'):
            raise Exception('actions must implement the execute(s, ...) method')
        arg_spec = inspect.getfullargspec(getattr(self, 'execute'))
        self.types = []
        for arg in arg_spec.args[2:]:
            if arg not in arg_spec.annotations:
                raise Exception('execute() arguments must have type annotation')
            self.types.append(arg_spec.annotations[arg])

    def __call__(self, *args):
        if len(args) != len(self.types):
            raise TypeError('bad number of arguments (got %d, expected %d)' % (len(args), len(self.types)))
        for i, (arg, expected_type) in enumerate(zip(args, self.types)):
            if not isinstance(arg, expected_type) and not isinstance(arg, Variable):
                raise TypeError('bad type for arg %d (got %s, expected %s)' % (i, type(arg), expected_type))

        return GroundAction(self, *args)

class Fluent(object):
    def __init__(self, name, *types):
        if not isinstance(name, str):
            raise TypeError('name must be str, not %s' % type(name))
        self.name = name
        self.types = types

    def __call__(self, *args):
        if len(args) != len(self.types):
            raise TypeError('bad number of arguments (got %d, expected %d)' % (len(args), len(self.types)))
        for i, (arg, expected_type) in enumerate(zip(args, self.types)):
            if not isinstance(arg, expected_type) and not isinstance(arg, Variable):
                raise TypeError('bad type for arg %d (got %s, expected %s)' % (i, type(arg), expected_type))

        return GroundFluent(self, *args)

class GroundAction(object):
    def __init__(self, action, *args):
        self.action = action
        self.args = args

    def __str__(self):
        return '%s(%s)' % (self.action.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def execute(self, s):
        return self.action.execute(s, *self.args)

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
    def __init__(self, *contents):
        if len(contents) == 1 and isinstance(contents[0], set):
            self.contents = contents[0]
        else:
            self.contents = set(contents)

    def query(self, q):
        for fact in self.contents:
            sigma = dict()
            if unify(fact, q, sigma):
                yield fact

    def holds(self, *qs):
        return all(any(self.query(q)) for q in qs)

    def add(self, *qs):
        return State(self.contents | set(qs))

    def remove(self, *qs):
        return State(self.contents - set(qs))

    def __str__(self):
        return str(self.contents)

    def __repr__(self):
        return self.__str__()

    def __or__(self, other):
        return State(self.contents | other.contents)

    def __sub__(self, other):
        return State(self.contents - other.contents)

    def __eq__(self, other):
        return self.contents == other.contents

    def __ne__(self, other):
        return not self.__eq__(other)

class UnsatisfiedPreconditions(Exception):
    pass

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
