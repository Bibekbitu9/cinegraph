#!/bin/bash

echo "🚀 CineGraph - Deploy to Production Branch"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    print_error "vercel.json not found. Make sure you're in the CineGraph project directory."
    exit 1
fi

print_info "Found CineGraph project files"

# Configure Git identity if not set
if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
    print_warning "Git identity not configured"
    
    # Set default identity (you can change these)
    git config user.name "Bibekbitu9"
    git config user.email "bibekbitu9@example.com"
    
    print_status "Git identity configured"
fi

# Initialize git if needed
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
fi

# Add remote origin if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    print_info "Adding GitHub remote..."
    git remote add origin https://github.com/Bibekbitu9/cinegraph.git
    print_status "Remote origin added"
else
    print_status "Remote origin already exists"
fi

# Check current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "main")
print_info "Current branch: $current_branch"

# Create and switch to production branch
print_info "Switching to production branch..."
git checkout -b production 2>/dev/null || git checkout production
print_status "On production branch"

# Add all files
print_info "Adding all files to staging..."
git add .
print_status "Files staged for commit"

# Show what will be committed
echo ""
print_info "Files to be committed:"
git status --short

# Commit changes
print_info "Committing changes..."
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
- Serverless FastAPI backend (/backend/api/)
- Optimized React frontend
- Environment variables configured
- Fallback data for offline mode

🔧 Technical stack:
- Backend: FastAPI + Python serverless functions
- Frontend: React 18 + TailwindCSS + Framer Motion
- API: TMDB integration with caching
- Deployment: Vercel edge network

📱 Ready for one-click deployment to Vercel!"

if [ $? -eq 0 ]; then
    print_status "Changes committed successfully"
else
    print_error "Commit failed"
    exit 1
fi

# Push to GitHub
print_info "Pushing to GitHub production branch..."
git push -u origin production

if [ $? -eq 0 ]; then
    print_status "Successfully pushed to GitHub!"
    
    echo ""
    echo "🎉 DEPLOYMENT READY!"
    echo "==================="
    echo ""
    print_info "Your CineGraph project is now on GitHub in the production branch"
    echo ""
    print_info "Next steps:"
    echo "1. Go to: https://vercel.com/new"
    echo "2. Sign in with GitHub"
    echo "3. Import repository: Bibekbitu9/cinegraph"
    echo "4. Select branch: production"
    echo "5. Click Deploy"
    echo ""
    print_info "Your app will be live in ~3 minutes at: https://cinegraph-[random].vercel.app"
    echo ""
    print_info "Features ready to test:"
    echo "• Movie search and recommendations"
    echo "• Trending movies"
    echo "• Responsive design"
    echo "• Global streaming availability"
    echo ""
    echo "🚀 Happy deploying!"
    
else
    print_error "Push failed!"
    echo ""
    print_info "Common solutions:"
    echo "1. Check your GitHub authentication"
    echo "2. Make sure the repository exists: https://github.com/Bibekbitu9/cinegraph"
    echo "3. Try: git remote set-url origin https://github.com/Bibekbitu9/cinegraph.git"
    echo ""
    print_info "Repository URL should be: https://github.com/Bibekbitu9/cinegraph.git"
fi