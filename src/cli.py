"""
CLI interface for Binance Futures Trading Bot
"""
import sys
from config import Config
from logger import logger
from validator import Validator
from market_orders import MarketOrderBot
from limit_orders import LimitOrderBot
from advanced.stop_limit import StopLimitBot
from advanced.oco import OCOBot
from advanced.twap import TWAPBot
from advanced.grid import GridBot


class TradingBotCLI:
    """Command-line interface for the trading bot"""
    
    def __init__(self):
        self.bot = None
        self.validator = Validator()
    
    def setup_credentials(self):
        """Setup API credentials"""
        print("\n" + "="*60)
        print("BINANCE FUTURES TRADING BOT - TESTNET")
        print("="*60)
        
        if Config.validate_credentials():
            print("✓ API credentials loaded from environment")
            use_env = input("Use these credentials? (y/n): ").lower()
            if use_env == 'y':
                return True
        
        print("\nPlease enter your Binance Testnet API credentials:")
        api_key = input("API Key: ").strip()
        api_secret = input("API Secret: ").strip()
        
        if not api_key or not api_secret:
            print("❌ API credentials are required!")
            return False
        
        Config.set_credentials(api_key, api_secret)
        return True
    
    def initialize_bot(self):
        """Initialize the bot connection"""
        try:
            self.bot = MarketOrderBot(testnet=True)
            print("✓ Connected to Binance Futures Testnet\n")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("Core Orders:")
        print("  1. Market Order")
        print("  2. Limit Order")
        print("\nAdvanced Orders:")
        print("  3. Stop-Limit Order")
        print("  4. OCO Order (Take Profit + Stop Loss)")
        print("  5. TWAP Order")
        print("  6. Grid Trading")
        print("\nOther:")
        print("  7. View Open Orders")
        print("  8. Cancel Order")
        print("  9. Check Account Balance")
        print("  0. Exit")
        print("="*60)
    
    def get_input(self, prompt: str, validator_func=None) -> any:
        """Get and validate user input"""
        while True:
            value = input(prompt).strip()
            if not value:
                print("❌ Input cannot be empty")
                continue
            
            if validator_func:
                is_valid, validated_value = validator_func(value)
                if is_valid:
                    return validated_value
                else:
                    print(f"❌ Invalid input. Please try again.")
            else:
                return value
    
    def handle_market_order(self):
        """Handle market order placement"""
        print("\n--- MARKET ORDER ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        side = self.get_input("Side (BUY/SELL): ", self.validator.validate_side)
        quantity = self.get_input("Quantity: ", self.validator.validate_quantity)
        
        confirm = input(f"\nConfirm {side} {quantity} {symbol} at MARKET price? (y/n): ")
        if confirm.lower() == 'y':
            bot = MarketOrderBot(testnet=True)
            bot.place_market_order(symbol, side, quantity)
    
    def handle_limit_order(self):
        """Handle limit order placement"""
        print("\n--- LIMIT ORDER ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        side = self.get_input("Side (BUY/SELL): ", self.validator.validate_side)
        quantity = self.get_input("Quantity: ", self.validator.validate_quantity)
        price = self.get_input("Limit Price: ", self.validator.validate_price)
        
        confirm = input(f"\nConfirm {side} {quantity} {symbol} @ {price}? (y/n): ")
        if confirm.lower() == 'y':
            bot = LimitOrderBot(testnet=True)
            bot.place_limit_order(symbol, side, quantity, price)
    
    def handle_stop_limit_order(self):
        """Handle stop-limit order placement"""
        print("\n--- STOP-LIMIT ORDER ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        side = self.get_input("Side (BUY/SELL): ", self.validator.validate_side)
        quantity = self.get_input("Quantity: ", self.validator.validate_quantity)
        stop_price = self.get_input("Stop Price: ", self.validator.validate_price)
        limit_price = self.get_input("Limit Price: ", self.validator.validate_price)
        
        confirm = input(f"\nConfirm STOP-LIMIT {side} {quantity} {symbol}? (y/n): ")
        if confirm.lower() == 'y':
            bot = StopLimitBot(testnet=True)
            bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    
    def handle_oco_order(self):
        """Handle OCO order placement"""
        print("\n--- OCO ORDER (Take Profit + Stop Loss) ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        side = self.get_input("Side (BUY/SELL): ", self.validator.validate_side)
        quantity = self.get_input("Quantity: ", self.validator.validate_quantity)
        tp_price = self.get_input("Take Profit Price: ", self.validator.validate_price)
        sl_price = self.get_input("Stop Loss Price: ", self.validator.validate_price)
        
        confirm = input(f"\nConfirm OCO {side} {quantity} {symbol}? (y/n): ")
        if confirm.lower() == 'y':
            bot = OCOBot(testnet=True)
            bot.place_oco_order(symbol, side, quantity, tp_price, sl_price)
    
    def handle_twap_order(self):
        """Handle TWAP order execution"""
        print("\n--- TWAP ORDER ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        side = self.get_input("Side (BUY/SELL): ", self.validator.validate_side)
        total_qty = self.get_input("Total Quantity: ", self.validator.validate_quantity)
        num_orders = self.get_input("Number of Orders: ", 
                                   lambda x: self.validator.validate_integer(x, 2))
        interval = self.get_input("Interval (seconds): ", 
                                 lambda x: self.validator.validate_integer(x, 1))
        
        confirm = input(f"\nConfirm TWAP {side} {total_qty} {symbol}? (y/n): ")
        if confirm.lower() == 'y':
            bot = TWAPBot(testnet=True)
            bot.execute_twap_order(symbol, side, total_qty, num_orders, interval)
    
    def handle_grid_trading(self):
        """Handle grid trading setup"""
        print("\n--- GRID TRADING ---")
        
        symbol = self.get_input("Symbol (e.g., BTCUSDT): ", self.validator.validate_symbol)
        lower = self.get_input("Lower Price: ", self.validator.validate_price)
        upper = self.get_input("Upper Price: ", self.validator.validate_price)
        num_grids = self.get_input("Number of Grids: ", 
                                   lambda x: self.validator.validate_integer(x, 2))
        qty_per_grid = self.get_input("Quantity per Grid: ", self.validator.validate_quantity)
        
        confirm = input(f"\nConfirm Grid setup for {symbol}? (y/n): ")
        if confirm.lower() == 'y':
            bot = GridBot(testnet=True)
            bot.setup_grid(symbol, lower, upper, num_grids, qty_per_grid)
    
    def handle_view_orders(self):
        """View open orders"""
        print("\n--- OPEN ORDERS ---")
        symbol = input("Symbol (leave empty for all): ").strip().upper() or None
        
        bot = LimitOrderBot(testnet=True)
        orders = bot.get_open_orders(symbol)
        
        if not orders:
            print("No open orders found.")
        else:
            for order in orders:
                print(f"\nOrder ID: {order['orderId']}")
                print(f"Symbol: {order['symbol']}")
                print(f"Type: {order['type']}")
                print(f"Side: {order['side']}")
                print(f"Price: {order.get('price', 'N/A')}")
                print(f"Quantity: {order['origQty']}")
                print(f"Status: {order['status']}")
    
    def handle_cancel_order(self):
        """Cancel an order"""
        print("\n--- CANCEL ORDER ---")
        
        symbol = self.get_input("Symbol: ", self.validator.validate_symbol)
        order_id = self.get_input("Order ID: ", 
                                 lambda x: self.validator.validate_integer(x, 1))
        
        confirm = input(f"\nConfirm cancel order {order_id}? (y/n): ")
        if confirm.lower() == 'y':
            bot = LimitOrderBot(testnet=True)
            bot.cancel_order(symbol, order_id)
    
    def handle_account_balance(self):
        """Check account balance"""
        print("\n--- ACCOUNT BALANCE ---")
        
        bot = MarketOrderBot(testnet=True)
        account = bot.get_account_balance()
        
        if account:
            print(f"Total Wallet Balance: {account.get('totalWalletBalance')} USDT")
            print(f"Available Balance: {account.get('availableBalance')} USDT")
            print(f"Total Unrealized Profit: {account.get('totalUnrealizedProfit')} USDT")
    
    def run(self):
        """Run the CLI application"""
        if not self.setup_credentials():
            return
        
        if not self.initialize_bot():
            return
        
        while True:
            try:
                self.display_menu()
                choice = input("\nSelect option: ").strip()
                
                if choice == '1':
                    self.handle_market_order()
                elif choice == '2':
                    self.handle_limit_order()
                elif choice == '3':
                    self.handle_stop_limit_order()
                elif choice == '4':
                    self.handle_oco_order()
                elif choice == '5':
                    self.handle_twap_order()
                elif choice == '6':
                    self.handle_grid_trading()
                elif choice == '7':
                    self.handle_view_orders()
                elif choice == '8':
                    self.handle_cancel_order()
                elif choice == '9':
                    self.handle_account_balance()
                elif choice == '0':
                    print("\n✓ Exiting bot. Goodbye!")
                    logger.info("Bot terminated by user")
                    break
                else:
                    print("❌ Invalid option. Please try again.")
                
            except KeyboardInterrupt:
                print("\n\n✓ Bot interrupted. Exiting...")
                logger.info("Bot interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.error(f"Unexpected error: {e}")


def main():
    """Main entry point"""
    cli = TradingBotCLI()
    cli.run()


if __name__ == "__main__":
    main()
