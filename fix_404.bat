@echo off
echo 🔧 Fixing 404 Error - Simplified Structure
echo ==========================================

:: Configure git
git config user.name "Bibekbitu9" >nul 2>&1
git config user.email "bibekbitu9@example.com" >nul 2>&1

:: Switch to production branch
git checkout production >nul 2>&1

:: Remove old frontend folder to avoid conflicts
if exist "frontend" rmdir /s /q "frontend" >nul 2>&1

:: Add all files
git add .

:: Commit
git commit -m "🔧 Fix 404 error - Move to root structure

✨ Simplified deployment:
- Moved React app to root directory
- Updated vercel.json for proper routing
- Fixed static file serving
- Backend API at /api/* routes

🚀 Should resolve 404 errors and work properly"

:: Push
git push -u origin production

if %errorlevel% equ 0 (
    echo.
    echo ✅ Fixed structure pushed to GitHub!
    echo.
    echo 🚀 Vercel will auto-redeploy:
    echo 1. Check your Vercel dashboard
    echo 2. Wait for auto-deployment
    echo 3. Test your URL again
    echo.
    echo ✨ The 404 error should be fixed now!
) else (
    echo ❌ Push failed
)

pause