# 🚀 Binance Futures Trading Bot - Professional Web Platform

A complete, production-ready trading platform for Binance USDT-M Futures with modern React UI, real-time features, and comprehensive order management.

![Platform](https://img.shields.io/badge/Platform-Web-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![React](https://img.shields.io/badge/React-18-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Live Demo

**Frontend**: http://localhost:3000  
**Backend API**: http://localhost:5001

## 📸 Screenshots

### Dashboard
Modern glassmorphism design with live price feeds

### Order Management
6 order types with intuitive interface

### Mobile Responsive
Perfect experience on all devices

## ✨ Features

### 🎨 Modern Web Interface
- **React 18** with Hooks
- **Tailwind CSS** for styling
- **Glassmorphism** design
- **Fully Responsive** (Mobile, Tablet, Desktop)
- **Dark Theme** optimized

### 🔐 Authentication System
- **Login/Signup** with local storage
- **Auto-login** for returning users
- **Secure** credential management
- **API key** storage

### 📊 Core Trading Features
- ✅ **Market Orders** - Instant execution
- ✅ **Limit Orders** - Price-specific orders
- ✅ **Stop-Limit Orders** - Conditional orders
- ✅ **OCO Orders** - Take Profit + Stop Loss
- ✅ **TWAP Orders** - Time-weighted execution
- ✅ **Grid Trading** - Automated range trading

### 🚀 Advanced Features
- ✅ **Order History** - Track all trades (last 100)
- ✅ **Telegram Alerts** - Real-time notifications
- ✅ **Live Prices** - Updates every 2 seconds
- ✅ **Open Orders** - View and cancel orders
- ✅ **Account Balance** - Real-time balance display

### 📚 Education
- ✅ **Blog Section** - Learn all order types
- ✅ **Trading Glossary** - Key terms explained
- ✅ **Risk Warnings** - Important information

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Binance Testnet Account**:
   - Register at: https://testnet.binancefuture.com
   - Generate API Key and Secret from account settings

## Installation

1. **Extract the project files**
```bash
unzip [your_name]_binance_bot.zip
cd [project_root]
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Configuration

### Option 1: Environment Variables (Recommended)
```bash
export BINANCE_TESTNET_API_KEY="your_api_key_here"
export BINANCE_TESTNET_API_SECRET="your_api_secret_here"
```

### Option 2: Manual Input
The bot will prompt you for credentials when you run it.

## Usage

### Start the Bot
```bash
python src/cli.py
```

### Main Menu Options

```
1. Market Order       - Execute immediate trades
2. Limit Order        - Place orders at specific prices
3. Stop-Limit Order   - Conditional limit orders
4. OCO Order          - Take profit + stop loss combo
5. TWAP Order         - Split large orders over time
6. Grid Trading       - Automated range trading
7. View Open Orders   - Check pending orders
8. Cancel Order       - Cancel specific order
9. Account Balance    - View account info
0. Exit              - Close the bot
```

## Examples

### Example 1: Market Order
```
Select option: 1
Symbol: BTCUSDT
Side: BUY
Quantity: 0.001
Confirm? y
✓ Market order placed successfully!
```

### Example 2: Limit Order
```
Select option: 2
Symbol: ETHUSDT
Side: SELL
Quantity: 0.01
Limit Price: 2500
Confirm? y
✓ Limit order placed successfully!
```

### Example 3: TWAP Order
```
Select option: 5
Symbol: BTCUSDT
Side: BUY
Total Quantity: 0.01
Number of Orders: 5
Interval (seconds): 10
Confirm? y
✓ TWAP execution completed!
```

### Example 4: Grid Trading
```
Select option: 6
Symbol: BTCUSDT
Lower Price: 30000
Upper Price: 35000
Number of Grids: 10
Quantity per Grid: 0.001
Confirm? y
✓ Grid setup completed!
```

## Project Structure

```
[project_root]/
│
├── /src/
│   ├── cli.py              # Main CLI interface
│   ├── config.py           # Configuration settings
│   ├── logger.py           # Logging setup
│   ├── validator.py        # Input validation
│   ├── base_bot.py         # Base bot class
│   ├── market_orders.py    # Market order implementation
│   ├── limit_orders.py     # Limit order implementation
│   │
│   └── /advanced/
│       ├── __init__.py
│       ├── stop_limit.py   # Stop-limit orders
│       ├── oco.py          # OCO orders
│       ├── twap.py         # TWAP strategy
│       └── grid.py         # Grid trading
│
├── bot.log                 # Execution logs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Logging

All bot activities are logged to `bot.log` with timestamps:
- API connections
- Order placements
- Order executions
- Errors and exceptions
- User actions

Example log entry:
```
2024-01-15 10:30:45 - BinanceBot - INFO - Placing MARKET BUY order: 0.001 BTCUSDT
2024-01-15 10:30:46 - BinanceBot - INFO - ✓ Market order placed successfully!
2024-01-15 10:30:46 - BinanceBot - INFO - Order ID: 12345678
```

## Validation

The bot validates all inputs:
- **Symbol**: Must be valid USDT pair (e.g., BTCUSDT, ETHUSDT)
- **Quantity**: Must be positive number
- **Price**: Must be positive number
- **Side**: Must be BUY or SELL
- **Percentages**: Must be between 0-100
- **Integers**: Must be valid positive integers

## Error Handling

The bot handles various error scenarios:
- Invalid API credentials
- Network connectivity issues
- Invalid trading pairs
- Insufficient balance
- Invalid order parameters
- API rate limits

## Safety Features

- **Testnet Only**: Configured for Binance Testnet (no real money)
- **Confirmation Prompts**: Requires confirmation before placing orders
- **Input Validation**: Validates all user inputs
- **Comprehensive Logging**: Tracks all actions for audit
- **Error Recovery**: Graceful error handling

## Troubleshooting

### Connection Issues
```
❌ Failed to connect: Invalid API credentials
```
**Solution**: Verify your API key and secret are correct

### Invalid Symbol
```
❌ Invalid input. Please try again.
```
**Solution**: Use valid USDT pairs (BTCUSDT, ETHUSDT, etc.)

### Insufficient Balance
```
❌ Binance API Error: Insufficient balance
```
**Solution**: Add testnet funds to your account

## API Documentation

- Binance Futures API: https://binance-docs.github.io/apidocs/futures/en/
- Python-Binance Library: https://python-binance.readthedocs.io/

## Security Notes

⚠️ **Important Security Practices**:
- Never share your API keys
- Use testnet for development/testing
- Enable IP whitelist on Binance
- Use read-only keys when possible
- Keep your API secret secure

## Support

For issues or questions:
1. Check the `bot.log` file for error details
2. Verify API credentials are correct
3. Ensure you're using Binance Testnet
4. Check network connectivity

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

This bot is designed for Binance Futures Testnet only. Trading cryptocurrencies involves risk. Always test thoroughly before using real funds.
