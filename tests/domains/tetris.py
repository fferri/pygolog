#!/usr/bin/env python3

from collections import defaultdict
from copy import deepcopy
from strips import *
import sys, time, random, itertools

class Tetromino(Object):
    def __init__(self, name, data):
        super().__init__(name)
        self.data = data

class Tetris(State):
    ROWS = 18
    COLS = 10

    tetrominoes = {
            'i': Tetromino('i',[[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]),
            'o': Tetromino('o',[[0,2,2,0],[0,2,2,0],[0,0,0,0],[0,0,0,0]]),
            'l': Tetromino('l',[[0,3,0,0],[0,3,0,0],[0,3,3,0],[0,0,0,0]]),
            'j': Tetromino('j',[[0,0,4,0],[0,0,4,0],[0,4,4,0],[0,0,0,0]]),
            't': Tetromino('t',[[0,5,0,0],[0,5,5,0],[0,5,0,0],[0,0,0,0]]),
            's': Tetromino('s',[[0,6,0,0],[0,6,6,0],[0,0,6,0],[0,0,0,0]]),
            'z': Tetromino('z',[[0,0,7,0],[0,7,7,0],[0,7,0,0],[0,0,0,0]]),
    }

    def __init__(self):
        self.current = None
        self.row = 0
        self.col = (Tetris.COLS - 4) // 2
        self.board = [[0] * Tetris.COLS for i in range(Tetris.ROWS)]

    def copy(self):
        return deepcopy(self)

    def copy_current_to_board(self):
        for i, j in self.subidx():
            if self.current[i][j]:
                self.board[self.row + i][self.col + j] = self.current[i][j]

    def generate_new_tetromino(self):
        t = random.choice(list(Tetris.tetrominoes.values()))
        self.current = deepcopy(t.data)

    def idx(self):
        return itertools.product(range(Tetris.ROWS), range(Tetris.COLS))

    def subidx(self):
        return itertools.product(range(4), range(4))

    def is_collision(self, dr = 0, dc = 0):
        r, c = (self.row + dr, self.col + dc)
        for i, j in self.subidx():
            if not self.current[i][j]: continue
            if r + i >= Tetris.ROWS: return True
            if c + j < 0 or c + j >= Tetris.COLS: return True
            if self.board[r + i][c + j]: return True
        return False

    def check_collision(self, dr = 0, dc = 0):
        if self.is_collision(dr, dc):
            raise UnsatisfiedPreconditions()

    def transform(self, t):
        d = deepcopy(self.current)
        for i, j in self.subidx():
            i1, j1 = t(i, j)
            self.current[i][j] = d[i1][j1]

    @Action
    def rotate_left(self):
        self.transform(lambda i, j: (3 - j, i))
        self.check_collision()

    @Action
    def rotate_right(self):
        self.transform(lambda i, j: (j, 3 - i))
        self.check_collision()

    @Action
    def move_left(self):
        self.col -= 1
        self.check_collision()

    @Action
    def move_right(self):
        self.col += 1
        self.check_collision()

    def is_row_full(self, row):
        return all(self.board[row])

    def clear_row(self, row):
        for i in range(row, 0, -1):
            for col in range(Tetris.COLS):
                self.board[i][col] = self.board[i - 1][col]
        self.board[0] = [0] * Tetris.COLS

    def clear_full_rows(self):
        for row in range(Tetris.ROWS):
            if self.is_row_full(row):
                self.clear_row(row)

    def down(self):
        if self.is_collision(1):
            self.copy_current_to_board()
            self.clear_full_rows()
            self.generate_new_tetromino()
            self.row = 0
            self.col = (Tetris.COLS - 4) // 2
        else:
            self.row += 1
    @Action
    def move_down(self):
        self.down()
        #self.check_collision()

    @Action
    def drop(self):
        while not self.is_collision(1):
            self.row += 1
        self.down()

    @Action
    def tick(self):
        if not self.current or self.is_collision():
            self.generate_new_tetromino()
            return
        self.down()

    def final_positions(self):
        valid_dcols = [dcol for dcol in range(-Tetris.COLS, Tetris.COLS) if not self.is_collision(0, dcol)]
        def end_row(dc):
            dr = 0
            while not self.is_collision(dr + 1, dc): dr += 1
            return dr
        return [(self.row + end_row(dc), self.col + dc) for dc in valid_dcols]

    def all_final_positions(self):
        ss = [self]
        for i in [0,0,0]:
            try:
                ss.append(Tetris.rotate_right().apply(ss[-1]))
            except UnsatisfiedPreconditions:
                pass
        ret = dict()
        for i, s in enumerate(ss):
            ret['r%d' % i] = s.final_positions()
        return ret

    def print(self):
        for i in range(Tetris.ROWS):
            ln = '#'
            for j in range(Tetris.COLS):
                if self.board[i][j]:
                    ln += '@'
                elif self.current and i - self.row >= 0 and i - self.row < 4 and j - self.col >= 0 and j - self.col < 4 and self.current[i - self.row][j - self.col]:
                    ln += '$'
                else:
                    ln += ' '
            ln += '#'
            print(ln)
        print('#' * (Tetris.COLS + 2))


def curses_tetris(scr):
    s = Tetris()
    s.generate_new_tetromino()

    curses.noecho()
    curses.cbreak()
    scr.keypad(1)
    scr.timeout(100)
    curses.start_color()
    for i in range(1,8): curses.init_pair(i, curses.COLOR_BLACK, i)

    t = 0.600
    last = 0.0
    while True:
        try:
            for i, j in s.idx():
                col = 0
                if s.board[i][j]: col = s.board[i][j]
                elif s.current and i - s.row >= 0 and i - s.row < 4 and j - s.col >= 0 and j - s.col < 4 and s.current[i - s.row][j - s.col]: col = s.current[i-s.row][j-s.col]
                scr.addstr(i, j * 2, '  ', curses.color_pair(col))
            scr.addstr(Tetris.ROWS+1, 0, ' ' * 400)
            scr.addstr(Tetris.ROWS+1, 0, 'Pos.: (%d, %d)' % (s.row, s.col))
            scr.addstr(Tetris.ROWS+2, 0, ' ' * 400)
            scr.addstr(Tetris.ROWS+2, 0, 'Fin.pos.: %s' % (s.all_final_positions(), ))
            c = scr.getch()
            if c == curses.KEY_LEFT:
                s = Tetris.move_left().apply(s)
            elif c == curses.KEY_RIGHT:
                s = Tetris.move_right().apply(s)
            elif c == curses.KEY_DOWN:
                s = Tetris.move_down().apply(s)
            elif c == curses.KEY_UP:
                s = Tetris.rotate_right().apply(s)
            elif c == ord(' '):
                s = Tetris.drop().apply(s)
            elif c == ord('q'):
                break
            elif c == -1: # timeout
                now = time.time()
                if last + t < now:
                    last = now
                    s = Tetris.tick().apply(s)
            else:
                scr.addstr(Tetris.ROWS, 0, 'Unknown key pressed: %d' % c)
        except UnsatisfiedPreconditions:
            curses.flash()

import curses
curses.wrapper(curses_tetris)

