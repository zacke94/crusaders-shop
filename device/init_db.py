import sqlite3

connection = sqlite3.connect('crusaders-shop.db')

with open('sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Adam Erlandsson', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", ('Markus Österberg', 1111))
cur.execute("INSERT INTO admin_user (pin_code) VALUES (?)", (941022,))
cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", ('Läsk', 15))
cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", ('Nocco', 25))
cur.execute("INSERT INTO orders (customer_name, customer_id) VALUES (?, ?)", ('Adam Erlandsson', 1))
cur.execute('''
    INSERT INTO order_products (order_id, product_id, quantity, total_price)
    VALUES (?, ?, ?, ?) 
    ''', (1, 1, 2, 50))
cur.execute('''
    INSERT INTO order_products (order_id, product_id, quantity, total_price)
    VALUES (?, ?, ?, ?) 
    ''', (1, 2, 1, 15))

cur.execute("INSERT INTO orders (customer_name, customer_id) VALUES (?, ?)", ('Markus Österberg', 2))
cur.execute('''
    INSERT INTO order_products (order_id, product_id, quantity, total_price)
    VALUES (?, ?, ?, ?) 
    ''', (2, 1, 2, 50))
cur.execute('''
    INSERT INTO order_products (order_id, product_id, quantity, total_price)
    VALUES (?, ?, ?, ?) 
    ''', (2, 2, 1, 15))

connection.commit()
connection.close()