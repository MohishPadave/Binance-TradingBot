"""
TWAP (Time-Weighted Average Price) order implementation
"""
import time
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class TWAPBot(BaseBot):
    """Bot for executing TWAP orders"""
    
    def execute_twap_order(self, symbol: str, side: str, total_quantity: float,
                          num_orders: int, interval_seconds: int):
        """
        Execute TWAP order by splitting into smaller orders over time
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            total_quantity: Total quantity to trade
            num_orders: Number of orders to split into
            interval_seconds: Time interval between orders
            
        Returns:
            List of executed orders
        """
        try:
            logger.info(f"Starting TWAP execution: {total_quantity} {symbol}")
            logger.info(f"Split into {num_orders} orders, {interval_seconds}s interval")
            
            quantity_per_order = total_quantity / num_orders
            executed_orders = []
            
            for i in range(num_orders):
                logger.info(f"Executing TWAP order {i+1}/{num_orders}")
                
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=round(quantity_per_order, 3)
                )
                
                executed_orders.append(order)
                logger.info(f"✓ Order {i+1} executed. Order ID: {order['orderId']}")
                logger.info(f"Executed Qty: {order.get('executedQty')}, Avg Price: {order.get('avgPrice')}")
                
                # Wait before next order (except for last order)
                if i < num_orders - 1:
                    logger.info(f"Waiting {interval_seconds} seconds...")
                    time.sleep(interval_seconds)
            
            # Calculate average execution price
            total_cost = sum(float(o.get('avgPrice', 0)) * float(o.get('executedQty', 0)) 
                           for o in executed_orders)
            total_qty = sum(float(o.get('executedQty', 0)) for o in executed_orders)
            avg_price = total_cost / total_qty if total_qty > 0 else 0
            
            logger.info(f"✓ TWAP execution completed!")
            logger.info(f"Total executed: {total_qty} @ avg price {avg_price:.2f}")
            
            return executed_orders
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return []
        except Exception as e:
            logger.error(f"Error executing TWAP order: {e}")
            return []
