import os
import re
from flask import Flask, render_template, session, url_for, request, redirect, jsonify, flash
from orders.food_items import get_food_items, get_food_price, FOODS
from orders.cart import add_existing, check_existing, calculate_total, remove_food
from orders.order import Order
from orders.customer import Customer
from db.operations import add_order, add_customer, get_order_by_id, get_customer_by_id, custom_query, get_all_orders, get_all_customers, delete_order_by_id
from db.serialisation import serialise_order, serialise_customer

app = Flask(__name__)

# set secret key via environment variables

# Loads menu items from csv file at server startup
@app.before_first_request
def load_menu_items():
    get_food_items("food_items.csv")


# The home (menu) page of the web app
@app.route('/')
def menu():
    try:
        cart = session['cart']            # try to get cart from the existing session and calculate total
        total = calculate_total(session)
    except:                               # the except block will run if the cart does not exist
        session['cart'] = []              # therefore, create an empty cart and set the total to 0
        cart = session['cart']
        total = 0.0
    return render_template("menu.html", title="Menu", categories=FOODS.keys(), foods=FOODS, total=total, cart=cart)
    
    
# Handles the "Add to Cart" button click
@app.route('/add', methods=['POST'])
def add_item():
    
    item_name = request.form['food']        # get the item_name and quantity from the form
    quantity = request.form['quantity']
    price = get_food_price(item_name)       # gets the unit price of the item by querying the dictionary structure

    try:
        if check_existing(item_name, session):            # check if the item is already in the cart
            add_existing(item_name, quantity, session)    # update quantity of existing item
        else:
            session['cart'].append((item_name, quantity, price))   # if not already in cart, simply add it
        session.modified = True
    except:
        session['cart'] = []
    
    return redirect(url_for("menu"))   # redirect to menu page


# Handles the "Remove" button click for the items in the cart
@app.route('/remove', methods=['POST'])
def remove_item():
    
    item_name = request.form['food']        # get the item name from the form
    try:
        remove_food(item_name, session)     # remove the item from the cart
        session.modified = True
    except:
        session['cart'] = []
    
    return redirect(url_for("menu"))   # redirect to menu page


# The checkout page of the website
@app.route('/checkout')
def checkout():
    
    try:                            # try block to check for session existing
        cart = session['cart']
        # if the cart is empty, checkout is not allowed, so redirect to menu
        if cart == []:
            return redirect(url_for("menu"))
            
        total = calculate_total(session)
        return render_template("checkout.html", title="Checkout", total=total, cart=cart)
    except:
        return redirect(url_for("menu"))   # redirect to menu page

    
# Handles the checkout once the form is submitted
@app.route('/process-checkout', methods=['POST'])
def process_checkout():

    cart = session['cart']
    
    if session['cart'] != []:    # if cart is not empty, proceed, otherwise, redirect back to menu
        session['cart'] = []     # reset the cart 
        custFirstName = request.form['firstName']        # get all the customer's data from the form
        custSurname = request.form['surname']
        custTelephone = request.form['contactNumber']
        category = request.form['category']
        
        
        newCustomer = Customer(custFirstName, custSurname, custTelephone)    # create customer object from data
        newOrder = Order(cart, category, newCustomer.id)                     # create order object


        print("New order ID: " + newOrder.id)
        
        # commits the new order and customer to the database
        add_order(newOrder)
        add_customer(newCustomer)
        
        errors = validate_form(custFirstName, custSurname, custTelephone)
        if not errors:
            return render_template('confirmation.html', title='Order Confirmed', order_id=newOrder.id)
        else:
            for e in errors:
                flash(e)
            session['cart'] = cart   # get current cart and reload it into session
            return redirect(url_for("checkout"))
    else:
        return redirect(url_for("menu"))
    

# validate form and return any errors
def validate_form(name, surname, telephone):
    
    errors = []
    
    if len(name) > 30 or len(name.replace(" ", "")) == 0:
        errors.append("Invalid First Name")
    
    if len(surname) > 35 or len(surname.replace(" ", "")) == 0:
        errors.append("Invalid Surname")

    if not re.match("^((\+44\s?\d{4}|\(?\d{5}\)?)\s?\d{6})|((\+44\s?|0)7\d{3}\s?\d{6})$", telephone):
        errors.append("Invalid Telephone Number")
        
    return errors
    

    
################ REST API CODE ####################

# return json data for order given its id
@app.route('/orders/<order_id>')
def get_order(order_id):
    try:
        order = get_order_by_id(order_id)[0]
        data = serialise_order(order)
        return jsonify(data)
    except:
        return jsonify({"data": "Invalid request/error occured"})


# return json data for all orders
@app.route('/orders/all/<limit>')
def get_orders(limit):
    try:
        limit = int(limit)                       # convert limit to numeric value
        orders = get_all_orders(limit)
        data = []
        for o in orders:
            data.append(serialise_order(o))
        return jsonify(data)
    except:
        return jsonify({"data": "Invalid request/error occured"})


# return json data for customer given its id
@app.route('/customers/<customer_id>')
def get_customer(customer_id):
    try:
        customer = get_customer_by_id(customer_id)[0]
        data = serialise_customer(customer)
        return jsonify(data)
    except:
        return jsonify({"data": "Invalid request/error occured"})


# return json data for all customers up to a certain number
@app.route('/customers/all/<limit>')
def get_customers(limit):
    try:
        limit = int(limit)                       # convert limit to numeric value
        customers = get_all_customers(limit)
        data = []
        for c in customers:
            data.append(serialise_customer(c))
        return jsonify(data)
    except:
        return jsonify({"data": "Invalid request/error occured"})
        
        
# delete order based on the order id
@app.route('/orders/delete/', methods=['POST'])
def delete_order():
    try:
        data = request.get_json()   # get the json data
        delete_order_by_id(data["id"])      # call the database operation
        return jsonify({"data": "Success"})
    except:
        return jsonify({"data": "Invalid request/error occured"})


# 2nd iteration        
@app.route('/orders/create/', methods=['POST'])
def create_order_and_customer():
    try:
        data = request.get_json()
        data["contents"] = eval(data["contents"].replace("'","\"").replace("[\"", "[").replace("]\"", "]").replace("Item1", "name").replace("Item2", "quantity").replace("Item3", "price"))
        
        contents = []
        for food in data["contents"]:
            contents.append((food["name"], food["quantity"], food["price"]))
        
        # create customer object from data
        newCustomer = Customer(data["firstName"], data["surname"], 
                                data["telephone"], data["customerID"])    
        
        
        # create order object from data
        newOrder = Order(contents, data["category"], data["customerID"], 
                        data["orderID"], data["timestamp"])                     

        add_order(newOrder)
        add_customer(newCustomer)
        
        return jsonify({"data": "Success"})
    except:
        return jsonify({"data": "Invalid request/error occured"})


# query the database using a custom query
@app.route('/orders/query/', methods=['POST'])
def query_database():
    try:
        data = request.get_json()  
        orders = custom_query(data["query"])  # get orders
        print(data["query"])
        response = []
        for o in orders:
            response.append(serialise_order(o))  # serialise orders
        return jsonify(response)
    except:
        return jsonify({"data": "Invalid request/error occured"})
        

############# CUSTOM TEMPLATE FILTERS ###############

# a template filter to convert food names to lowercase and remove spaces for IDs in HTML tags
@app.template_filter()
def lower_strip(food): 
    return food.lower().replace(' ', '')


# a template filter to show 2 decimals for the price
@app.template_filter()
def price_format(total): 
    return "%.2f" % total


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
