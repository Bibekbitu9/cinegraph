#!/bin/bash

echo "🚀 Simple Git Setup for CineGraph"
echo "================================="

# Set Git identity (replace with your details)
echo "Setting up Git identity..."
git config user.name "Bibekbitu9"
git config user.email "your-email@example.com"

# Initialize if needed
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
fi

# Add remote if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    git remote add origin https://github.com/Bibekbitu9/cinegraph.git
    echo "✅ Remote added"
fi

# Create production branch
git checkout -b production 2>/dev/null || git checkout production
echo "✅ On production branch"

# Add files
git add .
echo "✅ Files staged"

# Simple commit
git commit -m "Deploy CineGraph to Vercel"
echo "✅ Committed"

# Push
git push -u origin production
echo "✅ Pushed to GitHub"

echo ""
echo "🎉 Done! Go to vercel.com to deploy"