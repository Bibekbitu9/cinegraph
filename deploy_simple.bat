@echo off
echo 🚀 CineGraph - Simple Deployment
echo ================================

:: Configure git
git config user.name "Bibekbitu9" >nul 2>&1
git config user.email "bibekbitu9@example.com" >nul 2>&1

:: Switch to production branch
git checkout production >nul 2>&1

:: Remove problematic files
if exist "frontend\node_modules" rmdir /s /q "frontend\node_modules" >nul 2>&1
if exist "frontend\package-lock.json" del "frontend\package-lock.json" >nul 2>&1
if exist "frontend\yarn.lock" del "frontend\yarn.lock" >nul 2>&1

:: Add all files
git add .

:: Commit
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

:: Push
git push -u origin production

if %errorlevel% equ 0 (
    echo.
    echo ✅ Successfully pushed simplified version!
    echo.
    echo 🚀 Now deploy on Vercel:
    echo 1. Go to vercel.com/dashboard
    echo 2. Find your cinegraph project
    echo 3. It should auto-redeploy
    echo 4. Or click 'Redeploy' button
    echo.
    echo ✨ This simplified version should work!
) else (
    echo ❌ Push failed
)

pause