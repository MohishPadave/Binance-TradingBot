"""
Input validation module
"""
from typing import Tuple, Optional
from logger import logger

class Validator:
    """Validates trading inputs"""
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP']
    
    @staticmethod
    def validate_symbol(symbol: str) -> Tuple[bool, Optional[str]]:
        """Validate trading symbol"""
        if not symbol:
            return False, "Symbol cannot be empty"
        
        symbol = symbol.upper().strip()
        
        if not symbol.endswith('USDT'):
            return False, "Only USDT pairs are supported"
        
        if len(symbol) < 6:
            return False, "Invalid symbol format"
        
        logger.debug(f"Symbol validated: {symbol}")
        return True, symbol
    
    @staticmethod
    def validate_quantity(quantity: str) -> Tuple[bool, Optional[float]]:
        """Validate order quantity"""
        try:
            qty = float(quantity)
            if qty <= 0:
                return False, None
            logger.debug(f"Quantity validated: {qty}")
            return True, qty
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_price(price: str) -> Tuple[bool, Optional[float]]:
        """Validate price"""
        try:
            p = float(price)
            if p <= 0:
                return False, None
            logger.debug(f"Price validated: {p}")
            return True, p
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_side(side: str) -> Tuple[bool, Optional[str]]:
        """Validate order side"""
        side = side.upper().strip()
        if side not in Validator.VALID_SIDES:
            return False, None
        logger.debug(f"Side validated: {side}")
        return True, side
    
    @staticmethod
    def validate_percentage(percentage: str) -> Tuple[bool, Optional[float]]:
        """Validate percentage value"""
        try:
            pct = float(percentage)
            if pct <= 0 or pct > 100:
                return False, None
            logger.debug(f"Percentage validated: {pct}")
            return True, pct
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_integer(value: str, min_val: int = 1) -> Tuple[bool, Optional[int]]:
        """Validate integer value"""
        try:
            val = int(value)
            if val < min_val:
                return False, None
            logger.debug(f"Integer validated: {val}")
            return True, val
        except ValueError:
            return False, None
