#!/usr/bin/env python3.3

from collections import defaultdict
from copy import copy
from strips import *

class Floor(Object):
    def __init__(self, num):
        super(Floor, self).__init__('floor[%d]' % num)
        self.num = num

floor = {n: Floor(n) for n in [1,2,3,4,5,6]}

class ElevatorState(State):
    def __init__(self, s=None):
        self.num_floors = 6
        self.at = 1
        self.light = defaultdict(bool)

    @Action
    def up(self):
        if self.at >= self.num_floors:
            raise UnsatisfiedPreconditions()
        self.at += 1

    @Action
    def down(self):
        if self.at <= 1:
            raise UnsatisfiedPreconditions()
        self.at -= 1

    @Action
    def turn_off(self):
        if not self.light[self.at]:
            raise UnsatisfiedPreconditions()
        del self.light[self.at]

s = ElevatorState()
s.at = 3
s.light[2] = True
s.light[5] = True

goal = lambda s: not any(s.light.values())

