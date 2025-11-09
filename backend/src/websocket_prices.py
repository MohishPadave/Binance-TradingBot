"""
WebSocket Live Price Feed
"""
import json
import asyncio
from binance import AsyncClient, BinanceSocketManager
from logger import logger

class WebSocketPriceFeed:
    """Real-time price updates via WebSocket"""
    
    def __init__(self):
        self.client = None
        self.bsm = None
        self.price_callbacks = []
        self.current_prices = {}
        self.running = False
    
    async def start(self, symbols=['BTCUSDT', 'ETHUSDT']):
        """Start WebSocket connection"""
        try:
            self.client = await AsyncClient.create()
            self.bsm = BinanceSocketManager(self.client)
            
            # Create multiplex socket for multiple symbols
            streams = [f"{symbol.lower()}@ticker" for symbol in symbols]
            socket = self.bsm.multiplex_socket(streams)
            
            self.running = True
            logger.info(f"WebSocket started for {symbols}")
            
            async with socket as stream:
                while self.running:
                    msg = await stream.recv()
                    if msg:
                        await self._process_message(msg)
                        
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            self.running = False
    
    async def _process_message(self, msg):
        """Process incoming WebSocket message"""
        try:
            if 'data' in msg:
                data = msg['data']
                symbol = data['s']
                price = float(data['c'])  # Current price
                
                self.current_prices[symbol] = {
                    'price': price,
                    'high': float(data['h']),
                    'low': float(data['l']),
                    'volume': float(data['v']),
                    'change': float(data['P'])  # Percentage change
                }
                
                # Notify callbacks
                for callback in self.price_callbacks:
                    await callback(symbol, self.current_prices[symbol])
                    
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}")
    
    def add_price_callback(self, callback):
        """Add callback for price updates"""
        self.price_callbacks.append(callback)
    
    def get_current_price(self, symbol):
        """Get current price from cache"""
        return self.current_prices.get(symbol, {}).get('price', 0)
    
    async def stop(self):
        """Stop WebSocket connection"""
        self.running = False
        if self.client:
            await self.client.close_connection()
        logger.info("WebSocket stopped")

# Global instance
websocket_feed = WebSocketPriceFeed()
