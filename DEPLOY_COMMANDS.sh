#!/bin/bash
# Copy and paste these commands one by one

# ============================================
# STEP 1: INITIALIZE GIT
# ============================================
git init
git add .
git commit -m "Complete Binance Trading Bot - Ready for Vercel"

# ============================================
# STEP 2: PUSH TO GITHUB
# ============================================
# First, create a repository on GitHub: https://github.com/new
# Then replace YOUR_USERNAME below with your GitHub username

git remote add origin https://github.com/YOUR_USERNAME/binance-trading-bot.git
git branch -M main
git push -u origin main

# ============================================
# STEP 3: DEPLOY ON VERCEL
# ============================================
# Go to: https://vercel.com/new
# Import your repository
# Configure build settings (see DEPLOY_NOW.md)
# Add environment variables
# Deploy!

# ============================================
# DONE! 🎉
# ============================================
