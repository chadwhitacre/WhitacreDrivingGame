from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import time


def double(val):
    return val * 2

def half(val):
    return val / 2

class BadShiftTo(Exception):
    pass

class Car(object):

    position = 40
    magnitude = 0
    direction = 0

    def __init__(self, color, make, model, year):
        self.color = color
        self.make = make
        self.model = model
        self.year = year

    def shift_to(self, gear):
        if gear == 'D':
            self.direction = 1
        elif gear == 'R':
            self.direction = -1
        elif gear == 'P':
            self.direction = 0
        else:
            raise BadShiftTo

    def hit_gas(self):
        if self.magnitude < 100:
            self.magnitude += 1

    def hit_brake(self):
        if self.magnitude > 0:
            self.magnitude += -1

    def drive(self):
        print("Driving a {color} {year} {make} {model}! "
              "Wheee!".format(**self.__dict__))
        print('\n\n\n\n')
        colorcode = { 'red': 41
                    , 'green': 42
                    , 'gray': 40
                    , 'yellow': 43
                    , 'blue': 46
                     }[self.color]
        while 1:
            self.position = self.position + (self.magnitude * self.direction)
            output = (' ' * self.position)
            output += '\033[{};1m \033[39;49m\r'.format(colorcode)
            print(output, end='')
            sys.stdout.flush()
            time.sleep(1)


seths_car = Car('gray', 'Hyundai', 'Elantra', 2010)
leahs_car = Car('green', 'Jeep', 'Wrangler', 2015)
sams_car = Car('orange', 'Hummer', 'H2', 2015)

leahs_car.shift_to('D')
leahs_car.hit_gas()
leahs_car.drive()
