#!/bin/bash

# Quick Deploy Script for Vercel
# Run this script to prepare and deploy your app

echo "🚀 Binance Trading Bot - Vercel Deployment"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo ""
echo "📝 Adding files to Git..."
git add .

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "Complete Binance Trading Bot - Ready for Vercel" || echo "No changes to commit"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "Please create a GitHub repository and run:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/binance-trading-bot.git"
    echo "git push -u origin main"
    echo ""
    echo "Then go to https://vercel.com/new to deploy"
else
    echo ""
    echo "📤 Pushing to GitHub..."
    git push origin main || git push -u origin main
    
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "🌐 Next steps:"
    echo "1. Go to https://vercel.com/new"
    echo "2. Import your repository"
    echo "3. Add environment variables"
    echo "4. Deploy!"
fi

echo ""
echo "📖 For detailed instructions, see DEPLOY_NOW.md"
echo ""
