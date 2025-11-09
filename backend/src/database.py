"""
MongoDB database connection and management
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from logger import logger

class Database:
    """MongoDB database wrapper"""
    
    def __init__(self, connection_string=None):
        self.connection_string = connection_string or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = None
        self.db = None
        self.users = None
        self.orders = None
        self.sessions = None
    
    def connect(self, db_name='binance_trading_bot'):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[db_name]
            self.users = self.db['users']
            self.orders = self.db['orders']
            self.sessions = self.db['sessions']
            
            # Create indexes
            self.create_indexes()
            
            logger.info(f"Connected to MongoDB: {db_name}")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"MongoDB error: {e}")
            return False
    
    def create_indexes(self):
        """Create database indexes"""
        try:
            # Users collection indexes
            self.users.create_index('email', unique=True)
            self.users.create_index('created_at')
            
            # Orders collection indexes
            self.orders.create_index('user_email')
            self.orders.create_index('timestamp')
            self.orders.create_index([('user_email', 1), ('timestamp', -1)])
            
            logger.info("Database indexes created")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

# Global database instance
db = Database()
