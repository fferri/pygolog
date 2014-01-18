#!/usr/bin/env python3.3

from strips import *

class Locatable(Object): pass
class Dude(Locatable): pass
class Block(Locatable): pass
class Space(Object): pass

player = Dude('player')
a = Block('a')
p = list(Space('p%d' % i) for i in range(14))

is_left = Fluent('is_left', Space, Space)
is_above = Fluent('is_above', Space, Space)
at = Fluent('at', Locatable, Space)
has_dude = Fluent('has_dude', Space)
has_block = Fluent('has_block', Space)

s = State(is_left(p[1], p[2]), is_left(p[4], p[5]), is_left(p[5], p[6]), is_left(p[6], p[7]), is_left(p[8], p[9]), is_left(p[9], p[10]), is_left(p[10], p[11]), is_left(p[12], p[13]), is_above(p[4], p[8]), is_above(p[8], p[12]), is_above(p[9], p[13]), is_above(p[5], p[9]), is_above(p[3], p[5]), is_above(p[2], p[3]), is_above(p[6], p[10]), is_above(p[7], p[11]), at(player, p[3]), has_dude(p[3]), at(a, p[10]), has_block(p[10]))

# move without pushing anything
class Move(Action):
    def execute(self, s, dude: Dude, start: Space, end: Space):
        if not ((s.holds(is_above(start, end)) or s.holds(is_above(end, start)) or s.holds(is_left(start, end)) or s.holds(is_left(end, start))) and s.holds(at(dude, start)) and s.holds(has_dude(start)) and start != end and not s.holds(has_dude(end)) and not s.holds(has_block(end)) and not s.holds(has_block(start))):
            raise UnsatisfiedPreconditions()
        return s.add(at(dude, end), has_dude(end)).remove(at(dude, start), has_dude(start))

# move block
class MoveBlock(Action):
    def execute(self, s, dude: Dude, block: Block, dude_start: Space, block_start: Space, block_end: Space):
        if not (dude_start != block_start and block_start != block_end and dude_start != block_end and s.holds(has_dude(dude_start)) and not s.holds(has_dude(block_start)) and not s.holds(has_dude(block_end)) and s.holds(has_block(block_start)) and not s.holds(has_block(dude_start)) and not s.holds(has_block(block_end)) and (s.holds(is_above(block_start, dude_start), is_above(block_end, block_start)) or s.holds(is_above(dude_start, block_start), is_above(block_start, block_end)) or s.holds(is_left(block_start, dude_start), is_left(block_end, block_start)) or s.holds(is_left(dude_start, block_start), is_left(block_start, block_end))) and s.holds(at(dude, dude_start)) and s.holds(at(block, block_start))):
            raise UnsatisfiedPreconditions()
        return s.add(at(dude, block_start), has_dude(block_start), at(block, block_end), has_block(block_end)).remove(at(dude, dude_start), has_dude(block_start), at(block, block_start), has_block(block_start))

move = Move()
move_block = MoveBlock()

goal = lambda s: s.holds(at(a, p[11]), has_block(p[11]))

