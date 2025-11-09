"""
Order History Management
"""
import json
import os
from datetime import datetime
from logger import logger

class OrderHistory:
    """Manages order history storage and retrieval"""
    
    def __init__(self, history_file='order_history.json'):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self):
        """Load order history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save order history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def add_order(self, order_type, symbol, side, quantity, price=None, 
                  order_id=None, status='FILLED', additional_info=None):
        """Add order to history"""
        order_record = {
            'timestamp': datetime.now().isoformat(),
            'order_type': order_type,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'order_id': order_id,
            'status': status,
            'additional_info': additional_info or {}
        }
        
        self.history.insert(0, order_record)  # Add to beginning
        
        # Keep only last 100 orders
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        self._save_history()
        logger.info(f"Order added to history: {order_type} {side} {quantity} {symbol}")
        
        return order_record
    
    def get_recent_orders(self, limit=10):
        """Get recent orders"""
        return self.history[:limit]
    
    def get_orders_by_symbol(self, symbol, limit=10):
        """Get orders for specific symbol"""
        filtered = [o for o in self.history if o['symbol'] == symbol]
        return filtered[:limit]
    
    def get_orders_by_type(self, order_type, limit=10):
        """Get orders by type"""
        filtered = [o for o in self.history if o['order_type'] == order_type]
        return filtered[:limit]
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self._save_history()
        logger.info("Order history cleared")

# Global instance
order_history = OrderHistory()
