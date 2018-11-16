import ast

def serialise_order(order):
    so = {
        "orderID": order[0],
        "timestamp": str(order[1]),
        "customerID": order[4],
        "category": order[3],
        "contents": []
    }
    
    contents = ast.literal_eval(order[2])   # parse text blob into list
    
    for item in contents:
        so["contents"].append( {"name": item[0], "quantity": int(item[1]), "price": float(item[2])} )
    
    return so
    

def serialise_customer(customer):
    sc = {
        "customerID": customer[0],
        "firstName": customer[1],
        "surname": customer[2],
        "telephone": customer[3]
    }
    
    return sc
    
    
    