#!/usr/bin/env python3
"""
Quick test script to verify Binance connection
"""
import sys
sys.path.insert(0, 'src')

from config import Config
from base_bot import BaseBot

# Set credentials
Config.set_credentials(
    'QN6mQ5PxWbZhZ8h7UBYiwnvpZqAfbwAQ4h8pozxtXgTkkpqfWnkGJNdYD1uhz9in',
    'uqU8sqEe8hldYXWSYtv4mwHYLG59dFtUvpH5hdne4ohWqnMOy1ETQjQiDrxeIz86'
)

print("Testing Binance Testnet Connection...")
print("="*60)

try:
    bot = BaseBot(testnet=True)
    print('✓ Connection successful!')
    print()
    
    # Get account info
    print("Fetching account information...")
    account = bot.get_account_balance()
    if account:
        print(f'Total Balance: {account.get("totalWalletBalance")} USDT')
        print(f'Available Balance: {account.get("availableBalance")} USDT')
    print()
    
    # Get current prices
    print("Fetching current prices...")
    btc_price = bot.get_current_price('BTCUSDT')
    eth_price = bot.get_current_price('ETHUSDT')
    print(f'Current BTC Price: ${btc_price:,.2f}')
    print(f'Current ETH Price: ${eth_price:,.2f}')
    print()
    
    print("="*60)
    print("✓ All tests passed! You're ready to trade.")
    print()
    print("Next step: Run the bot with:")
    print("  python3 src/cli.py")
    
except Exception as e:
    print(f'❌ Error: {e}')
    print()
    print("Troubleshooting:")
    print("1. Check your API credentials are correct")
    print("2. Ensure Futures permission is enabled")
    print("3. Verify internet connection")
