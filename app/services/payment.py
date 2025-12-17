"""
Payment Service
Handles coin insertion, balance management, and refunds
"""

from typing import Dict


class PaymentService:
    """Manages payment operations for the vending machine"""
    
    # Accepted coin denominations
    ACCEPTED_COINS = [0.25, 0.50, 1.00, 2.00]
    
    def __init__(self):
        """Initialize payment service"""
        pass
    
    def is_valid_coin(self, amount: float) -> bool:
        """Check if the coin amount is valid"""
        return amount in self.ACCEPTED_COINS
    
    def insert_coin(self, vending_machine, amount: float) -> Dict:
        """
        Insert a coin into the vending machine
        Returns: success status and message
        """
        if not self.is_valid_coin(amount):
            return {
                "success": False,
                "message": f"Invalid coin. Accepted: {self.ACCEPTED_COINS}",
                "balance": vending_machine.get_balance()
            }
        
        # Add amount to balance
        vending_machine.add_balance(amount)
        
        return {
            "success": True,
            "message": f"${amount:.2f} inserted successfully",
            "balance": vending_machine.get_balance()
        }
    
    def check_sufficient_balance(self, vending_machine, required_amount: float) -> bool:
        """Check if current balance is sufficient for purchase"""
        return vending_machine.get_balance() >= required_amount
    
    def process_payment(self, vending_machine, amount: float) -> Dict:
        """
        Process payment by deducting from balance
        Returns: success status and remaining balance
        """
        if vending_machine.deduct_balance(amount):
            return {
                "success": True,
                "message": "Payment processed successfully",
                "balance": vending_machine.get_balance()
            }
        else:
            return {
                "success": False,
                "message": "Insufficient balance",
                "balance": vending_machine.get_balance()
            }
    
    def process_refund(self, vending_machine) -> Dict:
        """
        Process refund and return all balance
        Returns: refunded amount
        """
        refund_amount = vending_machine.clear_balance()
        
        return {
            "success": True,
            "message": f"Refunded ${refund_amount:.2f}",
            "refund_amount": refund_amount,
            "balance": 0.0
        }
    
    def calculate_change(self, balance: float, item_price: float) -> float:
        """Calculate change after purchase"""
        return balance - item_price


# Create a singleton instance
payment_service = PaymentService()
