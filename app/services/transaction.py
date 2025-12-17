"""
Transaction Service
Handles purchase, cancel, and refund logic
Coordinates between state manager, payment, and inventory services
"""

from datetime import datetime
from typing import Dict
from app.models.vending_machine import MachineState
from app.services.state_manager import state_manager
from app.services.payment import payment_service
from app.services.inventory import inventory_service


class TransactionService:
    """Manages complete transaction workflows"""
    
    def __init__(self):
        """Initialize transaction service"""
        pass
    
    def initiate_purchase(self, vending_machine, item_id: str) -> Dict:
        """
        Add item to cart (for multi-item purchases)
        """
        # Check current state - must have coins inserted
        if vending_machine.current_state == MachineState.IDLE:
            return {
                "success": False,
                "message": "Please insert coins first",
                "state": vending_machine.get_state()
            }
        
        # Check if item exists
        item = inventory_service.get_item(item_id)
        if not item:
            return {
                "success": False,
                "message": "Item not found",
                "state": vending_machine.get_state()
            }
        
        # Check if item is in stock
        if not inventory_service.is_item_available(item_id):
            return {
                "success": False,
                "message": f"{item['name']} is out of stock",
                "state": vending_machine.get_state(),
                "item": item
            }
        
        # Add to cart
        vending_machine.add_to_cart(item_id)
        
        # Transition to ITEM_SELECTED state if we're in COIN_INSERTED
        if vending_machine.current_state == MachineState.COIN_INSERTED:
            state_manager.transition(vending_machine, "select_item")
        
        return {
            "success": True,
            "message": f"{item['name']} added to cart",
            "state": vending_machine.get_state(),
            "cart": vending_machine.get_cart(),
            "item": item
        }
    
    def complete_purchase(self, vending_machine) -> Dict:
        """
        Complete the purchase transaction for all items in cart
        """
        # Verify we have items in cart
        cart = vending_machine.get_cart()
        if not cart:
            return {
                "success": False,
                "message": "Cart is empty",
                "state": vending_machine.get_state()
            }
        
        # Calculate total price
        total_price = 0
        items_to_purchase = []
        
        for item_id in cart:
            item = inventory_service.get_item(item_id)
            if not item:
                continue
            
            # Check stock
            if not inventory_service.is_item_available(item_id):
                return {
                    "success": False,
                    "message": f"{item['name']} is out of stock",
                    "state": vending_machine.get_state()
                }
            
            total_price += item['price']
            items_to_purchase.append(item)
        
        # Check if balance is sufficient
        if not payment_service.check_sufficient_balance(vending_machine, total_price):
            return {
                "success": False,
                "message": f"Insufficient balance. Need ${total_price:.2f}, have ${vending_machine.get_balance():.2f}",
                "state": vending_machine.get_state(),
                "balance": vending_machine.get_balance()
            }
        
        # Transition to DISPENSING state
        state_manager.transition(vending_machine, "dispense")
        
        # Process payment
        payment_result = payment_service.process_payment(vending_machine, total_price)
        
        if not payment_result["success"]:
            state_manager.reset_to_idle(vending_machine)
            return {
                "success": False,
                "message": payment_result["message"],
                "state": vending_machine.get_state()
            }
        
        # Store the change amount before clearing balance
        change_amount = payment_result["balance"]
        
        # Decrease stock for all items
        for item in items_to_purchase:
            inventory_service.decrease_stock(item['id'])
        
        # Record transaction
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "items": [{"id": item['id'], "name": item['name'], "price": item['price']} for item in items_to_purchase],
            "total_price": total_price,
            "change": change_amount
        }
        vending_machine.add_transaction(transaction)
        
        # Clear cart
        vending_machine.clear_cart()
        
        # Clear remaining balance (dispense change)
        vending_machine.clear_balance()
        
        # Complete dispensing and return to IDLE
        state_manager.transition(vending_machine, "complete")
        
        # Clear selected item
        vending_machine.set_selected_item(None)
        
        return {
            "success": True,
            "message": f"{len(items_to_purchase)} item(s) dispensed successfully!",
            "transaction": transaction,
            "change": change_amount,
            "state": vending_machine.get_state()
        }
    
    def cancel_transaction(self, vending_machine) -> Dict:
        """
        Cancel current transaction and process refund
        Returns all money to user and clears cart
        """
        # Transition to REFUND state
        success, message, new_state = state_manager.transition(
            vending_machine, "refund"
        )
        
        if not success:
            return {
                "success": False,
                "message": "Cannot process refund from current state",
                "state": vending_machine.get_state()
            }
        
        # Process refund
        refund_result = payment_service.process_refund(vending_machine)
        
        # Clear cart and selected item
        vending_machine.clear_cart()
        vending_machine.set_selected_item(None)
        
        # Complete refund and return to IDLE
        state_manager.transition(vending_machine, "complete")
        
        return {
            "success": True,
            "message": refund_result["message"],
            "refund_amount": refund_result["refund_amount"],
            "state": vending_machine.get_state()
        }
    
    def get_transaction_status(self, vending_machine) -> Dict:
        """Get current transaction status"""
        return {
            "state": vending_machine.get_state(),
            "balance": vending_machine.get_balance(),
            "selected_item": vending_machine.get_selected_item(),
            "cart": vending_machine.get_cart(),
            "cart_count": len(vending_machine.get_cart()),
            "available_actions": state_manager.get_available_actions(
                vending_machine.current_state
            )
        }


# Create a singleton instance
transaction_service = TransactionService()
