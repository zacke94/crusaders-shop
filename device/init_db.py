import sqlite3

connection = sqlite3.connect('crusaders-shop.db')

with open('sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO admin_user (pin_code) VALUES (?)", (941022,))
connection.commit()
connection.close()