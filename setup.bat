@echo off
echo 🎬 CineGraph - Standalone Setup Script (Windows)
echo =============================================

:: Check if required tools are installed
echo 📋 Checking requirements...

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.9+ from https://python.org/
    pause
    exit /b 1
)

echo ✅ Requirements check completed

:: Setup backend
echo 🐍 Setting up backend...
cd backend

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

:: Check if .env exists
if not exist .env (
    echo 📝 Creating backend .env file...
    (
        echo TMDB_API_KEY=YOUR_TMDB_API_KEY_HERE
        echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001
    ) > .env
    echo ⚠️  Please add your TMDB API key to backend\.env
    echo    Get it from: https://www.themoviedb.org/settings/api
)

cd ..
echo ✅ Backend setup completed

:: Setup frontend
echo ⚛️  Setting up frontend...
cd frontend

:: Install dependencies
where yarn >nul 2>&1
if %errorlevel% equ 0 (
    yarn install
) else (
    npm install
)

:: Check if .env exists
if not exist .env (
    echo 📝 Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8001 > .env
)

cd ..
echo ✅ Frontend setup completed

echo 🎬 CineGraph uses TMDB API directly - no database needed!

echo.
echo 🎉 Setup completed!
echo.
echo 📋 Next steps:
echo 1. Add your TMDB API key to backend\.env
echo 2. Run: npm run dev
echo 3. Open http://localhost:3000
echo.
echo 🔗 Get TMDB API key: https://www.themoviedb.org/settings/api

pause