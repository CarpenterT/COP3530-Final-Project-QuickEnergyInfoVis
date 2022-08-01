# -*- coding: utf-8 -*-
"""
This file contains many static details and some functions for the main program.
Some of these lists are redundant or very similar to others. This was necessary because of the
format of the data from CORGIS. You may notice, for example, that the USstates list is not
in alphabetical order. This is because the CORGIS data is the same way, and I had to modify
things on this end to make it fit.
"""
#this function allows the main program to pass in a name from the user-selected input
#and get a list from the dictionary
def getList(name):
    return listOfLists.get(name)

abrevYearMap = {}
abrevYears = []
def mapAbrevYears(sortedYears):
    abrevYearMap.clear()
    abrevYears.clear()
    for x in range(len(yearRange3)):
        abrevYearMap[yearRange2[x]] = yearRange3[x]
    for x in range(len(sortedYears)):
        abrevYears.append(abrevYearMap[sortedYears[x]])

yearRange = ["None",1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,
1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,
1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,
2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]


yearRange2 = [1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,
1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,
1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,
2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]

yearRange3 = ["'60","'61","'62","'63","'64","'65","'66","'67","'68","'69","'70",
"'71","'72","'73","'74","'75","'76","'77","'78","'79","'80","'81","'82","'83","'84","'85","'86",
"'87","'88","'89","'90","'91","'92","'93","'94","'95","'96","'97","'98","'99","'00","'01","'02","'03","'04",
"'05","'06","'07","'08","'09","'10","'11","'12","'13","'14","'15","'16","'17","'18","'19"]


#List of all US states
USstates = ["Alaska","Alabama","Arkansas","Arizona","California","Colorado",
  "Connecticut", "District of Columbia","Delaware","Florida","Georgia","Hawaii","Iowa","Idaho",
  "Illinois","Indiana","Kansas","Kentucky","Louisiana","Massachusetts","Maryland",
  "Maine","Michigan","Minnesota","Missouri","Mississippi","Montana",
  "North Carolina","North Dakota","Nebraska","New Hampshire","New Jersey","New Mexico",
  "Nevada","New York","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Virginia","Vermont","Washington","Wisconsin","West Virginia","Wyoming"]

USstatesAbrev = ["AK","AL","AR","AZ","CA","CO",
  "CT", "DC","DE","FL","GA","HI","IA","ID",
  "IL","IN","KS","KY","LA","MA","MD",
  "ME","MI","MN","MO","MS","MT",
  "NC","ND","NE","NH","NJ","NM",
  "NV","NY","OH","OK","OR","PA",
  "RI","SC","SD","TN","TX","UT",
  "VA","VT","WA","WI","WV","WY"]

statesToInt = {}
yearsToIndex = {}
for x in range(0, len(USstates)):
    statesToInt[USstates[x]] = x
for x in range(1, len(yearRange)):
    yearsToIndex[yearRange[x]] = x

#this empty list is for initializing the gui
blankList = []

#the following is a dictionary of all the necessary lists of names
listOfLists = { 
    "Category1" : ["Consumption", "Expenditure", "Price"], 
    
    "ConsumptionSubCats" : ["Commercial", "Electric Power", "Industrial", "Transportation", "Residential", "Refinery"],
    
    "ExpenditureSubCats" : ["Commercial", "Electric Power", "Industrial", "Transportation", "Residential"],

    "PriceSubCats" : ["Commercial", "Electric Power", "Industrial", "Transportation"],

    "Consumption_Commercial" : ["Coal", "Distillate Fuel Oil", "Geothermal", "Hydropower", "Kerosene", "Petroleum",
                              "Natural Gas", "Solar", "Wind", "Wood"],

    "Consumption_Electric Power" : ["Coal", "Distillate Fuel Oil", "Natural Gas", "Wood"],

    "Consumption_Industrial" : ["Coal", "Distillate Fuel Oil", "Geothermal", "Hydropower", "Kerosene", "Petroleum",
                              "Natural Gas", "Other Petroleum Products", "Solar", "Wind", "Wood"],

    "Consumption_Refinery" : ["Coal", "Distillate Fuel Oil", "Natural Gas"],

    "Consumption_Residential" : ["Coal", "Distillate Fuel Oil", "Geothermal", "Kerosene", "Petroleum",
                              "Natural Gas", "Wood"],

    "Consumption_Transportation" : ["Coal", "Distillate Fuel Oil", "Petroleum", "Natural Gas"],

    "Expenditure_Commercial" : ["Coal", "Distillate Fuel Oil", "Kerosene", "Petroleum", "Natural Gas"],

    "Expenditure_Electric Power" : ["Coal", "Distillate Fuel Oil", "Natural Gas"],

    "Expenditure_Industrial" : ["Coal", "Distillate Fuel Oil", "Kerosene", "Petroleum", "Natural Gas", "Other Petroleum Products"],

    "Expenditure_Residential" : ["Coal", "Distillate Fuel Oil", "Kerosene", "Petroleum", "Natural Gas", "Wood"],

    "Expenditure_Transportation" : ["Coal", "Distillate Fuel Oil", "Petroleum", "Natural Gas"],

    "Price_Commercial" : ["Coal", "Distillate Fuel Oil", "Kerosene", "Petroleum", "Natural Gas"],

    "Price_Electric Power" : ["Coal", "Distillate Fuel Oil", "Natural Gas"],

    "Price_Industrial" : ["Coal", "Distillate Fuel Oil", "Kerosene", "Petroleum", "Natural Gas", "Other Petroleum Products"],

    "Price_Transportation" : ["Coal", "Distillate Fuel Oil", "Petroleum", "Natural Gas"],
    "Sorting_Algos" : ["None", "MergeSort", "QuickSort", "TimSort", "All"]
    }

numRange = [
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,
28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]

numRange2 = [
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,
28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,
52,53,54,55,56,57,58,59,60]


























