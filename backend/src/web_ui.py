"""
Web UI for Binance Futures Trading Bot
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from config import Config
from market_orders import MarketOrderBot
from limit_orders import LimitOrderBot
from advanced.stop_limit import StopLimitBot
from advanced.oco import OCOBot
from advanced.twap import TWAPBot
from advanced.grid import GridBot
from logger import logger
from order_history import order_history
from telegram_alerts import telegram_alerts

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
bot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/connect', methods=['POST'])
def connect():
    global bot
    try:
        data = request.json
        Config.set_credentials(data['api_key'], data['api_secret'])
        bot = MarketOrderBot(testnet=True)
        
        account = bot.get_account_balance()
        balance = account.get('totalWalletBalance', '0')
        
        return jsonify({
            'success': True,
            'message': 'Connected successfully!',
            'balance': balance
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/price/<symbol>')
def get_price(symbol):
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        price = bot.get_current_price(symbol)
        return jsonify({'success': True, 'price': price})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/market_order', methods=['POST'])
def market_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = MarketOrderBot(testnet=True)
        order = order_bot.place_market_order(
            data['symbol'],
            data['side'],
            float(data['quantity'])
        )
        
        if order:
            # Add to history
            order_history.add_order(
                'MARKET',
                data['symbol'],
                data['side'],
                float(data['quantity']),
                order.get('avgPrice'),
                order['orderId'],
                order['status']
            )
            
            # Send Telegram alert
            telegram_alerts.alert_order_executed(
                'MARKET',
                data['symbol'],
                data['side'],
                float(data['quantity']),
                float(order.get('avgPrice', 0))
            )
            
            return jsonify({
                'success': True,
                'message': 'Market order placed!',
                'order_id': order['orderId'],
                'status': order['status']
            })
        return jsonify({'success': False, 'message': 'Order failed'})
    except Exception as e:
        telegram_alerts.alert_error(f"Market order failed: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/limit_order', methods=['POST'])
def limit_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = LimitOrderBot(testnet=True)
        order = order_bot.place_limit_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['price'])
        )
        
        if order:
            return jsonify({
                'success': True,
                'message': 'Limit order placed!',
                'order_id': order['orderId'],
                'status': order['status']
            })
        return jsonify({'success': False, 'message': 'Order failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/stop_limit_order', methods=['POST'])
def stop_limit_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = StopLimitBot(testnet=True)
        order = order_bot.place_stop_limit_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['stop_price']),
            float(data['limit_price'])
        )
        
        if order:
            return jsonify({
                'success': True,
                'message': 'Stop-Limit order placed!',
                'order_id': order['orderId']
            })
        return jsonify({'success': False, 'message': 'Order failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/oco_order', methods=['POST'])
def oco_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = OCOBot(testnet=True)
        tp_order, sl_order = order_bot.place_oco_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['tp_price']),
            float(data['sl_price'])
        )
        
        if tp_order and sl_order:
            return jsonify({
                'success': True,
                'message': 'OCO orders placed!',
                'tp_order_id': tp_order['orderId'],
                'sl_order_id': sl_order['orderId']
            })
        return jsonify({'success': False, 'message': 'Order failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/twap_order', methods=['POST'])
def twap_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = TWAPBot(testnet=True)
        orders = order_bot.execute_twap_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            int(data['num_orders']),
            int(data['interval'])
        )
        
        if orders:
            return jsonify({
                'success': True,
                'message': f'TWAP completed! {len(orders)} orders executed',
                'num_orders': len(orders)
            })
        return jsonify({'success': False, 'message': 'TWAP failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/grid_order', methods=['POST'])
def grid_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = GridBot(testnet=True)
        orders = order_bot.setup_grid(
            data['symbol'],
            float(data['lower_price']),
            float(data['upper_price']),
            int(data['num_grids']),
            float(data['quantity_per_grid'])
        )
        
        if orders:
            return jsonify({
                'success': True,
                'message': f'Grid setup! {len(orders)} orders placed',
                'num_orders': len(orders)
            })
        return jsonify({'success': False, 'message': 'Grid setup failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/open_orders')
def open_orders():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        order_bot = LimitOrderBot(testnet=True)
        orders = order_bot.get_open_orders()
        
        return jsonify({
            'success': True,
            'orders': orders
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/cancel_order', methods=['POST'])
def cancel_order():
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'})
        
        data = request.json
        order_bot = LimitOrderBot(testnet=True)
        result = order_bot.cancel_order(data['symbol'], int(data['order_id']))
        
        if result:
            return jsonify({'success': True, 'message': 'Order cancelled!'})
        return jsonify({'success': False, 'message': 'Cancel failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/order_history')
def get_order_history():
    try:
        limit = request.args.get('limit', 10, type=int)
        history = order_history.get_recent_orders(limit)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/telegram/config', methods=['POST'])
def configure_telegram():
    try:
        data = request.json
        telegram_alerts.bot_token = data.get('bot_token')
        telegram_alerts.chat_id = data.get('chat_id')
        telegram_alerts.enabled = bool(telegram_alerts.bot_token and telegram_alerts.chat_id)
        
        if telegram_alerts.enabled:
            telegram_alerts.send_message("✅ Telegram alerts configured successfully!")
            return jsonify({'success': True, 'message': 'Telegram configured!'})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/telegram/test', methods=['POST'])
def test_telegram():
    try:
        result = telegram_alerts.send_message("🧪 Test message from Binance Trading Bot")
        if result:
            return jsonify({'success': True, 'message': 'Test message sent!'})
        return jsonify({'success': False, 'message': 'Failed to send message'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("="*60)
    print("BINANCE FUTURES TRADING BOT - WEB UI")
    print("="*60)
    print("\nStarting web server...")
    print("API Server: http://localhost:5001")
    print("React UI will be at: http://localhost:3000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60)
    app.run(debug=True, port=5001)
