#!/bin/bash

echo "🚀 Git Commands for Production Branch"
echo "====================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📋 Step 1: Initialize Git repository"
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "📋 Step 2: Add remote origin"
    echo "Please run this command with your actual GitHub repo URL:"
    echo "git remote add origin https://github.com/Bibekbitu9/cinegraph.git"
    echo ""
    read -p "Press Enter after adding the remote origin..."
else
    echo "✅ Remote origin already exists"
fi

echo "📋 Step 3: Create and switch to production branch"
git checkout -b production 2>/dev/null || git checkout production
echo "✅ Switched to production branch"

echo "📋 Step 4: Add all files"
git add .
echo "✅ Files added to staging"

echo "📋 Step 5: Commit changes"
git commit -m "🎬 CineGraph: Ready for Vercel deployment

✨ Features:
- Movie search with TMDB API integration
- AI-powered movie recommendations
- Trending movies section
- Responsive design with TailwindCSS
- Framer Motion animations

🚀 Deployment Ready:
- Vercel configuration (vercel.json)
- Serverless FastAPI backend
- React frontend with clean dependencies
- Fallback data for offline mode
- Environment variables configured

🔧 Technical Stack:
- Backend: FastAPI + Python
- Frontend: React 18 + TailwindCSS
- API: TMDB integration
- Deployment: Vercel serverless

📱 Ready to deploy to Vercel!"

echo "✅ Changes committed"

echo "📋 Step 6: Push to GitHub"
git push -u origin production
echo "✅ Pushed to GitHub production branch"

echo ""
echo "🎉 Done! Your production branch is ready for Vercel deployment."
echo "📱 Next steps:"
echo "1. Go to vercel.com"
echo "2. Sign up/login with GitHub"
echo "3. Import your repository"
echo "4. Select the 'production' branch"
echo "5. Click Deploy"
echo ""
echo "🌐 Your app will be live in ~3 minutes!"