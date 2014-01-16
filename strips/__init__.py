#!/usr/bin/env python

from ._Action import *
from ._Fluent import *
from ._GroundAction import *
from ._GroundFluent import *
from ._Object import *
from ._State import *
from ._UnsatisfiedPreconditions import *
from ._Variable import *

def plan_bfs(s, goal, maxlength):
    for length in range(maxlength + 1):
        for plan, s1 in action_sequence(s, length):
            if goal(s1):
                yield plan
