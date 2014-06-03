#!/usr/bin/env python3

from collections import defaultdict
from copy import copy
from strips import *

class S(State):
    def __init__(self, n):
        self.n = n

    @Action
    def incr(self):
        self.n += 1

    @Action
    def double(self):
        self.n *= 2

s = S(0)
goal = lambda s: s.n == 123

