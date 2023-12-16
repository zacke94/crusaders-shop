from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost*'])

@app.route('/getConnectionStatus', methods=['GET'])
def getConnectionStatus():
    return jsonify(connected='true')

@app.route('/getLockStatus', methods=['GET'])
def getLockStatus():
    return jsonify(locked='true')

@app.route('/lock', methods=['POST'])
def lock():
    return 'Success', 201

@app.route('/unlock', methods=['POST'])
def unlock():
    return 'Success', 201


if __name__ == '__main__':
    app.run(debug=True)
