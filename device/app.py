from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app, origins=['*'])

@app.route('/users', methods=['GET'])
def getUsers():
    # Connect to the SQLite database
    conn = sqlite3.connect('crusaders-shop.db')
    cursor = conn.cursor()
    
    # Execute the query to select all users
    cursor.execute('SELECT id, name, admin FROM users')
    
    # Fetch all the results
    users = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    # Convert the results to a JSON format
   
    user_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'name': user[1],
            'admin': user[2]
        }
        user_list.append(user_dict)
    
    # Return the JSON response
    return jsonify({'users': user_list})

@app.route('/login', methods=['POST'])
def login():
    request_data = request.json # Access JSON data from the request body
    pin_code = get_pin_code(request_data['userId'])

    if pin_code == request_data['pinCode']:
        return 200
    else:
        return 401

    # Process the data...
    # return jsonify({'received': request_data}), 200  # Respond with a JSON object

def get_pin_code(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('crusaders-shop.db')
    cursor = conn.cursor()
    
    # Execute the query to select all users
    cursor.execute(f'SELECT pin_code FROM users WHERE id = {user_id}')
    
    # Fetch all the results
    result = cursor.fetchone()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    if result:
            return result[0]
    else:
        return jsonify({"message": "No result found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
