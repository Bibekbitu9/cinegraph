@echo off
echo 🔧 Fixing Vercel Build Issues
echo =============================

:: Configure git identity
git config user.name "Bibekbitu9" >nul 2>&1
git config user.email "bibekbitu9@example.com" >nul 2>&1

:: Switch to production branch
git checkout production >nul 2>&1

:: Add the fixes
git add .

:: Commit the fixes
git commit -m "🔧 Fix Vercel build issues

- Fixed @ alias imports in index.js
- Removed problematic cp command from build script  
- Updated vercel.json configuration
- Ready for successful deployment"

:: Push to GitHub
git push -u origin production

if %errorlevel% equ 0 (
    echo ✅ Fixes pushed to GitHub!
    echo.
    echo 🚀 Now redeploy on Vercel:
    echo 1. Go to your Vercel dashboard
    echo 2. Find your cinegraph project
    echo 3. Click 'Redeploy' or it will auto-deploy
    echo 4. The build should succeed now!
) else (
    echo ❌ Push failed. Try manually:
    echo git add .
    echo git commit -m "Fix build issues"
    echo git push -u origin production
)

pause