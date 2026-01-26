# 🚀 Deploy CineGraph to Vercel

## Quick Deployment Steps

### 1. **Prepare for Deployment**
Your project is already configured for Vercel deployment with:
- ✅ `vercel.json` configuration
- ✅ Simplified backend API
- ✅ Frontend build configuration
- ✅ TMDB API key included

### 2. **Deploy to Vercel**

**Option A: GitHub Integration (Recommended)**
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. Go to [vercel.com](https://vercel.com)
3. Sign up/login with GitHub
4. Click "New Project"
5. Import your `cinegraph` repository
6. Vercel will auto-detect the configuration
7. Click "Deploy"

**Option B: Vercel CLI**
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from your project directory:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N**
   - Project name: **cinegraph** (or your preferred name)
   - Directory: **./frontend**
   - Override settings? **N**

### 3. **Environment Variables**
The TMDB API key is already configured in `vercel.json`. If you need to update it:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add: `TMDB_API_KEY` = `472ac4e44f0b0ca278574b175a34ebbd`

### 4. **Test Your Deployment**
Once deployed, Vercel will provide a URL like:
`https://cinegraph-xyz.vercel.app`

Test these endpoints:
- **Frontend**: `https://your-app.vercel.app`
- **API**: `https://your-app.vercel.app/api/`
- **Search**: `https://your-app.vercel.app/api/search?query=inception`
- **Trending**: `https://your-app.vercel.app/api/trending`

## 🎯 What's Included

### Backend (`/api/*`)
- FastAPI serverless functions
- TMDB API integration with fallback data
- CORS enabled for frontend
- Caching for better performance

### Frontend
- React 18 application
- TailwindCSS styling
- Framer Motion animations
- Responsive design
- SEO optimized

## 🔧 Troubleshooting

**Build Errors:**
- Check Vercel build logs in dashboard
- Ensure all dependencies are in `package.json`

**API Errors:**
- Verify TMDB API key in environment variables
- Check function logs in Vercel dashboard

**CORS Issues:**
- Backend is configured to allow all origins
- Frontend uses relative API paths (`/api/*`)

## 🚀 Next Steps

After successful deployment:
1. **Custom Domain**: Add your own domain in Vercel settings
2. **Analytics**: Enable Vercel Analytics
3. **Performance**: Monitor Core Web Vitals
4. **Updates**: Push to GitHub to auto-deploy updates

## 📱 Expected Result

Your CineGraph app will be live with:
- ✅ Movie search functionality
- ✅ AI-powered recommendations  
- ✅ Trending movies
- ✅ Responsive design
- ✅ Fast global CDN delivery

**Deployment time**: ~2-3 minutes
**Global availability**: Immediate via Vercel Edge Network

---

**Ready to deploy? Push to GitHub and connect to Vercel!** 🎬