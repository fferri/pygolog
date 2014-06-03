#!/usr/bin/env python3

from strips import *
from domains.math import *

print('initial state: %s' % (s))

print('searching for a plan...')
for p in s.plan_bfs(goal):
    print('found plan: %s' % p)
    break
else:
    print('no plans found.')
