#!/usr/bin/env python3

from strips import *
from domains.blocks2 import *

for t in Object.get_types():
    print('objects of type %s: %s' % (t.__name__, Object.get_objects_of_type(t)))
print('initial state: %s' % (s))

print('searching for a plan...')
for p in s.plan_bfs(goal):
    print('found plan: %s' % p)
    break
else:
    print('no plans found.')
