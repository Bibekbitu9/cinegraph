#!/bin/bash

echo "🔧 Fixing Vercel Build Issues"
echo "============================="

# Configure git identity
git config user.name "Bibekbitu9" 2>/dev/null
git config user.email "bibekbitu9@example.com" 2>/dev/null

# Switch to production branch
git checkout production 2>/dev/null || git checkout -b production

# Add the fixes
git add .

# Commit the fixes
git commit -m "🔧 Fix Vercel build issues

- Fixed @ alias imports in index.js
- Removed problematic cp command from build script
- Updated vercel.json configuration
- Ready for successful deployment"

# Push to GitHub
git push -u origin production

if [ $? -eq 0 ]; then
    echo "✅ Fixes pushed to GitHub!"
    echo ""
    echo "🚀 Now redeploy on Vercel:"
    echo "1. Go to your Vercel dashboard"
    echo "2. Find your cinegraph project"
    echo "3. Click 'Redeploy' or it will auto-deploy"
    echo "4. The build should succeed now!"
else
    echo "❌ Push failed. Try manually:"
    echo "git add ."
    echo "git commit -m 'Fix build issues'"
    echo "git push -u origin production"
fi