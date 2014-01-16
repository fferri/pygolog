#!/usr/bin/env python

class Condition:
    pass

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

class Not(Condition):
    def __init__(self, c1):
        self.c1 = c1

    def __str__(self):
        return 'not %s' % (self.c1)

    def replace(self, var, obj):
        return self

    def holds(self, s):
        return not self.c1.holds(s)

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
