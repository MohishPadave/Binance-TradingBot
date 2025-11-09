"""
Flask API with MongoDB authentication, JWT, and trading features
"""
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from config import Config
from logger import logger
from database import db
from auth import init_auth_service, auth_service
from email_service import email_service
from market_orders import MarketOrderBot
from limit_orders import LimitOrderBot
from advanced.stop_limit import StopLimitBot
from advanced.oco import OCOBot
from advanced.twap import TWAPBot
from advanced.grid import GridBot
from order_history import order_history
from telegram_alerts import telegram_alerts

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
CORS(app, origins=["*"])  # Configure for production
jwt = JWTManager(app)
email_service.init_app(app)

# Initialize database and auth service
if not db.connect():
    logger.error("Failed to connect to MongoDB")
    exit(1)

init_auth_service(app.config['SECRET_KEY'])

# Global bot instance
bot = None

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.json
        
        result = auth_service.register_user(
            email=data.get('email'),
            password=data.get('password'),
            name=data.get('name'),
            api_key=data.get('api_key'),
            api_secret=data.get('api_secret')
        )
        
        if result['success']:
            # Send verification email (optional)
            base_url = request.host_url.rstrip('/')
            email_service.send_verification_email(
                data.get('email'),
                result['verification_token'],
                base_url
            )
            
            return jsonify({
                'success': True,
                'message': 'Registration successful. Please check your email for verification.',
                'user_id': result['user_id']
            })
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        
        result = auth_service.login_user(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/verify-email', methods=['GET'])
def verify_email():
    """Verify user email"""
    try:
        token = request.args.get('token')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token required'}), 400
        
        result = auth_service.verify_email(token)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        email = get_jwt_identity()
        result = auth_service.get_user_profile(email)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/update-credentials', methods=['POST'])
@jwt_required()
def update_credentials():
    """Update API credentials"""
    try:
        email = get_jwt_identity()
        data = request.json
        
        result = auth_service.update_api_credentials(
            email=email,
            api_key=data.get('api_key'),
            api_secret=data.get('api_secret')
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Update credentials error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================================================
# TRADING ROUTES (JWT Protected)
# ============================================================================

@app.route('/api/connect', methods=['POST'])
@jwt_required()
def connect():
    """Connect to Binance using user's stored credentials"""
    global bot
    try:
        email = get_jwt_identity()
        
        # Get user's API credentials from database
        user_result = auth_service.get_user_profile(email)
        if not user_result['success']:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user = user_result['user']
        api_key = user.get('api_key')
        api_secret = user.get('api_secret')
        
        if not api_key or not api_secret:
            return jsonify({'success': False, 'message': 'API credentials not set'}), 400
        
        # Set credentials and connect
        Config.set_credentials(api_key, api_secret)
        bot = MarketOrderBot(testnet=True)
        
        # Get account info
        account = bot.get_account_balance()
        if account:
            balance = account.get('totalWalletBalance', '0')
            return jsonify({
                'success': True,
                'message': 'Connected successfully!',
                'balance': balance
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to get account info'}), 500
            
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/price/<symbol>')
def get_price(symbol):
    """Get current price (public endpoint)"""
    try:
        if not bot:
            # Create temporary bot for price checking
            temp_bot = MarketOrderBot(testnet=True)
            price = temp_bot.get_current_price(symbol)
        else:
            price = bot.get_current_price(symbol)
        
        return jsonify({'success': True, 'price': price})
    except Exception as e:
        logger.error(f"Price error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/market_order', methods=['POST'])
@jwt_required()
def market_order():
    """Place market order"""
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'}), 400
        
        email = get_jwt_identity()
        data = request.json
        
        order_bot = MarketOrderBot(testnet=True)
        order = order_bot.place_market_order(
            data['symbol'],
            data['side'],
            float(data['quantity'])
        )
        
        if order:
            # Store order in database
            order_doc = {
                'user_email': email,
                'order_type': 'MARKET',
                'symbol': data['symbol'],
                'side': data['side'],
                'quantity': float(data['quantity']),
                'price': order.get('avgPrice'),
                'order_id': order['orderId'],
                'status': order['status'],
                'timestamp': datetime.utcnow()
            }
            db.orders.insert_one(order_doc)
            
            # Add to local history
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
        
        return jsonify({'success': False, 'message': 'Order failed'}), 500
        
    except Exception as e:
        logger.error(f"Market order error: {e}")
        telegram_alerts.alert_error(f"Market order failed: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/limit_order', methods=['POST'])
@jwt_required()
def limit_order():
    """Place limit order"""
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'}), 400
        
        email = get_jwt_identity()
        data = request.json
        
        order_bot = LimitOrderBot(testnet=True)
        order = order_bot.place_limit_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['price'])
        )
        
        if order:
            # Store in database
            order_doc = {
                'user_email': email,
                'order_type': 'LIMIT',
                'symbol': data['symbol'],
                'side': data['side'],
                'quantity': float(data['quantity']),
                'price': float(data['price']),
                'order_id': order['orderId'],
                'status': order['status'],
                'timestamp': datetime.utcnow()
            }
            db.orders.insert_one(order_doc)
            
            return jsonify({
                'success': True,
                'message': 'Limit order placed!',
                'order_id': order['orderId'],
                'status': order['status']
            })
        
        return jsonify({'success': False, 'message': 'Order failed'}), 500
        
    except Exception as e:
        logger.error(f"Limit order error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/order_history')
@jwt_required()
def get_order_history():
    """Get user's order history"""
    try:
        email = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        # Get from database
        orders = list(db.orders.find(
            {'user_email': email},
            {'_id': 0}
        ).sort('timestamp', -1).limit(limit))
        
        return jsonify({'success': True, 'history': orders})
        
    except Exception as e:
        logger.error(f"Order history error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/open_orders')
@jwt_required()
def open_orders():
    """Get open orders"""
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'}), 400
        
        order_bot = LimitOrderBot(testnet=True)
        orders = order_bot.get_open_orders()
        
        return jsonify({'success': True, 'orders': orders})
        
    except Exception as e:
        logger.error(f"Open orders error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cancel_order', methods=['POST'])
@jwt_required()
def cancel_order():
    """Cancel an order"""
    try:
        if not bot:
            return jsonify({'success': False, 'message': 'Not connected'}), 400
        
        data = request.json
        order_bot = LimitOrderBot(testnet=True)
        result = order_bot.cancel_order(data['symbol'], int(data['order_id']))
        
        if result:
            return jsonify({'success': True, 'message': 'Order cancelled!'})
        
        return jsonify({'success': False, 'message': 'Cancel failed'}), 500
        
    except Exception as e:
        logger.error(f"Cancel order error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/telegram/config', methods=['POST'])
@jwt_required()
def configure_telegram():
    """Configure Telegram alerts"""
    try:
        data = request.json
        telegram_alerts.bot_token = data.get('bot_token')
        telegram_alerts.chat_id = data.get('chat_id')
        telegram_alerts.enabled = bool(telegram_alerts.bot_token and telegram_alerts.chat_id)
        
        if telegram_alerts.enabled:
            telegram_alerts.send_message("✅ Telegram alerts configured successfully!")
            return jsonify({'success': True, 'message': 'Telegram configured!'})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 400
        
    except Exception as e:
        logger.error(f"Telegram config error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'success': False, 'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'success': False, 'message': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'success': False, 'message': 'Authorization token required'}), 401

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    # Get port from environment (Render/Heroku set this)
    port = int(os.getenv('PORT', 5001))
    
    # Check if running in production
    is_production = os.getenv('RENDER') or os.getenv('DYNO')
    
    print("="*60)
    if is_production:
        print("BINANCE TRADING BOT - PRODUCTION MODE")
        print("="*60)
        print(f"Starting on port {port}")
        print("Environment: Production")
    else:
        print("BINANCE TRADING BOT - DEVELOPMENT MODE")
        print("="*60)
        print(f"API Server: http://localhost:{port}")
        print("Environment: Development")
    
    print("\nFeatures:")
    print("✅ MongoDB Authentication")
    print("✅ Bcrypt Password Hashing")
    print("✅ JWT Token Management")
    print("✅ Email Verification")
    print("✅ Secure Trading API")
    print("="*60)
    
    if is_production:
        # Production mode
        app.run(host='0.0.0.0', port=port)
    else:
        # Development mode with debug
        app.run(debug=True, port=port, host='0.0.0.0')
