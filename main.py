#!/usr/bin/env python -u
""" Main entry point for the project. """

from random import shuffle
from scrape import scrapeRecipe, scrapeSearch, selectRecipe

def main():
    try:
        print "Welcome to creative recipe v1.0"
        while (True):
            query = raw_input("Enter a search query(q/Q to quit): ")
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
        print

if __name__ == '__main__':
    main()
