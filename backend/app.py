import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
CORS(app)

# Simple in-memory user database
users_db = {
    'admin': {'password': 'admin123', 'role': 'admin', 'company': 'TechCorp'},
    'manager': {'password': 'manager123', 'role': 'manager', 'company': 'LogiTech'},
    'viewer': {'password': 'viewer123', 'role': 'viewer', 'company': 'SupplyChain Inc'}
}

SECRET_KEY = 'supply-chain-ai-secret-key-2024'

def generate_token(username):
    payload = {
        'username': username,
        'role': users_db[username]['role'],
        'company': users_db[username]['company'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Authentication routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
        
    username = data.get('username')
    password = data.get('password')

    if username in users_db and users_db[username]['password'] == password:
        token = generate_token(username)
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'username': username,
                'role': users_db[username]['role'],
                'company': users_db[username]['company']
            }
        })

    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

# Public routes (no authentication needed)
@app.route('/api/inventory')
def get_inventory():
    return jsonify({
        "total_units": 1635,
        "status": "Good Stock", 
        "low_stock_items_count": 0,
        "warehouses": ["Mumbai", "Delhi", "Bangalore"]
    })

@app.route('/api/deliveries')
def get_deliveries():
    return jsonify({
        "active_deliveries": 2,
        "delayed": 1, 
        "on_time": 3
    })

@app.route('/')
def home():
    return "🚚 Supply Chain AI Backend with Authentication is Running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)