"""
Vending Machine Routes
Flask Blueprint for all vending machine API endpoints
"""

from flask import Blueprint, jsonify, request
from app.models.vending_machine import VendingMachine, MachineState
from app.services.state_manager import state_manager
from app.services.payment import payment_service
from app.services.inventory import inventory_service
from app.services.transaction import transaction_service

# Create Blueprint
vending_bp = Blueprint('vending', __name__, url_prefix='/api')

# Create a global vending machine instance (in production, use session management)
vending_machine = VendingMachine()


@vending_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get current vending machine status
    Returns: current state, balance, selected item, available actions
    """
    status = transaction_service.get_transaction_status(vending_machine)
    return jsonify({
        "success": True,
        "data": status
    }), 200


@vending_bp.route('/items', methods=['GET'])
def get_items():
    """
    Get all available items in the vending machine
    Returns: list of items with id, name, price, and stock
    """
    items = inventory_service.get_all_items()
    return jsonify({
        "success": True,
        "data": items
    }), 200


@vending_bp.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get details of a specific item
    Returns: item details or error if not found
    """
    item = inventory_service.get_item(item_id)
    
    if not item:
        return jsonify({
            "success": False,
            "message": "Item not found"
        }), 404
    
    return jsonify({
        "success": True,
        "data": item
    }), 200


@vending_bp.route('/insert-coin', methods=['POST'])
def insert_coin():
    """
    Insert a coin into the vending machine
    Request body: { "amount": 1.0 }
    Returns: updated balance and state
    """
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({
            "success": False,
            "message": "Amount is required"
        }), 400
    
    try:
        amount = float(data['amount'])
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Invalid amount format"
        }), 400
    
    # Check current state - must be IDLE, COIN_INSERTED, or ITEM_SELECTED (for adding more coins)
    current_state = vending_machine.current_state
    if current_state not in [MachineState.IDLE, MachineState.COIN_INSERTED, MachineState.ITEM_SELECTED]:
        return jsonify({
            "success": False,
            "message": f"Cannot insert coin in {current_state.value} state",
            "state": vending_machine.get_state()
        }), 400
    
    # Transition state if in IDLE - MUST happen before inserting coin
    if current_state == MachineState.IDLE:
        success, message, new_state = state_manager.transition(vending_machine, "insert_coin")
        if not success:
            return jsonify({
                "success": False,
                "message": message,
                "state": vending_machine.get_state()
            }), 400
    # If in ITEM_SELECTED state, we stay in that state (items already in cart)
    # No state transition needed for COIN_INSERTED or ITEM_SELECTED
    
    # Insert coin
    result = payment_service.insert_coin(vending_machine, amount)
    
    # Add state information
    result['state'] = vending_machine.get_state()
    result['cart'] = vending_machine.get_cart()
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@vending_bp.route('/select-item', methods=['POST'])
def select_item():
    """
    Select an item to purchase (add to cart)
    Request body: { "item_id": "A1" }
    Returns: transaction status
    """
    data = request.get_json()
    
    if not data or 'item_id' not in data:
        return jsonify({
            "success": False,
            "message": "item_id is required"
        }), 400
    
    item_id = data['item_id']
    
    # Check if we're in the right state (must have coins inserted)
    if vending_machine.current_state not in [MachineState.COIN_INSERTED, MachineState.ITEM_SELECTED]:
        return jsonify({
            "success": False,
            "message": "Insert coins before selecting an item",
            "state": vending_machine.get_state(),
            "cart": vending_machine.get_cart()
        }), 400
    
    # Add item to cart
    result = transaction_service.initiate_purchase(vending_machine, item_id)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@vending_bp.route('/purchase', methods=['POST'])
def purchase():
    """
    Complete the purchase and dispense item
    Returns: transaction details and change
    """
    # Check if we're in the right state
    if vending_machine.current_state != MachineState.ITEM_SELECTED:
        return jsonify({
            "success": False,
            "message": "No item ready for dispensing",
            "state": vending_machine.get_state()
        }), 400
    
    # Complete purchase
    result = transaction_service.complete_purchase(vending_machine)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@vending_bp.route('/refund', methods=['POST'])
def refund():
    """
    Cancel transaction and refund all money
    Returns: refunded amount
    """
    # Check if refund is possible
    if vending_machine.current_state not in [MachineState.COIN_INSERTED, 
                                              MachineState.ITEM_SELECTED, 
                                              MachineState.OUT_OF_STOCK]:
        return jsonify({
            "success": False,
            "message": "No active transaction to refund",
            "state": vending_machine.get_state()
        }), 400
    
    # Process refund
    result = transaction_service.cancel_transaction(vending_machine)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@vending_bp.route('/reset', methods=['POST'])
def reset():
    """
    Reset the vending machine to IDLE state
    Admin function for testing
    """
    vending_machine.reset()
    state_manager.reset_to_idle(vending_machine)
    
    return jsonify({
        "success": True,
        "message": "Vending machine reset to IDLE state",
        "state": vending_machine.get_state()
    }), 200


@vending_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get transaction history
    Returns: list of all completed transactions
    """
    history = vending_machine.get_transaction_history()
    
    return jsonify({
        "success": True,
        "data": history,
        "count": len(history)
    }), 200
