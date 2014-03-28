#!/usr/bin/env python3

from strips import *

def trans_star(p, s, a):
    if p.final(s):
        yield (p, s, a)
    for p1, s1, a1 in p.trans(s):
        yield from trans_star(p1, s1, a + a1)

def indigolog(p, s, a, exog=lambda s: s, verbose=True):
    # at each step apply exogenous events if any:
    s = exog(s)
    for p1, s1, a1 in p.trans(s):
        if verbose: print(a1)
        # commit to the first step, since we are executing in an online fashion:
        return indigolog(p1, s1, a + a1, exog, verbose)
    else:
        if not verbose: return
        if p.final(s): print('%d actions.' % len(a))
        else: print('execution failed; %d actions.' % len(a))
        return

class Program:
    pass

class Choose(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        self.p2 = Choose(p2, ps[0], *ps[1:]) if ps else p2

    def trans(self, s):
        yield from self.p1.trans(s)
        yield from self.p2.trans(s)

    def final(self, s):
        return self.p1.final(s) or self.p2.final(s)

    def __repr__(self): return '(%s|%s)' % (self.p1, self.p2)

class Empty(Program):
    def trans(self, s):
        yield from () # yield nothing

    def final(self, s):
        return True

    def __repr__(self): return 'nil'

class Exec(Program):
    def __init__(self, ground_action):
        self.ground_action = ground_action

    def trans(self, s):
        try: yield (Empty(), self.ground_action.apply(s), [self.ground_action])
        except UnsatisfiedPreconditions: pass

    def final(self, s):
        return False

    def __repr__(self): return '%s' % (self.ground_action)

class If(Program):
    def __init__(self, condition, p1, p2):
        self.condition = condition
        self.p1 = p1
        self.p2 = p2

    def trans(self, s):
        if self.condition(s): yield from self.p1.trans(s)
        else: yield from self.p2.trans(s)

    def final(self, s):
        if self.condition(s): return self.p1.final(s)
        else: return self.p2.final(s)

    def __repr__(self): return 'if %s then %s else %s endIf' % ('<cond>', self.p1, self.p2)

class Pick(Program):
    def __init__(self, domain, p1):
        self.domain = domain
        self.p1 = p1

    def trans(self, s):
        for obj in Object.get_objects_of_type(self.domain):
            yield from self.p1(obj).trans(s)

    def final(self, s):
        for obj in Object.get_objects_of_type(self.domain):
            if self.p1(obj).final(s): return True
        return False

    def __repr__(self): return 'pick from %s and (%s)' % (self.domain.__name__, self.p1)

class Search(Program):
    def __init__(self, p1):
        self.p1 = p1

    def trans(self, s):
        yield from trans_star(self.p1, s, [])

    def final(self, s):
        return any(trans_star(self.p1, s, []))

    def __repr__(self): return 'search { %s }' % self.p1

class Sequence(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        self.p2 = Sequence(p2, ps[0], *ps[1:]) if ps else p2

    def trans(self, s):
        if self.p1.final(s):
            yield from self.p2.trans(s)
        for pn, sn, an in self.p1.trans(s):
            yield (Sequence(pn, self.p2), sn, an)

    def final(self, s):
        return self.p1.final(s) and self.p2.final(s)

    def __repr__(self): return '(%s;%s)' % (self.p1, self.p2)

class Star(Program):
    def __init__(self, p1):
        self.p1 = p1

    def trans(self, s):
        for pn, sn, an in self.p1.trans(s):
            yield (Sequence(pn, self), sn, an)

    def final(self, s):
        return True

    def __repr__(self): return '(%s)*' % (self.p1)

class Test(Program):
    def __init__(self, condition):
        self.condition = condition

    def trans(self, s):
        if self.condition(s):
            yield (Empty(), s, [])

    def final(self, s):
        return False

    def __repr__(self): return '?(%s)' % ('<cond>')

class While(Program):
    def __init__(self, condition, p1):
        self.condition = condition
        self.p1 = p1

    def trans(self, s):
        if self.condition(s):
            for pn, sn, an in self.p1.trans(s):
                yield (Sequence(pn, self), sn, an)

    def final(self, s):
        return not self.condition(s) or self.p1.final(s)

    def __repr__(self): return 'while %s do %s endWhile' % ('<cond>', self.p1)

# ConGolog constructs:

class Conc(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        self.p2 = Conc(p2, ps[0], *ps[1:]) if ps else p2

    def trans(self, s):
        p1_trans = False
        for pn, sn, an in self.p1.trans(s):
            p1_trans = True
            yield (Conc(pn, self.p2), sn, an)
        if p1_trans: return
        for pn, sn, an in self.p2.trans(s):
            yield (Conc(self.p1, pn), sn, an)

    def final(self, s):
        return self.p1.final(s) and self.p2.final(s)

    def __repr__(self): return '(%s||%s)' % (self.p1, self.p2)

class PConc(Program):
    def __init__(self, p1, p2, *ps):
        self.p1 = p1
        self.p2 = PConc(p2, ps[0], *ps[1:]) if ps else p2

    def trans(self, s):
        p1_trans = False
        for pn, sn, an in self.p1.trans(s):
            p1_trans = True
            yield (PConc(pn, self.p2), sn, an)
        if p1_trans: return
        for pn, sn, an in self.p2.trans(s):
            yield (PConc(self.p1, pn), sn, an)

    def final(self, s):
        return self.p1.final(s) and self.p2.final(s)

    def __repr__(self): return '(%s>>%s)' % (self.p1, self.p2)

class IConc(Program):
    def __init__(self, p1):
        self.p1 = p1

    def trans(self, s):
        for pn, sn, an in self.p1.trans(s):
            yield (Conc(pn, IConc(self.p1)), sn, an)

    def final(self, s):
        return True

    def __repr__(self): return 'iconc(%s)' % (self.p1)

def interrupt(trigger, body):
    return While(lambda s: True, If(trigger, body, Test(lambda s: False)))

def prioritized_interrupts(*args):
    return PConc(*args)
