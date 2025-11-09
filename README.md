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

### 🔐 Enterprise-Grade Security
- **MongoDB Database** - Secure user data storage
- **Bcrypt Password Hashing** - Industry-standard encryption
- **JWT Authentication** - Secure token-based sessions
- **Email Verification** - Confirm user identity
- **HTTPS Support** - SSL/TLS encryption ready
- **Protected API Routes** - Authorization required

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
2. **MongoDB** installed and running
   - macOS: `brew install mongodb-community && brew services start mongodb-community`
   - Linux: `sudo apt-get install mongodb && sudo systemctl start mongodb`
   - Windows: Download from https://www.mongodb.com/try/download/community
3. **Binance Testnet Account**:
   - Register at: https://testnet.binancefuture.com
   - Generate API Key and Secret from account settings

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB installed and running

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Generate secure keys
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
# Add these to your .env file

# 5. Verify setup
python3 verify_setup.py

# 6. Start server
cd src
python3 web_ui.py
```

Backend runs on: **http://localhost:5001**

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

## Security Setup

For detailed security configuration including:
- MongoDB setup
- Email verification
- HTTPS/SSL certificates
- Production deployment

See: **[backend/SECURITY_SETUP.md](backend/SECURITY_SETUP.md)**

### Quick HTTPS Setup

```bash
cd backend
./setup_https.sh
```

Choose from:
1. Self-signed certificate (development)
2. Let's Encrypt (production)
3. Nginx reverse proxy (recommended)

## 📁 Project Structure

```
Finance ChatBot/
├── backend/              # Python Flask API
│   ├── src/             # Source code
│   │   ├── advanced/    # Advanced trading strategies
│   │   ├── auth.py      # Authentication (Bcrypt, JWT)
│   │   ├── database.py  # MongoDB integration
│   │   ├── web_ui.py    # Flask API server
│   │   └── ...          # Other modules
│   ├── .env.example     # Environment template
│   ├── requirements.txt # Python dependencies
│   └── *.md            # Documentation
│
├── frontend/            # React Application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.js      # Main app
│   └── package.json    # Node dependencies
│
└── README.md           # This file
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

## 💻 Usage

### Web Interface (Recommended)
1. Start backend: `cd backend/src && python3 web_ui.py`
2. Start frontend: `cd frontend && npm start`
3. Open browser: http://localhost:3000
4. Register/Login and start trading!

### Command Line Interface
```bash
cd backend/src
python3 cli.py
```

**Available Commands**:
- Market Order - Instant execution
- Limit Order - Price-specific orders
- Stop-Limit Order - Conditional orders
- OCO Order - Take profit + stop loss
- TWAP Order - Time-weighted execution
- Grid Trading - Automated range trading

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

## 📊 Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: MongoDB with PyMongo
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: Bcrypt
- **Email**: Flask-Mail
- **Trading**: python-binance

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Design**: Glassmorphism UI

### Security
- Bcrypt password hashing
- JWT token authentication
- MongoDB with indexed collections
- Email verification
- HTTPS/SSL support

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

## 🔒 Security Features

This bot implements **enterprise-grade security**:

✅ **Bcrypt Password Hashing** - Industry-standard encryption  
✅ **MongoDB Database** - Secure data storage with indexes  
✅ **JWT Authentication** - Token-based session management  
✅ **Email Verification** - Confirm user identity  
✅ **HTTPS Support** - SSL/TLS encryption ready  
✅ **Protected API Routes** - Authorization required for trading  

### Security Documentation

- 📖 [Quick Start Guide](backend/QUICK_START.md) - Get running in 5 minutes
- 🔐 [Security Setup](backend/SECURITY_SETUP.md) - Detailed configuration
- ✅ [Security Checklist](backend/SECURITY_CHECKLIST.md) - Implementation verification
- 🏗️ [Architecture](backend/ARCHITECTURE.md) - System design
- 🧪 [Testing Guide](backend/TESTING_GUIDE.md) - Security testing

### Security Best Practices

⚠️ **Important**:
- Never share your API keys
- Use testnet for development/testing
- Enable IP whitelist on Binance
- Use strong passwords (8+ chars, uppercase, lowercase, numbers)
- Keep your API secret secure
- Enable HTTPS in production
- Regular security audits

## 🚀 Deployment to Production

### Backend Deployment (Railway) ⭐ Recommended

Deploy your Flask API to Railway - **better than Render!**

**Why Railway?**
- ✅ No sleep (always on!)
- ✅ $5 free credit monthly
- ✅ Faster deployments
- ✅ Better performance
- ✅ Simpler setup

**Quick Deploy (10 minutes)**:
1. **Setup MongoDB Atlas** (free cloud database)
2. **Push code to GitHub**
3. **Create Railway project**
4. **Add environment variables**
5. **Deploy!**

**📖 Complete Guides**:
- [Railway Deployment Guide](backend/RAILWAY_DEPLOYMENT.md) - Complete step-by-step
- [Railway Quick Start](backend/RAILWAY_QUICK_START.md) - Deploy in 10 minutes
- [Render Alternative](backend/RENDER_DEPLOYMENT.md) - If you prefer Render

**Your API will be live at**: `https://your-app.up.railway.app`

### Frontend Deployment (Vercel/Netlify)

Deploy your React app:

```bash
cd frontend
npm run build
# Deploy to Vercel or Netlify
```

Update `frontend/.env.production`:
```env
REACT_APP_API_URL=https://your-backend.onrender.com
```

---

## Support

For issues or questions:
1. Check the `bot.log` file for error details
2. Verify API credentials are correct
3. Ensure you're using Binance Testnet
4. Check network connectivity
5. Review deployment guides in `backend/` folder

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

This bot is designed for Binance Futures Testnet only. Trading cryptocurrencies involves risk. Always test thoroughly before using real funds.
