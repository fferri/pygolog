#!/usr/bin/env python

import inspect, itertools

from ._GroundAction import *
from ._Object import *
from ._UnsatisfiedPreconditions import *

_actions = {}

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
            if not isinstance(arg, expected_type):
                raise TypeError('bad type for arg %d (got %s, expected %s)' % (i, type(arg), expected_type))

        return GroundAction(self, *args)
