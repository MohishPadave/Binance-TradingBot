"""
Limit order implementation
"""
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class LimitOrderBot(BaseBot):
    """Bot for placing limit orders"""
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Place a limit order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response or None
        """
        try:
            logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} @ {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',  # Good Till Cancel
                quantity=quantity,
                price=price
            )
            
            logger.info(f"✓ Limit order placed successfully!")
            logger.info(f"Order ID: {order['orderId']}")
            logger.info(f"Status: {order['status']}")
            logger.info(f"Price: {order['price']}")
            logger.info(f"Quantity: {order['origQty']}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return None
    
    def cancel_order(self, symbol: str, order_id: int):
        """Cancel an open order"""
        try:
            logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"✓ Order cancelled successfully!")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return None
    
    def get_open_orders(self, symbol: str = None):
        """Get all open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            
            logger.info(f"Found {len(orders)} open orders")
            return orders
            
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            return []
