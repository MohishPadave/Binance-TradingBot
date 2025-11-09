"""
OCO (One-Cancels-the-Other) order implementation
Note: Binance Futures doesn't support native OCO orders,
so we implement a simulated version with stop-loss and take-profit
"""
from binance.exceptions import BinanceAPIException
from base_bot import BaseBot
from logger import logger

class OCOBot(BaseBot):
    """Bot for placing OCO-style orders (Take Profit + Stop Loss)"""
    
    def place_oco_order(self, symbol: str, side: str, quantity: float,
                        take_profit_price: float, stop_loss_price: float):
        """
        Place OCO-style order (Take Profit + Stop Loss)
        
        Args:
            symbol: Trading pair
            side: BUY or SELL (for the closing position)
            quantity: Order quantity
            take_profit_price: Take profit price
            stop_loss_price: Stop loss price
            
        Returns:
            Tuple of (take_profit_order, stop_loss_order)
        """
        try:
            logger.info(f"Placing OCO orders: {quantity} {symbol}")
            logger.info(f"Take Profit: {take_profit_price}, Stop Loss: {stop_loss_price}")
            
            # Place Take Profit (Limit Order)
            tp_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='TAKE_PROFIT',
                timeInForce='GTC',
                quantity=quantity,
                stopPrice=take_profit_price,
                price=take_profit_price
            )
            
            logger.info(f"✓ Take Profit order placed! Order ID: {tp_order['orderId']}")
            
            # Place Stop Loss (Stop Market Order)
            sl_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_MARKET',
                quantity=quantity,
                stopPrice=stop_loss_price
            )
            
            logger.info(f"✓ Stop Loss order placed! Order ID: {sl_order['orderId']}")
            logger.info(f"✓ OCO orders placed successfully!")
            
            return tp_order, sl_order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None, None
        except Exception as e:
            logger.error(f"Error placing OCO orders: {e}")
            return None, None
    
    def cancel_oco_orders(self, symbol: str, tp_order_id: int, sl_order_id: int):
        """Cancel both OCO orders"""
        try:
            logger.info(f"Cancelling OCO orders for {symbol}")
            
            # Cancel Take Profit
            self.client.futures_cancel_order(symbol=symbol, orderId=tp_order_id)
            logger.info(f"✓ Take Profit order cancelled")
            
            # Cancel Stop Loss
            self.client.futures_cancel_order(symbol=symbol, orderId=sl_order_id)
            logger.info(f"✓ Stop Loss order cancelled")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling OCO orders: {e}")
            return False
