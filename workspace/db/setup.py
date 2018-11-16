import sqlite3

conn = sqlite3.connect('database.db')  # creates the file for the database

# SQL queries 
create_customers = "CREATE TABLE customers (id INTEGER PRIMARY KEY, firstName TEXT, surname TEXT, telephone VARCHAR(15))"
create_orders = "CREATE TABLE orders (id INTEGER PRIMARY KEY, timestamp NUMERIC, contents BLOB, category TEXT, customerID INTEGER, FOREIGN KEY(customerId) REFERENCES customer(id))"


# create the customers and orders table in the database
conn.execute(create_customers)
conn.execute(create_orders)
conn.close()


