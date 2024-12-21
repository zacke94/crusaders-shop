from flask import jsonify, request, current_app
from .db import *
from .camera import record
from .electro_magnet import electro_magnet_instance
from .logger import logger_instance

@current_app.route('/active-users', methods=['GET'])
def get_active_users():
    try:
        users = get_active_users_from_db()
        user_list = [{'id': user[0], 'name': user[1]} for user in users]
        return jsonify({'users': user_list})
    except Exception as e:
        logger_instance.error(f"Error in '/active-users': {e}")
        return "Something went wrong", 500

@current_app.route('/all-users', methods=['GET'])
def get_all_users():
    try:
        users = get_all_users_from_db()
        user_list = [{'id': user[0], 'name': user[1], 'isActive': bool(user[2])} for user in users]
        return jsonify({'users': user_list})
    except Exception as e:
        logger_instance.error(f"Error in '/all-users': {e}")
        return "Something went wrong", 500

@current_app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_from_db(user_id)
        return jsonify({"id": user[0], "name": user[1]})
    except Exception as e:
        logger_instance.error(f"Error in '/user/{user_id}': {e}")
        return "Something went wrong", 500

@current_app.route('/add-users', methods=['POST'])
def add_users():
    try:
        adjusted_column_name = [{'name': user['name'], 'pin_code': user['pinCode']} for user in request.json]
        add_users_to_db(adjusted_column_name)
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Could not add users: {e}")
        return "Something went wrong", 500

@current_app.route('/inactivate-user/<user_id>', methods=['PUT'])
def inactive_user(user_id):
    try:
        inactive_user_from_db(user_id)
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/inactivate-user/{user_id}': {e}")
        return "Something went wrong", 500

@current_app.route('/activate-user/<user_id>', methods=['PUT'])
def active_user(user_id):
    try:
        active_user_from_db(user_id)
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/activate-user/{user_id}': {e}")
        return "Something went wrong", 500

@current_app.route('/change-pin-code', methods=['PUT'])
def change_pin_code():
    try:
        edit_pin_code(request.json['id'], request.json['pinCode'])
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/change-pin-code': {e}")
        return "Something went wrong", 500

@current_app.route('/login-user', methods=['POST'])
def login():
    try:
        request_data = request.json

        if get_user_pin_code(request_data['id']) == int(request_data['pinCode']):
            return "Success", 200
        else:
            return "Unauthorized", 401
    except Exception as e:
        logger_instance.error(f"Error in '/login-user': {e}")
        return "Something went wrong", 500

@current_app.route('/login-admin', methods=['POST'])
def login_admin():
    try:
        request_data = request.json
    
        if get_admin_pin_code(request_data['pinCode']) == int(request_data['pinCode']):
            return "Success", 200
        else:
            return "Unauthorized", 401
    except Exception as e:
        logger_instance.error(f"Error in '/login-admin': {e}")
        return "Something went wrong", 500

@current_app.route('/products', methods=['GET'])
def get_products():
    try:
        products = [{'id': product[0], 'name': product[1], 'price': product[2], 'quantity': product[3]} 
            for product in get_products_from_db()]
        return jsonify({'products': products})
    except Exception as e:
        logger_instance.error(f"Error in '/products': {e}")
        return "Something went wrong", 500

@current_app.route('/add-product', methods=['POST'])
def add_product():
    try:
        add_product_to_db(request.json['name'], request.json['price'])
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/add-product': {e}")
        return "Something went wrong", 500

@current_app.route('/edit-product', methods=['PUT'])
def edit_product():
    try:
        edit_product_db(request.json['id'], request.json['name'], request.json['price'], request.json['quantity'])
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/edit-product': {e}")
        return "Something went wrong", 500

@current_app.route('/delete-product/<id>', methods=['DELETE'])
def delete_products(id):
    try:
        delete_products_from_db(id)
        return "Success", 200
    except Exception as e:
        logger_instance.error(f"Error in '/delete-product/{id}': {e}")
        return "Something went wrong", 500

@current_app.route('/add-order', methods=['POST'])
def add_order():
    try:
        adjusted_column_name = [{
            'id': product['id'], 
            'name': product['name'], 
            'price': product['price'],
            'quantity': product['quantity'],
            'total_price': product['totalPrice']
            } for product in request.json['products']
        ]
        customer_id = request.json['customerId']
        total_price = request.json['totalPrice']
        order_id = add_order_to_db(customer_id, adjusted_column_name, total_price)
        return jsonify({'orderId': order_id})
    except Exception as e:
        logger_instance.error(f"Error in '/add-order': {e}")
        return "Something went wrong", 500
    
@current_app.route('/get-orders', methods=['GET'])
def get_orders():
    orders = []
    total_price = 0
    
    try:
        for order in get_orders_from_db():
            order_id = order[0]
            order_products = get_order_products_from_db(order_id)

            if order_products is not None:
                adjusted_column_names = [{
                    'productId': order_product[1],
                    'productName': order_product[2],
                    'quantity': order_product[3],
                    'totalPrice': order_product[4]
                    } for order_product in order_products
                ]
                total_price_for_order = [t['totalPrice'] for t in adjusted_column_names]
                
                order_dict = {
                    'orderId': order_id,
                    'customerName': order[1],
                    'customerId': order[2],
                    'orderDate': order[3],
                    'totalPrice': sum(total_price_for_order),
                    'products': adjusted_column_names
                }
                orders.append(order_dict)

        return jsonify(orders), 200
    except Exception as e:
        logger_instance.error(f"Error in '/get-orders': {e}")
        return "Something went wrong", 500
 
@current_app.route('/get-order/<user_id>', methods=['GET'])
def get_orders_from_user(user_id):
    orders = []
    total_price = 0

    try:
        for order in get_orders_from_user_from_db(user_id):
            order_id = order[0]
            order_products = get_order_products_from_db(order_id)

            adjusted_column_names = [{
                'productId': order_product[1],
                'productName': order_product[2],
                'quantity': order_product[3],
                'totalPrice': order_product[4]
                } for order_product in order_products
            ]
            total_price_for_order = [t['totalPrice'] for t in adjusted_column_names]
            
            order_dict = {
                'orderId': order_id,
                'customerName': order[1],
                'customerId': order[2],
                'orderDate': order[3],
                'totalPrice': sum(total_price_for_order),
                'products': adjusted_column_names
            }
            orders.append(order_dict)

        return jsonify(orders), 200
        
    except Exception as e:
        logger_instance.error(f"Error in '/get-order/{user_id}': {e}")
        return "Something went wrong", 500

@current_app.route('/unlock-fridge', methods=['POST'])
def unlock_fridge():
    try:
        electro_magnet_instance.unlock()
        logger_instance.info("Electro magnet is UNLOCKED")
        if request.json['isAdmin'] == False:
            record(request.json['customerId'], request.json['orderId'])
        return "OK", 200
    except Exception as e:
        logger_instance.error(f"Could not unlock electro magnet: {e}")
        return "Something went wrong", 500

@current_app.route('/lock-fridge', methods=['POST'])
def lock_fridge():
    try:
        electro_magnet_instance.lock()
        logger_instance.info("Electro magnet is LOCKED")
        return "OK", 200
    except Exception as e:
        logger_instance.error(f"Could not lock electro magnet: {e}")
        return "Something went wrong", 500