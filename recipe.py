#!/usr/bin/env python
""" Contains the Recipe data structure and functions for creating and
manipulating them. """

import re
from sys import stdout
#class ingredient:
#    def __init__(self):
#        self.amount
#        self.name

class Recipe(object):
    """ Represents a single recipe. Notice all times are represented as mins """
    def __init__(self):
        self.title = ""
        self.preptime = 0
        self.cooktime = 0
        self.totaltime = 0
        self.ingredients = []
	self.ingredients_amount = []
        self.directions = []
    def my_print(self):
        print #print an empty line, the same below
        print '{0:20}'.format(self.title)
        print 
	print 'Prep: {0:5} mins. Cook:{1:5} mins. Total:{2:5} mins.'.format(self.preptime, self.cooktime, self.totaltime)
	print
        print 'Ingredients:'
        for index in range(len(self.ingredients)):
            print '{0} {1}'.format(self.ingredients_amount[index].encode('utf8'), self.ingredients[index].encode('utf8'))
        print
        print 'Directions:'
        for num in range(len(self.directions)):
            print 'Step{0:2d}: {1}'.format(num+1, self.directions[num])
        print
