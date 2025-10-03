import sqlite3
import random
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='supply_chain.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                warehouse TEXT NOT NULL,
                min_stock_level INTEGER,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deliveries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_name TEXT NOT NULL,
                status TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                eta TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data if empty
        cursor.execute('SELECT COUNT(*) FROM inventory')
        if cursor.fetchone()[0] == 0:
            self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        # Sample inventory
        inventory_items = [
            ('iPhone 15', 450, 'Mumbai Warehouse', 100),
            ('MacBook Pro', 320, 'Delhi Warehouse', 50),
            ('AirPods', 475, 'Bangalore Warehouse', 200),
            ('iPad Air', 210, 'Mumbai Warehouse', 80),
            ('Apple Watch', 180, 'Delhi Warehouse', 60)
        ]
        
        for item in inventory_items:
            cursor.execute('''
                INSERT INTO inventory (product_name, quantity, warehouse, min_stock_level)
                VALUES (?, ?, ?, ?)
            ''', item)
        
        # Sample deliveries
        deliveries = [
            ('Raj Kumar', 'in_transit', 'Mumbai', 'Pune', '45 mins'),
            ('Amit Sharma', 'delayed', 'Delhi', 'Gurgaon', '2 hours'),
            ('Priya Singh', 'in_transit', 'Bangalore', 'Chennai', '30 mins'),
            ('Suresh Patel', 'pending', 'Hyderabad', 'Bangalore', '4 hours')
        ]
        
        for delivery in deliveries:
            cursor.execute('''
                INSERT INTO deliveries (driver_name, status, origin, destination, eta)
                VALUES (?, ?, ?, ?, ?)
            ''', delivery)
    
    def get_inventory_summary(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(quantity) FROM inventory')
        total_units = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM inventory 
            WHERE quantity < min_stock_level
        ''')
        low_stock_count = cursor.fetchone()[0]
        
        status = "Good Stock" if low_stock_count == 0 else "Low Stock Alert"
        
        conn.close()
        
        return {
            "total_units": total_units,
            "status": status,
            "low_stock_items_count": low_stock_count,
            "warehouses": ["Mumbai", "Delhi", "Bangalore", "Hyderabad"]
        }
    
    def get_delivery_summary(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM deliveries')
        total_deliveries = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM deliveries WHERE status="delayed"')
        delayed = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM deliveries WHERE status="in_transit"')
        in_transit = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT driver_name, status, origin, destination, eta 
            FROM deliveries LIMIT 5
        ''')
        recent_deliveries = [
            {
                "driver": row[0],
                "status": row[1],
                "route": f"{row[2]} → {row[3]}",
                "eta": row[4]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            "active_deliveries": in_transit,
            "delayed": delayed,
            "on_time": total_deliveries - delayed,
            "recent_deliveries": recent_deliveries
        }

# Global database instance
db = Database()