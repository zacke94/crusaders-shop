import sqlite3

connection = sqlite3.connect('crusaders-shop.db')


with open('sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, pin_code, admin) VALUES (?, ?, ?)",
            ('Adam Erlandsson', 1111, True)
            )

cur.execute("INSERT INTO users (name, pin_code, admin) VALUES (?, ?, ?)",
            ('Markus Österberg', 1111, False)
            )

connection.commit()
connection.close()