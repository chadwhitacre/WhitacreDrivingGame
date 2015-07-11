from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import time
import threading
from math import pi, sin


def double(val):
    return val * 2

def half(val):
    return val / 2

COLORS = 'blue cyan green magenta red white yellow'.split()
class BadColor(Exception): pass


class Car(object):

    scr = None              # a curses screen object
    position = (None, None) # (y, x)
    speed = None            # magnitude as float; 0.0 is stopped
    direction = None        # radians as float, with 0.0 at the top of the screen

    def __init__(self, color, make, model, year):
        if color not in COLORS:
            raise BadColor()
        self.color = color
        self._color = curses.color_pair(getattr(curses, 'COLOR_'+color.upper()))
        self.make = make
        self.model = model
        self.year = year
        ymax, xmax = self.scr.getmaxyx()

        self.position = (ymax // 2, xmax // 10) # Start at left middle,
        self.direction = 90.0                   # facing right,
        self.speed = 0.0                        # standing still.

    def hit_gas(self):
        if self.speed < 100:
            self.speed += 1

    def hit_brake(self):
        if self.speed > 0:
            self.speed += -1

    def steer(self, direction):
        assert direction in ('left', 'right')
        newdirection = direction + {'left': -1, 'right': 1}[direction]
        if newdirection == 360:
            newdirection = 0
        elif newdirection == -1:
            newdirection = 359
        self.direction = newdirection

    def start(self):
        self.scr.move(self.ymax-1, 0)
        self.scr.addstr("Driving a ")
        self.scr.addstr(self.color, self._color)
        self.scr.addstr(" {year} {make} {model}! Wheee!".format(**self.__dict__))

        t = threading.Thread(target=self.redraw_loop)
        t.daemon = True
        t.start()

        while 1:
            c = self.scr.getch()
            if c == curses.KEY_DOWN:
                self.hit_brake()
            elif c == curses.KEY_UP:
                self.hit_gas()
            elif c == curses.KEY_LEFT:
                self.steer('left')
            elif c == curses.KEY_RIGHT:
                self.steer('right')
            elif c == ord('q'):
                raise SystemExit

    @staticmethod
    def get_new_position(y, x, speed, direction):

        C = pi/2
        B = direction % pi/2    # adjust for quadrant
        A = pi - C - B

        c = speed
        b = (c * sin(B)) / sin(C)
        a = (c * sin(A)) / sin(A)

        y = a
        x = b

        if 0 < direction <
        if pi/2 < direction < pi:
            y =

        return y, x

    def redraw_loop(self):
        while 1:
            y, x = self.position
            self.scr.delch(y, x)
            y, x = self.get_new_position(y, x, self.speed, self.direction)
            self.scr.addstr(int(round(y)), int(round(x)), '#', self._color)
            self.scr.refresh()
            self.position = (y, x)
            time.sleep(0.1)


def main(stdscr):

    # wrapper doesn't actually initialize colors fully
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

    # make cursor invisible
    curses.curs_set(0)

    # clear the screen
    stdscr.clear()
    stdscr.refresh()

    Car.scr = stdscr

    seths_car = Car('blue', 'Hyundai', 'Elantra', 2010)
    leahs_car = Car('green', 'Jeep', 'Wrangler', 2015)
    sams_car = Car('yellow', 'Hummer', 'H2', 2015)

    leahs_car.start()


def ctrl_c_wrapper(stdscr):
    try:
        main(stdscr)
    except (KeyboardInterrupt, SystemExit):
        stdscr.clear()
        y, x = stdscr.getmaxyx()
        stdscr.move(y//2, (x//2)-2)
        stdscr.addstr('Bye!', curses.color_pair(curses.COLOR_GREEN))
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(ctrl_c_wrapper)
