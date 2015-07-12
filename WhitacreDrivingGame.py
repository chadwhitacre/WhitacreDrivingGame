from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import locale
import time
import threading
from math import pi, sin

locale.setlocale(locale.LC_ALL,"")
encoding = locale.getpreferredencoding()

def double(val):
    return val * 2

def half(val):
    return val / 2

COLORS = 'blue cyan green magenta red white yellow'.split()
class BadColor(Exception): pass

fix = lambda v: int(round(v))


class Car(object):

    scr = None              # a curses screen object
    position = (None, None) # (y, x)
    speed = None            # magnitude as float; 0.0 is stopped
    direction = None        # radians as float, with 0.0 at the top of the screen
    char = None             # indicates direction: < ^ > v

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
        self.direction = pi/2                   # facing right,
        self.char = '>'
        self.speed = 0.0                        # standing still.

        self._log = open('log', 'w+', buffering=0)

    def log(self, *a, **kw):
        kw.setdefault('file', self._log)
        print(*a, **kw)


    def hit_gas(self):
        self.speed = min(self.speed + 0.1, 10)

    def hit_brake(self):
        self.speed = max(self.speed - 0.1, 0)

    def steer(self, direction):
        assert direction in ('left', 'right')
        newdirection = self.direction + {'left': -pi/2, 'right': pi/2}[direction]

        if newdirection >= 2*pi:
            newdirection -= 2*pi
        elif newdirection < 0:
            newdirection += 2*pi

        self.char = { 0.0:      '^'
                    , pi/2:     '>'
                    , pi:       'v'
                    , (3*pi)/2: '<'
                     }.get(newdirection, '\u2306'.encode(encoding))

        self.direction = newdirection


    def start(self):
        self.scr.move(self.scr.getmaxyx()[0]-1, 0)
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


    def get_new_position(self, y, x, speed, direction):

        C = pi/2
        B = direction % (pi/2)  # adjust for quadrant
        A = pi - C - B

        c = speed
        b = (c * sin(B)) / sin(C)
        a = (c * sin(A)) / sin(A)

        if 0 <= direction < pi/2:
            y -= a
            x += b
        elif pi/2 <= direction < pi:
            y += b
            x += a
        elif pi <= direction < (3*pi)/2:
            y += a
            x -= b
        else:
            assert (3*pi)/2 <= direction <= 2*pi
            y -= b
            x -= a

        Y, X = self.scr.getmaxyx()
        if y < 0:       y = Y-2
        elif y >= Y-2:  y = 0
        if x < 0:       x = X-1
        elif x >= X-1:  x = 0

        return y, x


    def redraw_loop(self):
        while 1:
            # Redraw car.
            y, x = self.position
            self.scr.delch(fix(y), fix(x))
            y, x = self.get_new_position(y, x, self.speed, self.direction)
            self.scr.addstr(fix(y), fix(x), self.char, self._color)
            self.position = (y, x)

            # Redraw speedometer.
            Y, X = self.scr.getmaxyx()
            self.scr.addstr(Y-1, X-20, 'Speed: {: >3d}'.format(int(self.speed * 10)))
            self.scr.addstr(Y-1, X-40, 'Direction: {: >.2f}'.format(self.direction))

            self.scr.refresh()
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
