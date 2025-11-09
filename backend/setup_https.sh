#!/bin/bash

# HTTPS Setup Script for Binance Trading Bot
# This script helps you set up SSL/TLS certificates

echo "=========================================="
echo "HTTPS Setup for Binance Trading Bot"
echo "=========================================="
echo ""

# Check if running as root for production setup
if [ "$EUID" -eq 0 ]; then 
    PRODUCTION=true
    echo "Running as root - Production mode"
else
    PRODUCTION=false
    echo "Running as user - Development mode"
fi

echo ""
echo "Choose setup type:"
echo "1) Self-signed certificate (Development/Testing)"
echo "2) Let's Encrypt certificate (Production with domain)"
echo "3) Generate Nginx config (Production reverse proxy)"
echo "4) Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Generating self-signed certificate..."
        echo ""
        
        # Check if openssl is installed
        if ! command -v openssl &> /dev/null; then
            echo "Error: openssl is not installed"
            echo "Install with: brew install openssl (macOS) or apt-get install openssl (Linux)"
            exit 1
        fi
        
        # Generate certificate
        openssl req -x509 -newkey rsa:4096 -nodes \
            -out cert.pem -keyout key.pem -days 365 \
            -subj "/C=US/ST=State/L=City/O=TradingBot/CN=localhost"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Certificate generated successfully!"
            echo ""
            echo "Files created:"
            echo "  - cert.pem (certificate)"
            echo "  - key.pem (private key)"
            echo ""
            echo "To use HTTPS, update web_ui.py:"
            echo "  app.run(ssl_context=('cert.pem', 'key.pem'))"
            echo ""
            echo "Access your app at: https://localhost:5001"
            echo ""
            echo "⚠️  Note: Browsers will show a security warning for self-signed certificates."
            echo "    This is normal for development. Click 'Advanced' and proceed."
        else
            echo "❌ Error generating certificate"
            exit 1
        fi
        ;;
        
    2)
        echo ""
        if [ "$PRODUCTION" = false ]; then
            echo "❌ Error: Let's Encrypt setup requires root privileges"
            echo "Run with: sudo ./setup_https.sh"
            exit 1
        fi
        
        read -p "Enter your domain name (e.g., tradingbot.example.com): " domain
        read -p "Enter your email address: " email
        
        echo ""
        echo "Installing certbot..."
        
        # Detect OS and install certbot
        if [ -f /etc/debian_version ]; then
            apt-get update
            apt-get install -y certbot
        elif [ -f /etc/redhat-release ]; then
            yum install -y certbot
        else
            echo "❌ Unsupported OS. Please install certbot manually."
            exit 1
        fi
        
        echo ""
        echo "Generating Let's Encrypt certificate..."
        echo "⚠️  Make sure:"
        echo "  1. Port 80 is open"
        echo "  2. Domain $domain points to this server"
        echo "  3. No other service is using port 80"
        echo ""
        read -p "Press Enter to continue..."
        
        certbot certonly --standalone -d "$domain" --email "$email" --agree-tos
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Certificate generated successfully!"
            echo ""
            echo "Certificate files:"
            echo "  - /etc/letsencrypt/live/$domain/fullchain.pem"
            echo "  - /etc/letsencrypt/live/$domain/privkey.pem"
            echo ""
            echo "To use HTTPS, update web_ui.py:"
            echo "  app.run(ssl_context=("
            echo "      '/etc/letsencrypt/live/$domain/fullchain.pem',"
            echo "      '/etc/letsencrypt/live/$domain/privkey.pem'"
            echo "  ))"
            echo ""
            echo "Certificate will auto-renew. Test renewal with:"
            echo "  certbot renew --dry-run"
        else
            echo "❌ Error generating certificate"
            exit 1
        fi
        ;;
        
    3)
        echo ""
        read -p "Enter your domain name: " domain
        read -p "Enter backend port [5001]: " port
        port=${port:-5001}
        
        config_file="nginx_tradingbot.conf"
        
        cat > "$config_file" << EOF
# Nginx configuration for Binance Trading Bot
# Copy this to /etc/nginx/sites-available/tradingbot
# Then: sudo ln -s /etc/nginx/sites-available/tradingbot /etc/nginx/sites-enabled/

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $domain;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $domain;

    # SSL certificates (update paths after running certbot)
    ssl_certificate /etc/letsencrypt/live/$domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$domain/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy to Flask backend
    location / {
        proxy_pass http://localhost:$port;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://localhost:$port;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Logging
    access_log /var/log/nginx/tradingbot_access.log;
    error_log /var/log/nginx/tradingbot_error.log;
}
EOF
        
        echo "✅ Nginx configuration generated: $config_file"
        echo ""
        echo "To install:"
        echo "  1. sudo cp $config_file /etc/nginx/sites-available/tradingbot"
        echo "  2. sudo ln -s /etc/nginx/sites-available/tradingbot /etc/nginx/sites-enabled/"
        echo "  3. sudo nginx -t  # Test configuration"
        echo "  4. sudo systemctl restart nginx"
        echo ""
        echo "Make sure to:"
        echo "  - Install SSL certificates first (option 2)"
        echo "  - Update certificate paths in the config"
        echo "  - Start your Flask app on port $port"
        ;;
        
    4)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
