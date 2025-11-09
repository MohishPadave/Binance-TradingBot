#!/bin/bash

# Script to create submission zip file
# Usage: ./create_submission.sh your_name

if [ -z "$1" ]; then
    echo "Usage: ./create_submission.sh your_name"
    echo "Example: ./create_submission.sh john_doe"
    exit 1
fi

NAME=$1
ZIP_NAME="${NAME}_binance_bot.zip"

echo "Creating submission package: $ZIP_NAME"
echo "================================"

# Check required files exist
echo "Checking required files..."

REQUIRED_FILES=(
    "src/cli.py"
    "src/market_orders.py"
    "src/limit_orders.py"
    "bot.log"
    "README.md"
    "requirements.txt"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        MISSING=1
    else
        echo "✓ Found: $file"
    fi
done

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "❌ Some required files are missing!"
    echo "Please ensure all files are present before creating submission."
    exit 1
fi

# Check if report.pdf exists
if [ ! -f "report.pdf" ]; then
    echo ""
    echo "⚠️  WARNING: report.pdf not found!"
    echo "You need to create report.pdf before submission."
    echo "Use REPORT_TEMPLATE.md as a guide."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create zip file
echo ""
echo "Creating zip file..."

zip -r "$ZIP_NAME" \
    src/ \
    bot.log \
    README.md \
    requirements.txt \
    report.pdf \
    -x "*.pyc" -x "__pycache__/*" -x ".DS_Store" -x "*.swp"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Successfully created: $ZIP_NAME"
    echo ""
    echo "File size: $(du -h $ZIP_NAME | cut -f1)"
    echo ""
    echo "Contents:"
    unzip -l "$ZIP_NAME"
    echo ""
    echo "================================"
    echo "✓ Submission package ready!"
    echo "Submit: $ZIP_NAME"
else
    echo "❌ Failed to create zip file"
    exit 1
fi
