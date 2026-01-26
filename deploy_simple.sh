#!/bin/bash

echo "🚀 CineGraph - Simple Deployment"
echo "================================"

# Configure git
git config user.name "Bibekbitu9" 2>/dev/null
git config user.email "bibekbitu9@example.com" 2>/dev/null

# Switch to production branch
git checkout production 2>/dev/null || git checkout -b production

# Remove problematic files
rm -rf frontend/node_modules 2>/dev/null
rm -f frontend/package-lock.json 2>/dev/null
rm -f frontend/yarn.lock 2>/dev/null

# Add all files
git add .

# Commit
git commit -m "🎬 CineGraph: Simplified for Vercel deployment

✨ Simplified frontend:
- Removed complex dependencies
- Clean React setup with minimal dependencies
- Fixed all import paths
- Simplified Vercel configuration

🚀 Ready for deployment:
- Backend: FastAPI serverless functions
- Frontend: Simple React app
- API: TMDB integration with fallback data

📱 Should deploy successfully on Vercel!"

# Push
git push -u origin production

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed simplified version!"
    echo ""
    echo "🚀 Now deploy on Vercel:"
    echo "1. Go to vercel.com/dashboard"
    echo "2. Find your cinegraph project"
    echo "3. It should auto-redeploy"
    echo "4. Or click 'Redeploy' button"
    echo ""
    echo "✨ This simplified version should work!"
else
    echo "❌ Push failed"
fi