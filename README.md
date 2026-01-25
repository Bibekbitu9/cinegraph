# 🎬 CineGraph - AI-Powered Movie Recommendation Platform

<div align="center">

![CineGraph Banner](https://img.shields.io/badge/CineGraph-AI%20Movie%20Recommendations-7C3AED?style=for-the-badge&logo=movie&logoColor=white)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Now-2DD4BF?style=for-the-badge)](https://screenscout-5.preview.emergentagent.com)
[![API Docs](https://img.shields.io/badge/API-Documentation-E11D48?style=for-the-badge)](https://screenscout-5.preview.emergentagent.com/api/api-info)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**Discover your next favorite movie with AI-powered recommendations**

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack) • [API](#-api) • [Documentation](#-documentation)

</div>

---

## ✨ Features

### 🎯 Core Features
- **🤖 AI-Powered Recommendations** - Get 10 similar movies based on genres, themes, and keywords
- **🔍 Smart Search** - Real-time autocomplete search across 1M+ movies
- **🌍 Global Streaming** - See where to watch in 40+ countries (Netflix, Disney+, Prime Video, JioHotstar, etc.)
- **🔗 Direct Links** - Clickable OTT platform links that take you straight to the movie
- **📍 Geolocation** - Auto-detect your country or manually select from 40+ options
- **📊 Trending Movies** - Weekly updated list of popular films

### 🎨 Design
- **Dark Electric Noir Theme** - Cinematic aesthetic with glassmorphism effects
- **Smooth Animations** - Framer Motion powered interactions
- **Film Grain Texture** - Authentic cinema experience
- **Responsive Design** - Perfect on mobile, tablet, and desktop

### 🚀 Technical Features
- **SEO Optimized** - Meta tags, Schema.org, robots.txt, sitemap
- **AI Agent Ready** - Discoverable by ChatGPT, Claude, Perplexity
- **Fast Performance** - Caching, debouncing, optimized API calls
- **Error Handling** - User-friendly error messages
- **Real-time Updates** - Hot reload, instant feedback

---

## 🎥 Demo

### Live Application
👉 **[Try CineGraph Now](https://screenscout-5.preview.emergentagent.com)**

### Key Flows

**1. Search for a Movie**
```
Type "Inception" → See autocomplete results → Click to explore
```

**2. Get Recommendations**
```
View movie → Click "Get Similar Movies" → Browse 10 recommendations
```

**3. Find Where to Watch**
```
Open movie details → See streaming options in your country → Click provider link
```

**4. Change Country**
```
Click country selector → Search/browse 40+ countries → Update streaming data
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB
- TMDB API Key (free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Bibekbitu9/cinegraph.git
cd cinegraph
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Add your TMDB API key to .env
echo 'TMDB_API_KEY="your_api_key_here"' >> .env

# Start backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

3. **Frontend Setup**
```bash
cd frontend
yarn install
yarn start
```

4. **Get TMDB API Key**
   - Visit [TMDB](https://www.themoviedb.org/settings/api)
   - Create free account
   - Request API key (Developer option)
   - Copy API Key (v3 auth)

### Environment Variables

**Backend** (`/backend/.env`):
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="cinegraph"
TMDB_API_KEY="your_tmdb_api_key"
CORS_ORIGINS="*"
```

**Frontend** (`/frontend/.env`):
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI framework
- **Framer Motion** - Animations
- **TailwindCSS** - Styling
- **Shadcn/UI** - Component library
- **Lenis** - Smooth scrolling
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **Motor** - Async MongoDB driver
- **httpx** - Async HTTP client
- **Pydantic** - Data validation

### External APIs
- **TMDB API** - Movie data and streaming availability
- **ipapi.co** - IP geolocation

### Infrastructure
- **MongoDB** - Database
- **Supervisor** - Process management
- **Kubernetes** - Container orchestration

---

## 📡 API

### Base URL
```
https://screenscout-5.preview.emergentagent.com/api
```

### Endpoints

#### Search Movies
```http
GET /api/search?query={movie_name}
```

#### Get Movie Details
```http
GET /api/movie/{movie_id}
```

#### Get Recommendations
```http
GET /api/movie/{movie_id}/recommendations
```

#### Get Streaming Availability
```http
GET /api/movie/{movie_id}/streaming?country={country_code}
```

#### Get Trending Movies
```http
GET /api/trending
```

#### Detect Location
```http
GET /api/geolocation
```

#### API Documentation
```http
GET /api/api-info
```

**Full API Guide:** [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)

---

## 📚 Documentation

### User Guides
- **[README.md](README.md)** - Complete project overview
- **[SETUP.md](SETUP.md)** - 3-minute quick start guide
- **[STATUS.md](STATUS.md)** - Current operational status

### Developer Guides
- **[AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)** - AI integration guide for ChatGPT, Claude, etc.
- **[SEO_IMPLEMENTATION.md](SEO_IMPLEMENTATION.md)** - Complete SEO documentation
- **[DEPLOYMENT_READINESS.md](DEPLOYMENT_READINESS.md)** - Production deployment checklist
- **[STREAMING_LINKS_FEATURE.md](STREAMING_LINKS_FEATURE.md)** - OTT platform links implementation

---

## 🌍 Supported Countries

**40+ Countries Including:**
- 🇺🇸 United States
- 🇮🇳 India
- 🇬🇧 United Kingdom
- 🇨🇦 Canada
- 🇦🇺 Australia
- 🇩🇪 Germany
- 🇫🇷 France
- 🇪🇸 Spain
- 🇮🇹 Italy
- 🇧🇷 Brazil
- 🇲🇽 Mexico
- 🇯🇵 Japan
- 🇰🇷 South Korea
- 🇸🇬 Singapore
- ... and 25+ more

---

## 🎯 Use Cases

### For Movie Enthusiasts
- Discover similar movies based on favorites
- Find where to watch legally
- Track trending movies weekly
- Explore movies by genre and theme

### For AI Agents (ChatGPT, Claude, Perplexity)
- Help users find movie recommendations
- Answer "Where can I watch X?" questions
- Suggest trending movies
- Provide streaming availability

### For Developers
- REST API for movie data
- Streaming availability by country
- Real-time recommendations
- Open API documentation

---

## 🔧 Configuration

### Customization

**Colors** (`tailwind.config.js`):
```javascript
colors: {
  'electric-violet': '#7C3AED',
  'neon-teal': '#2DD4BF',
  'cinema-red': '#E11D48',
  'obsidian': '#030305',
}
```

**Fonts** (`index.css`):
```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=DM+Sans:wght@400;500;700&display=swap');
```

---

## 📈 Performance

- **First Load:** < 2 seconds
- **Search Response:** < 500ms
- **API Caching:** 1 hour TTL
- **Lighthouse Score:** 95+
- **SEO Score:** 95/100

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **TMDB** - Movie data and streaming information
- **Emergent Labs** - Development platform
- **Shadcn/UI** - Beautiful component library
- **Framer Motion** - Animation library
- Movie enthusiasts worldwide 🎬

---

## 📧 Contact

**Project Link:** [https://github.com/Bibekbitu9/cinegraph](https://github.com/Bibekbitu9/cinegraph)

**Live Demo:** [https://screenscout-5.preview.emergentagent.com](https://screenscout-5.preview.emergentagent.com)

**Issues:** [GitHub Issues](https://github.com/Bibekbitu9/cinegraph/issues)

---

<div align="center">

**Built with ❤️ for movie enthusiasts**

⭐ Star this repo if you found it helpful!

</div>
