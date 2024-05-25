# Description: A simple Flask application with user registration, login, and a protected route.
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from bson.json_util import dumps

# Initialize Flask App
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/newstradingDB'  # Adjust as needed
app.config['JWT_SECRET_KEY'] = 'very_secret_key'  # Change this to a more secure key

# Initialize Flask extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)  



# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Check if the user already exists
    if users.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 409

    # Hash the password and insert new user
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    users.insert_one({'email': email, 'password': password_hash})
    return jsonify({"msg": "User registered successfully"}), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401

# Protected Route Example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# News Retrieval Endpoint
@app.route('/get-news', methods=['GET'])
def get_news():
    news_data = mongo.db.news.find()
    return jsonify([news for news in news_data])


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
