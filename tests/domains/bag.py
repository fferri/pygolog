#!/usr/bin/env python3

from collections import defaultdict
from strips import *
from golog_program import *

class S(State):
    def __init__(self, *args):
        self.exists = set(args)

    @Action
    def remove(self, obj):
        if obj not in self.exists:
            raise UnsatisfiedPreconditions()
        self.exists.remove(obj)

a = Object('a')
b = Object('b')
c = Object('c')

s = S(a, b, c)

