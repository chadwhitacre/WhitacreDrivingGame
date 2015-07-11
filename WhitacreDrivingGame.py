from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import time


def double(val):
    return val * 2

def half(val):
    return val / 2

COLORS = 'blue cyan green magenta red white yellow'.split()
class BadColor(Exception): pass


class Car(object):

    scr = None
    position = (None, None)  # (y, x)
    speed = 0
    direction = (0, 1)

    def __init__(self, color, make, model, year):
        if color not in COLORS:
            raise BadColor()
        self.color = color
        self._color = curses.color_pair(getattr(curses, 'COLOR_'+color.upper()))
        self.make = make
        self.model = model
        self.year = year
        self.ymax, self.xmax = self.scr.getmaxyx()
        self.position = (self.ymax // 2, self.xmax // 10)  # start at left middle

    def hit_gas(self):
        if self.speed < 100:
            self.speed += 1

    def hit_brake(self):
        if self.speed > 0:
            self.speed += -1

    def steer(self):
        raise NotImplementedError

    def drive(self):

        self.scr.move(self.ymax-1, 0)
        self.scr.addstr("Driving a ")
        self.scr.addstr(self.color, self._color)
        self.scr.addstr(" {year} {make} {model}! Wheee!".format(**self.__dict__))

        #colorcode = { 'red': 41
        #            , 'green': 42
        #            , 'gray': 40
        #            , 'yellow': 43
        #            , 'blue': 46
        #             }[self.color]

        while 1:
            # Redraw the car.
            y, x = self.position
            self.scr.delch(y, x)
            y += self.speed * self.direction[0]
            x += self.speed * self.direction[1]
            self.scr.addstr(y, x, '#', self._color)
            self.scr.refresh()
            self.position = (y, x)
            time.sleep(0.5)


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

    leahs_car.hit_gas()
    leahs_car.drive()


def ctrl_c_wrapper(stdscr):
    try:
        main(stdscr)
    except KeyboardInterrupt:
        stdscr.clear()
        y, x = stdscr.getmaxyx()
        stdscr.move(y//2, (x//2)-2)
        stdscr.addstr('Bye!', curses.color_pair(curses.COLOR_GREEN))
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(ctrl_c_wrapper)
