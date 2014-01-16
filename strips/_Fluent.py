#!/usr/bin/env python

from ._GroundFluent import *
from ._Variable import *

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
