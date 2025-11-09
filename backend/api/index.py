"""
Vercel serverless function for Binance Trading Bot API
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import Flask app
from web_ui import app

# Export for Vercel
application = app
