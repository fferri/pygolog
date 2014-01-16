#!/usr/bin/env python

from strips import UnsatisfiedPreconditions

def trans_star(p, s, a):
    if p.final(s):
        yield (p, s, a)
    if isinstance(p, Empty):
        return
    for p1, s1, a1 in p.trans(s):
        yield from trans_star(p1, s1, a + [a1])

class Program:
    pass

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
        return self.p1.final() or self.p2.final()

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

class Pick(Program):
    def __init__(self, var, domain, prog):
        self.var = var
        self.domain = domain
        self.prog = prog

    def __str__(self):
        return 'pick %s from %s . %s' % (self.var, self.domain, self.prog)

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

class Star(Program):
    def __init__(self, p1):
        self.p1 = p1

    def __str__(self):
        return '%s*' % (self.p1)

    def replace(self, var, obj):
        return Star(self.p1.replace(var, obj))

    def trans(self, s):
        yield from self.p1.trans(s)

    def final(self, s):
        return True

class While(Program):
    def __init__(self, condition, p1):
        self.condition = condition
        self.p1 = p1

    def __str__(self):
        return 'while %s do %s endWhile' % (self.condition, self.p1)

    def replace(self, var, obj):
        return While(self.condition.replace(var, obj), self.then_branch.replace(var, obj), self.else_branch.replace(var, obj))

    def trans(self, s):
        if self.condition.holds(s):
            for pn, sn, an in self.p1.trans(s):
                yield (Sequence(pn, While(self.condition, self.p1)), s1, an)

    def final(self, s):
        return not self.condition.holds(s) or self.p1.final()
