"""
Inventory Management Service
Handles item list, pricing, and stock management
"""

from typing import Dict, List, Optional


class InventoryService:
    """Manages vending machine inventory"""
    
    def __init__(self):
        """Initialize inventory with default items"""
        self.items = {
            "A1": {
                "id": "A1",
                "name": "Coca Cola",
                "price": 1.50,
                "stock": 10,
                "image": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=200&h=200&fit=crop"
            },
            "A2": {
                "id": "A2",
                "name": "Pepsi",
                "price": 1.50,
                "stock": 8,
                "image": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=200&h=200&fit=crop"
            },
            "A3": {
                "id": "A3",
                "name": "Water",
                "price": 1.00,
                "stock": 15,
                "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=200&h=200&fit=crop"
            },
            "B1": {
                "id": "B1",
                "name": "Chips",
                "price": 2.00,
                "stock": 12,
                "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=200&h=200&fit=crop"
            },
            "B2": {
                "id": "B2",
                "name": "Chocolate",
                "price": 2.50,
                "stock": 7,
                "image": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=200&h=200&fit=crop"
            },
            "B3": {
                "id": "B3",
                "name": "Candy",
                "price": 1.75,
                "stock": 20,
                "image": "https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=200&h=200&fit=crop"
            },
            "C1": {
                "id": "C1",
                "name": "Cookie",
                "price": 2.25,
                "stock": 5,
                "image": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=200&h=200&fit=crop"
            },
            "C2": {
                "id": "C2",
                "name": "Juice",
                "price": 2.00,
                "stock": 4,
                "image": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=200&h=200&fit=crop"
            },
            "C3": {
                "id": "C3",
                "name": "Energy Drink",
                "price": 3.00,
                "stock": 6,
                "image": "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=200&h=200&fit=crop"
            }
        }
    
    def get_all_items(self) -> List[Dict]:
        """Return all items in inventory"""
        return list(self.items.values())
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """Get a specific item by ID"""
        return self.items.get(item_id)
    
    def is_item_available(self, item_id: str) -> bool:
        """Check if item exists and is in stock"""
        item = self.get_item(item_id)
        if item and item["stock"] > 0:
            return True
        return False
    
    def get_item_price(self, item_id: str) -> Optional[float]:
        """Get the price of an item"""
        item = self.get_item(item_id)
        return item["price"] if item else None
    
    def get_item_stock(self, item_id: str) -> Optional[int]:
        """Get the stock count of an item"""
        item = self.get_item(item_id)
        return item["stock"] if item else None
    
    def decrease_stock(self, item_id: str) -> bool:
        """Decrease stock by 1 for a given item"""
        item = self.get_item(item_id)
        if item and item["stock"] > 0:
            item["stock"] -= 1
            return True
        return False
    
    def increase_stock(self, item_id: str, quantity: int = 1) -> bool:
        """Increase stock for a given item"""
        item = self.get_item(item_id)
        if item:
            item["stock"] += quantity
            return True
        return False
    
    def update_item_price(self, item_id: str, new_price: float) -> bool:
        """Update the price of an item"""
        item = self.get_item(item_id)
        if item:
            item["price"] = new_price
            return True
        return False


# Create a singleton instance
inventory_service = InventoryService()
