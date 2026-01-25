# 🎬 Quick Setup Guide - CineGraph

## ⚡ 3-Minute Setup

### Step 1: Get TMDB API Key (2 minutes)

1. Visit: https://www.themoviedb.org/settings/api
2. Sign up or log in (free account)
3. Request API key → Choose "Developer"
4. Copy your **API Key (v3 auth)**

### Step 2: Add API Key (30 seconds)

Edit `/app/backend/.env` and replace the placeholder:

```bash
TMDB_API_KEY="paste_your_key_here"
```

### Step 3: Restart Backend (30 seconds)

```bash
sudo supervisorctl restart backend
```

### ✅ Done!

Your movie recommendation platform is now live! Open your app and start discovering movies.

---

## 🎯 Quick Test

1. **Search**: Type "inception" in the search bar
2. **Explore**: Click on the movie card
3. **Discover**: Get 10 similar recommendations
4. **Stream**: See where to watch in your country

---

## 🆘 Troubleshooting

**Still seeing "API key not configured"?**
- Double-check the key has no extra spaces
- Make sure you saved the `.env` file
- Restart: `sudo supervisorctl restart backend`

**Need more help?**
- Check backend logs: `tail -n 50 /var/log/supervisor/backend.err.log`
- Verify backend is running: `sudo supervisorctl status backend`

---

## 📚 Full Documentation

See `/app/README.md` for complete documentation including:
- Project structure
- API endpoints
- Design system details
- Advanced features
- Enhancement ideas
