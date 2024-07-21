from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173"}})

    with app.app_context():
        from . import routes
    
    return app
