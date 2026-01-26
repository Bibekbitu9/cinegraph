const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🎬 CineGraph - Standalone Setup Script');
console.log('=====================================');

// Check if required tools are installed
function checkRequirements() {
    console.log('📋 Checking requirements...');
    
    try {
        execSync('node --version', { stdio: 'ignore' });
        console.log('✅ Node.js found');
    } catch (error) {
        console.log('❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/');
        process.exit(1);
    }
    
    try {
        execSync('python --version', { stdio: 'ignore' });
        console.log('✅ Python found');
    } catch (error) {
        try {
            execSync('python3 --version', { stdio: 'ignore' });
            console.log('✅ Python3 found');
        } catch (error) {
            console.log('❌ Python is not installed. Please install Python 3.9+ from https://python.org/');
            process.exit(1);
        }
    }
    
    try {
        execSync('docker --version', { stdio: 'ignore' });
        console.log('✅ Docker found');
    } catch (error) {
        console.log('⚠️  Docker not found - MongoDB will need to be installed manually');
    }
}

// Setup backend
function setupBackend() {
    console.log('🐍 Setting up backend...');
    
    process.chdir('backend');
    
    // Create virtual environment
    try {
        execSync('python -m venv venv', { stdio: 'inherit' });
    } catch (error) {
        try {
            execSync('python3 -m venv venv', { stdio: 'inherit' });
        } catch (error) {
            console.log('❌ Failed to create virtual environment');
            process.exit(1);
        }
    }
    
    // Install dependencies
    const activateScript = process.platform === 'win32' ? 'venv\\Scripts\\activate' : 'source venv/bin/activate';
    const pipCommand = process.platform === 'win32' 
        ? 'venv\\Scripts\\pip install -r requirements.txt'
        : 'venv/bin/pip install -r requirements.txt';
    
    try {
        execSync(pipCommand, { stdio: 'inherit' });
    } catch (error) {
        console.log('❌ Failed to install Python dependencies');
        process.exit(1);
    }
    
    // Check if .env exists and has API key
    if (!fs.existsSync('.env')) {
        echo "📝 Creating backend .env file..."
        const envContent = `TMDB_API_KEY=YOUR_TMDB_API_KEY_HERE
CORS_ORIGINS=http://localhost:3000,http://localhost:3001`;
        fs.writeFileSync('.env', envContent);
        console.log('⚠️  Please add your TMDB API key to backend/.env');
        console.log('   Get it from: https://www.themoviedb.org/settings/api');
    }
    
    process.chdir('..');
    console.log('✅ Backend setup completed');
}

// Setup frontend
function setupFrontend() {
    console.log('⚛️  Setting up frontend...');
    
    process.chdir('frontend');
    
    // Install dependencies
    try {
        execSync('yarn --version', { stdio: 'ignore' });
        execSync('yarn install', { stdio: 'inherit' });
    } catch (error) {
        try {
            execSync('npm install', { stdio: 'inherit' });
        } catch (error) {
            console.log('❌ Failed to install frontend dependencies');
            process.exit(1);
        }
    }
    
    // Check if .env exists
    if (!fs.existsSync('.env')) {
        console.log('📝 Creating frontend .env file...');
        fs.writeFileSync('.env', 'REACT_APP_BACKEND_URL=http://localhost:8001');
    }
    
    process.chdir('..');
    console.log('✅ Frontend setup completed');
}

// Setup MongoDB
function setupMongoDB() {
    console.log('🎬 CineGraph uses TMDB API directly - no database needed!');
    console.log('✅ Ready to go!');
}

// Main setup
function main() {
    checkRequirements();
    setupBackend();
    setupFrontend();
    setupMongoDB();
    
    console.log('');
    console.log('🎉 Setup completed!');
    console.log('');
    console.log('📋 Next steps:');
    console.log('1. Add your TMDB API key to backend/.env');
    console.log('2. Run: npm run dev');
    console.log('3. Open http://localhost:3000');
    console.log('');
    console.log('🔗 Get TMDB API key: https://www.themoviedb.org/settings/api');
}

main();