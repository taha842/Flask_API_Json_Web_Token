# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:33:11 2023
@author: M-Taha
"""

from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678910'  # Replace with a strong, secret key

# Function to generate a JWT token
def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=0.1)
    payload = {'username': username, 'exp': expiration_time}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Decorator for route protection using JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token1 = request.headers.get('Authorization')
        token = token1.replace("Bearer", "").strip()
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(data, *args, **kwargs)

    return decorated

# Route for generating a token (login)
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Username and password required'}), 401

    # Perform authentication logic (e.g., check username and password against database)
    # Replace the following with your actual authentication logic
    if auth.username == 'Taha' and auth.password == 'Taha':
        token = generate_token(auth.username)
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401

# Protected route that requires a valid token
@app.route('/protected', methods=['GET'])
@token_required
def protected(data):
    return jsonify({'message': 'This is a protected route', 'username': data['username']})

@app.route('/Test/', methods=['GET'])
@token_required
def get_json_data(data):
    # Read data from a JSON file (replace 'data.json' with your file path)
    print("Execution");
    return "Hello EXE " 


app.run()
