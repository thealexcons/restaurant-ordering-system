import csv
from collections import OrderedDict

# constant global variable data structure
FOODS = OrderedDict([('Express Lunch', []), ('Panini', []), ('Vegetarian Wraps', []), 
                     ('Meat Wraps', []), ('Side Orders', []), ('Cold Drinks', []),
                     ('Hot Drinks', []), ('Smoothies', [])])
                     
# use OrderedDict because when looping over a standard dict in python, order of definition is not conserved

# Load food items from csv file into python dictionary
def get_food_items(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == "EXPRESS LUNCH":
                FOODS["Express Lunch"].append((row[0], row[2], row[3]))
            elif row[1] == "PANINI":
                FOODS["Panini"].append((row[0], row[2], row[3]))
            elif row[1] == "VEGETARIAN WRAPS":
                FOODS["Vegetarian Wraps"].append((row[0], row[2], row[3]))
            elif row[1] == "MEAT WRAPS":
                FOODS["Meat Wraps"].append((row[0], row[2], row[3]))
            elif row[1] == "SIDE ORDERS":
                FOODS["Side Orders"].append((row[0], row[2], row[3]))
            elif row[1] == "HOT DRINKS":
                FOODS["Hot Drinks"].append((row[0], row[2], row[3]))
            elif row[1] == "COLD DRINKS":
                FOODS["Cold Drinks"].append((row[0], row[2], row[3]))
            elif row[1] == "SMOOTHIES":
                FOODS["Smoothies"].append((row[0], row[2], row[3]))
                

# gets the price of the food given the food name             
def get_food_price(food_name):
    categories = FOODS.keys()
    for category in categories:       # loop through every item and get its price based on the item name
        for item in FOODS[category]:
            if item[0] == food_name:     
                return item[2]
            