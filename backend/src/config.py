"""
Configuration module for Binance Futures Trading Bot
"""
import os
from typing import Optional

class Config:
    """Configuration class for API credentials and settings"""
    
    # Binance Testnet Configuration
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    # API Credentials (to be set via environment variables or direct input)
    API_KEY: Optional[str] = os.getenv('BINANCE_TESTNET_API_KEY')
    API_SECRET: Optional[str] = os.getenv('BINANCE_TESTNET_API_SECRET')
    
    # Trading Configuration
    DEFAULT_SYMBOL = "BTCUSDT"
    MIN_QUANTITY = 0.001
    
    # Logging Configuration
    LOG_FILE = "bot.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv('TELEGRAM_CHAT_ID')
    
    @classmethod
    def set_credentials(cls, api_key: str, api_secret: str):
        """Set API credentials"""
        cls.API_KEY = api_key
        cls.API_SECRET = api_secret
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that credentials are set"""
        return bool(cls.API_KEY and cls.API_SECRET)
