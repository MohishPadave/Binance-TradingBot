"""
Email service for sending verification emails
"""
import os
from flask_mail import Mail, Message
from logger import logger

class EmailService:
    """Email service for sending verification and notification emails"""
    
    def __init__(self, app=None):
        self.mail = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Flask-Mail"""
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@tradingbot.com')
        
        self.mail = Mail(app)
        logger.info("Email service initialized")
    
    def send_verification_email(self, email: str, token: str, base_url: str):
        """Send email verification link"""
        try:
            verification_url = f"{base_url}/verify-email?token={token}"
            
            msg = Message(
                subject="Verify Your Email - Binance Trading Bot",
                recipients=[email],
                html=f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Welcome to Binance Trading Bot!</h2>
                    <p>Thank you for registering. Please verify your email address by clicking the link below:</p>
                    <p>
                        <a href="{verification_url}" 
                           style="background-color: #4CAF50; color: white; padding: 14px 20px; 
                                  text-decoration: none; border-radius: 4px; display: inline-block;">
                            Verify Email
                        </a>
                    </p>
                    <p>Or copy and paste this link in your browser:</p>
                    <p>{verification_url}</p>
                    <p>This link will expire in 24 hours.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        If you didn't create an account, please ignore this email.
                    </p>
                </body>
                </html>
                """
            )
            
            self.mail.send(msg)
            logger.info(f"Verification email sent to: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            return False
    
    def send_password_reset_email(self, email: str, token: str, base_url: str):
        """Send password reset link"""
        try:
            reset_url = f"{base_url}/reset-password?token={token}"
            
            msg = Message(
                subject="Reset Your Password - Binance Trading Bot",
                recipients=[email],
                html=f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Password Reset Request</h2>
                    <p>You requested to reset your password. Click the link below to proceed:</p>
                    <p>
                        <a href="{reset_url}" 
                           style="background-color: #2196F3; color: white; padding: 14px 20px; 
                                  text-decoration: none; border-radius: 4px; display: inline-block;">
                            Reset Password
                        </a>
                    </p>
                    <p>Or copy and paste this link in your browser:</p>
                    <p>{reset_url}</p>
                    <p>This link will expire in 1 hour.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        If you didn't request this, please ignore this email.
                    </p>
                </body>
                </html>
                """
            )
            
            self.mail.send(msg)
            logger.info(f"Password reset email sent to: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return False

# Global email service instance
email_service = EmailService()
