#!/usr/bin/env python3.3

import inspect, itertools

class UnsatisfiedPreconditions(Exception): pass

def unify(a, b):
    if isinstance(a, tuple) and isinstance(b, tuple):
        return len(a) == len(b) and all(unify(x, y) for x, y in zip(a, b))
    else:
        return a is None or b is None or a == b

def query(s, q):
    for fact in s:
        if unify(fact, q):
            yield fact

def holds(s, *qs):
    return all(any(query(s, q)) for q in qs)

def pickaction(s):
    global actions, objects
    for action in actions.values():
        arg_domains = list(objects[t] for t in action.types)
        for args in itertools.product(*arg_domains):
            ground_action = action(*args)
            try:
                s1 = ground_action.execute(s)
                yield (ground_action, s1)
            except UnsatisfiedPreconditions:
                pass

def actionsequence(s, length):
    if length == 0:
        yield ([], s)
        return
    for action, s1 in pickaction(s):
        for p, s2 in actionsequence(s1, length - 1):
            yield ([action] + p, s2)

def planbfs(s, goal, maxlength):
    for length in range(maxlength + 1):
        for plan, s1 in actionsequence(s, length):
            if goal(s1):
                yield plan

class Fluent():
    def __init__(self, name, *types):
        if not isinstance(name, str):
            raise TypeError('name must be str, not %s' % type(name))
        self.name = name
        self.types = types

    def __call__(self, *args):
        if len(args) != len(self.types):
            raise TypeError('bad number of arguments (got %d, expected %d)' % (len(args), len(self.types)))
        for i, (arg, expected_type) in enumerate(zip(args, self.types)):
            if not isinstance(arg, expected_type):
                raise TypeError('bad type for arg %d (got %s, expected %s)' % (i, type(arg), expected_type))

        return GroundFluent(self, *args)

class GroundFluent():
    def __init__(self, fluent, *args):
        self.fluent = fluent
        self.args = args

    def __str__(self):
        return '%s(%s)' % (self.fluent.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.fluent.name == other.fluent.name and self.args == other.args

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.fluent.name) + sum(hash(arg) for arg in self.args)

class Action():
    def __init__(self):
        global actions
        if 'actions' not in globals():
            actions = {}
        self.name = self.__class__.__name__
        if self.name not in actions:
            actions[self.name] = self

        if not hasattr(self, 'execute'):
            raise Exception('actions must implement the execute(s, ...) method')
        arg_spec = inspect.getfullargspec(getattr(self, 'execute'))
        self.types = []
        for arg in arg_spec.args[2:]:
            if arg not in arg_spec.annotations:
                raise Exception('execute() arguments must have type annotation')
            self.types.append(arg_spec.annotations[arg])

    def __call__(self, *args):
        if len(args) != len(self.types):
            raise TypeError('bad number of arguments (got %d, expected %d)' % (len(args), len(self.types)))
        for i, (arg, expected_type) in enumerate(zip(args, self.types)):
            if not isinstance(arg, expected_type):
                raise TypeError('bad type for arg %d (got %s, expected %s)' % (i, type(arg), expected_type))

        return GroundAction(self, *args)

class GroundAction():
    def __init__(self, action, *args):
        self.action = action
        self.args = args

    def __str__(self):
        return '%s(%s)' % (self.action.name, ', '.join(str(arg) for arg in self.args))

    def __repr__(self): return self.__str__()

    def execute(self, s):
        return self.action.execute(s, *self.args)

class Object():
    def __init__(self, name):
        global objects
        if 'objects' not in globals():
            objects = {}
        t = type(self)
        while t is not object:
            if t not in objects:
                objects[t] = []
            objects[t].append(self)
            t = t.__base__
        self.name = name

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self): return hash(self.name)




class Condition: pass

class Holds(Condition):
    def __init__(self, ground_fluent):
        self.ground_fluent = ground_fluent

    def __str__(self):
        return '%s' % (self.ground_fluent)

    def replace(self, var, obj):
        new_args = []
        for arg in self.ground_fluent.args:
            if arg == var: new_args.append(obj)
            else: new_args.append(arg)
        return Holds(GroundFluent(self.ground_fluent.fluent, *new_args))

    def holds(self, s):
        return holds(s, self.ground_fluent)

class And(Condition):
    def __init__(self, c1, c2, *cs):
        self.c1 = c1
        if len(cs) > 0:
            self.c2 = And(c2, cs[0], *cs[1:])
        else:
            self.c2 = c2

    def __str__(self):
        return '%s and %s' % (self.c1, self.c2)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return self.c1.holds(s) and self.c2.holds(s)

class Or(Condition):
    def __init__(self, c1, c2, *cs):
        self.c1 = c1
        if len(cs) > 0:
            self.c2 = And(c2, cs[0], *cs[1:])
        else:
            self.c2 = c2

    def __str__(self):
        return '%s or %s' % (self.c1, self.c2)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return self.c1.holds(s) or self.c2.holds(s)

class Not(Condition):
    def __init__(self, c1):
        self.c1 = c1

    def __str__(self):
        return 'not %s' % (self.c1)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return not self.c1.holds(s)



class Program: pass

class Empty(Program):
    def __str__(self):
        return 'nil'

    def replace(self, var, obj):
        return self

    def trans(self, s):
        raise Exception('cannot step empty program')

    def final(self, s):
        return True

class Exec(Program):
    def __init__(self, ground_action):
        self.ground_action = ground_action

    def __str__(self):
        return '%s' % (self.ground_action)

    def replace(self, var, obj):
        new_args = []
        for arg in self.ground_action.args:
            if arg == var: new_args.append(obj)
            else: new_args.append(arg)
        return Exec(GroundAction(self.ground_action.action, *new_args))

    def trans(self, s):
        try: yield (Empty(), self.ground_action.execute(s), self.ground_action)
        except UnsatisfiedPreconditions: pass

    def final(self, s):
        return False

class If(Program):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __str__(self):
        return 'if %s then %s else %s endIf' % (self.condition, self.then_branch, self.else_branch)

    def replace(self, var, obj):
        return If(self.condition.replace(var, obj), self.then_branch.replace(var, obj), self.else_branch.replace(var, obj))

    def trans(self, s):
        if self.condition.holds(s):
            yield from self.then_branch.trans(s)
        else:
            yield from self.else_branch.trans(s)

    def final(self, s):
        if self.condition.holds(s):
            return self.then_branch.final(s)
        else:
            return self.else_branch.final(s)

class Sequence(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        if len(ps) > 0:
            self.p2 = Sequence(p2, ps[0], *ps[1:])
        else:
            self.p2 = p2

    def __str__(self):
        return '%s; %s' % (self.p1, self.p2)

    def replace(self, var, obj):
        return Sequence(self.p1.replace(var, obj), self.p2.replace(var, obj))

    def trans(self, s):
        if self.p1.final(s):
            yield from self.p2.trans(s)
        else:
            for p1t, st, at in self.p1.trans(s):
                yield (Sequence(p1t, self.p2), st, at)

    def final(self, s):
        return self.p1.final(s) and self.p2.final(s)

class Choose(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        if len(ps) > 0:
            self.p2 = Choose(p2, ps[0], *ps[1:])
        else:
            self.p2 = p2

    def __str__(self):
        return '%s | %s' % (self.p1, self.p2)

    def replace(self, var, obj):
        return Choose(self.p1.replace(var, obj), self.p2.replace(var, obj))

    def trans(self, s):
        yield from self.p1.trans(s)
        yield from self.p2.trans(s)

    def final(self, s):
        pass

class Pick(Program):
    def __init__(self, var, domain, prog):
        self.var = var
        self.domain = domain
        self.prog = prog

    def __str__(self):
        return 'pi %s from %s . %s' % (self.var, self.domain, self.prog)

    def replace(self, var, obj):
        if var == self.var: return self
        else: return Pick(self.var, self.domain, self.prog.replace(var, obj))

    def trans(self, s):
        for obj in objects[self.domain]:
            yield from self.prog.replace(self.var, obj).trans(s)

    def final(self, s):
        for obj in objects[self.domain]:
            if self.prog.replace(self.var, obj).final(s): return True
        return False


def indigolog(p):
    pass

# ---------------------------------------------------------------------------
# ------------------------------ DOMAIN -------------------------------------
# ---------------------------------------------------------------------------

class Block(Object):
    pass

a = Block('a')
b = Block('b')
c = Block('c')
d = Block('d')
table = Object('table')

on = Fluent('on', Block, Object)
clear = Fluent('clear', Object)

s = set([
    clear(b),
    on(b, d),
    on(d, a),
    on(a, table),
    clear(c),
    on(c, table)
])

class Move(Action):
    def execute(self, s, obj: Block, objfrom: Object, objto: Object):
        if objfrom == objto or obj == objto:
            raise UnsatisfiedPreconditions()
        if not holds(s, on(obj, objfrom), clear(obj)):
            raise UnsatisfiedPreconditions()
        if not holds(s, clear(objto)) and objto != table:
            raise UnsatisfiedPreconditions()
        del_set = set([on(obj, objfrom), clear(objto)])
        add_set = set([on(obj, objto), clear(objfrom)])
        return s - del_set | add_set

move = Move()

#ga = move(b, d, table)

print('s = ' + str(s))
#print('execute %s in s gives: %s' % (ga, ga.execute(s)))
#
#print('blocks: ' + str(objects[Block]))
#print('objects: ' + str(objects[Object]))

#goal = lambda s: holds(s, clear(a), on(a, b), on(b, c), on(c, d), on(d, table))
#for p in planbfs(s, goal, 5):
#    print(p)

p0 = Sequence(
    If(And(Holds(clear(b)), Holds(clear(c))),
        Exec(move(c,table,b)),
        Exec(move(c,table,a))
    ),
    Exec(move(c,b,table))
)

x = Block('x')

p = Sequence(
        Choose(
            Exec(move(b, d, table)),
            Exec(move(b, d, c))
            ),
        Choose(
            Exec(move(d, a, table)),
            Exec(move(d, a, b)),
            Exec(move(d, a, c))
            ),
        Pick(x, Block, Exec(move(b, x, table)))
        )

p3 = Sequence(
        Exec(move(b,d,table)),
        Pick(x, Object, Exec(move(d, a, x)))
        )
def trans_star(p, s, a):
    if p.final(s):
        yield (p, s, a)
    if isinstance(p, Empty):
        return
    for p1, s1, a1 in p.trans(s):
        yield from trans_star(p1, s1, a + [a1])

for p1, s1, a1 in trans_star(p, s, []):
    print('p\' = %s' % p1)
    print('s\' = %s' % s1)
    print('a\' = %s' % a1)
