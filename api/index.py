"""
Vercel serverless function for Binance Trading Bot API
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import Flask app
from src.web_ui import app

# Vercel handler
def handler(request, response):
    return app(request, response)
