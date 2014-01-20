#!/usr/bin/env python

from strips import *
from domains.blocks import *

for t in get_types():
    print('objects of type %s: %s' % (t.__name__, get_objects_of_type(t)))
print('initial state = %s' % (s))

print('searching plans...')
for p in plan_bfs(s, goal, 5):
    print(p)
print('finished.')
