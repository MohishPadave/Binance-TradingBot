// API base URL
const API_URL = '';

// Connect to Binance
async function connect() {
    const apiKey = document.getElementById('api-key').value;
    const apiSecret = document.getElementById('api-secret').value;
    
    if (!apiKey || !apiSecret) {
        showStatus('Please enter API credentials', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({api_key: apiKey, api_secret: apiSecret})
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('connection-card').style.display = 'none';
            document.getElementById('trading-section').style.display = 'block';
            document.getElementById('balance').textContent = parseFloat(data.balance).toFixed(2);
            showStatus('Connected successfully!', 'success');
            updatePrices();
        } else {
            showStatus('Connection failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Update prices
async function updatePrices() {
    try {
        const btcResponse = await fetch('/api/price/BTCUSDT');
        const btcData = await btcResponse.json();
        if (btcData.success) {
            document.getElementById('btc-price').textContent = '$' + parseFloat(btcData.price).toLocaleString();
        }
        
        const ethResponse = await fetch('/api/price/ETHUSDT');
        const ethData = await ethResponse.json();
        if (ethData.success) {
            document.getElementById('eth-price').textContent = '$' + parseFloat(ethData.price).toLocaleString();
        }
    } catch (error) {
        console.error('Error updating prices:', error);
    }
}

// Place Market Order
async function placeMarketOrder() {
    const symbol = document.getElementById('market-symbol').value;
    const side = document.getElementById('market-side').value;
    const quantity = document.getElementById('market-quantity').value;
    
    if (!symbol || !quantity) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/market_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, side, quantity})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ Market order placed! Order ID: ${data.order_id}`, 'success');
        } else {
            showStatus('Order failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Place Limit Order
async function placeLimitOrder() {
    const symbol = document.getElementById('limit-symbol').value;
    const side = document.getElementById('limit-side').value;
    const quantity = document.getElementById('limit-quantity').value;
    const price = document.getElementById('limit-price').value;
    
    if (!symbol || !quantity || !price) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/limit_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, side, quantity, price})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ Limit order placed! Order ID: ${data.order_id}`, 'success');
        } else {
            showStatus('Order failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Place Stop-Limit Order
async function placeStopLimitOrder() {
    const symbol = document.getElementById('sl-symbol').value;
    const side = document.getElementById('sl-side').value;
    const quantity = document.getElementById('sl-quantity').value;
    const stop_price = document.getElementById('sl-stop-price').value;
    const limit_price = document.getElementById('sl-limit-price').value;
    
    if (!symbol || !quantity || !stop_price || !limit_price) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/stop_limit_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, side, quantity, stop_price, limit_price})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ Stop-Limit order placed! Order ID: ${data.order_id}`, 'success');
        } else {
            showStatus('Order failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Place OCO Order
async function placeOCOOrder() {
    const symbol = document.getElementById('oco-symbol').value;
    const side = document.getElementById('oco-side').value;
    const quantity = document.getElementById('oco-quantity').value;
    const tp_price = document.getElementById('oco-tp-price').value;
    const sl_price = document.getElementById('oco-sl-price').value;
    
    if (!symbol || !quantity || !tp_price || !sl_price) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/oco_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, side, quantity, tp_price, sl_price})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ OCO orders placed! TP: ${data.tp_order_id}, SL: ${data.sl_order_id}`, 'success');
        } else {
            showStatus('Order failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Place TWAP Order
async function placeTWAPOrder() {
    const symbol = document.getElementById('twap-symbol').value;
    const side = document.getElementById('twap-side').value;
    const quantity = document.getElementById('twap-quantity').value;
    const num_orders = document.getElementById('twap-num-orders').value;
    const interval = document.getElementById('twap-interval').value;
    
    if (!symbol || !quantity || !num_orders || !interval) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    showStatus('⏳ Executing TWAP... This will take some time.', 'info');
    
    try {
        const response = await fetch('/api/twap_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, side, quantity, num_orders, interval})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ ${data.message}`, 'success');
        } else {
            showStatus('TWAP failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Place Grid Order
async function placeGridOrder() {
    const symbol = document.getElementById('grid-symbol').value;
    const lower_price = document.getElementById('grid-lower').value;
    const upper_price = document.getElementById('grid-upper').value;
    const num_grids = document.getElementById('grid-num').value;
    const quantity_per_grid = document.getElementById('grid-quantity').value;
    
    if (!symbol || !lower_price || !upper_price || !num_grids || !quantity_per_grid) {
        showStatus('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/grid_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, lower_price, upper_price, num_grids, quantity_per_grid})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✓ ${data.message}`, 'success');
        } else {
            showStatus('Grid setup failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Load Open Orders
async function loadOpenOrders() {
    try {
        const response = await fetch('/api/open_orders');
        const data = await response.json();
        
        const ordersList = document.getElementById('orders-list');
        
        if (data.success && data.orders.length > 0) {
            ordersList.innerHTML = data.orders.map(order => `
                <div class="order-item">
                    <div class="order-info">
                        <strong>${order.symbol}</strong>
                        <span>${order.type} ${order.side}</span>
                        <span>Qty: ${order.origQty}</span>
                        <span>Price: ${order.price || 'Market'}</span>
                        <span>Status: ${order.status}</span>
                    </div>
                    <button class="btn btn-danger" onclick="cancelOrder('${order.symbol}', ${order.orderId})">Cancel</button>
                </div>
            `).join('');
        } else {
            ordersList.innerHTML = '<p style="text-align: center; color: #666;">No open orders</p>';
        }
    } catch (error) {
        showStatus('Error loading orders: ' + error.message, 'error');
    }
}

// Cancel Order
async function cancelOrder(symbol, orderId) {
    if (!confirm('Cancel this order?')) return;
    
    try {
        const response = await fetch('/api/cancel_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol, order_id: orderId})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus('✓ Order cancelled!', 'success');
            loadOpenOrders();
        } else {
            showStatus('Cancel failed: ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

// Show status message
function showStatus(message, type) {
    const statusDiv = document.getElementById('status-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `status-message status-${type}`;
    messageDiv.textContent = message;
    
    statusDiv.insertBefore(messageDiv, statusDiv.firstChild);
    
    // Remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

// Auto-update prices every 10 seconds
setInterval(updatePrices, 10000);
