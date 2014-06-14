#!/usr/bin/env python3

from strips import *
from golog_program import *
from domains.elevator import *

up = lambda: Exec(ElevatorState.up())
down = lambda: Exec(ElevatorState.down())
turn_off = lambda: Exec(ElevatorState.turn_off())

def next_floor_to_serve(fl):
    return Test(lambda s: s.light[fl])

def go_floor(fl):
    return While(lambda s: s.at != fl, If(lambda s: s.at <  fl, up(), down()))

def serve_a_floor():
    return Pick(Floor, lambda x: Sequence(next_floor_to_serve(x.num), go_floor(x.num), turn_off()))

def control():
    return Sequence(While(lambda s: any(s.light.values()), serve_a_floor()), go_floor(1))

p = control()
print('initial state: %s' % s)
print('program: %s' % p)

def ask_exog(s):
    print('current state: %s' % s)
    ans = input('exog? [type the numbers of buttons pressed, from 1 to %d] ' % s.num_floors)
    print('\n\n')
    for i in map(int, ans):
        s.light[i] = True
    return s

def print_exec(a):
    print('executing %s' % a)

indigolog(p, s, [], exec_cb=print_exec, exog_cb=ask_exog)

