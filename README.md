# CineGraph - Movie Recommendation Platform

A professional-grade movie recommendation platform with AI-powered suggestions, featuring real-time streaming availability detection and a stunning Electric Noir cinematic design.

## 🎬 Features

- **Smart Movie Search**: Dynamic autocomplete search with instant results
- **Intelligent Recommendations**: Get 10 similar movies based on metadata analysis (genres, themes, keywords)
- **Detailed Movie Profiles**: Complete information including synopsis, release year, ratings, runtime, and high-quality posters
- **Streaming Availability**: Real-time detection of where to watch (subscription/rental/purchase) based on your location
- **Geographic Detection**: Automatic IP-based location detection with manual country selection
- **Responsive Design**: Seamless experience across mobile, tablet, and desktop
- **Cinematic Aesthetic**: Dark Electric Noir theme with glassmorphism effects and smooth animations

## 🚀 Getting Started

### Prerequisites

- The application is already running in your Emergent environment
- You need a free TMDB API key to fetch movie data

### Step 1: Get Your TMDB API Key

1. Go to [The Movie Database (TMDB)](https://www.themoviedb.org/)
2. Create a free account or sign in
3. Navigate to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy your API Key (v3 auth)

### Step 2: Configure Your API Key

1. Open the file `/app/backend/.env`
2. Replace `YOUR_API_KEY_HERE` with your actual TMDB API key:

```env
TMDB_API_KEY="your_actual_api_key_here"
```

3. Restart the backend:
```bash
sudo supervisorctl restart backend
```

### Step 3: Start Using CineGraph

1. Open your application in the browser
2. Search for any movie in the hero search bar
3. Click on a movie to see 10 similar recommendations
4. View detailed information and streaming availability
5. Discover your next favorite film!

## 📁 Project Structure

```
/app/
├── backend/
│   ├── server.py              # FastAPI backend with TMDB integration
│   ├── .env                   # Environment variables (add your API key here)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.js           # Landing page with search
│   │   │   └── RecommendationsPage.js # Movie recommendations grid
│   │   ├── components/
│   │   │   ├── HeroSearch.js         # Search with autocomplete
│   │   │   ├── MovieCard.js          # Movie card component
│   │   │   ├── MovieDetailModal.js   # Movie details modal
│   │   │   └── TrendingSection.js    # Trending movies
│   │   ├── App.js              # Main app with routing
│   │   └── index.css           # Global styles
│   └── package.json           # Node dependencies
└── design_guidelines.json     # Electric Noir design system
```

## 🎨 Design System

**CineGraph** features an "Electric Noir" aesthetic:
- **Colors**: Deep obsidian background with electric violet and neon teal accents
- **Typography**: Outfit (headings) + DM Sans (body text)
- **Effects**: Film grain texture, glassmorphism, neon glows
- **Animations**: Smooth scrolling (Lenis), entrance animations (Framer Motion)

## 🔌 API Endpoints

### Backend Routes (All prefixed with `/api`)

- `GET /api/search?query={movie_name}` - Search for movies
- `GET /api/movie/{movie_id}` - Get detailed movie information
- `GET /api/movie/{movie_id}/recommendations` - Get 10 similar movies
- `GET /api/movie/{movie_id}/streaming?country={code}` - Get streaming availability
- `GET /api/trending` - Get trending movies this week
- `GET /api/geolocation` - Detect user's country

## 🛠️ Tech Stack

- **Frontend**: React 19, Framer Motion, Lenis, TailwindCSS, Shadcn/UI
- **Backend**: FastAPI, httpx, Motor (MongoDB)
- **Database**: MongoDB
- **External APIs**: TMDB API v3, ipapi.co (geolocation)

## 🌍 Supported Countries

Streaming availability supports 60+ countries. The platform auto-detects your location or you can manually select your country.

## 📝 Usage Tips

1. **Search Tips**: Type at least 2 characters for autocomplete results
2. **Recommendations**: Click any movie card to see similar films
3. **Streaming Info**: Availability is based on your detected location (may vary by region)
4. **Navigation**: Use the back button to return to search from recommendations

## 🐛 Troubleshooting

### "TMDB API key not configured" Error
- Make sure you've added your API key to `/app/backend/.env`
- Restart the backend: `sudo supervisorctl restart backend`
- Verify the key is valid on TMDB's API settings page

### Streaming Information Not Showing
- Some movies may not have streaming data available in all regions
- Try a different country or popular movies for better results

### Search Not Working
- Check your internet connection
- Verify the backend is running: `sudo supervisorctl status backend`
- Check backend logs: `tail -n 50 /var/log/supervisor/backend.err.log`

## 📦 Dependencies

All dependencies are pre-installed. If you need to reinstall:

**Backend:**
```bash
cd /app/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd /app/frontend
yarn install
```

## 🎯 Next Steps & Enhancements

- **User Accounts**: Save favorite movies and create watchlists
- **Advanced Filters**: Filter by genre, year, rating, runtime
- **AI-Powered Insights**: Use LLMs for deeper movie analysis and personalized descriptions
- **Social Features**: Share recommendations with friends
- **Trailer Integration**: Watch trailers directly in the modal
- **Review System**: Add user reviews and ratings
- **Multiple Movies**: Search multiple movies at once for combined recommendations

## 📄 License

Built with ❤️ for movie enthusiasts. Powered by TMDB.

---

**Need Help?** Check the backend logs or frontend console for detailed error messages.
