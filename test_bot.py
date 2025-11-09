"""
Test script for Binance Futures Trading Bot
Run this to verify all components work correctly
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from validator import Validator
from logger import logger

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from market_orders import MarketOrderBot
        from limit_orders import LimitOrderBot
        from advanced.stop_limit import StopLimitBot
        from advanced.oco import OCOBot
        from advanced.twap import TWAPBot
        from advanced.grid import GridBot
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_validator():
    """Test validation functions"""
    print("\nTesting validators...")
    validator = Validator()
    
    # Test symbol validation
    valid, symbol = validator.validate_symbol("BTCUSDT")
    assert valid and symbol == "BTCUSDT", "Symbol validation failed"
    
    # Test quantity validation
    valid, qty = validator.validate_quantity("0.001")
    assert valid and qty == 0.001, "Quantity validation failed"
    
    # Test price validation
    valid, price = validator.validate_price("50000")
    assert valid and price == 50000.0, "Price validation failed"
    
    # Test side validation
    valid, side = validator.validate_side("buy")
    assert valid and side == "BUY", "Side validation failed"
    
    print("✓ All validators working")
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    # Test config values
    assert Config.TESTNET_BASE_URL == "https://testnet.binancefuture.com"
    assert Config.LOG_FILE == "bot.log"
    
    print("✓ Configuration correct")
    return True

def test_logger():
    """Test logging"""
    print("\nTesting logger...")
    
    logger.info("Test log entry")
    logger.debug("Test debug entry")
    logger.warning("Test warning entry")
    
    # Check if log file exists
    if os.path.exists("bot.log"):
        print("✓ Logger working, bot.log created")
        return True
    else:
        print("❌ Log file not created")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("BINANCE FUTURES BOT - COMPONENT TEST")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Validators", test_validator),
        ("Configuration", test_config),
        ("Logger", test_logger),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("\nYou can now run the bot with: python src/cli.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the errors before running the bot")
    print("="*60)

if __name__ == "__main__":
    main()
