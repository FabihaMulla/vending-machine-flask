# Vending Machine - Mealy Machine Implementation

A modern web-based vending machine application implementing Mealy Machine state transitions using Flask (Python) backend and HTML/CSS/JavaScript frontend.

## 🎯 Project Overview

This project demonstrates a complete vending machine system based on **Mealy Machine** architecture, suitable for Automata Theory, Software Design & Architecture (SDA), and Object-Oriented Programming (OOP) courses.

### Mealy Machine States

1. **IDLE** - Ready to accept coins
2. **COIN_INSERTED** - Money added, can add more coins or select item
3. **ITEM_SELECTED** - Item chosen, validating purchase
4. **DISPENSING** - Item being dispensed
5. **OUT_OF_STOCK** - Selected item unavailable
6. **REFUND** - Returning money to user

## 📁 Project Structure

```
vending/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── models/
│   │   └── vending_machine.py      # VendingMachine class & states
│   ├── routes/
│   │   └── vending_routes.py       # API endpoints (Blueprint)
│   └── services/
│       ├── state_manager.py        # Mealy machine state transitions
│       ├── payment.py              # Coin insertion & balance handling
│       ├── inventory.py            # Item management
│       └── transaction.py          # Purchase & refund logic
├── static/
│   ├── css/
│   │   └── style.css               # Professional styling
│   └── js/
│       └── vending.js              # Frontend logic & API calls
├── templates/
│   └── index.html                  # Main UI
├── run.py                          # Application entry point
└── requirements.txt                # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Navigate to project directory:**
   ```bash
   cd vending
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

6. **Open browser:**
   Navigate to `http://localhost:5000`

## 🎮 How to Use

1. **Insert Coins** - Click coin buttons ($0.25, $0.50, $1.00, $2.00)
2. **Select Item** - Click on an available item card
3. **Purchase** - Click "Purchase" button when item is selected
4. **Refund** - Click "Refund/Cancel" to get your money back
5. **View History** - Toggle transaction history to see past purchases

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Get current machine status |
| `/api/items` | GET | Get all items |
| `/api/items/<id>` | GET | Get specific item |
| `/api/insert-coin` | POST | Insert coin |
| `/api/select-item` | POST | Select item |
| `/api/purchase` | POST | Complete purchase |
| `/api/refund` | POST | Process refund |
| `/api/reset` | POST | Reset machine |
| `/api/history` | GET | Get transaction history |

## 🎨 Features

- ✅ Modular architecture with clear separation of concerns
- ✅ Flask Blueprints for route organization
- ✅ Mealy Machine state management
- ✅ Real-time balance tracking
- ✅ Stock management
- ✅ Transaction history
- ✅ Professional UI with light colors
- ✅ Responsive design
- ✅ Error handling & validation
- ✅ JSON API responses

## 📚 Academic Use

This project demonstrates:
- **Automata Theory**: Mealy machine implementation with state transitions
- **Software Design**: Modular architecture, separation of concerns, service layer pattern
- **OOP Principles**: Encapsulation, single responsibility, dependency management
- **Web Development**: RESTful API, MVC pattern, frontend-backend integration

## 🧪 Testing the Mealy Machine

Try these scenarios:
1. **Normal Purchase**: Insert $2.00 → Select item → Purchase
2. **Insufficient Balance**: Insert $0.50 → Select $2.00 item → See error
3. **Out of Stock**: Try to select item C2 (Juice)
4. **Refund**: Insert coins → Request refund
5. **Multiple Coins**: Insert multiple coins before selecting item

## 📝 Code Comments

All code is thoroughly commented explaining:
- Purpose of each function
- Mealy machine transitions
- State validations
- Error handling

## 🔐 Security Notes

**Note**: This is a demonstration project. For production use:
- Implement proper session management
- Add authentication & authorization
- Use environment variables for sensitive data
- Implement rate limiting
- Add input sanitization

## 👨‍💻 Author

Created for Automata Theory / SDA / OOP academic project
Date: December 15, 2025

## 📄 License

This project is for educational purposes.
