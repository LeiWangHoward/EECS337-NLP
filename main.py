#!/usr/bin/env python -u
""" Main entry point for the project. """

from random import shuffle
from sys import stdin, stdout

import nltk

from scrape import scrapeRecipe, scrapeSearch, selectRecipe


def trim(text):
    return text.lstrip(' \t\n').rstrip(' \t\n')

def main():
    try:
        print "Welcome to creative recipe v1.0"
        while (True):
            print "Enter a search query(q/Q to quit): "
            query = trim(stdin.readline())
            if query == 'q' or query == 'Q':
                print "Bye! Have fun!"
                break
            print "Getting recipe from AllRecipe.com"
            results = scrapeSearch(query)
            print "Searching Done!"
            if not results:
                print "I don't think it is some kind of food, do you?"
            else:
                print "Search results:"
		select = selectRecipe(results);
                print "Processing..."
                recipe = scrapeRecipe(select.replace(" ","-"))
                recipe.my_print()
                print "Done! "

    except KeyboardInterrupt:
        stdout.write("\n")


if __name__ == '__main__':
    main()
