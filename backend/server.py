from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import httpx
import time
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# TMDB Configuration
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'YOUR_API_KEY_HERE')
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

# Simple in-memory cache
cache = {}
CACHE_TTL = 3600  # 1 hour

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# HTTP client for TMDB API
http_client = httpx.AsyncClient(timeout=10.0)

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
    """Make a request to TMDB API with caching"""
    params = params or {}
    cache_key = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
    
    # Check cache
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
    
    # Make request
    url = f"{TMDB_BASE_URL}{endpoint}"
    params['api_key'] = TMDB_API_KEY
    
    try:
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Cache the result
        cache[cache_key] = (data, time.time())
        return data
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid TMDB API key. Please add your API key to backend/.env")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TMDB API error: {str(e)}")

def get_image_url(path: Optional[str], size: str = "w500") -> Optional[str]:
    """Generate full image URL"""
    if not path:
        return None
    return f"{IMAGE_BASE_URL}{size}{path}"

# API Routes
@api_router.get("/")
async def root():
    return {"message": "CineGraph API - Movie Recommendation Platform"}

@api_router.get("/search", response_model=List[MovieSearchResult])
async def search_movies(query: str = Query(..., min_length=1)):
    """Search for movies by title with autocomplete"""
    data = await tmdb_request("/search/movie", {"query": query, "page": 1})
    results = data.get('results', [])[:10]  # Limit to 10 results
    
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

@api_router.get("/movie/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: int):
    """Get detailed information about a specific movie"""
    data = await tmdb_request(f"/movie/{movie_id}", {
        "append_to_response": "credits,videos,keywords"
    })
    
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

@api_router.get("/movie/{movie_id}/recommendations", response_model=List[MovieSearchResult])
async def get_recommendations(movie_id: int):
    """Get movie recommendations based on a specific movie"""
    # Try recommendations endpoint first
    data = await tmdb_request(f"/movie/{movie_id}/recommendations", {"page": 1})
    results = data.get('results', [])
    
    # If no recommendations, try similar movies
    if not results:
        data = await tmdb_request(f"/movie/{movie_id}/similar", {"page": 1})
        results = data.get('results', [])
    
    # Limit to 10 results
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

@api_router.get("/movie/{movie_id}/streaming", response_model=StreamingAvailability)
async def get_streaming_availability(movie_id: int, country: str = "US"):
    """Get streaming availability for a movie in a specific country"""
    data = await tmdb_request(f"/movie/{movie_id}/watch/providers")
    providers_data = data.get('results', {}).get(country.upper(), {})
    
    # Provider ID to URL mapping for popular services
    provider_urls = {
        8: "https://www.netflix.com/search?q=",  # Netflix
        337: "https://www.disneyplus.com/search?q=",  # Disney+
        384: "https://www.hbomax.com/search?q=",  # HBO Max
        531: "https://www.paramountplus.com/search/?query=",  # Paramount+
        15: "https://tv.apple.com/search?q=",  # Apple TV+
        9: "https://www.amazon.com/s?k=",  # Amazon Prime
        10: "https://www.amazon.com/s?k=",  # Amazon Video
        2: "https://tv.apple.com/search?q=",  # Apple TV
        3: "https://play.google.com/store/search?q=",  # Google Play
        192: "https://www.youtube.com/results?search_query=",  # YouTube
        386: "https://www.peacocktv.com/search?q=",  # Peacock
        350: "https://www.apple.com/apple-tv-plus/",  # Apple TV+
        1899: "https://www.max.com/search?q=",  # Max (HBO Max)
    }
    
    def parse_providers(provider_list, movie_title: str = ""):
        return [
            StreamingProvider(
                provider_id=p['provider_id'],
                provider_name=p['provider_name'],
                logo_path=get_image_url(p.get('logo_path'), 'w92'),
                link=f"{provider_urls.get(p['provider_id'], 'https://www.google.com/search?q=')}{movie_title.replace(' ', '+')}" if movie_title else None
            )
            for p in provider_list
        ]
    
    # Get movie title for search links
    movie_data = await tmdb_request(f"/movie/{movie_id}")
    movie_title = movie_data.get('title', '')
    
    return StreamingAvailability(
        country=country.upper(),
        subscription=parse_providers(providers_data.get('flatrate', []), movie_title),
        rent=parse_providers(providers_data.get('rent', []), movie_title),
        buy=parse_providers(providers_data.get('buy', []), movie_title),
        tmdb_link=f"https://www.themoviedb.org/movie/{movie_id}/watch?locale={country.upper()}"
    )

@api_router.get("/trending", response_model=List[MovieSearchResult])
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

@api_router.get("/geolocation", response_model=GeolocationResponse)
async def get_geolocation():
    """Detect user's country via IP geolocation"""
    try:
        # Using a free IP geolocation service
        response = await http_client.get("https://ipapi.co/json/")
        data = response.json()
        return GeolocationResponse(
            country_code=data.get('country_code', 'US'),
            country_name=data.get('country_name', 'United States')
        )
    except Exception:
        # Default to US if geolocation fails
        return GeolocationResponse(
            country_code='US',
            country_name='United States'
        )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    await http_client.aclose()