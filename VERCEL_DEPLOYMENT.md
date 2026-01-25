# 🚀 CineGraph Vercel Deployment Guide

## Overview

CineGraph is a full-stack application:
- **Frontend:** React (can be deployed on Vercel)
- **Backend:** FastAPI (needs serverless or separate hosting)
- **Database:** MongoDB (use MongoDB Atlas)

## Deployment Strategy

### Option 1: Frontend on Vercel + Backend Elsewhere (Recommended)
- Deploy React frontend to Vercel
- Keep FastAPI backend on Emergent or deploy to Railway/Render
- Use MongoDB Atlas for database

### Option 2: Full Stack on Vercel (Serverless)
- Deploy React frontend to Vercel
- Deploy FastAPI as Vercel Serverless Functions
- Use MongoDB Atlas for database

---

## 🎯 Option 1: Frontend Only on Vercel (Easiest)

### Step 1: Prepare Frontend for Vercel

Create `vercel.json` in `/app/frontend/`:

```json
{
  "buildCommand": "yarn build",
  "outputDirectory": "build",
  "devCommand": "yarn start",
  "installCommand": "yarn install",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Step 2: Update Environment Variables

The frontend `.env` needs to point to your backend:

```env
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

Options for backend:
1. **Keep Emergent URL:** `https://screenscout-5.preview.emergentagent.com`
2. **Deploy backend to Railway:** Railway.app (free tier)
3. **Deploy backend to Render:** Render.com (free tier)

### Step 3: Deploy Frontend to Vercel

#### Via Vercel Dashboard:
1. Go to: https://vercel.com/new
2. Click "Import Project"
3. Select "Import Git Repository"
4. Choose: `Bibekbitu9/cinegraph`
5. **Root Directory:** Set to `frontend`
6. **Framework Preset:** Create React App (auto-detected)
7. **Build Command:** `yarn build`
8. **Output Directory:** `build`
9. **Install Command:** `yarn install`

#### Environment Variables:
Add in Vercel dashboard:
```
REACT_APP_BACKEND_URL=https://screenscout-5.preview.emergentagent.com
```

10. Click **"Deploy"**

### Step 4: Configure Backend CORS

Update backend `/app/backend/server.py` to allow Vercel domain:

```python
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

# Or specifically:
CORS_ORIGINS = [
    "https://your-vercel-app.vercel.app",
    "https://screenscout-5.preview.emergentagent.com",
    "*"
]
```

---

## 🚀 Option 2: Full Stack on Vercel (Advanced)

### Architecture
- Frontend: `/frontend` → Vercel static hosting
- Backend: `/api` → Vercel Serverless Functions
- Database: MongoDB Atlas

### Step 1: Create Vercel Configuration

Create `/app/vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "backend/server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/server.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "TMDB_API_KEY": "@tmdb_api_key",
    "MONGO_URL": "@mongo_url"
  }
}
```

### Step 2: Restructure Backend for Serverless

Create `/app/api/index.py` (Vercel entry point):

```python
from backend.server import app

# Vercel expects app to be named 'app' or handler
handler = app
```

### Step 3: Update Requirements

Create `/app/api/requirements.txt`:
```
fastapi
motor
httpx
pydantic
```

### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd /app
vercel --prod
```

### Step 5: Add Environment Variables

```bash
vercel env add TMDB_API_KEY
vercel env add MONGO_URL
vercel env add DB_NAME
```

---

## 📊 Comparison

| Feature | Frontend Only | Full Stack Vercel |
|---------|--------------|-------------------|
| Setup Complexity | ⭐⭐ Easy | ⭐⭐⭐⭐ Complex |
| Backend Control | Keep current | Serverless limits |
| Cost | Free | Free (with limits) |
| Performance | Excellent | Good |
| Scalability | High | Medium |
| Maintenance | Low | Medium |

---

## 🎯 Recommended Approach

**Deploy Frontend to Vercel + Keep Backend on Emergent**

### Advantages:
- ✅ Simple setup
- ✅ Frontend gets Vercel CDN
- ✅ Backend stays fully functional
- ✅ No serverless limitations
- ✅ Easy to manage

### Steps:
1. Create `frontend/vercel.json`
2. Push to GitHub
3. Connect GitHub repo to Vercel
4. Set root directory to `frontend`
5. Add `REACT_APP_BACKEND_URL` env var
6. Deploy!

---

## 🔧 Manual Deployment Steps

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Navigate to Frontend

```bash
cd /app/frontend
```

### Step 4: Deploy

```bash
vercel --prod
```

### Step 5: Follow Prompts

- Setup and deploy: Yes
- Which scope: Your account
- Link to existing project: No
- Project name: cinegraph
- Directory: ./ (current)
- Override settings: No

### Step 6: Add Environment Variables

After deployment:
```bash
vercel env add REACT_APP_BACKEND_URL production
# Enter: https://screenscout-5.preview.emergentagent.com
```

---

## 🌐 Custom Domain (Optional)

### On Vercel:
1. Go to project settings
2. Click "Domains"
3. Add your domain: `cinegraph.yourdomain.com`
4. Follow DNS setup instructions

---

## 🗄️ MongoDB Atlas Setup (If needed)

If you want to move database to cloud:

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Create free cluster
3. Get connection string
4. Update `MONGO_URL` in backend

---

## ⚡ Quick Start (Frontend Only)

```bash
# 1. Create frontend/vercel.json
cat > /app/frontend/vercel.json << 'EOF'
{
  "buildCommand": "yarn build",
  "outputDirectory": "build",
  "devCommand": "yarn start",
  "framework": "create-react-app"
}
EOF

# 2. Commit and push
cd /app
git add frontend/vercel.json
git commit -m "Add Vercel configuration"
git push origin main

# 3. Deploy via Vercel dashboard
# Go to https://vercel.com/new
# Import from GitHub
# Select cinegraph repo
# Set root directory: frontend
# Deploy!
```

---

## 📝 Important Notes

### Backend Considerations:
- Vercel serverless functions have **10s timeout**
- TMDB API calls might be slow
- Consider keeping backend on Emergent

### Database Considerations:
- MongoDB on Vercel needs serverless connection
- Use MongoDB Atlas for production
- Connection pooling is different

### Cost Considerations:
- Vercel: Free for hobby projects
- Emergent: 50 credits/month for full deployment
- MongoDB Atlas: Free tier available

---

## 🆘 Troubleshooting

### Build Fails:
- Check `package.json` has all dependencies
- Ensure `yarn.lock` is committed
- Check Node version compatibility

### API Not Working:
- Verify `REACT_APP_BACKEND_URL` is set
- Check backend CORS allows Vercel domain
- Test API endpoint directly

### Environment Variables Not Working:
- Must start with `REACT_APP_` for React
- Must be set in Vercel dashboard
- Redeploy after adding env vars

---

## ✅ Success Checklist

- [ ] Frontend deploys successfully
- [ ] Can access Vercel URL
- [ ] Search functionality works
- [ ] Movie recommendations load
- [ ] Streaming links work
- [ ] Country selector functional
- [ ] API calls succeed

---

## 🎉 After Deployment

Your app will be live at:
- **Vercel URL:** `https://cinegraph-xxx.vercel.app`
- **Custom Domain:** `https://cinegraph.yourdomain.com` (if configured)

Update your GitHub README with new URL!

---

**Ready to deploy? Let me know which option you prefer, and I'll help you set it up!**
