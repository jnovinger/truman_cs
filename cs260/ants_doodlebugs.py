#!/usr/bin/env python

"""
Ants & Doodlebugs from Savitch, 3rd ed. Assigned in Truman CS 260, Object
Oriented Programming.
"""

from random import randint
from time import sleep
from pdb import set_trace

DEBUG = False
def debug(text):
    if DEBUG:
        print text

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Bug():
    """ Base class for all bug types, provides common behaviors """

    def __init__(self):
        self.age = 0

    def move(self):
        """ Generates the grid offset for the current turn's move """
        x, y = MOVES[randint(0, len(MOVES) - 1)]
        debug("Moving %s by %s,%s" % (self.__class__, x, y))
        self.age += 1
        return (x, y)


class Ant(Bug):
    """ Provides Ant specific behaviors and properties """

    def __str__(self):
        """ Display character for our ant """
        return 'o'


class Doodlebug(Bug):
    """ Provide Doodlebug specific behaviors and properties """

    def __init__(self):
        #super(Doodlebug)
        self.age = 0
        self.hunger = 0

    def __str__(self):
        """ Display charactor for our doodlebug """
        return 'X'


class Grid():
    """ Provides the data structure and methods to manage the world's map """

    def __init__(self, width, height):
        """ Constructor """
        self._width = width
        self._height = height
        self.turn_number = 0
        # setup world, dict with (x, y) coord tuple as key
        self.ants = {}
        self.doodlebugs = {}
        self.world = {}

    def _get_random_pos(self):
        x = randint(0, self._width - 1)
        y = randint(0, self._height - 1)
        return (x, y)

    def add(self, bug, loc = None):
        """ Add a bug """
        if loc is None:
            self._build_grid()
            loc = self._get_random_pos()
            while loc in self.world:
                loc = self._get_random_pos()
        if isinstance(bug, Ant):
            self.ants[loc] = bug
        else:
            self.doodlebugs[loc] = bug

    def _build_grid(self):
        self.world = {}
        for key in self.ants.keys():
            self.world[key] = self.ants[key]
        for key in self.doodlebugs.keys():
            self.world[key] = self.doodlebugs[key]

    def display(self):
        """ Draw the map of the grid """
        self._build_grid()
        for y in xrange(self._height):
            line = ''
            for x in xrange(self._width):
                line += '%s' % (self.world.get((x, y)) or '.')
            if y == 0:
                line += '\t      Ants: %00d' % len(self.ants)
            elif y == 1:
                line += '\tDoodlebugs: %00d' % len(self.doodlebugs)
            elif y == 2:
                line += '\t      Turn: %00d' % self.turn_number
            print line
        print "\n"

    def game_over(self):
        if len(self.ants) == 0 or len(self.doodlebugs) == 0:
            debug("Game over!")
            return True
        else:
            return False

    def _out_of_range(self, location):
        if (location[0] < 0 or location[0] > self._width - 1 or
            location[1] < 0 or location[1] > self._height -1):
            return True
        else:
            return False

    def turn(self):
        """
        This runs one turn of the world, should probably live there. And be
        less ugly. Indentation is bad.
        """
        self.turn_number += 1
        #set_trace()

        world = self._build_grid()

        # loop through doodlebugs
        for location in self.doodlebugs.keys():
            if self._out_of_range(location):
                print location


            dbug = self.doodlebugs[location]

            # detect adjacent and LUNCH!
            found = False
            for offset in MOVES:
                new_loc = (location[0] + offset[0], location[1] + offset[1])
                if new_loc in self.ants:
                    del(self.ants[new_loc])
                    del(self.doodlebugs[location])
                    self.doodlebugs[new_loc] = dbug
                    dbug.hunger = 0
                    found = True
                    break
            if found:
                continue

            offset = dbug.move()
            new_loc = (location[0] + offset[0], location[1] + offset[1])

            if dbug.hunger >= 3:
                del(self.doodlebugs[location])
                continue

            dbug.hunger += 1

            # make sure we're not out of bounds
            if self._out_of_range(new_loc):
                continue

            # make sure we don't move on top of another bug of the same kind
            if new_loc in self.doodlebugs:
                continue


            # Ok, by now:
            #   1) We're a doodlebug
            #   2) We're not trying to move off the board
            #   3) We're not jumping on top of a bug that is the same kind
            #   4) If we're jumping on an ant, the ant is removed
            # So, delete us from our old location and add us at our new location
            del(self.doodlebugs[location])
            self.doodlebugs[new_loc] = dbug

            # see if we need to breed
            if dbug.age % 5 == 0:
                self._build_grid()
                offset = dbug.move()
                new_pos = (location[0] + offset[0], location[1] + offset[1])
                if self._out_of_range(new_pos):
                    continue
                if new_pos not in self.world:
                    self.add(Doodlebug(), new_pos)

        # loop through ants
        for location in self.ants.keys():
            ant = self.ants[location]
            offset = ant.move()
            new_loc = (location[0] + offset[0], location[1] + offset[1])

            #make sure we're not out of bounds
            if (new_loc[0] < 0 or new_loc[0] > (self._width - 1) or
                new_loc[1] < 0 or new_loc[1] > (self._height - 1)):
                continue

            # make sure we don't move on top of another bug
            if new_loc in self.ants or new_loc in self.doodlebugs:
                continue

            # all good? make the move
            del(self.ants[location])
            self.ants[new_loc] = ant

            # see if we need to brred
            if ant.age % 3 == 0:
                self._build_grid()
                offset = ant.move()
                new_ant_pos = (location[0] + offset[0], location[1] + offset[1])
                if self._out_of_range(new_ant_pos):
                    continue
                if new_ant_pos not in self.world:
                    self.add(Ant(), new_ant_pos)

        self.display()


class World:
    """ Represents the world that our bugs live in """

    def __init__(self, width=20, height=20, sleep=0.1, ants=100, doodlebugs=5):
        """ Constructor, let's get this going """
        self.grid = Grid(width, height)
        self.sleep = sleep

        # populate grid with bugs
        for ant in range(ants):
            self.grid.add(Ant())

        for dbug in range(doodlebugs):
            self.grid.add(Doodlebug())

        self.grid.display()

    def run(self):
        begin_count = float(len(self.grid.ants) + len(self.grid.doodlebugs))
        try:
            while not self.grid.game_over():
                cur_count = len(self.grid.ants) + len(self.grid.doodlebugs)
                if self.sleep:
                    sleep(self.sleep)
                self.grid.turn()
        except KeyboardInterrupt:
            print "Bye!"


width = 45
height = 45
ratio = (width * height) / 400

world = World(width, height, 0, int(100 * ratio), int(5 * ratio))
#world = World()
world.run()
