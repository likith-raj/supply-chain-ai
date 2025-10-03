from datetime import datetime

class Inventory:
    def __init__(self, product_id, name, quantity, warehouse, min_stock_level):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.warehouse = warehouse
        self.min_stock_level = min_stock_level
        self.last_updated = datetime.now()

class Delivery:
    def __init__(self, delivery_id, driver_name, status, origin, destination, eta):
        self.delivery_id = delivery_id
        self.driver_name = driver_name
        self.status = status  # 'pending', 'in_transit', 'delivered', 'delayed'
        self.origin = origin
        self.destination = destination
        self.eta = eta
        self.created_at = datetime.now()