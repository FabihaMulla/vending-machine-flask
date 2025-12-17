"""
Vending Machine Model
Represents the core vending machine class with state management
Based on Mealy Machine architecture
"""

from enum import Enum
from typing import Dict, Optional


class MachineState(Enum):
    """Enumeration of all possible vending machine states (Mealy Machine)"""
    IDLE = "idle"
    COIN_INSERTED = "coin_inserted"
    ITEM_SELECTED = "item_selected"
    DISPENSING = "dispensing"
    OUT_OF_STOCK = "out_of_stock"
    REFUND = "refund"


class VendingMachine:
    """
    Main Vending Machine class
    Implements Mealy machine state management
    """
    
    def __init__(self):
        """Initialize the vending machine in IDLE state"""
        self.current_state = MachineState.IDLE
        self.balance = 0.0
        self.selected_item = None
        self.cart = []  # Shopping cart for multiple items
        self.transaction_history = []
        
    def get_state(self) -> str:
        """Return the current state of the machine"""
        return self.current_state.value
    
    def set_state(self, new_state: MachineState) -> None:
        """Set the machine to a new state"""
        self.current_state = new_state
    
    def get_balance(self) -> float:
        """Return the current balance"""
        return self.balance
    
    def add_balance(self, amount: float) -> None:
        """Add amount to the current balance"""
        self.balance += amount
    
    def deduct_balance(self, amount: float) -> bool:
        """Deduct amount from balance if sufficient funds"""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def clear_balance(self) -> float:
        """Clear and return the current balance"""
        refund_amount = self.balance
        self.balance = 0.0
        return refund_amount
    
    def set_selected_item(self, item_id: Optional[str]) -> None:
        """Set the selected item"""
        self.selected_item = item_id
    
    def get_selected_item(self) -> Optional[str]:
        """Get the selected item"""
        return self.selected_item
    
    def add_transaction(self, transaction: Dict) -> None:
        """Add a transaction to history"""
        self.transaction_history.append(transaction)
    
    def get_transaction_history(self) -> list:
        """Get all transaction history"""
        return self.transaction_history
    
    def reset(self) -> None:
        """Reset machine to IDLE state"""
        self.current_state = MachineState.IDLE
        self.balance = 0.0
        self.selected_item = None
        self.cart = []
    
    def add_to_cart(self, item_id: str) -> None:
        """Add an item to the shopping cart"""
        self.cart.append(item_id)
    
    def remove_from_cart(self, item_id: str) -> bool:
        """Remove an item from the cart"""
        if item_id in self.cart:
            self.cart.remove(item_id)
            return True
        return False
    
    def clear_cart(self) -> None:
        """Clear all items from cart"""
        self.cart = []
    
    def get_cart(self) -> list:
        """Get current cart items"""
        return self.cart
