"""
Grid trading strategy implementation
"""
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class GridBot(BaseBot):
    """Bot for grid trading strategy"""
    
    def setup_grid(self, symbol: str, lower_price: float, upper_price: float,
                   num_grids: int, quantity_per_grid: float):
        """
        Setup grid trading orders
        
        Args:
            symbol: Trading pair
            lower_price: Lower bound of grid
            upper_price: Upper bound of grid
            num_grids: Number of grid levels
            quantity_per_grid: Quantity for each grid order
            
        Returns:
            List of placed orders
        """
        try:
            logger.info(f"Setting up Grid Trading for {symbol}")
            logger.info(f"Range: {lower_price} - {upper_price}, Grids: {num_grids}")
            
            current_price = self.get_current_price(symbol)
            logger.info(f"Current price: {current_price}")
            
            # Calculate grid levels
            price_step = (upper_price - lower_price) / (num_grids - 1)
            grid_levels = [lower_price + (i * price_step) for i in range(num_grids)]
            
            placed_orders = []
            
            for level in grid_levels:
                # Place buy orders below current price
                if level < current_price:
                    try:
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side='BUY',
                            type='LIMIT',
                            timeInForce='GTC',
                            quantity=quantity_per_grid,
                            price=round(level, 2)
                        )
                        placed_orders.append(order)
                        logger.info(f"✓ BUY grid order @ {level:.2f}, Order ID: {order['orderId']}")
                    except Exception as e:
                        logger.error(f"Failed to place BUY order @ {level:.2f}: {e}")
                
                # Place sell orders above current price
                elif level > current_price:
                    try:
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side='SELL',
                            type='LIMIT',
                            timeInForce='GTC',
                            quantity=quantity_per_grid,
                            price=round(level, 2)
                        )
                        placed_orders.append(order)
                        logger.info(f"✓ SELL grid order @ {level:.2f}, Order ID: {order['orderId']}")
                    except Exception as e:
                        logger.error(f"Failed to place SELL order @ {level:.2f}: {e}")
            
            logger.info(f"✓ Grid setup completed! {len(placed_orders)} orders placed")
            return placed_orders
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return []
        except Exception as e:
            logger.error(f"Error setting up grid: {e}")
            return []
    
    def cancel_all_grid_orders(self, symbol: str):
        """Cancel all open orders for the symbol"""
        try:
            logger.info(f"Cancelling all grid orders for {symbol}")
            
            result = self.client.futures_cancel_all_open_orders(symbol=symbol)
            
            logger.info(f"✓ All grid orders cancelled")
            return result
            
        except Exception as e:
            logger.error(f"Error cancelling grid orders: {e}")
            return None
