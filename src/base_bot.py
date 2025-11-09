"""
Base bot class with Binance client initialization
"""
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import Config
from logger import logger

class BaseBot:
    """Base trading bot with Binance client"""
    
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        """
        Initialize the bot with API credentials
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (default: True)
        """
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            logger.error("API credentials not provided")
            raise ValueError("API key and secret are required")
        
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=testnet)
            
            # Test connection
            self.client.futures_ping()
            logger.info("Successfully connected to Binance Futures Testnet")
            
            # Get account info
            account = self.client.futures_account()
            logger.info(f"Account connected. Total Balance: {account.get('totalWalletBalance', 'N/A')} USDT")
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise
    
    def get_symbol_info(self, symbol: str):
        """Get symbol information"""
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except Exception as e:
            logger.error(f"Error getting symbol info: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> float:
        """Get current market price for symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.debug(f"Current price for {symbol}: {price}")
            return price
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return 0.0
    
    def get_account_balance(self):
        """Get account balance"""
        try:
            account = self.client.futures_account()
            return account
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return None
