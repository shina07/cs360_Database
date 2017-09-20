import sys

from flask import Flask
from flask import request
from flask import render_template

import sqlitedb
from datetime import datetime

app = Flask(__name__)

"""""""""""""""""""""""""""""""""""""""""""""""""""
!!!!!DO NOT CHANGE ANYTHING ABOVE THIS LINE!!!!!
"""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""
BEGIN HELPER METHODS
"""""""""""""""""""""""""""""""""""""""""""""""""""


def string_to_time(date_str):
    """Helper method to convert times from database (which will return a string) into datetime objects.

    This will allow you to compare times correctly (using # ==, !=, <, >, etc.) instead of
    lexicographically as strings.

    >>> current_time = string_to_time(sqlitedb.getTime())
    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


"""""""""""""""""""""""""""""""""""""""""""""""""""
END HELPER METHODS
"""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/currtime', methods=['GET'])
def get_curr_time():
    """A simple GET request, to '/currtime'.

    Notice that we pass in `current_time' to our `render_template' call
    in order to have its value displayed on the web page
    """
    current_time = sqlitedb.getTime()
    return render_template('curr_time.html', time=current_time)


@app.route('/selecttime', methods=['GET', 'POST'])
def select_time():
    if request.method == 'POST':
        # A POST request
        #
        # You can fetch the parameters passed to the URL
        # by calling `request.form' for POST requests
        post_params = request.form
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss']
        enter_name = post_params['entername']

        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        # TODO: save the selected time as the current time in the database

        sqlitedb.setTime(selected_time)
        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)
    else:
        return render_template('select_time.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""
IMPLEMENT OTHER FEATURES IN HERE
"""""""""""""""""""""""""""""""""""""""""""""""""""
@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return render_template("index.html")


@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':

        post_params = request.form
        itemID = post_params["itemID"]
        category = post_params["category"]
        description = post_params["description"]
        price = post_params["price"]
        status = post_params["status"]
        #print post_params
        results = sqlitedb.getItems(itemID, category, description, price, status)

        return render_template('search.html', results = results)
    else:
        return render_template('search.html')

@app.route('/add_bid', methods = ['GET', 'POST'])
def add_bid():
    if request.method == 'POST':

        post_params = request.form
        itemID = post_params["itemID"]
        userID = post_params["userID"]
        price = post_params["price"]
        current_time = sqlitedb.getTime()

        if (itemID == '') or (userID == '') or (price == ''):
            return render_template('add_bid.html', add_result = False, message = "Not all field is filled")

        item = sqlitedb.getItemById(itemID)
        print item[7]

        if (item == None):
            return render_template('add_bid.html', add_result = False, message = "Cannot find item")

        if (string_to_time(item[7]) <= string_to_time(current_time)):
            return render_template('add_bid.html', add_result = False, message = "The auction is already Closed")

        user = sqlitedb.getUserById(userID)

        if (user == None):
            return render_template('add_bid.html', add_result = False, message = "Cannot find user")

        if float(price) <= float(item[2]):
            return render_template('add_bid.html', add_result = False, message = "Price is Lower than current price")

        sqlitedb.addBid(userID, price, current_time, itemID)

        return render_template('add_bid.html', add_result = True, message = "Add Bid Successful")
    else:
        return render_template('add_bid.html')

"""""""""""""""""""""""""""""""""""""""""""""""""""
!!!!!DO NOT CHANGE ANYTHING ABOVE THIS LINE!!!!!
"""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == '__main__':
    port = 5000 if len(sys.argv) == 1 else int(sys.argv[1])
    app.run(host = "0.0.0.0", port = port, debug = True)
