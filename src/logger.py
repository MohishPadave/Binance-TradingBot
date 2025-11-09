"""
Logging module for the trading bot
"""
import logging
from config import Config

def setup_logger(name: str = "BinanceBot") -> logging.Logger:
    """
    Setup and configure logger for the trading bot
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Global logger instance
logger = setup_logger()
