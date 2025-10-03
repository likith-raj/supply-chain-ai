import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from database import db  # Import our database

app = Flask(__name__)
CORS(app)

@app.route('/api/inventory')
def get_inventory():
    try:
        inventory_data = db.get_inventory_summary()
        return jsonify(inventory_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deliveries')
def get_deliveries():
    try:
        delivery_data = db.get_delivery_summary()
        return jsonify(delivery_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    return jsonify({
        "status": "success", 
        "message": "Data refreshed from database",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/low-stock')
def get_low_stock():
    try:
        conn = sqlite3.connect(db.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_name, quantity, min_stock_level 
            FROM inventory 
            WHERE quantity < min_stock_level
        ''')
        
        low_stock_items = [
            {
                "product": row[0],
                "current_stock": row[1],
                "min_required": row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({"low_stock_items": low_stock_items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "🚚 Supply Chain AI Backend with Database is Running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)