"""
Telegram Alert System
"""
import requests
from logger import logger
from config import Config

class TelegramAlerts:
    """Send trading alerts via Telegram"""
    
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or Config.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or Config.TELEGRAM_CHAT_ID
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            logger.warning("Telegram alerts disabled - no credentials provided")
    
    def send_message(self, message):
        """Send message to Telegram"""
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=5)
            
            if response.status_code == 200:
                logger.info("Telegram alert sent successfully")
                return True
            else:
                logger.error(f"Telegram alert failed: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False
    
    def alert_order_executed(self, order_type, symbol, side, quantity, price=None):
        """Alert when order is executed"""
        price_str = f" @ ${price:,.2f}" if price else ""
        message = f"""
🎯 <b>Order Executed</b>

Type: {order_type}
Symbol: {symbol}
Side: {side}
Quantity: {quantity}{price_str}

✅ Order filled successfully!
"""
        return self.send_message(message)
    
    def alert_stop_loss_triggered(self, symbol, side, quantity, trigger_price):
        """Alert when stop-loss is triggered"""
        message = f"""
🛑 <b>Stop-Loss Triggered</b>

Symbol: {symbol}
Side: {side}
Quantity: {quantity}
Trigger Price: ${trigger_price:,.2f}

⚠️ Position closed to limit losses
"""
        return self.send_message(message)
    
    def alert_take_profit_hit(self, symbol, side, quantity, target_price):
        """Alert when take-profit is hit"""
        message = f"""
💰 <b>Take Profit Hit</b>

Symbol: {symbol}
Side: {side}
Quantity: {quantity}
Target Price: ${target_price:,.2f}

🎉 Profit target reached!
"""
        return self.send_message(message)
    
    def alert_price_target(self, symbol, current_price, target_price, direction):
        """Alert when price hits target"""
        emoji = "📈" if direction == "above" else "📉"
        message = f"""
{emoji} <b>Price Alert</b>

Symbol: {symbol}
Current Price: ${current_price:,.2f}
Target Price: ${target_price:,.2f}

Price is now {direction} your target!
"""
        return self.send_message(message)
    
    def alert_error(self, error_message):
        """Alert on errors"""
        message = f"""
❌ <b>Trading Bot Error</b>

{error_message}

Please check the logs for details.
"""
        return self.send_message(message)

# Global instance
telegram_alerts = TelegramAlerts()
