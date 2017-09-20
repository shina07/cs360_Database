import sqlite3
from flask import g

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('auctionDB.db') #TODO: add your SQLite database filename
        db.row_factory = sqlite3.Row
    return db

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    get_db().execute('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return get_db().transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except:
#     t.rollback()
#     raise
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select Time from CurrentTime'
    results = query(query_string, one=True)
    # print(results)
    # alternatively: return results[0]['currenttime']
    return results['Time'] # TODO: update this as well to match the column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id}, one = True)
    return result

# helper method to determine whether query result is empty
# Sample use:
# query_result = sqlitedb.query('select currenttime from Time')
# if (sqlitedb.isResultEmpty(query_result)):
#   print 'No results found'
# else:
#   .....
#
# NOTE: this will consume the first row in the table of results,
# which means that data will no longer be available to you.
# You must re-query in order to retrieve the full table of results
def isResultEmpty(result):
    try:
        result[0]
        return False
    except:
        return True

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}, one=False):
    cur = get_db().execute(query_string, vars)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time

def setTime(time):
    query_string = "update CurrentTime set Time = $selected_time"
    query(query_string, {'selected_time' : time})
    return

def getUserById(user_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Users where UserID = $userID'
    result = query(query_string, {'userID': user_id}, one = True)
    return result

def setItemEndTime(item_id, time):
    query_string = "update Items set Ends = $end_time where ItemID = $itemID"
    query(query_string, {'end_time' : time, 'itemID' : item_id })
    return

def addBid(user_id, price, time, item_id):
    query_string = "insert into Bids (UserID, Amount, Time, ItemID) values ($userID, $amount, $time, $itemID)"
    query(query_string, {'userID' : user_id, 'amount' : price, 'time' : time, 'itemID' : item_id })
    return

def getItems(item_id = '', category = '', description = '', price = '', status = 'all'):
    query_string = "select * from Items"

    if (item_id != '') or (category != '') or (description != '') or (price != '') or (status != 'all'):
        query_string += " where "

    if (item_id != ''):
        query_string += "ItemID = " + item_id

    if (category != ''):
        if (item_id != ''):
            query_string += " AND "

        query_string += "EXISTS (select * from Categories where ItemID = %s and Category = %s)" %(item_id, category)

    if (description != ''):
        if (item_id != '') or (category != ''):
            query_string += " AND "

        query_string += "Description LIKE %%%s%%" %description

    if (price != ''):
        if (item_id != '') or (category != '') or (description != ''):
            query_string += " AND "

        query_string += "Price = " + price

    if (status != 'all'):
        if (item_id != '') or (category != '') or (description != '') or (price != ''):
            query_string += " AND "

        if status == 'open':
            query_string += 'Ends >= (select Time from CurrentTime) and Started <= (select Time from CurrentTime)'
        
        elif status == 'close':
            query_string += 'Ends < (select Time from CurrentTime)'
        
        elif status == 'notStarted':
            query_string += 'Started > (select Time from CurrentTime)'

    print query_string
    result = query(query_string)
    return result
