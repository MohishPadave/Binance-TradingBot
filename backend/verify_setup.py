#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all security components are properly configured
"""

import os
import sys
from dotenv import load_dotenv

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_mark(passed):
    return f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print(f"{RED}❌ .env file not found{RESET}")
        print(f"{YELLOW}   Run: cp .env.example .env{RESET}")
        return False
    
    load_dotenv()
    
    required_vars = {
        'SECRET_KEY': 'Flask secret key',
        'JWT_SECRET_KEY': 'JWT secret key',
        'MONGODB_URI': 'MongoDB connection string',
    }
    
    optional_vars = {
        'MAIL_SERVER': 'Email server',
        'MAIL_USERNAME': 'Email username',
        'MAIL_PASSWORD': 'Email password',
        'TELEGRAM_BOT_TOKEN': 'Telegram bot token',
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value not in ['your-secret-key-change-in-production', 
                                     'your-jwt-secret-key-change-in-production',
                                     'mongodb://localhost:27017/']:
            print(f"{check_mark(True)} {var}: {description}")
        else:
            print(f"{check_mark(False)} {var}: {description} - {YELLOW}Not configured{RESET}")
            all_good = False
    
    print(f"\n{YELLOW}Optional configurations:{RESET}")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        configured = bool(value and value != 'your_email@gmail.com')
        print(f"{check_mark(configured)} {var}: {description}")
    
    return all_good

def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking Python dependencies...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('flask_jwt_extended', 'Flask-JWT-Extended'),
        ('pymongo', 'PyMongo'),
        ('bcrypt', 'Bcrypt'),
        ('dotenv', 'python-dotenv'),
        ('flask_mail', 'Flask-Mail'),
        ('itsdangerous', 'itsdangerous'),
        ('binance', 'python-binance'),
    ]
    
    all_installed = True
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"{check_mark(True)} {name}")
        except ImportError:
            print(f"{check_mark(False)} {name} - {YELLOW}Not installed{RESET}")
            all_installed = False
    
    if not all_installed:
        print(f"\n{YELLOW}Install missing packages with:{RESET}")
        print(f"  pip install -r requirements.txt")
    
    return all_installed

def check_mongodb():
    """Check MongoDB connection"""
    print("\nChecking MongoDB connection...")
    
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        load_dotenv()
        uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        
        print(f"{check_mark(True)} MongoDB is running and accessible")
        print(f"   URI: {uri}")
        
        # Check database
        db = client['binance_trading_bot']
        collections = db.list_collection_names()
        
        if collections:
            print(f"   Collections: {', '.join(collections)}")
        else:
            print(f"   {YELLOW}No collections yet (will be created on first use){RESET}")
        
        client.close()
        return True
        
    except ConnectionFailure:
        print(f"{check_mark(False)} MongoDB connection failed")
        print(f"{YELLOW}   Make sure MongoDB is running:{RESET}")
        print(f"   macOS: brew services start mongodb-community")
        print(f"   Linux: sudo systemctl start mongodb")
        return False
    except Exception as e:
        print(f"{check_mark(False)} Error: {str(e)}")
        return False

def check_ssl_certificates():
    """Check if SSL certificates exist"""
    print("\nChecking SSL/TLS certificates...")
    
    has_self_signed = os.path.exists('cert.pem') and os.path.exists('key.pem')
    
    if has_self_signed:
        print(f"{check_mark(True)} Self-signed certificates found (cert.pem, key.pem)")
        print(f"   {YELLOW}Good for development, not for production{RESET}")
    else:
        print(f"{check_mark(False)} No SSL certificates found")
        print(f"{YELLOW}   Generate with: ./setup_https.sh{RESET}")
    
    # Check for Let's Encrypt certificates
    if os.path.exists('/etc/letsencrypt/live'):
        print(f"{check_mark(True)} Let's Encrypt directory exists")
    
    return has_self_signed

def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking file structure...")
    
    required_files = [
        'src/web_ui.py',
        'src/auth.py',
        'src/database.py',
        'src/email_service.py',
        'src/config.py',
        'src/logger.py',
        'requirements.txt',
        '.env.example',
    ]
    
    all_exist = True
    
    for file in required_files:
        exists = os.path.exists(file)
        print(f"{check_mark(exists)} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def generate_secret_keys():
    """Generate secure secret keys"""
    import secrets
    
    print(f"\n{YELLOW}Generate new secret keys:{RESET}")
    print(f"\nAdd these to your .env file:")
    print(f"\nSECRET_KEY={secrets.token_hex(32)}")
    print(f"JWT_SECRET_KEY={secrets.token_hex(32)}")
    print()

def main():
    print_header("Security Setup Verification")
    
    # Change to backend directory if needed
    if os.path.exists('backend'):
        os.chdir('backend')
    
    checks = {
        'File Structure': check_file_structure(),
        'Dependencies': check_dependencies(),
        'Environment': check_env_file(),
        'MongoDB': check_mongodb(),
        'SSL Certificates': check_ssl_certificates(),
    }
    
    print_header("Summary")
    
    for check_name, passed in checks.items():
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"{check_name:.<40} {status}")
    
    all_passed = all(checks.values())
    
    print()
    
    if all_passed:
        print(f"{GREEN}✅ All checks passed! You're ready to go.{RESET}")
        print(f"\nStart the server with:")
        print(f"  cd src && python web_ui.py")
    else:
        print(f"{YELLOW}⚠️  Some checks failed. Please fix the issues above.{RESET}")
        
        if not checks['Environment']:
            generate_secret_keys()
    
    print()
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
