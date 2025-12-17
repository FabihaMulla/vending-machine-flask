/**
 * Vending Machine Frontend Logic
 * Handles API calls and UI interactions
 */

// API Base URL
const API_BASE = '/api';

// Global state
let currentState = {
    state: 'IDLE',
    balance: 0.0,
    selectedItem: null,
    cart: [],
    items: []
};

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🤖 Vending Machine Application Started');
    
    // Load initial data
    loadItems();
    updateStatus();
    
    // Setup event listeners
    setupEventListeners();
    
    // Load transaction history
    loadTransactionHistory();
});

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Coin buttons
    document.querySelectorAll('.coin-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const amount = parseFloat(e.target.closest('.coin-btn').dataset.amount);
            insertCoin(amount);
        });
    });
    
    // Purchase button
    document.getElementById('purchase-btn').addEventListener('click', completePurchase);
    
    // Refund button
    document.getElementById('refund-btn').addEventListener('click', processRefund);
    
    // Reset button
    document.getElementById('reset-btn').addEventListener('click', resetMachine);
    
    // History toggle
    document.getElementById('toggle-history-btn').addEventListener('click', toggleHistory);
}

/**
 * API Call Helper
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        showLoading(true);
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();
        
        showLoading(false);
        return result;
        
    } catch (error) {
        showLoading(false);
        console.error('API Error:', error);
        showMessage(`Error: ${error.message}`, 'error');
        return { success: false, message: error.message };
    }
}

/**
 * Load all items from inventory
 */
async function loadItems() {
    const result = await apiCall('/items');
    
    if (result.success) {
        currentState.items = result.data;
        renderItems(result.data);
    } else {
        showMessage('Failed to load items', 'error');
    }
}

/**
 * Render items in the grid
 */
function renderItems(items) {
    const grid = document.getElementById('items-grid');
    grid.innerHTML = '';
    
    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'item-card';
        
        // Add out-of-stock class if needed
        if (item.stock === 0) {
            card.classList.add('out-of-stock');
        }
        
        // Determine stock class
        let stockClass = '';
        if (item.stock > 0 && item.stock <= 5) {
            stockClass = 'low';
        }
        
        card.innerHTML = `
            <div class="item-image-container">
                <img src="${item.image}" alt="${item.name}" class="item-image" loading="lazy">
                <div class="item-id-badge">${item.id}</div>
            </div>
            <div class="item-details">
                <div class="item-name">${item.name}</div>
                <div class="item-price">$${item.price.toFixed(2)}</div>
                <div class="item-stock ${stockClass}">Stock: ${item.stock}</div>
            </div>
        `;
        
        // Add click handler if item is in stock
        if (item.stock > 0) {
            card.addEventListener('click', () => selectItem(item.id));
        }
        
        grid.appendChild(card);
    });
}

/**
 * Update status display
 */
async function updateStatus() {
    const result = await apiCall('/status');
    
    if (result.success) {
        const status = result.data;
        currentState.state = status.state;
        currentState.balance = status.balance;
        currentState.selectedItem = status.selected_item;
        currentState.cart = status.cart || [];
        
        // Update UI
        updateStateDisplay(status.state);
        updateBalanceDisplay(status.balance);
        updateCartDisplay(status.cart || []);
        updatePurchaseButton();
        
        // Re-render items to update selection
        if (currentState.items.length > 0) {
            renderItems(currentState.items);
        }
    }
}

/**
 * Update state display
 */
function updateStateDisplay(state) {
    const stateDisplay = document.getElementById('current-state');
    const stateIcon = document.getElementById('state-icon');
    stateDisplay.textContent = state.toUpperCase().replace('_', ' ');
    
    // Update state icon and color based on state
    const stateConfig = {
        'idle': {
            icon: 'fa-power-off',
            gradient: 'linear-gradient(135deg, #6366F1, #8B5CF6)'
        },
        'coin_inserted': {
            icon: 'fa-coins',
            gradient: 'linear-gradient(135deg, #10B981, #059669)'
        },
        'item_selected': {
            icon: 'fa-hand-pointer',
            gradient: 'linear-gradient(135deg, #F59E0B, #D97706)'
        },
        'dispensing': {
            icon: 'fa-box-open',
            gradient: 'linear-gradient(135deg, #8B5CF6, #7C3AED)'
        },
        'out_of_stock': {
            icon: 'fa-exclamation-triangle',
            gradient: 'linear-gradient(135deg, #EF4444, #DC2626)'
        },
        'refund': {
            icon: 'fa-undo',
            gradient: 'linear-gradient(135deg, #3B82F6, #2563EB)'
        }
    };
    
    const config = stateConfig[state] || stateConfig['idle'];
    
    stateIcon.innerHTML = `<i class="fas ${config.icon}"></i>`;
    stateDisplay.style.background = config.gradient;
    stateIcon.style.background = config.gradient;
}

/**
 * Update balance display
 */
function updateBalanceDisplay(balance) {
    const balanceDisplay = document.getElementById('balance-display');
    balanceDisplay.textContent = balance.toFixed(2);
}

/**
 * Update cart display
 */
function updateCartDisplay(cart) {
    const cartDisplay = document.getElementById('cart-display');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    const totalItemsCount = document.getElementById('total-items-count');
    
    cartCount.textContent = cart.length;
    
    if (cart.length === 0) {
        cartDisplay.innerHTML = '<p class="cart-empty"><i class="fas fa-shopping-cart"></i> Cart is empty</p>';
        cartTotal.style.display = 'none';
        return;
    }
    
    // Show cart items
    cartDisplay.innerHTML = '';
    cart.forEach(itemId => {
        const item = currentState.items.find(i => i.id === itemId);
        if (item) {
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-details">
                    <span class="cart-item-name">${item.id} - ${item.name}</span>
                    <span class="cart-item-price">$${item.price.toFixed(2)}</span>
                </div>
            `;
            cartDisplay.appendChild(cartItem);
        }
    });
    
    totalItemsCount.textContent = cart.length;
    cartTotal.style.display = 'block';
}

/**
 * Update purchase button state
 */
function updatePurchaseButton() {
    const purchaseBtn = document.getElementById('purchase-btn');
    
    // Enable if we have items in cart and in ITEM_SELECTED state
    if (currentState.cart && currentState.cart.length > 0 && currentState.state === 'item_selected') {
        purchaseBtn.disabled = false;
    } else {
        purchaseBtn.disabled = true;
    }
}

/**
 * Insert coin
 */
async function insertCoin(amount) {
    console.log(`Inserting coin: $${amount}`);
    
    const result = await apiCall('/insert-coin', 'POST', { amount });
    
    if (result.success) {
        showMessage(result.message, 'success');
        await updateStatus();
    } else {
        showMessage(result.message, 'error');
    }
}

/**
 * Select item (add to cart)
 */
async function selectItem(itemId) {
    console.log(`Selecting item: ${itemId}`);
    
    // Check if we can select items
    if (currentState.state !== 'coin_inserted' && currentState.state !== 'item_selected') {
        showMessage('Please insert coins first', 'error');
        return;
    }
    
    const result = await apiCall('/select-item', 'POST', { item_id: itemId });
    
    if (result.success) {
        showMessage(result.message, 'success');
        await updateStatus();
        await loadItems();
    } else {
        showMessage(result.message, 'error');
        await updateStatus();
    }
}

/**
 * Complete purchase
 */
async function completePurchase() {
    console.log('Completing purchase...');
    
    const result = await apiCall('/purchase', 'POST');
    
    if (result.success) {
        // Show dispense animation
        showDispenseAnimation();
        
        const message = `${result.message}\nChange: $${result.change.toFixed(2)}`;
        showMessage(message, 'success');
        
        // Update displays
        await updateStatus();
        await loadItems();
        await loadTransactionHistory();
    } else {
        showMessage(result.message, 'error');
        await updateStatus();
    }
}

/**
 * Process refund
 */
async function processRefund() {
    console.log('Processing refund...');
    
    if (!confirm('Are you sure you want to cancel and get a refund?')) {
        return;
    }
    
    const result = await apiCall('/refund', 'POST');
    
    if (result.success) {
        showMessage(result.message, 'success');
        await updateStatus();
    } else {
        showMessage(result.message, 'error');
    }
}

/**
 * Reset machine
 */
async function resetMachine() {
    console.log('Resetting machine...');
    
    if (!confirm('Reset the vending machine to IDLE state?')) {
        return;
    }
    
    const result = await apiCall('/reset', 'POST');
    
    if (result.success) {
        showMessage(result.message, 'info');
        await updateStatus();
        await loadItems();
    } else {
        showMessage(result.message, 'error');
    }
}

/**
 * Load transaction history
 */
async function loadTransactionHistory() {
    const result = await apiCall('/history');
    
    if (result.success) {
        renderTransactionHistory(result.data);
    }
}

/**
 * Render transaction history
 */
function renderTransactionHistory(transactions) {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';
    
    if (transactions.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No transactions yet</div>';
        return;
    }
    
    // Reverse to show latest first
    transactions.reverse().forEach(transaction => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const date = new Date(transaction.timestamp);
        const timeString = date.toLocaleString();
        
        // Handle both single item and multi-item transactions
        let itemDetails = '';
        if (transaction.items) {
            // Multi-item transaction
            itemDetails = transaction.items.map(i => i.name).join(', ');
            itemDetails += ` - $${transaction.total_price.toFixed(2)}`;
        } else {
            // Single item transaction (legacy)
            itemDetails = `${transaction.item_name} - $${transaction.price.toFixed(2)}`;
        }
        
        item.innerHTML = `
            <div class="transaction-time">${timeString}</div>
            <div class="transaction-details">
                ${itemDetails}
                ${transaction.change > 0 ? ` (Change: $${transaction.change.toFixed(2)})` : ''}
            </div>
        `;
        
        historyList.appendChild(item);
    });
}

/**
 * Toggle history display
 */
function toggleHistory() {
    const historyList = document.getElementById('history-list');
    const toggleBtn = document.getElementById('toggle-history-btn');
    
    historyList.classList.toggle('hidden');
    
    if (historyList.classList.contains('hidden')) {
        toggleBtn.innerHTML = '<i class="fas fa-eye"></i> Show History';
    } else {
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide History';
        loadTransactionHistory();
    }
}

/**
 * Show message to user
 */
function showMessage(message, type = 'info') {
    const messageDisplay = document.getElementById('message-display');
    const stateMessage = document.getElementById('state-message');
    
    // Clear previous classes
    messageDisplay.className = 'message-display';
    stateMessage.className = 'state-message';
    
    // Add new class
    messageDisplay.classList.add(type);
    stateMessage.classList.add(type);
    
    // Set message
    messageDisplay.textContent = message;
    stateMessage.textContent = message;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDisplay.textContent = '';
        messageDisplay.className = 'message-display';
        stateMessage.textContent = '';
        stateMessage.className = 'state-message';
    }, 5000);
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

/**
 * Show dispense animation
 */
function showDispenseAnimation() {
    const animation = document.getElementById('dispense-animation');
    animation.classList.remove('hidden');
    
    // Hide after 2 seconds
    setTimeout(() => {
        animation.classList.add('hidden');
    }, 2000);
}
