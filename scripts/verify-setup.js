const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔍 CineGraph Setup Verification');
console.log('===============================');

let issues = [];
let warnings = [];

// Check Node.js
try {
    const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
    const majorVersion = parseInt(nodeVersion.replace('v', '').split('.')[0]);
    if (majorVersion >= 18) {
        console.log(`✅ Node.js ${nodeVersion} (OK)`);
    } else {
        issues.push(`Node.js version ${nodeVersion} is too old. Need 18+`);
    }
} catch (error) {
    issues.push('Node.js not found');
}

// Check Python
try {
    let pythonVersion;
    try {
        pythonVersion = execSync('python --version', { encoding: 'utf8' }).trim();
    } catch {
        try {
            pythonVersion = execSync('python3 --version', { encoding: 'utf8' }).trim();
        } catch {
            pythonVersion = execSync('py --version', { encoding: 'utf8' }).trim();
        }
    }
    const version = pythonVersion.split(' ')[1];
    const [major, minor] = version.split('.').map(Number);
    if (major >= 3 && minor >= 9) {
        console.log(`✅ Python ${version} (OK)`);
    } else {
        issues.push(`Python version ${version} is too old. Need 3.9+`);
    }
} catch (error) {
    issues.push('Python not found');
}

// Check Docker
try {
    const dockerVersion = execSync('docker --version', { encoding: 'utf8' }).trim();
    console.log(`✅ Docker found (${dockerVersion}) - Optional for deployment`);
} catch (error) {
    console.log('ℹ️  Docker not found - not required for development');
}

// Check backend setup
console.log('\n📁 Checking backend setup...');
if (fs.existsSync('backend/venv')) {
    console.log('✅ Python virtual environment exists');
} else {
    issues.push('Backend virtual environment not found. Run setup first.');
}

if (fs.existsSync('backend/.env')) {
    const envContent = fs.readFileSync('backend/.env', 'utf8');
    if (envContent.includes('YOUR_TMDB_API_KEY_HERE')) {
        warnings.push('TMDB API key not set in backend/.env');
    } else {
        console.log('✅ Backend .env configured');
    }
} else {
    issues.push('Backend .env file not found');
}

if (fs.existsSync('backend/requirements.txt')) {
    console.log('✅ Backend requirements.txt exists');
} else {
    issues.push('Backend requirements.txt not found');
}

// Check frontend setup
console.log('\n📁 Checking frontend setup...');
if (fs.existsSync('frontend/node_modules')) {
    console.log('✅ Frontend dependencies installed');
} else {
    issues.push('Frontend node_modules not found. Run setup first.');
}

if (fs.existsSync('frontend/.env')) {
    console.log('✅ Frontend .env configured');
} else {
    warnings.push('Frontend .env file not found');
}

if (fs.existsSync('frontend/package.json')) {
    console.log('✅ Frontend package.json exists');
} else {
    issues.push('Frontend package.json not found');
}

// Check Docker setup
console.log('\n🐳 Checking Docker setup (optional)...');
if (fs.existsSync('docker-compose.yml')) {
    console.log('✅ Docker Compose configuration exists');
} else {
    warnings.push('docker-compose.yml not found');
}

if (fs.existsSync('backend/Dockerfile')) {
    console.log('✅ Backend Dockerfile exists');
} else {
    warnings.push('Backend Dockerfile not found');
}

if (fs.existsSync('frontend/Dockerfile')) {
    console.log('✅ Frontend Dockerfile exists');
} else {
    warnings.push('Frontend Dockerfile not found');
}

// Check scripts
console.log('\n📜 Checking setup scripts...');
const scripts = ['setup.bat', 'start-dev.bat'];
scripts.forEach(script => {
    if (fs.existsSync(script)) {
        console.log(`✅ ${script} exists`);
    } else {
        warnings.push(`${script} not found`);
    }
});

// Summary
console.log('\n📊 Verification Summary');
console.log('=======================');

if (issues.length === 0) {
    console.log('🎉 All critical checks passed!');
} else {
    console.log('❌ Issues found:');
    issues.forEach(issue => console.log(`   • ${issue}`));
}

if (warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    warnings.forEach(warning => console.log(`   • ${warning}`));
}

console.log('\n📋 Next Steps:');
if (issues.length > 0) {
    console.log('1. Fix the issues listed above');
    console.log('2. Run setup: npm run setup');
} else if (warnings.some(w => w.includes('TMDB API key'))) {
    console.log('1. Add your TMDB API key to backend/.env');
    console.log('2. Start development: npm run dev');
} else {
    console.log('1. Start development: npm run dev');
    console.log('2. Open http://localhost:3000');
}

console.log('\n🔗 Resources:');
console.log('• TMDB API Key: https://www.themoviedb.org/settings/api');
console.log('• Documentation: README.md');

process.exit(issues.length > 0 ? 1 : 0);