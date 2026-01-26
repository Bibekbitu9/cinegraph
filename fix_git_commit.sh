#!/bin/bash

echo "🔧 Fixing Git Commit Issues"
echo "============================"

# Configure Git identity (required for commits)
echo "📋 Step 1: Configure Git identity"
echo "Please enter your details:"

read -p "Enter your name: " git_name
read -p "Enter your email: " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"

echo "✅ Git identity configured"
echo "Name: $git_name"
echo "Email: $git_email"

# Check git status
echo ""
echo "📋 Step 2: Check git status"
git status

# Try to commit again with a simpler message
echo ""
echo "📋 Step 3: Commit with simple message"
git add .
git commit -m "CineGraph: Ready for Vercel deployment"

if [ $? -eq 0 ]; then
    echo "✅ Commit successful!"
    
    # Push to production branch
    echo ""
    echo "📋 Step 4: Push to GitHub"
    git push -u origin production
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "🎉 Ready for Vercel deployment!"
        echo "Go to: https://vercel.com/new"
    else
        echo "❌ Push failed. Check your GitHub remote URL"
        echo "Run: git remote -v"
    fi
else
    echo "❌ Commit failed. Let's check what's wrong:"
    echo ""
    echo "Checking git status:"
    git status
    echo ""
    echo "Checking git log:"
    git log --oneline -5
fi