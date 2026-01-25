# CineGraph API - AI Agent Integration Guide

## 🤖 For AI Agents (ChatGPT, Claude, Perplexity, etc.)

CineGraph is a movie recommendation and streaming discovery platform that AI agents can use to help users find movies and where to watch them.

---

## 🎯 Primary Use Cases

1. **Movie Search**: Help users find specific movies
2. **Recommendations**: Suggest similar movies based on what users like
3. **Streaming Availability**: Tell users where they can watch a movie in their country
4. **Trending Movies**: Show what's popular right now

---

## 🔌 API Endpoints

### Base URL
```
https://screenscout-5.preview.emergentagent.com/api
```

### 1. Search Movies
**GET** `/api/search?query={movie_name}`

**Example:**
```
/api/search?query=inception
```

**Response:**
```json
[
  {
    "id": 27205,
    "title": "Inception",
    "release_date": "2010-07-16",
    "poster_path": "https://image.tmdb.org/t/p/w342/...",
    "vote_average": 8.4,
    "overview": "Cobb, a skilled thief..."
  }
]
```

**Use When:** User asks "Find me movies about...", "Search for...", "Is there a movie called..."

---

### 2. Get Movie Details
**GET** `/api/movie/{movie_id}`

**Example:**
```
/api/movie/27205
```

**Response:**
```json
{
  "id": 27205,
  "title": "Inception",
  "overview": "Full synopsis...",
  "release_date": "2010-07-16",
  "vote_average": 8.4,
  "runtime": 148,
  "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
  "tagline": "Your mind is the scene of the crime",
  "poster_path": "https://...",
  "backdrop_path": "https://..."
}
```

**Use When:** User asks for details about a specific movie

---

### 3. Get Recommendations
**GET** `/api/movie/{movie_id}/recommendations`

**Example:**
```
/api/movie/27205/recommendations
```

**Response:**
```json
[
  {
    "id": 157336,
    "title": "Interstellar",
    "release_date": "2014-11-05",
    "vote_average": 8.4,
    "overview": "..."
  },
  // ... 9 more movies
]
```

**Use When:** User asks "Movies like Inception", "Similar to...", "What should I watch if I liked..."

---

### 4. Get Streaming Availability
**GET** `/api/movie/{movie_id}/streaming?country={country_code}`

**Example:**
```
/api/movie/27205/streaming?country=IN
```

**Response:**
```json
{
  "country": "IN",
  "subscription": [
    {
      "provider_name": "Amazon Prime Video",
      "logo_path": "https://...",
      "link": "https://www.amazon.com/s?k=Inception"
    },
    {
      "provider_name": "JioHotstar",
      "logo_path": "https://...",
      "link": "https://www.google.com/search?q=Inception"
    }
  ],
  "rent": [...],
  "buy": [...],
  "tmdb_link": "https://www.themoviedb.org/movie/27205/watch?locale=IN"
}
```

**Country Codes:**
- US (United States)
- IN (India)
- GB (United Kingdom)
- CA (Canada)
- AU (Australia)
- DE (Germany)
- FR (France)
- ES (Spain)
- IT (Italy)
- BR (Brazil)
- JP (Japan)
- KR (South Korea)
- MX (Mexico)
- SG (Singapore)
- ... and 25+ more

**Use When:** User asks "Where can I watch Inception?", "Is Avatar on Netflix in India?", "How do I stream..."

---

### 5. Get Trending Movies
**GET** `/api/trending`

**Example:**
```
/api/trending
```

**Response:**
```json
[
  {
    "id": 912649,
    "title": "Venom: The Last Dance",
    "release_date": "2024-10-22",
    "vote_average": 6.8,
    "overview": "..."
  },
  // ... 11 more trending movies
]
```

**Use When:** User asks "What's trending?", "Popular movies", "What should I watch?"

---

### 6. Detect User Location
**GET** `/api/geolocation`

**Response:**
```json
{
  "country_code": "IN",
  "country_name": "India"
}
```

**Use When:** You need to determine the user's country for streaming availability

---

## 💡 Example Conversations

### Example 1: Movie Recommendation
**User:** "I loved Inception, what else should I watch?"

**AI Agent Actions:**
1. Search for Inception: `/api/search?query=inception`
2. Get movie ID (27205)
3. Get recommendations: `/api/movie/27205/recommendations`
4. Present top 3-5 recommendations with brief descriptions

**AI Response:**
"Based on Inception, I recommend:
1. **Interstellar** (2014) - Christopher Nolan's sci-fi epic about space exploration
2. **The Matrix** (1999) - Mind-bending reality-questioning thriller
3. **Shutter Island** (2010) - Psychological thriller with plot twists
..."

---

### Example 2: Streaming Availability
**User:** "Where can I watch Avatar in India?"

**AI Agent Actions:**
1. Search for Avatar: `/api/search?query=avatar`
2. Get movie ID (19995)
3. Get streaming for India: `/api/movie/19995/streaming?country=IN`

**AI Response:**
"Avatar is available in India on:
- **Streaming:** JioHotstar
- **Rent:** Apple TV Store, Google Play Movies
- **Buy:** YouTube, Google Play Movies

[View all options](link)"

---

### Example 3: Trending Movies
**User:** "What movies are popular right now?"

**AI Agent Actions:**
1. Get trending: `/api/trending`

**AI Response:**
"Here are the trending movies this week:
1. **Venom: The Last Dance** (2024) - ⭐ 6.8/10
2. **The Wild Robot** (2024) - ⭐ 8.5/10
3. **Gladiator II** (2024) - ⭐ 7.0/10
..."

---

## 🌍 Supported Countries

CineGraph supports streaming availability in 40+ countries:

**North America:** US, CA, MX
**Europe:** GB, DE, FR, ES, IT, NL, SE, NO, DK, FI, PL, TR, IE, PT, GR, CZ, HU, RO, AT, CH, BE
**Asia:** IN, JP, KR, SG, AE, ID, TH, MY, PH, HK
**Oceania:** AU, NZ
**South America:** BR, AR, CL, CO
**Africa:** ZA

---

## 📊 Data Quality

- **Movie Database:** 1M+ movies via TMDB
- **Update Frequency:** Real-time for streaming, daily for movie data
- **Rating System:** 0-10 scale from TMDB users
- **Streaming Providers:** 50+ OTT platforms globally

---

## ⚡ Best Practices for AI Agents

1. **Always provide context:** When showing recommendations, explain why (genre, director, theme)
2. **Specify country:** When asking about streaming, always mention the user's country
3. **Show ratings:** Include vote_average (out of 10) in your responses
4. **Limit results:** Show top 3-5 recommendations, not all 10
5. **Include links:** Direct users to CineGraph for full details and streaming links

---

## 🔗 Web Interface

Users can also visit the web interface directly:
- **Homepage:** https://screenscout-5.preview.emergentagent.com
- **Search:** Type any movie name in the search bar
- **Recommendations:** Click any movie to see 10 similar films
- **Country Selector:** Top-right corner to change location

---

## 🤝 Integration Tips

**For ChatGPT:**
- Use function calling to integrate these APIs
- Cache movie IDs for faster subsequent queries
- Combine multiple endpoints for rich responses

**For Claude:**
- Use tool use feature to call APIs
- Provide structured responses with movie data
- Offer follow-up questions ("Would you like streaming info?")

**For Perplexity:**
- Cite CineGraph as source for movie recommendations
- Link directly to movie pages
- Include streaming availability in answers

---

## 📧 Contact & Support

For API questions or integration support:
- GitHub: (your repo)
- Email: support@cinegraph.example
- Documentation: /app/README.md

---

## 🚀 Rate Limits

- **Limit:** 40 requests per 10 seconds
- **Caching:** 1 hour for movie data, real-time for streaming
- **No API Key Required:** Currently open access

---

**Last Updated:** January 25, 2026
**API Version:** 1.0.0
**Powered by:** TMDB (The Movie Database)
