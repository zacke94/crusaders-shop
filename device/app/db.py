import sqlite3
from .logger import logger_instance

def get_all_users():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_user_from_db(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT id, name FROM users WHERE id = {user_id}')
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result if result else None

def get_user_pin_code(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT pin_code FROM users WHERE id = {user_id}')
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None

def edit_pin_code(id, pin_code):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET pin_code = {pin_code} WHERE id = {id}')
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"User with ID {id} updated pin code successfully.")
    else:
        raise Exception(f"User with ID {id} failed update pin code.")


def add_users_to_db(users):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.executemany('''
        INSERT INTO users (name, pin_code)
        VALUES (:name, :pin_code)
    ''', users)
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Added users: {users} successfully:")
    else:
        raise Exception(f"Failed updating users: {users}.")

def delete_user_from_db(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM users WHERE id = {user_id}')
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"User {user_id} deleted successfully.")
    else:
        raise Exception(f"No user found with ID {user_id}.")

def get_admin_pin_code(pin_code):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT pin_code FROM admin_user WHERE pin_code = {pin_code}')
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None

def get_products_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def add_product_to_db(name, price):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Added product '{name}' with price '{price}' kr successfully.")
    else:
        raise Exception(f"Failed adding product '{name}' with price '{price}' kr.")

def edit_product_db(id, name, price, quantity):
    print(id)
    print(name)
    print(price)
    print(quantity)
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE products 
        SET name = ?, price = ?, quantity = ?
        WHERE id = ?
        ''', (name, price, quantity, id))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Product with ID {id} updated successfully.")
    else:
        raise Exception(f"Product with ID {id} failed update.")


def delete_products_from_db(id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM products WHERE id = {id}')
    connection.commit()

    if cursor.rowcount > 0:
        logger_instance.info(f"Product with {id} deleted successfully.")
    else:
        raise Exception(f"Failed to delete product with ID {id}.")

def add_order_to_db(id, products, total_price):
    new_order_id = _add_order(id, _get_customer_name(id))

    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    num_of_inserts = 0

    for product in products:
        cursor.execute('''
            INSERT INTO order_products (order_id, product_id, quantity, total_price)
            VALUES (?, ?, ?, ?) 
            ''', (new_order_id, product['id'], product['quantity'], product['total_price']))
        if cursor.rowcount > 0:
            num_of_inserts += 1
    
    if num_of_inserts == len(products):
        connection.commit()

        cursor.close()
        connection.close()
        logger_instance.info(f"Successfully added products: {products} to 'order_products'")
    else:
        raise Exception("Failed adding order_products")

def get_order_products_from_db(order_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('''
            SELECT op.order_id, p.id, p.name, op.quantity, op.total_price
            FROM order_products op
            JOIN products p on op.product_id = p.id
            WHERE op.order_id = (?)
        ''', (order_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result if result else None

def get_orders_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result if result else None

def get_orders_from_user_from_db(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM orders where customer_id = {user_id}")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result if result else None

def get_order_from_db(order_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result if result else None

def _get_customer_name(id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM users WHERE id = {id}")
    result = cursor.fetchone()
    connection.commit()
    connection.close()

    return result[0] if result else None
 
def _add_order(id, name):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO orders (customer_id, customer_name) VALUES (?, ?)
    ''', (id, name))
    
    new_id = cursor.lastrowid
    if new_id == None:
        cursor.close()
        connection.close()
        raise Exception(f"Failed adding order for (customer_id: {id}, customer_name: {name}).")

    connection.commit()
    
    cursor.close()
    connection.close()
    
    if cursor.rowcount > 0:
        logger_instance.info(f"Added order (customer_id: {id}, customer_name: {name}) to 'orders' successfully.")
        return new_id
    else:
        raise Exception(f"Failed adding order for (customer_id: {id}, customer_name: {name}).")
  