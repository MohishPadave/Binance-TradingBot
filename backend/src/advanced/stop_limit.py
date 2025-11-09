"""
Stop-Limit order implementation
"""
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class StopLimitBot(BaseBot):
    """Bot for placing stop-limit orders"""
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                               stop_price: float, limit_price: float):
        """
        Place a stop-limit order
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            stop_price: Stop trigger price
            limit_price: Limit price after stop is triggered
            
        Returns:
            Order response or None
        """
        try:
            logger.info(f"Placing STOP-LIMIT {side} order: {quantity} {symbol}")
            logger.info(f"Stop Price: {stop_price}, Limit Price: {limit_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price
            )
            
            logger.info(f"✓ Stop-Limit order placed successfully!")
            logger.info(f"Order ID: {order['orderId']}")
            logger.info(f"Status: {order['status']}")
            logger.info(f"Stop Price: {order['stopPrice']}")
            logger.info(f"Limit Price: {order['price']}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error placing stop-limit order: {e}")
            return None
