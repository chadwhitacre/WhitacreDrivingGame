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

    def shift(self, to):
        if to == 'D':
            self.direction = 1
        elif to == 'R':
            self.direction = -1
        elif to == 'P':
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
        while 1:
            self.position = self.position + (self.magnitude * self.direction)
            output = (' ' * self.position) + '*\r'
            print(output, end='')
            sys.stdout.flush()
            time.sleep(1)


seths_car = Car('gray', 'Hyundai', 'Elantra', 2010)
leahs_car = Car('green', 'Jeep', 'Wrangler', 2015)
sams_car = Car('orange', 'Hummer', 'H2', 2015)

leahs_car.drive()
