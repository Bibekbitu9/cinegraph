@echo off
echo 🚀 CineGraph - Deploy to Production Branch
echo ==========================================

:: Check if we're in the right directory
if not exist "vercel.json" (
    echo ❌ vercel.json not found. Make sure you're in the CineGraph project directory.
    pause
    exit /b 1
)

echo ✅ Found CineGraph project files

:: Configure Git identity
git config user.name "Bibekbitu9" >nul 2>&1
git config user.email "bibekbitu9@example.com" >nul 2>&1
echo ✅ Git identity configured

:: Initialize git if needed
if not exist ".git" (
    echo ℹ️  Initializing Git repository...
    git init
    echo ✅ Git repository initialized
)

:: Add remote origin if not exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo ℹ️  Adding GitHub remote...
    git remote add origin https://github.com/Bibekbitu9/cinegraph.git
    echo ✅ Remote origin added
) else (
    echo ✅ Remote origin already exists
)

:: Create and switch to production branch
echo ℹ️  Switching to production branch...
git checkout -b production >nul 2>&1
if %errorlevel% neq 0 (
    git checkout production >nul 2>&1
)
echo ✅ On production branch

:: Add all files
echo ℹ️  Adding all files to staging...
git add .
echo ✅ Files staged for commit

:: Show status
echo ℹ️  Files to be committed:
git status --short

:: Commit changes
echo ℹ️  Committing changes...
git commit -m "🎬 CineGraph: Production deployment ready

✨ Features implemented:
- Movie search with TMDB API integration
- AI-powered movie recommendations  
- Trending movies section
- Responsive design with TailwindCSS
- Framer Motion animations
- Global streaming availability

🚀 Vercel deployment ready:
- Complete vercel.json configuration
- Serverless FastAPI backend
- Optimized React frontend
- Environment variables configured
- Fallback data for offline mode

🔧 Technical stack:
- Backend: FastAPI + Python serverless functions
- Frontend: React 18 + TailwindCSS + Framer Motion
- API: TMDB integration with caching
- Deployment: Vercel edge network

📱 Ready for one-click deployment to Vercel!"

if %errorlevel% equ 0 (
    echo ✅ Changes committed successfully
) else (
    echo ❌ Commit failed
    pause
    exit /b 1
)

:: Push to GitHub
echo ℹ️  Pushing to GitHub production branch...
git push -u origin production

if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🎉 DEPLOYMENT READY!
    echo ===================
    echo.
    echo ℹ️  Your CineGraph project is now on GitHub in the production branch
    echo.
    echo ℹ️  Next steps:
    echo 1. Go to: https://vercel.com/new
    echo 2. Sign in with GitHub
    echo 3. Import repository: Bibekbitu9/cinegraph
    echo 4. Select branch: production
    echo 5. Click Deploy
    echo.
    echo ℹ️  Your app will be live in ~3 minutes at: https://cinegraph-[random].vercel.app
    echo.
    echo ℹ️  Features ready to test:
    echo • Movie search and recommendations
    echo • Trending movies
    echo • Responsive design
    echo • Global streaming availability
    echo.
    echo 🚀 Happy deploying!
    
) else (
    echo ❌ Push failed!
    echo.
    echo ℹ️  Common solutions:
    echo 1. Check your GitHub authentication
    echo 2. Make sure the repository exists: https://github.com/Bibekbitu9/cinegraph
    echo 3. Try: git remote set-url origin https://github.com/Bibekbitu9/cinegraph.git
    echo.
    echo ℹ️  Repository URL should be: https://github.com/Bibekbitu9/cinegraph.git
)

echo.
pause