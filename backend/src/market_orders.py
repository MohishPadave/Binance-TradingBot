"""
Market order implementation
"""
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class MarketOrderBot(BaseBot):
    """Bot for placing market orders"""
    
    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response or None
        """
        try:
            logger.info(f"Placing MARKET {side} order: {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"✓ Market order placed successfully!")
            logger.info(f"Order ID: {order['orderId']}")
            logger.info(f"Status: {order['status']}")
            logger.info(f"Executed Quantity: {order.get('executedQty', 'N/A')}")
            logger.info(f"Average Price: {order.get('avgPrice', 'N/A')}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            return None
