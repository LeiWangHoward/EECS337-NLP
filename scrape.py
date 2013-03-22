#!/usr/bin/env python
""" Contains functions for scraping allrecipes.com. 
    ver 1.1 March 14 Fixed time parse issue, now deal with hours
    ver 1.2 March 21 Fixed 'no amount' issue, e.g. cooking spray"""
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup
from recipe import Recipe

#now scale to 1 serve
SEARCH_URL = "http://allrecipes.com/search/default.aspx?qt=k&wt=%s"
RECIPE_URL = "http://allrecipes.com/Recipe/%s/Detail.aspx?scale=1&ismetric=0"
RECIPE_TEST = "http://allrecipes.com/recipe/broiled-parmesan-lemon-tilapia/detail.aspx?scale=1&ismetric=0"

def scrapeSearch(query):
    """ Search for query and return a list of recipies."""
    entity = urlopen(SEARCH_URL % (query.replace(" ", "%20"))).read()
    soup = BeautifulSoup(entity)
    links = soup.find_all(class_="title", id=re.compile('ctl00_CenterColumnPlaceHolder_rptResults_ct'))
    return [link.text for link in links]

def scrapeRecipe(title):
    """ Scrape the page for the recipe with the given title. Return a recipe
    parsed from that page. """
    #print title #test
    entity = urlopen(RECIPE_URL % title).read()
    #entity = urlopen(RECIPE_TEST).read()
    soup = BeautifulSoup(entity)
    #print soup.prettify() #test use
    details = soup.find(class_='detail-section greydotted ingredients')
    recipe = Recipe()

    # Get title
    recipe.title = title.replace("-"," ")#details.find(id='itemTitle').text

    # Get ingredients and amounts, save them to seperate array.
    initIngredients(recipe, details.find(id='zoneIngredients'))

    # Get prep, cook, and total times.
    initTime(recipe, details)
    # Get cooking directions
    recipe.directions = initDirections(details.find(class_='directions'))
    #print recipe.__dict__ #test
    return recipe

def selectRecipe(results):
    """Let user select a recipe from search results"""
    if len(results) > 10:
        range_max = 10
    else:
        range_max = len(results)
    for index in range(0, range_max):
        print '{0} : {1}'.format(index+1, results[index])
    select = int(raw_input("Select a recipe: "))
    return results[select-1]

def initTime(recipe, details):
    """ Parse times """
    # prep time
    time = details.find(id='prepMinsSpan')
    if time:
        recipe.preptime += calculateTime(time.text)
    time_h = details.find(id='prepHoursSpan')
    if time_h:
        recipe.preptime = recipe.preptime + calculateTime(time_h.text)
   
    # cook time
    time2 = details.find(id='cookMinsSpan')
    if time2:
        recipe.cooktime += calculateTime(time2.text)
    time2_h = details.find(id='cookHoursSpan')
    if time2_h:
        recipe.cooktime = recipe.cooktime + calculateTime(time2_h.text)
 
    #time3 = details.find(id='totalMinsSpan')
    recipe.totaltime = recipe.preptime + recipe.cooktime

def calculateTime(text):
    #match=re.match('(?:(\d*)hr)?(?:(\d*)mins)?',text)
    parts = text.split(' ')
    if parts[1]=="mins":
        minutes = int(parts[0])
    else:
        minutes = int(parts[0]) * 60
    return minutes

def initIngredients(recipe,div):
    """ Parse a list of ingredient strings and init ingredients and amount in recipe class """
    temp = []
    temp = div.find_all("p", class_="fl-ing")
    print temp #test use
    #recipe.ingredients=[ingredient.find(id='lblIngName').text for ingredient in temp] #the website has problem, not always have ingredients
    for ingredient in temp:
        if ingredient.find(id='lblIngName'):
            recipe.ingredients.append(ingredient.find(id='lblIngName').text)
        else:
            recipe.ingredients.append('')

    for ingredient in temp:
        if ingredient.find(id='lblIngAmount'):
            recipe.ingredients_amount.append(ingredient.find(id='lblIngAmount').text)
        else:
            recipe.ingredients_amount.append('')

def initDirections(div):
    """ Parse a list of directions as strings and return them"""
    return [span.text for span in div.findAll('span', 'plaincharacterwrap break')]

