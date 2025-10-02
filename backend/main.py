from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock data - like fake database
inventory_data = {
    "total_units": 1245,
    "status": "Good Stock",
    "alerts": ["iPhone stock low", "Warehouse 3 needs restock"]
}

delivery_data = {
    "active_deliveries": 15,
    "delayed": 2,
    "on_time": 13
}

@app.route('/api/inventory')
def get_inventory():
    return jsonify(inventory_data)

@app.route('/api/deliveries')
def get_deliveries():
    return jsonify(delivery_data)

@app.route('/')
def home():
    return "🚚 Supply Chain AI Backend is Running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)