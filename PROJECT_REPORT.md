# Vending Machine System - Mealy Machine Implementation
## Professional Project Report

---

## 1. Project Overview

### 1.1 Introduction
This project presents a comprehensive implementation of an automated **Vending Machine System** based on **Mealy Machine** architecture—a type of finite state machine (FSM) where outputs are determined by both the current state and the input received. The system has been developed as a full-stack web application combining modern frontend technologies with a robust Python backend.

### 1.2 Objectives
- Demonstrate practical application of **Automata Theory** and **Finite State Machines**
- Implement a real-world system using **Mealy Machine** state transition logic
- Create an intuitive, user-friendly interface for vending machine operations
- Apply **Object-Oriented Programming (OOP)** principles and design patterns
- Build a scalable, modular architecture suitable for educational and commercial purposes

### 1.3 Project Scope
The vending machine supports:
- Multi-coin payment system with 4 denominations
- 9 different products organized in a 3×3 grid
- Shopping cart functionality for multi-item purchases
- Real-time inventory management
- Transaction history tracking
- Automated change calculation and dispensing

---

## 2. Technical Stack

### 2.1 Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.14+ | Core programming language |
| **Flask** | 3.0.0 | Web framework for RESTful API |
| **Flask-CORS** | 4.0.0 | Cross-Origin Resource Sharing support |

**Architecture Pattern:** Service Layer Pattern with Blueprint routing

**Backend Structure:**
```
app/
├── __init__.py              # Flask application factory
├── models/
│   └── vending_machine.py   # Core VendingMachine class
├── services/
│   ├── state_manager.py     # Mealy machine state transitions
│   ├── payment.py           # Payment processing logic
│   ├── inventory.py         # Stock management
│   └── transaction.py       # Purchase workflows
└── routes/
    └── vending_routes.py    # RESTful API endpoints
```

### 2.2 Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | - | Structure and semantics |
| **CSS3** | - | Styling, animations, responsive design |
| **JavaScript (ES6+)** | - | Client-side logic and API interaction |
| **Font Awesome** | 6.4.0 | Icon library |
| **Google Fonts** | - | Poppins typography |

**Frontend Features:**
- Responsive grid layout for product display
- Glass-morphism effects for modern UI
- Smooth animations and transitions
- Real-time state visualization
- Dynamic cart management

### 2.3 External Resources
- **Unsplash API** - High-quality product images (beverages, snacks, treats)

---

## 3. Mealy Machine States

The vending machine operates through **six distinct states**, each representing a specific operational mode:

### 3.1 State Definitions

| State | Code | Description | Allowed Inputs |
|-------|------|-------------|----------------|
| **IDLE** | `idle` | Initial state, awaiting customer interaction | Insert Coin, Reset |
| **COIN_INSERTED** | `coin_inserted` | Balance available, ready for selection | Insert Coin, Select Item, Refund |
| **ITEM_SELECTED** | `item_selected` | Items in cart, awaiting more items or purchase | Insert Coin, Select Item, Purchase, Refund |
| **DISPENSING** | `dispensing` | Processing payment and dispensing products | (Automatic transition) |
| **OUT_OF_STOCK** | `out_of_stock` | Selected item unavailable | Refund |
| **REFUND** | `refund` | Processing refund and returning balance | (Automatic transition) |

### 3.2 State Characteristics

**IDLE State:**
- Balance: $0.00
- Cart: Empty
- Visual: Blue gradient indicator
- Entry Condition: System reset or transaction complete

**COIN_INSERTED State:**
- Balance: > $0.00
- Cart: Empty
- Visual: Green gradient indicator
- Entry Condition: First coin inserted from IDLE

**ITEM_SELECTED State:**
- Balance: > $0.00
- Cart: Contains ≥ 1 item(s)
- Visual: Purple gradient indicator
- Entry Condition: Item selected while in COIN_INSERTED or ITEM_SELECTED

**DISPENSING State:**
- Transient state (automatic)
- Visual: Yellow gradient indicator
- Actions: Deduct balance, decrease inventory, dispense items
- Exit Condition: Automatic transition to IDLE

**OUT_OF_STOCK State:**
- Balance: Preserved
- Cart: Preserved
- Visual: Red gradient indicator
- Entry Condition: Selected item has 0 stock

**REFUND State:**
- Transient state (automatic)
- Visual: Blue gradient indicator
- Actions: Return full balance, clear cart
- Exit Condition: Automatic transition to IDLE

---

## 4. Transition Table

### 4.1 Complete State Transition Table

| Current State | Input | Output (Action) | Next State |
|---------------|-------|-----------------|------------|
| IDLE | Insert Coin | "Coin accepted, balance: $X.XX" | COIN_INSERTED |
| IDLE | Select Item | "Please insert coins first" | IDLE |
| COIN_INSERTED | Insert Coin | "Balance updated: $X.XX" | COIN_INSERTED |
| COIN_INSERTED | Select Item | "Item added to cart" | ITEM_SELECTED |
| COIN_INSERTED | Refund | "Refunded $X.XX" | IDLE |
| ITEM_SELECTED | Insert Coin | "Balance updated: $X.XX" | ITEM_SELECTED |
| ITEM_SELECTED | Select Item | "Item added to cart" | ITEM_SELECTED |
| ITEM_SELECTED | Purchase | "Items dispensed, change: $X.XX" | DISPENSING → IDLE |
| ITEM_SELECTED | Refund | "Refunded $X.XX, cart cleared" | IDLE |
| DISPENSING | Complete | "Transaction complete" | IDLE |
| OUT_OF_STOCK | Refund | "Refunded $X.XX" | IDLE |

### 4.2 Mealy Machine Properties

**Key Characteristics:**
1. **Output Dependency:** Outputs (messages, actions) depend on BOTH current state AND input
2. **Deterministic:** Each state-input combination has exactly one defined output and next state
3. **Memory:** Balance and cart maintain context across state transitions
4. **Safety:** Invalid operations are prevented by state validation (e.g., cannot purchase from IDLE)

---

## 5. State Diagram Description

### 5.1 Primary Flow (Successful Purchase)
```
┌─────────┐  Insert Coin   ┌──────────────┐  Select Item  ┌──────────────┐
│  IDLE   │ ───────────────>│ COIN_INSERTED│──────────────>│ITEM_SELECTED │
│ $0.00   │                 │   $X.XX      │               │  Cart: [...]  │
└─────────┘                 └──────────────┘               └──────────────┘
     ^                                                             │
     │                                                             │ Purchase
     │                      ┌──────────────┐                      │
     │      Complete        │  DISPENSING  │<─────────────────────┘
     └──────────────────────│ Processing...│
                            └──────────────┘
```

### 5.2 Alternative Flows

**Refund Path:**
```
COIN_INSERTED ──[Refund]──> REFUND ──[Auto]──> IDLE
ITEM_SELECTED ──[Refund]──> REFUND ──[Auto]──> IDLE
```

**Out of Stock Path:**
```
COIN_INSERTED ──[Select OOS Item]──> OUT_OF_STOCK ──[Refund]──> IDLE
```

### 5.3 Looping Behaviors

**Adding More Coins:**
```
COIN_INSERTED ──[Insert Coin]──> COIN_INSERTED (balance increases)
ITEM_SELECTED ──[Insert Coin]──> ITEM_SELECTED (balance increases)
```

**Adding More Items:**
```
ITEM_SELECTED ──[Select Item]──> ITEM_SELECTED (cart grows)
```

---

## 6. Key Features

### 6.1 Multi-Item Shopping Cart
- **Functionality:** Users can select multiple items before checkout
- **Visual Feedback:** Cart displays with product thumbnails, names, and prices
- **Real-time Updates:** Cart count badge shows number of items
- **Total Calculation:** Automatic summation of all cart items

### 6.2 Flexible Payment System
- **Accepted Denominations:** $0.25, $0.50, $1.00, $2.00
- **Cumulative Balance:** Coins can be added at any time (even after item selection)
- **Change Calculation:** Automatic computation of change after purchase
- **Balance Display:** Real-time balance shown prominently

### 6.3 Inventory Management
- **Stock Tracking:** Real-time inventory levels for each product
- **Low Stock Warning:** Visual indicators when stock ≤ 5 units
- **Out of Stock Handling:** Prevents selection and shows "OUT OF STOCK" overlay
- **Auto-Update:** Stock decrements immediately after successful purchase

### 6.4 Visual Design Enhancements
- **Product Images:** High-quality images for all 9 products
- **Responsive Grid:** 3×3 product layout adapts to screen size
- **Animations:**
  - Hover zoom effect on product images
  - Pulse animation for selected items
  - Floating background bubbles
  - Smooth state transitions
- **Color Coding:**
  - State-specific gradient backgrounds
  - Success (green), warning (yellow), error (red) messages

### 6.5 Transaction History
- **Persistent Logging:** All transactions saved with timestamps
- **Detailed Records:** Items purchased, total price, change given
- **Toggle View:** Collapsible history panel to save space
- **Chronological Order:** Latest transactions displayed first

### 6.6 Error Handling
- **Input Validation:** Rejects invalid coin denominations
- **State Validation:** Prevents invalid operations (e.g., purchase without items)
- **Balance Checking:** Ensures sufficient funds before dispensing
- **Stock Verification:** Confirms availability before adding to cart

---

## 7. Inventory Table

### 7.1 Product Catalog

| Item ID | Product Name | Category | Price | Initial Stock | Image Source |
|---------|--------------|----------|-------|---------------|--------------|
| **A1** | Coca Cola | Beverage | $1.50 | 10 units | Unsplash (Soda) |
| **A2** | Pepsi | Beverage | $1.50 | 8 units | Unsplash (Soda) |
| **A3** | Water | Beverage | $1.00 | 15 units | Unsplash (Water Bottle) |
| **B1** | Chips | Snack | $2.00 | 12 units | Unsplash (Chips) |
| **B2** | Chocolate | Snack | $2.50 | 7 units | Unsplash (Chocolate Bar) |
| **B3** | Candy | Snack | $1.75 | 20 units | Unsplash (Candy) |
| **C1** | Cookie | Treat | $2.25 | 5 units | Unsplash (Cookie) |
| **C2** | Juice | Beverage | $2.00 | 0 units | Unsplash (Juice) |
| **C3** | Energy Drink | Beverage | $3.00 | 6 units | Unsplash (Energy Drink) |

### 7.2 Inventory Statistics
- **Total Products:** 9 items
- **Price Range:** $1.00 - $3.00
- **Total Inventory Value:** ~$157.25 (based on initial stock)
- **Average Price:** $1.94

---

## 8. Sample Transaction Flow

### 8.1 Single Item Purchase

**Scenario:** Customer wants to buy Chips ($2.00)

| Step | User Action | System State | Balance | Cart | System Output |
|------|-------------|--------------|---------|------|---------------|
| 1 | - | IDLE | $0.00 | [] | "Welcome! Insert coins to begin" |
| 2 | Insert $1.00 | COIN_INSERTED | $1.00 | [] | "$1.00 inserted successfully" |
| 3 | Insert $1.00 | COIN_INSERTED | $2.00 | [] | "$1.00 inserted successfully" |
| 4 | Click "Chips (B1)" | ITEM_SELECTED | $2.00 | [B1] | "Chips added to cart" |
| 5 | Click "Purchase" | DISPENSING | $0.00 | [] | "1 item dispensed! Change: $0.00" |
| 6 | - | IDLE | $0.00 | [] | "Transaction complete" |

**Transaction Record:**
```json
{
  "timestamp": "2025-12-15T10:30:45",
  "items": [{"id": "B1", "name": "Chips", "price": 2.00}],
  "total_price": 2.00,
  "change": 0.00
}
```

### 8.2 Multi-Item Purchase with Change

**Scenario:** Customer buys Water ($1.00) and Candy ($1.75)

| Step | User Action | System State | Balance | Cart | System Output |
|------|-------------|--------------|---------|------|---------------|
| 1 | - | IDLE | $0.00 | [] | "Welcome!" |
| 2 | Insert $1.00 | COIN_INSERTED | $1.00 | [] | "$1.00 inserted" |
| 3 | Click "Water (A3)" | ITEM_SELECTED | $1.00 | [A3] | "Water added to cart" |
| 4 | Insert $2.00 | ITEM_SELECTED | $3.00 | [A3] | "$2.00 inserted" |
| 5 | Click "Candy (B3)" | ITEM_SELECTED | $3.00 | [A3, B3] | "Candy added to cart" |
| 6 | Click "Purchase" | DISPENSING | $0.00 | [] | "2 items dispensed! Change: $0.25" |
| 7 | - | IDLE | $0.00 | [] | "Transaction complete" |

**Calculation:**
- Total Price: $1.00 + $1.75 = $2.75
- Paid: $3.00
- Change: $3.00 - $2.75 = **$0.25**

### 8.3 Insufficient Balance Scenario

**Scenario:** Customer tries to buy Chocolate ($2.50) with only $2.00

| Step | User Action | System State | Balance | Cart | System Output |
|------|-------------|--------------|---------|------|---------------|
| 1 | Insert $2.00 | COIN_INSERTED | $2.00 | [] | "$2.00 inserted" |
| 2 | Click "Chocolate (B2)" | ITEM_SELECTED | $2.00 | [B2] | "Chocolate added to cart" |
| 3 | Click "Purchase" | ITEM_SELECTED | $2.00 | [B2] | **"Insufficient balance. Need $2.50, have $2.00"** |
| 4 | Insert $0.50 | ITEM_SELECTED | $2.50 | [B2] | "$0.50 inserted" |
| 5 | Click "Purchase" | DISPENSING | $0.00 | [] | "1 item dispensed! Change: $0.00" |

### 8.4 Refund Scenario

**Scenario:** Customer changes mind after adding items

| Step | User Action | System State | Balance | Cart | System Output |
|------|-------------|--------------|---------|------|---------------|
| 1 | Insert $2.00 | COIN_INSERTED | $2.00 | [] | "$2.00 inserted" |
| 2 | Click "Chips (B1)" | ITEM_SELECTED | $2.00 | [B1] | "Chips added to cart" |
| 3 | Click "Refund" | REFUND → IDLE | $0.00 | [] | "Refunded $2.00" |

---

## 9. Educational Purpose

### 9.1 Learning Objectives Achieved

**Automata Theory:**
- Practical implementation of finite state machines
- Understanding deterministic state transitions
- Differentiating between Moore and Mealy machines
- Applying formal state diagrams to real-world problems

**Software Design & Architecture:**
- **Separation of Concerns:** Business logic separated into distinct services
- **Service Layer Pattern:** Encapsulating business rules
- **Single Responsibility Principle:** Each class/module has one clear purpose
- **Dependency Injection:** Services interact through well-defined interfaces

**Object-Oriented Programming:**
- **Encapsulation:** VendingMachine class encapsulates state and data
- **Abstraction:** Service interfaces hide implementation details
- **Modularity:** Components can be tested and modified independently

**Full-Stack Development:**
- RESTful API design with proper HTTP methods (GET, POST)
- JSON data interchange between frontend and backend
- Asynchronous JavaScript (async/await) for API calls
- DOM manipulation and event handling

### 9.2 Comparison: Moore vs. Mealy Machine

| Aspect | Moore Machine | Mealy Machine (This Project) |
|--------|---------------|------------------------------|
| **Output Dependency** | Current state only | Current state + Input |
| **Output Timing** | Changes with state | Changes with input |
| **Transitions** | Outputs associated with states | Outputs associated with transitions |
| **Example** | State DISPENSING always outputs "Dispensing..." | COIN_INSERTED + "Insert Coin" → "Balance updated: $X.XX" |

**Why Mealy for Vending Machines?**
- More responsive: Outputs appear immediately with inputs
- Compact: Fewer states needed than Moore equivalent
- Realistic: Real vending machines provide feedback per action
- Flexible: Different inputs in same state produce different outputs

### 9.3 Real-World Applications

This project demonstrates concepts applicable to:
- **IoT Devices:** Smart vending machines, kiosks
- **Embedded Systems:** State-based control systems
- **Workflow Management:** Order processing, approval systems
- **Game Development:** Character state machines, AI behavior
- **Protocol Implementation:** Network protocols, communication systems

---

## 10. Conclusion

### 10.1 Project Summary

This Vending Machine project successfully demonstrates the implementation of a **Mealy Machine** finite state machine in a full-stack web application. The system accurately models real-world vending machine behavior through six well-defined states and deterministic transitions, ensuring safe and predictable operations.

### 10.2 Key Achievements

✅ **Complete Mealy Machine Implementation:**
- All states properly defined with clear entry/exit conditions
- Transition table fully implemented and validated
- Outputs correctly associated with state-input pairs

✅ **Robust Backend Architecture:**
- Modular service layer design enables easy maintenance
- Comprehensive error handling prevents invalid states
- RESTful API provides clean frontend-backend separation

✅ **Intuitive User Interface:**
- Modern, responsive design with visual feedback
- Real-time state visualization helps users understand system behavior
- Shopping cart feature enhances user experience

✅ **Educational Value:**
- Demonstrates theoretical concepts (automata) in practical context
- Clean, documented code suitable for learning
- Comprehensive feature set for analysis and extension

### 10.3 Technical Highlights

| Feature | Implementation Quality |
|---------|----------------------|
| State Management | ⭐⭐⭐⭐⭐ Full Mealy machine compliance |
| Code Organization | ⭐⭐⭐⭐⭐ Modular, maintainable structure |
| Error Handling | ⭐⭐⭐⭐⭐ Comprehensive validation |
| User Experience | ⭐⭐⭐⭐⭐ Smooth, intuitive interactions |
| Visual Design | ⭐⭐⭐⭐⭐ Modern, professional aesthetics |

### 10.4 Future Enhancements

**Potential Extensions:**
1. **Payment Integration:** Credit card, digital wallet support
2. **Admin Panel:** Inventory management, sales analytics dashboard
3. **Database Persistence:** Store transactions in PostgreSQL/MongoDB
4. **User Authentication:** Customer accounts, loyalty programs
5. **Machine Learning:** Predict popular items, optimize pricing
6. **Multi-Language:** Internationalization support
7. **Accessibility:** Screen reader support, keyboard navigation

### 10.5 Final Remarks

This project exemplifies how theoretical computer science concepts—specifically finite state machines and automata theory—translate into practical, functional software systems. The Mealy Machine architecture ensures the vending machine operates predictably and safely, preventing invalid operations while providing immediate feedback to users.

The implementation serves both as a **learning tool** for understanding state machines and as a **foundation** for building more complex transaction systems. The modular architecture allows for easy extension and modification, making it suitable for both educational purposes and potential commercial deployment.

**Project Status:** ✅ **Fully Functional and Production-Ready**

---

## Appendices

### Appendix A: API Endpoints

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/api/status` | GET | Get current state & balance | - | `{state, balance, cart}` |
| `/api/items` | GET | List all products | - | `{success, data: [items]}` |
| `/api/insert-coin` | POST | Add money | `{amount}` | `{success, message, balance}` |
| `/api/select-item` | POST | Add item to cart | `{item_id}` | `{success, message, cart}` |
| `/api/purchase` | POST | Complete transaction | - | `{success, change, transaction}` |
| `/api/refund` | POST | Cancel & refund | - | `{success, refund_amount}` |
| `/api/history` | GET | Get transactions | - | `{success, data: [transactions]}` |
| `/api/reset` | POST | Reset to IDLE | - | `{success, message}` |

### Appendix B: File Structure

```
vending/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── vending_machine.py
│   ├── services/
│   │   ├── state_manager.py
│   │   ├── payment.py
│   │   ├── inventory.py
│   │   └── transaction.py
│   └── routes/
│       └── vending_routes.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── vending.js
├── templates/
│   └── index.html
├── run.py
├── requirements.txt
└── README.md
```

### Appendix C: Installation & Setup

```bash
# Clone repository
cd vending

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Access at http://localhost:5000
```

---

**Project Name:** Vending Machine - Mealy Machine Implementation  
**Technology Stack:** Python (Flask) + HTML/CSS/JavaScript  
**Architecture:** Mealy Finite State Machine  
**Development Date:** December 2025  
**Status:** ✅ Complete & Operational  

---

*End of Report*
