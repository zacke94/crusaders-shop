import sqlite3
from .logger import logger_instance

def get_active_users_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name FROM users WHERE is_active = 1')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_all_users_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, is_active FROM users ORDER BY name ASC')
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

def inactive_user_from_db(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET is_active = 0 WHERE id = {user_id}')
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Inactivated user with ID {user_id} updated successfully.")
    else:
        raise Exception(f"Failed to inactive user with id {user_id}.")

def active_user_from_db(user_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET is_active = 1 WHERE id = {user_id}')
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Activated user with ID {user_id} updated successfully.")
    else:
        raise Exception(f"Failed to active user with id {user_id}.")

def get_admin_pin_code(pin_code):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT pin_code FROM admin_user WHERE pin_code = {pin_code}')
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None

def get_eligible_products_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, price, quantity FROM products WHERE show_product = 1 ORDER BY name ASC')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def get_all_products_from_db():
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def hide_product_from_db(id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE products SET show_product = 0 WHERE id = {id}')
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Hid product with ID {id} successfully.")
    else:
        raise Exception(f"Failed to hide product with id {id}.")

def show_product_from_db(id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE products SET show_product = 1 WHERE id = {id}')
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        logger_instance.info(f"Shown product with ID {id} successfully.")
    else:
        raise Exception(f"Failed to hide product with id {id}.")

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

def delete_order_from_db(order_id):
    try:
        connection = sqlite3.connect('crusaders-shop.db')
        connection.execute("BEGIN TRANSACTION;")

        connection.execute(f'DELETE FROM orders WHERE id = {order_id}')
        connection.execute(f'DELETE FROM order_products WHERE order_id = {order_id}')
        connection.commit()

    except sqlite3.Error as e:
        connection.rollback()
        connection.close()
        raise Exception(f"Failed to delete order with ID {order_id}.")
    
    finally:
        logger_instance.info(f"Order with {order_id} deleted successfully.")
        connection.close()

def add_order_to_db(id, products, total_price):
    product_quantity = _quantity_is_correct(products)
    
    if product_quantity > 0:
        raise Exception(f"Quantity of product '{product_quantity}' is not enough")

    new_order_id = _add_order(id, _get_customer_name(id))

    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    num_of_inserts = 0

    for product in products:
        edit_product_quanity = _edit_product_quanity(connection, product['id'], product['quantity'])
        if edit_product_quanity == 0:
            raise Exception(f"Failed to update quantity of product with id {product['id']}")

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
        return new_order_id
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

def _quantity_is_correct(products): 
    for product in products:
        product_quantity = _get_product_quantity(product['id'])

        if product_quantity is None or product_quantity < product['quantity']:
            return product['id']
    return 0

def _get_product_quantity(product_id):
    connection = sqlite3.connect('crusaders-shop.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT quantity FROM products WHERE id = {product_id}")
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result[0] if result else None

def _edit_product_quanity(connection, product_id, quantity):
    cursor = connection.cursor()
    cursor.execute(f'UPDATE products SET quantity = quantity - {quantity} WHERE id = {product_id}')
    connection.commit()

    if cursor.rowcount > 0:
        logger_instance.info(f"Quantity of product with ID {product_id} updated successfully.")
    return cursor.rowcount