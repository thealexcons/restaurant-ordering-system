
# updates the quantity of an item     
def add_existing(food_name, quantity, sesh):
    for idx, item in enumerate(sesh['cart']):
        if food_name == item[0]:
            sesh['cart'][idx] = (item[0], str(int(item[1]) + int(quantity)), item[2])
 
# checks if an added item is already in the cart, works along add_existing()           
def check_existing(food_name, sesh):
    for item in sesh['cart']:
        if food_name == item[0]:
            return True
    return False

# calculates total price from items in cart
def calculate_total(sesh):
    total = 0
    for item in sesh['cart']:
        total = total + float(item[2]) * float(item[1])   # multiplies price of item by its quantity
    return total
    
# removes an item from the cart
def remove_food(food_name, sesh):
    for idx, item in enumerate(sesh['cart']):
        if food_name == item[0]:
            del sesh['cart'][idx]              # delete item from dictionary
            return                             # stop
        

    
    
    