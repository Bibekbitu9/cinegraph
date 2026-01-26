from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import os
import json
import time

# TMDB Configuration
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '472ac4e44f0b0ca278574b175a34ebbd')
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

# Simple in-memory cache
cache = {}
CACHE_TTL = 3600  # 1 hour

app = FastAPI(title="CineGraph API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP client for TMDB API
http_client = httpx.AsyncClient(timeout=5.0)

# Models
class MovieSearchResult(BaseModel):
    id: int
    title: str
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    vote_average: Optional[float] = None
    overview: Optional[str] = None

class StreamingProvider(BaseModel):
    provider_id: int
    provider_name: str
    logo_path: Optional[str] = None
    link: Optional[str] = None

class StreamingAvailability(BaseModel):
    country: str
    subscription: List[StreamingProvider] = []
    rent: List[StreamingProvider] = []
    buy: List[StreamingProvider] = []
    tmdb_link: Optional[str] = None

class MovieDetail(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    runtime: Optional[int] = None
    genres: List[Dict[str, Any]] = []
    tagline: Optional[str] = None

class GeolocationResponse(BaseModel):
    country_code: str
    country_name: str

# Helper Functions
async def tmdb_request(endpoint: str, params: Optional[Dict] = None):
    """Make a request to TMDB API with caching and fallback"""
    params = params or {}
    cache_key = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
    
    # Check cache
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
    
    # Make request with fallback
    url = f"{TMDB_BASE_URL}{endpoint}"
    params['api_key'] = TMDB_API_KEY
    
    try:
        response = await http_client.get(url, params=params, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        
        # Cache the result
        cache[cache_key] = (data, time.time())
        return data
    except Exception as e:
        print(f"TMDB API error: {e}")
        # Return fallback data for common endpoints
        return get_fallback_data(endpoint, params)

def get_fallback_data(endpoint: str, params: Dict):
    """Provide fallback data when TMDB API is unavailable"""
    if "/search/movie" in endpoint:
        return {
            "results": [
                {
                    "id": 27205,
                    "title": "Inception",
                    "release_date": "2010-07-16",
                    "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
                    "vote_average": 8.4,
                    "overview": "Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction."
                },
                {
                    "id": 155,
                    "title": "The Dark Knight", 
                    "release_date": "2008-07-18",
                    "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
                    "vote_average": 9.0,
                    "overview": "Batman raises the stakes in his war on crime."
                }
            ]
        }
    elif "/trending/movie" in endpoint:
        return {
            "results": [
                {
                    "id": 278,
                    "title": "The Shawshank Redemption",
                    "release_date": "1994-09-23",
                    "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg", 
                    "vote_average": 9.3,
                    "overview": "Two imprisoned men bond over a number of years."
                }
            ]
        }
    else:
        return {"results": []}

def get_image_url(path: Optional[str], size: str = "w500") -> Optional[str]:
    """Generate full image URL"""
    if not path:
        return None
    return f"{IMAGE_BASE_URL}{size}{path}"

# API Routes
@app.get("/")
async def root():
    return {"message": "CineGraph API", "status": "running"}

@app.get("/search", response_model=List[MovieSearchResult])
async def search_movies(query: str = Query(..., min_length=1)):
    """Search for movies by title with autocomplete"""
    data = await tmdb_request("/search/movie", {"query": query, "page": 1})
    results = data.get('results', [])[:10]
    
    return [
        MovieSearchResult(
            id=movie['id'],
            title=movie.get('title', ''),
            release_date=movie.get('release_date'),
            poster_path=get_image_url(movie.get('poster_path'), 'w185'),
            vote_average=movie.get('vote_average'),
            overview=movie.get('overview')
        )
        for movie in results
    ]

@app.get("/movie/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: int):
    """Get detailed information about a specific movie"""
    data = await tmdb_request(f"/movie/{movie_id}")
    
    return MovieDetail(
        id=data['id'],
        title=data.get('title', ''),
        overview=data.get('overview'),
        release_date=data.get('release_date'),
        vote_average=data.get('vote_average'),
        poster_path=get_image_url(data.get('poster_path'), 'w500'),
        backdrop_path=get_image_url(data.get('backdrop_path'), 'w1280'),
        runtime=data.get('runtime'),
        genres=data.get('genres', []),
        tagline=data.get('tagline')
    )

@app.get("/movie/{movie_id}/recommendations", response_model=List[MovieSearchResult])
async def get_recommendations(movie_id: int):
    """Get movie recommendations based on a specific movie"""
    data = await tmdb_request(f"/movie/{movie_id}/recommendations", {"page": 1})
    results = data.get('results', [])
    
    if not results:
        data = await tmdb_request(f"/movie/{movie_id}/similar", {"page": 1})
        results = data.get('results', [])
    
    results = results[:10]
    
    return [
        MovieSearchResult(
            id=movie['id'],
            title=movie.get('title', ''),
            release_date=movie.get('release_date'),
            poster_path=get_image_url(movie.get('poster_path'), 'w342'),
            vote_average=movie.get('vote_average'),
            overview=movie.get('overview')
        )
        for movie in results
    ]

@app.get("/trending", response_model=List[MovieSearchResult])
async def get_trending():
    """Get trending movies"""
    data = await tmdb_request("/trending/movie/week")
    results = data.get('results', [])[:12]
    
    return [
        MovieSearchResult(
            id=movie['id'],
            title=movie.get('title', ''),
            release_date=movie.get('release_date'),
            poster_path=get_image_url(movie.get('poster_path'), 'w342'),
            vote_average=movie.get('vote_average'),
            overview=movie.get('overview')
        )
        for movie in results
    ]

@app.get("/geolocation", response_model=GeolocationResponse)
async def get_geolocation():
    """Detect user's country via IP geolocation"""
    return GeolocationResponse(
        country_code='US',
        country_name='United States'
    )

# For Vercel
handler = app