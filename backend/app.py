from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Sample data - later we'll use real database
inventory_data = {
    "total_units": 1245,
    "status": "Good Stock",
    "low_stock_items": ["iPhone 15", "MacBook Pro"],
    "warehouses": [
        {"name": "Mumbai", "stock": 450, "capacity": 1000},
        {"name": "Delhi", "stock": 320, "capacity": 800},
        {"name": "Bangalore", "stock": 475, "capacity": 900}
    ]
}

delivery_data = {
    "active_deliveries": 15,
    "delayed": 2,
    "on_time": 13,
    "deliveries": [
        {"id": 1, "driver": "Raj Kumar", "status": "In Transit", "eta": "45 mins"},
        {"id": 2, "driver": "Amit Sharma", "status": "Delayed", "eta": "2 hours"},
        {"id": 3, "driver": "Priya Singh", "status": "On Time", "eta": "30 mins"}
    ]
}

@app.route('/api/inventory')
def get_inventory():
    # Simulate real-time updates
    inventory_data['total_units'] = random.randint(1200, 1300)
    return jsonify(inventory_data)

@app.route('/api/deliveries')
def get_deliveries():
    # Simulate real-time updates
    delivery_data['active_deliveries'] = random.randint(12, 18)
    return jsonify(delivery_data)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    # Simulate data processing
    return jsonify({"status": "success", "message": "Data refreshed successfully", "timestamp": datetime.now().isoformat()})

@app.route('/')
def home():
    return "🚚 Supply Chain AI Backend Server is Running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# Add this at the very end of the file
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)