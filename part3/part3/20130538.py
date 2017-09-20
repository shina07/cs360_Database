
"""
FILE: skeleton_parser.py
------------------
Author: 
Modified: 

Skeleton parser for CS360 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys, os
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def transformDatFormat(*args):
    #print("args length: %d input: %s  type: %s" %(len(args), args, type(args)))
    result = ""
    for i in range(len(args)):
        if i != (len(args) - 1):
            result += "\"" + args[i].replace("\"", "\"\"") + "\"" + columnSeparator
        else:
            result += "\"" + args[i].replace("\"", "\"\"") + "\"" + "\n"

    return result

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        itemCollections = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        users = open("users.dat", "a")
        items = open("items.dat", "a")
        bids = open("bids.dat", "a")
        categories = open("categories.dat", "a")

        for item in itemCollections:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            #pass
            #print(items[item][0])
            for entry in itemCollections[item]:

                buyPriceEntry = ""
                descriptionEntry = ""

                locationEntry = ""
                countryEntry = ""
                ratingEntry = ""

                if ("Buy_Price" not in entry or (entry["Buy_Price"] is None)):
                    buyPriceEntry = "NULL"
                else:
                    buyPriceEntry = transformDollar(entry["Buy_Price"])

                if ("Description" not in entry or (entry["Description"] is None)):
                    descriptionEntry = "NULL"
                else:
                    descriptionEntry = entry["Description"]

                items.write(transformDatFormat(entry["_ItemID"], entry["Name"], transformDollar(entry["Currently"]), 
                    buyPriceEntry, transformDollar(entry["First_Bid"]), entry["Number_of_Bids"], transformDttm(entry["Started"]), 
                    transformDttm(entry["Ends"]), descriptionEntry, entry["Seller"]["_UserID"]))

                users.write(transformDatFormat(entry["Seller"]["_UserID"], entry["Location"], 
                    entry["Country"], entry["Seller"]["_Rating"]))

                if (entry["Number_of_Bids"] != "0"):
                    for bid in entry["Bids"]:
                        for bidEntry in entry["Bids"][bid]:

                            bids.write(transformDatFormat(bidEntry["Bidder"]["_UserID"], transformDollar(bidEntry["Amount"]), 
                                transformDttm(bidEntry["Time"]), entry["_ItemID"]))

                            if ("Location" not in bidEntry["Bidder"] or (bidEntry["Bidder"]["Location"] is None)):
                                locationEntry = "NULL"
                            else:
                                locationEntry = bidEntry["Bidder"]["Location"]

                            if ("Country" not in bidEntry["Bidder"] or (bidEntry["Bidder"]["Country"] is None)):
                                countryEntry = "NULL"
                            else:
                                countryEntry = bidEntry["Bidder"]["Country"]

                            if ("_Rating" not in bidEntry["Bidder"] or (bidEntry["Bidder"]["_Rating"] is None)):
                                ratingEntry = "NULL"
                            else:
                                ratingEntry = bidEntry["Bidder"]["_Rating"]

                            users.write(transformDatFormat(bidEntry["Bidder"]["_UserID"], locationEntry, 
                                countryEntry, ratingEntry))


                for category in entry["Category"]:
                   categories.write(transformDatFormat(entry["_ItemID"], category))

        users.close()
        items.close()
        bids.close()
        categories.close()

def removeOldFiles():
    try:
        os.system("rm -rf *.dat\n")
    except Exception:
        print("REMOVE OLD FILE EXCEPTION")

def sortAndDeleteDuplicate():
    try:
        os.system("sort users.dat | uniq > user_table.dat\n")
        os.system("sort items.dat | uniq > item_table.dat\n")
        os.system("sort bids.dat | uniq > bid_table.dat\n")
        os.system("sort categories.dat | uniq > category_table.dat\n")
    except Exception:
        print("SORT AND DELETE DUPLICATE EXCEPTION");

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):

    removeOldFiles();

    if len(argv) < 2:
        sys.stderr.write('Usage: python skeleton_json_parser.py <path to json files>\n')
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

    sortAndDeleteDuplicate()

if __name__ == '__main__':
    main(sys.argv)
