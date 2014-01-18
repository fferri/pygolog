#!/usr/bin/env python

from strips import *
from domains.sokoban import *

for t in get_types():
    print('objects of type %s: %s' % (t.__name__, get_objects_of_type(t)))
print('initial state = %s' % (s))

for maxlen in range(1,15):
    print('searching plans of len %d...' % maxlen)
    for p in plan_bfs(s, goal, maxlen):
        print(p)
print('finished.')
