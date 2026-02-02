from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import time
import json
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# OMDb Configuration
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')
OMDB_BASE_URL = "http://www.omdbapi.com"

# Simple in-memory cache
cache = {}
CACHE_TTL = 3600  # 1 hour

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# HTTP client for OMDb API
http_client = httpx.AsyncClient(timeout=10.0)

# Models
class MovieSearchResult(BaseModel):
    id: str
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
    imdb_link: Optional[str] = None

class MovieDetail(BaseModel):
    id: str
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
async def omdb_request(params: Dict[str, Any]):
    """Make a request to OMDb API with caching"""
    if not OMDB_API_KEY:
        raise HTTPException(status_code=500, detail="OMDB_API_KEY is missing in backend/.env")

    # Add API key to params
    params = params.copy()
    params['apikey'] = OMDB_API_KEY
    
    # Create cache key
    cache_key = f"omdb_{json.dumps(params, sort_keys=True)}"
    
    # Check cache
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
    
    # Make request
    try:
        response = await http_client.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Response') == 'False':
            # OMDb returns 200 even for errors like "Movie not found!"
            # We treat "Movie not found!" as empty result or 404 depending on context
            return data

        # Cache the result
        cache[cache_key] = (data, time.time())
        return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OMDb API error: {str(e)}")

# API Routes
@api_router.get("/")
async def root():
    return {"message": "CineGraph API - Movie Recommendation Platform (OMDb Backend)"}

@api_router.get("/search", response_model=List[MovieSearchResult])
async def search_movies(query: str = Query(..., min_length=1)):
    """Search for movies by title"""
    data = await omdb_request({"s": query, "type": "movie"})
    
    results = data.get('Search', [])
    
    return [
        MovieSearchResult(
            id=movie['imdbID'],
            title=movie.get('Title', ''),
            release_date=movie.get('Year'), # OMDb only gives Year in search
            poster_path=movie.get('Poster') if movie.get('Poster') != 'N/A' else None,
            vote_average=None, # Not available in search result
            overview=None # Not available in search result
        )
        for movie in results
    ]

@api_router.get("/movie/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: str):
    """Get detailed information about a specific movie"""
    data = await omdb_request({"i": movie_id, "plot": "full"})
    
    if data.get('Response') == 'False':
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Parse runtime "148 min" -> 148
    runtime = None
    if data.get('Runtime') and data.get('Runtime') != 'N/A':
        try:
            runtime = int(data['Runtime'].split(' ')[0])
        except:
            pass

    # Parse rating
    vote_average = None
    if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
        try:
            vote_average = float(data['imdbRating'])
        except:
            pass
            
    # Parse Genres
    genres = []
    if data.get('Genre') and data.get('Genre') != 'N/A':
        genres = [{"id": 0, "name": g.strip()} for g in data['Genre'].split(',')]

    return MovieDetail(
        id=data['imdbID'],
        title=data.get('Title', ''),
        overview=data.get('Plot') if data.get('Plot') != 'N/A' else None,
        release_date=data.get('Released') if data.get('Released') != 'N/A' else data.get('Year'),
        vote_average=vote_average,
        poster_path=data.get('Poster') if data.get('Poster') != 'N/A' else None,
        backdrop_path=data.get('Poster') if data.get('Poster') != 'N/A' else None, # OMDb doesn't have backdrops, reuse poster
        runtime=runtime,
        genres=genres,
        tagline=data.get('Awards') # Use Awards as tagline substitute or just empty
    )

@api_router.get("/movie/{movie_id}/recommendations", response_model=List[MovieSearchResult])
async def get_recommendations(movie_id: str):
    """
    Get dynamic movie recommendations using OMDb title search and genre matching.
    """
    try:
        # 1. Fetch source movie details to get genre and title
        source_data = await omdb_request({"i": movie_id})
        if source_data.get('Response') == 'False':
            return []

        source_title = source_data.get('Title', '')
        source_genres = [g.strip() for g in source_data.get('Genre', '').split(',')]
        
        results_map = {} # Use dict to avoid duplicates by IMDb ID

        # 2. Strategy A: Search for related titles (sequels, prequels, remakes)
        # Take the first 2 words of the title to find related movies
        title_query = " ".join(source_title.split(' ')[:2])
        if title_query:
            search_data = await omdb_request({"s": title_query, "type": "movie"})
            if search_data.get('Response') != 'False':
                for movie in search_data.get('Search', []):
                    if movie['imdbID'] != movie_id: # Don't recommend itself
                        results_map[movie['imdbID']] = MovieSearchResult(
                            id=movie['imdbID'],
                            title=movie.get('Title', ''),
                            release_date=movie.get('Year'),
                            poster_path=movie.get('Poster') if movie.get('Poster') != 'N/A' else None,
                            vote_average=None,
                            overview=None
                        )

        # 3. Strategy B: Genre-based fallbacks if we need more
        if len(results_map) < 6:
            # Curated IMDb IDs for major genres
            genre_fallbacks = {
                "Action": ["tt8178634", "tt12844910", "tt15354916", "tt13751694", "tt0468569"],
                "Drama": ["tt23849204", "tt15398776", "tt0111161", "tt0068646", "tt0110912"],
                "Sci-Fi": ["tt15239678", "tt0133093", "tt1375666", "tt0816692", "tt0468569"],
                "Comedy": ["tt1187043", "tt1517268", "tt0332280", "tt0113243", "tt0081512"],
                "Crime": ["tt0068646", "tt0110912", "tt0468569", "tt0102926", "tt0114709"],
                "Animation": ["tt6718170", "tt1323594", "tt0435625", "tt3104988", "tt0462499"]
            }

            # Gather relevant IDs from source genres
            fallback_ids = []
            for genre in source_genres:
                if genre in genre_fallbacks:
                    fallback_ids.extend(genre_fallbacks[genre])
            
            # If no matches, add some default popular ones
            if not fallback_ids:
                fallback_ids = ["tt0468569", "tt15398776", "tt0111161"]

            # Fetch details for fallback movies (limited to avoid too many requests)
            for imdb_id in list(set(fallback_ids))[:10]:
                if imdb_id != movie_id and imdb_id not in results_map:
                    try:
                        data = await omdb_request({"i": imdb_id})
                        if data.get('Response') != 'False':
                            vote_average = None
                            if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
                                try: vote_average = float(data['imdbRating'])
                                except: pass
                            
                            results_map[imdb_id] = MovieSearchResult(
                                id=data['imdbID'],
                                title=data.get('Title', ''),
                                release_date=data.get('Year'),
                                poster_path=data.get('Poster') if data.get('Poster') != 'N/A' else None,
                                vote_average=vote_average,
                                overview=data.get('Plot') if data.get('Plot') != 'N/A' else None
                            )
                    except:
                        continue
                    
                    if len(results_map) >= 8:
                        break

        # Return a list of results, max 10
        final_results = list(results_map.values())[:10]
        return final_results
        
    except Exception as e:
        logger.error(f"Failed to fetch dynamic recommendations: {e}")
        return []

@api_router.get("/movie/{movie_id}/streaming", response_model=StreamingAvailability)
async def get_streaming_availability(movie_id: str, country: str = "US"):
    """
    Get streaming availability.
    NOTE: OMDb does not support streaming data.
    """
    return StreamingAvailability(
        country=country.upper(),
        subscription=[],
        rent=[],
        buy=[],
        imdb_link=f"https://www.imdb.com/title/{movie_id}/"
    )

@api_router.get("/trending", response_model=List[MovieSearchResult])
async def get_trending():
    """
    Get trending movies.
    NOTE: OMDb does not support trending. Fetching actual data from OMDb API for popular movies.
    """
    # List of popular movie IMDb IDs (Global + Indian)
    movie_ids = [
        "tt15354916",  # Jawan
        "tt12844910",  # Pathaan
        "tt13751694",  # Animal
        "tt23849204",  # 12th Fail
        "tt15398776",  # Oppenheimer
        "tt1517268",   # Barbie
        "tt15239678",  # Dune: Part Two
    ]
    
    # Fetch each movie from OMDb API
    results = []
    for imdb_id in movie_ids:
        try:
            data = await omdb_request({"i": imdb_id})
            
            if data.get('Response') != 'False':
                # Parse rating
                vote_average = None
                if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
                    try:
                        vote_average = float(data['imdbRating'])
                    except:
                        pass
                
                results.append(MovieSearchResult(
                    id=data['imdbID'],
                    title=data.get('Title', ''),
                    release_date=data.get('Year'),
                    poster_path=data.get('Poster') if data.get('Poster') != 'N/A' else None,
                    vote_average=vote_average,
                    overview=data.get('Plot') if data.get('Plot') != 'N/A' else None
                ))
        except Exception as e:
            # Skip movies that fail to load
            logger.error(f"Failed to fetch movie {imdb_id}: {e}")
            continue
    
    return results

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

@api_router.get("/proxy-image")
async def proxy_image(url: str):
    """
    Proxy image requests to bypass CORS restrictions.
    This allows images from Amazon/IMDb to load properly.
    """
    from fastapi.responses import Response
    
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
    
    try:
        # Fetch the image from the original URL
        response = await http_client.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.imdb.com/"
            },
            timeout=10.0
        )
        response.raise_for_status()
        
        # Return the image with proper CORS headers
        return Response(
            content=response.content,
            media_type=response.headers.get("content-type", "image/jpeg"),
            headers={
                "Cache-Control": "public, max-age=86400",  # Cache for 24 hours
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch image: {str(e)}")

@api_router.get("/api-info")
async def get_api_info():
    """
    API Information
    """
    return {
        "name": "CineGraph API (OMDb)",
        "version": "2.0.0",
        "description": "Movie recommendation platform using OMDb API",
        "data_source": "OMDb (Open Movie Database)",
        "note": "Recommendations and Streaming data are limited/mocked in this version."
    }

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
async def shutdown_client():
    await http_client.aclose()
