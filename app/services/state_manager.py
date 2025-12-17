"""
State Manager Service
Implements Mealy Machine state transitions and validations
In a Mealy machine, outputs are determined by both current state and input
"""

from app.models.vending_machine import MachineState
from typing import Dict, Tuple


class StateManager:
    """
    Manages state transitions based on Mealy Machine architecture
    Each transition produces an output based on current state and input
    """
    
    def __init__(self):
        """Initialize state manager with transition rules"""
        # Define valid state transitions (Mealy Machine transition table)
        self.transitions = {
            MachineState.IDLE: {
                "insert_coin": MachineState.COIN_INSERTED,
            },
            MachineState.COIN_INSERTED: {
                "insert_coin": MachineState.COIN_INSERTED,
                "select_item": MachineState.ITEM_SELECTED,
                "refund": MachineState.REFUND,
            },
            MachineState.ITEM_SELECTED: {
                "dispense": MachineState.DISPENSING,
                "out_of_stock": MachineState.OUT_OF_STOCK,
                "insufficient_balance": MachineState.COIN_INSERTED,
                "refund": MachineState.REFUND,
            },
            MachineState.DISPENSING: {
                "complete": MachineState.IDLE,
            },
            MachineState.OUT_OF_STOCK: {
                "refund": MachineState.REFUND,
                "select_another": MachineState.COIN_INSERTED,
            },
            MachineState.REFUND: {
                "complete": MachineState.IDLE,
            }
        }
    
    def can_transition(self, current_state: MachineState, action: str) -> bool:
        """Check if a transition is valid from current state with given action"""
        if current_state in self.transitions:
            return action in self.transitions[current_state]
        return False
    
    def get_next_state(self, current_state: MachineState, action: str) -> MachineState:
        """Get the next state based on current state and action"""
        if self.can_transition(current_state, action):
            return self.transitions[current_state][action]
        return current_state
    
    def transition(self, vending_machine, action: str) -> Tuple[bool, str, MachineState]:
        """
        Perform state transition (Mealy Machine behavior)
        Returns: (success, message, new_state)
        Output depends on both current state and input action
        """
        current_state = vending_machine.current_state
        
        if not self.can_transition(current_state, action):
            return (
                False,
                f"Cannot perform '{action}' from state '{current_state.value}'",
                current_state
            )
        
        # Get next state
        next_state = self.get_next_state(current_state, action)
        
        # Update machine state
        vending_machine.set_state(next_state)
        
        # Generate output message (Mealy output)
        output_message = self._generate_output(current_state, action, next_state)
        
        return (True, output_message, next_state)
    
    def _generate_output(self, from_state: MachineState, action: str, to_state: MachineState) -> str:
        """
        Generate output message based on transition (Mealy Machine output function)
        Output is determined by current state AND input
        """
        outputs = {
            (MachineState.IDLE, "insert_coin"): "Coin accepted. Ready for more coins or item selection.",
            (MachineState.COIN_INSERTED, "insert_coin"): "Additional coin accepted.",
            (MachineState.COIN_INSERTED, "select_item"): "Item selected. Checking availability...",
            (MachineState.COIN_INSERTED, "refund"): "Processing refund...",
            (MachineState.ITEM_SELECTED, "dispense"): "Dispensing item...",
            (MachineState.ITEM_SELECTED, "out_of_stock"): "Item out of stock.",
            (MachineState.ITEM_SELECTED, "insufficient_balance"): "Insufficient balance. Add more coins.",
            (MachineState.ITEM_SELECTED, "refund"): "Processing refund...",
            (MachineState.DISPENSING, "complete"): "Transaction complete. Enjoy!",
            (MachineState.OUT_OF_STOCK, "refund"): "Processing refund...",
            (MachineState.OUT_OF_STOCK, "select_another"): "Select another item.",
            (MachineState.REFUND, "complete"): "Refund complete. Thank you!",
        }
        
        key = (from_state, action)
        return outputs.get(key, f"Transitioned from {from_state.value} to {to_state.value}")
    
    def get_available_actions(self, current_state: MachineState) -> list:
        """Get list of available actions from current state"""
        if current_state in self.transitions:
            return list(self.transitions[current_state].keys())
        return []
    
    def reset_to_idle(self, vending_machine) -> None:
        """Reset machine to IDLE state"""
        vending_machine.set_state(MachineState.IDLE)
        vending_machine.set_selected_item(None)


# Create a singleton instance
state_manager = StateManager()
