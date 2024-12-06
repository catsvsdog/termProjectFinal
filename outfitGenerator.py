from random import randint, choice
from loadImageFunction import loadImage
from clothingObjects import Item, Outfit
from cmu_graphics import *
import os
import copy
import math
import datetime

def getSeasonTops(topList, season):
  season_tops = []
  for top in topList:
    if season in top.season:
        season_tops.append(top)
  return season_tops


def getSeasonBottoms(bottomList, season):
  season_bottoms = []
  for bottom in bottomList:
    if season in bottom.season:
        season_bottoms.append(bottom)
  return season_bottoms


def generateAllGoodOutfits(topList, bottomList):
    if not topList:
        print('Error, top is empty, please add tops.')
    if not bottomList:
        print('Error, bottom is empty, please add bottoms')
    else:
        good_outfits = []
        for top in topList:
            for bottom in bottomList:
                outfit = Outfit(top, bottom)
                # print('outfit = ', outfit)
                if outfit.isColorMatch() and outfit.isTypeMatch():
                    good_outfits.append(outfit)
        return good_outfits
    return []



#source: chatgpt
def generateSeasonData():
  seasons = {
    "spring": (
        ("Average Range", (45, 70)),
        ("Early Spring", (40, 60)),
        ("Late Spring", (55, 75))
    ),
    "summer": (
        ("Average Range", (70, 90)),
        ("Early Summer", (65, 85)),
        ("Peak Summer", (80, 110))
    ),
    "autumn": (
        ("Average Range", (50, 70)),
        ("Early Autumn", (60, 80)),
        ("Late Autumn", (40, 60))
    ),
    "winter": (
        ("Average Range", (20, 50)),
        ("Mild Winter Regions", (30, 60)),
        ("Harsh Winter Regions", (-10, 30))
    )
  }
  return seasons

#source: chatgpt
def getSeasonFromTemp(temp):
    data = generateSeasonData()
    if isinstance(temp, int):
        for season in data:  # Iterate through keys (seasons)
            ranges = data[season]  # Access the range tuples for each season
            for time, (low, high) in ranges:
                if low <= temp <= high:  # Corrected condition
                    return season 
    
    return "Invalid season"  # Return this if no range matches

# print(getSeasonFromTemp(70))


# Get the current month and year
current_date = datetime.date.today()
month = current_date.month
year = current_date.year

# Create a function to get the first day of the month and total days - chatgpt
def get_calendar_data(year, month):
    first_day = datetime.date(year, month, 1)
    start_day = first_day.weekday()  # Monday = 0, Sunday = 6
    total_days = (datetime.date(year, month + 1, 1) - first_day).days if month != 12 else 31
    return start_day, total_days


def pickOutfitOnUserPreference(outfits, user_preferences):
  #Pick outfit based on user input
  if not outfits:
    return None
  for outfit in outfits: # iterate over each outfit and check color and type against it
    colors = outfit.getColor()
    for color in colors:
      if color in user_preferences:
        return outfit
  # print('Warning: no user preferred match, return None')
  return None

def get4UserPreferredOutfits(outfits, preferred_outfits, user_preferences):
  # display 4 outfits at a time.
  # check the outfits list len
  outfits_size = len(outfits)

  loop_range = loop_range = min(outfits_size, 4)

  for i in range(loop_range): # loop from 0 to 4
    outfit = pickOutfitOnUserPreference(outfits, user_preferences)
    if not outfit:
      print('Warning: outfit is empty, nothing to display!')
      return None
 
    outfits.remove(outfit)
    # add displayed outfit into display outfit list
    preferred_outfits.append(outfit)

  return outfits, preferred_outfits

def pickAGoodOutfitRandomly(outfits):
  #Randomly pick 1 outfit from good outfit list.
  if not outfits:
    print('Warning, outfit is empty.')
    return None
  outfit = choice(outfits)
  return outfit

def recycleDisplayedOutfits(displayed, recycled):
    recycled.extend(copy.copy(displayed))
    unique_list = list(dict.fromkeys(recycled))
    displayed.clear() 


def get4Outfits(outfits, displayed_outfits):
    #display 4 outfits, max 4
    outfits_size = len(outfits)
    print("possilbe outfits", outfits)
    length = min(outfits_size, 4)
    if len(outfits) == 1:
        outfit = pickAGoodOutfitRandomly(outfits)
        print(f"Selected single outfit: {outfit}")
        displayed_outfits.append(outfit)
    else:
        for i in range(length): # loop from 0 to 4
            outfit = pickAGoodOutfitRandomly(outfits)
            if not outfit:
                print('Warning: outfit is empty')
                return

            outfits.remove(outfit)
            displayed_outfits.append(outfit)

    return outfits, displayed_outfits




