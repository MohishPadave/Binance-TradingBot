"""
Vercel serverless function entry point
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from web_ui import app

# Export for Vercel
handler = app
