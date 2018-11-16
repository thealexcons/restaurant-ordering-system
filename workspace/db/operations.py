import sqlite3

def add_order(orderObject):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (id, timestamp, contents, category, customerId) VALUES (?,?,?,?,?)",
                (orderObject.id, orderObject.timestamp, str(orderObject.contents), orderObject.category, orderObject.customerId))
    conn.commit()
    conn.close()

    
def add_customer(custObject):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (id, firstName, surname, telephone) VALUES (?,?,?,?)",
                 (custObject.id, custObject.firstName, custObject.surname, custObject.telephone))
    conn.commit()
    conn.close()
    

def get_order_by_id(order_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    order = tuple(cur.execute('SELECT * FROM orders WHERE id=?', (order_id,)))
    conn.close()
    return order

  
def get_customer_by_id(customer_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cust = tuple(cur.execute('SELECT * FROM customers WHERE id=?', (customer_id,)))
    conn.close()
    return cust    
    
    
def get_all_orders(limit):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    orders = []
    for order in cur.execute('SELECT * FROM orders ORDER BY -timestamp LIMIT ?', (limit,)):  # most recent first
        orders.append(tuple(order))
    conn.close()
    return orders
    
def get_all_customers(limit):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    custs = []
    for cust in cur.execute('SELECT * FROM customers LIMIT ?', (limit,)):
        custs.append(tuple(cust))
    conn.close()
    return custs    
    
def delete_order_by_id(order_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('delete from orders where id=(?)', (order_id,))
    conn.commit()
    conn.close()
    
    
def custom_query(sql):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    orders = []
    for order in cur.execute(sql):    # execute the custom sql query
        print(order)
        orders.append(tuple(order))   # add orders to list
    conn.close()
    return orders
    
    
    