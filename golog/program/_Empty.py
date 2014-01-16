#!/usr/bin/env python

from ._Program import *

class Empty(Program):
    def __str__(self):
        return 'nil'

    def replace(self, var, obj):
        return self

    def trans(self, s):
        raise Exception('cannot step empty program')

    def final(self, s):
        return True
