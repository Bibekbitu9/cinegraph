@echo off
echo 🎬 Starting CineGraph Development Environment
echo ============================================

echo 🎬 CineGraph uses TMDB API directly - no database needed!

:: Start backend
echo 🐍 Starting backend server...
cd backend

if not exist venv (
    echo ❌ Virtual environment not found. Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

:: Check if TMDB API key is set
findstr "YOUR_TMDB_API_KEY_HERE" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Please add your TMDB API key to backend\.env
    echo    Get it from: https://www.themoviedb.org/settings/api
    pause
    exit /b 1
)

start "CineGraph Backend" cmd /k "uvicorn server:app --reload --host 0.0.0.0 --port 8001"
cd ..
echo ✅ Backend started on http://localhost:8001

:: Wait a moment for backend to start
timeout /t 3 >nul

:: Start frontend
echo ⚛️  Starting frontend server...
cd frontend

if not exist node_modules (
    echo ❌ Node modules not found. Please run setup.bat first
    pause
    exit /b 1
)

where yarn >nul 2>&1
if %errorlevel% equ 0 (
    start "CineGraph Frontend" cmd /k "yarn start"
) else (
    start "CineGraph Frontend" cmd /k "npm start"
)

cd ..
echo ✅ Frontend started on http://localhost:3000

echo.
echo 🎉 CineGraph is running!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8001
echo 📚 API Docs: http://localhost:8001/docs
echo.
echo Press any key to continue...
pause >nul