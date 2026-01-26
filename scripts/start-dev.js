const { spawn, execSync } = require('child_process');
const fs = require('fs');
const net = require('net');

console.log('🎬 Starting CineGraph Development Environment');
console.log('============================================');

// Check if port is in use
function checkPort(port) {
    return new Promise((resolve) => {
        const server = net.createServer();
        server.listen(port, () => {
            server.once('close', () => resolve(true));
            server.close();
        });
        server.on('error', () => resolve(false));
    });
}

// Check if MongoDB is running
async function checkMongoDB() {
    console.log('🎬 CineGraph uses TMDB API directly - no database needed!');
    return Promise.resolve();
}

// Start backend
function startBackend() {
    return new Promise((resolve, reject) => {
        console.log('🐍 Starting backend server...');
        
        if (!fs.existsSync('backend/venv')) {
            console.log('❌ Virtual environment not found. Please run npm run setup first');
            process.exit(1);
        }
        
        // Check if TMDB API key is set
        const envContent = fs.readFileSync('backend/.env', 'utf8');
        if (envContent.includes('YOUR_TMDB_API_KEY_HERE')) {
            console.log('⚠️  Please add your TMDB API key to backend/.env');
            console.log('   Get it from: https://www.themoviedb.org/settings/api');
            process.exit(1);
        }
        
        const pythonPath = process.platform === 'win32' 
            ? 'backend\\venv\\Scripts\\python'
            : 'backend/venv/bin/python';
        
        const backend = spawn(pythonPath, ['-m', 'uvicorn', 'server:app', '--reload', '--host', '0.0.0.0', '--port', '8001'], {
            cwd: 'backend',
            stdio: 'inherit'
        });
        
        backend.on('error', (error) => {
            console.log('❌ Failed to start backend:', error.message);
            reject(error);
        });
        
        // Wait a bit for backend to start
        setTimeout(() => {
            console.log('✅ Backend started on http://localhost:8001');
            resolve(backend);
        }, 3000);
    });
}

// Start frontend
function startFrontend() {
    return new Promise((resolve, reject) => {
        console.log('⚛️  Starting frontend server...');
        
        if (!fs.existsSync('frontend/node_modules')) {
            console.log('❌ Node modules not found. Please run npm run setup first');
            process.exit(1);
        }
        
        let command, args;
        try {
            execSync('yarn --version', { stdio: 'ignore' });
            command = 'yarn';
            args = ['start'];
        } catch (error) {
            command = 'npm';
            args = ['start'];
        }
        
        const frontend = spawn(command, args, {
            cwd: 'frontend',
            stdio: 'inherit'
        });
        
        frontend.on('error', (error) => {
            console.log('❌ Failed to start frontend:', error.message);
            reject(error);
        });
        
        setTimeout(() => {
            console.log('✅ Frontend started on http://localhost:3000');
            resolve(frontend);
        }, 5000);
    });
}

// Main execution
async function main() {
    try {
        // Check ports
        const backendPortFree = await checkPort(8001);
        const frontendPortFree = await checkPort(3000);
        
        if (!backendPortFree) {
            console.log('❌ Port 8001 is already in use');
            process.exit(1);
        }
        
        if (!frontendPortFree) {
            console.log('❌ Port 3000 is already in use');
            process.exit(1);
        }
        
        await checkMongoDB();
        const backend = await startBackend();
        const frontend = await startFrontend();
        
        console.log('');
        console.log('🎉 CineGraph is running!');
        console.log('📱 Frontend: http://localhost:3000');
        console.log('🔧 Backend API: http://localhost:8001');
        console.log('📚 API Docs: http://localhost:8001/docs');
        console.log('');
        console.log('Press Ctrl+C to stop all servers');
        
        // Handle cleanup
        process.on('SIGINT', () => {
            console.log('\n🛑 Shutting down servers...');
            backend.kill();
            frontend.kill();
            process.exit(0);
        });
        
        process.on('SIGTERM', () => {
            backend.kill();
            frontend.kill();
            process.exit(0);
        });
        
    } catch (error) {
        console.log('❌ Failed to start development environment:', error.message);
        process.exit(1);
    }
}

main();