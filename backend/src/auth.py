"""
Authentication module with MongoDB, bcrypt, and JWT
"""
import bcrypt
import re
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from logger import logger
from database import db

class AuthService:
    """Authentication service with secure password hashing and JWT"""
    
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.serializer = URLSafeTimedSerializer(secret_key)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"
    
    def generate_verification_token(self, email: str) -> str:
        """Generate email verification token"""
        return self.serializer.dumps(email, salt='email-verification')
    
    def verify_token(self, token: str, max_age: int = 3600) -> str:
        """Verify token and return email"""
        try:
            email = self.serializer.loads(token, salt='email-verification', max_age=max_age)
            return email
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    def register_user(self, email: str, password: str, name: str, api_key: str = None, api_secret: str = None):
        """Register new user"""
        try:
            # Validate email
            if not self.validate_email(email):
                return {'success': False, 'message': 'Invalid email format'}
            
            # Validate password
            is_valid, message = self.validate_password(password)
            if not is_valid:
                return {'success': False, 'message': message}
            
            # Check if user exists
            if db.users.find_one({'email': email}):
                return {'success': False, 'message': 'Email already registered'}
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Create user document
            user = {
                'email': email,
                'password': hashed_password,
                'name': name,
                'api_key': api_key,
                'api_secret': api_secret,
                'email_verified': False,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Insert into database
            result = db.users.insert_one(user)
            
            # Generate verification token
            verification_token = self.generate_verification_token(email)
            
            logger.info(f"User registered: {email}")
            
            return {
                'success': True,
                'message': 'Registration successful',
                'user_id': str(result.inserted_id),
                'verification_token': verification_token
            }
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {'success': False, 'message': str(e)}
    
    def login_user(self, email: str, password: str):
        """Login user and return JWT tokens"""
        try:
            # Find user
            user = db.users.find_one({'email': email})
            
            if not user:
                return {'success': False, 'message': 'Invalid credentials'}
            
            # Verify password
            if not self.verify_password(password, user['password']):
                return {'success': False, 'message': 'Invalid credentials'}
            
            # Check if email is verified (optional - can be disabled for testing)
            # if not user.get('email_verified', False):
            #     return {'success': False, 'message': 'Please verify your email first'}
            
            # Create JWT tokens
            access_token = create_access_token(
                identity=email,
                expires_delta=timedelta(hours=24)
            )
            refresh_token = create_refresh_token(
                identity=email,
                expires_delta=timedelta(days=30)
            )
            
            # Update last login
            db.users.update_one(
                {'email': email},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            
            logger.info(f"User logged in: {email}")
            
            return {
                'success': True,
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'email': user['email'],
                    'name': user['name'],
                    'api_key': user.get('api_key'),
                    'api_secret': user.get('api_secret'),
                    'email_verified': user.get('email_verified', False)
                }
            }
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            return {'success': False, 'message': str(e)}
    
    def verify_email(self, token: str):
        """Verify user email"""
        try:
            email = self.verify_token(token, max_age=86400)  # 24 hours
            
            if not email:
                return {'success': False, 'message': 'Invalid or expired token'}
            
            # Update user
            result = db.users.update_one(
                {'email': email},
                {'$set': {'email_verified': True, 'updated_at': datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Email verified: {email}")
                return {'success': True, 'message': 'Email verified successfully'}
            else:
                return {'success': False, 'message': 'User not found'}
                
        except Exception as e:
            logger.error(f"Email verification error: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_user_profile(self, email: str):
        """Get user profile"""
        try:
            user = db.users.find_one({'email': email}, {'password': 0})
            
            if not user:
                return {'success': False, 'message': 'User not found'}
            
            user['_id'] = str(user['_id'])
            return {'success': True, 'user': user}
            
        except Exception as e:
            logger.error(f"Get profile error: {e}")
            return {'success': False, 'message': str(e)}
    
    def update_api_credentials(self, email: str, api_key: str, api_secret: str):
        """Update user API credentials"""
        try:
            result = db.users.update_one(
                {'email': email},
                {
                    '$set': {
                        'api_key': api_key,
                        'api_secret': api_secret,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"API credentials updated: {email}")
                return {'success': True, 'message': 'Credentials updated'}
            else:
                return {'success': False, 'message': 'Update failed'}
                
        except Exception as e:
            logger.error(f"Update credentials error: {e}")
            return {'success': False, 'message': str(e)}

# Global auth service instance
auth_service = None

def init_auth_service(secret_key):
    """Initialize auth service"""
    global auth_service
    auth_service = AuthService(secret_key)
    return auth_service
