import sqlite3
import json

connection = sqlite3.connect('crusaders-shop.db')

with open('sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO admin_user (pin_code) VALUES (?)", (941022,))

cur.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", ('Cola (vanlig)', 15, 8))
cur.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", ('Powerade', 25, 6))
cur.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", ('Kexchoklad', 15, 7))

with open('users.json', 'r') as file:
    users = json.load(file)
    for user in users['data']:
        cur.execute("INSERT INTO users (name, pin_code) VALUES (?, ?)", (user['name'], user['pin_code']))

connection.commit()
connection.close()