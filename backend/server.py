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

# TMDB Configuration
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# Simple in-memory cache
cache = {}
CACHE_TTL = 3600  # 1 hour

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# HTTP client for OMDb & TMDB APIs
http_client = httpx.AsyncClient(timeout=10.0)

# Models
class MovieSearchResult(BaseModel):
    id: str  # This will remain IMDb ID (tt...)
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
            return data

        # Cache the result
        cache[cache_key] = (data, time.time())
        return data
    except Exception as e:
        logger.error(f"OMDb API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OMDb API error: {str(e)}")

async def tmdb_request(path: str, params: Dict[str, Any] = {}):
    """Make a request to TMDB API with caching"""
    if not TMDB_API_KEY:
        return None  # Fail gracefully if no key

    # Add API key to params
    params = params.copy()
    params['api_key'] = TMDB_API_KEY
    
    url = f"{TMDB_BASE_URL}{path}"
    cache_key = f"tmdb_{url}_{json.dumps(params, sort_keys=True)}"
    
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
            
    try:
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        cache[cache_key] = (data, time.time())
        return data
    except Exception as e:
        logger.error(f"TMDB API error: {str(e)}")
        return None

# API Routes
@api_router.get("/")
async def root():
    return {"message": "CineGraph API - Movie Recommendation Platform (Hybrid Backend)"}

@api_router.get("/search", response_model=List[MovieSearchResult])
async def search_movies(query: str = Query(..., min_length=1)):
    """Search for movies by title"""
    data = await omdb_request({"s": query, "type": "movie"})
    
    results = data.get('Search', [])
    
    return [
        MovieSearchResult(
            id=movie['imdbID'],
            title=movie.get('Title', ''),
            release_date=movie.get('Year'),
            poster_path=movie.get('Poster') if movie.get('Poster') != 'N/A' else None,
            vote_average=None,
            overview=None
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
        backdrop_path=data.get('Poster') if data.get('Poster') != 'N/A' else None,
        runtime=runtime,
        genres=genres,
        tagline=data.get('Awards')
    )

@api_router.get("/movie/{movie_id}/recommendations", response_model=List[MovieSearchResult])
async def get_recommendations(movie_id: str):
    """
    Get dynamic movie recommendations using TMDB (preferred) or OMDb genre fallback.
    """
    try:
        logger.info(f"Fetching recommendations for movie_id: {movie_id}")
        
        # 1. 🌟 Strategy A: Try TMDB Recommendations first (Language-Aware)
        if TMDB_API_KEY:
            logger.info("Attempting TMDB recommendation strategy")
            # Map IMDb ID -> TMDB ID
            find_data = await tmdb_request(f"/find/{movie_id}", {"external_source": "imdb_id"})
            if find_data and find_data.get('movie_results'):
                tmdb_movie = find_data['movie_results'][0]
                tmdb_id = tmdb_movie['id']
                logger.info(f"Found TMDB movie ID: {tmdb_id} for {movie_id}")
                
                # Get full movie details to extract language
                movie_details = await tmdb_request(f"/movie/{tmdb_id}")
                source_language = movie_details.get('original_language', 'en') if movie_details else 'en'
                logger.info(f"Source movie language: {source_language}")
                
                # Fetch recommendations from TMDB
                rec_data = await tmdb_request(f"/movie/{tmdb_id}/recommendations")
                if rec_data and rec_data.get('results'):
                    logger.info(f"Found {len(rec_data['results'])} recommendations from TMDB")
                    
                    # Filter by language first
                    language_filtered = [
                        m for m in rec_data['results']
                        if m.get('original_language') == source_language
                    ]
                    
                    logger.info(f"After language filter: {len(language_filtered)} movies match {source_language}")
                    
                    # If we have enough language-matched recommendations, use them
                    movies_to_process = language_filtered[:10] if len(language_filtered) >= 5 else rec_data['results'][:10]
                    
                    # Optimization: Fetch all external IDs in parallel
                    async def fetch_movie_with_imdb(movie):
                        ids_data = await tmdb_request(f"/movie/{movie['id']}/external_ids")
                        imdb_id = ids_data.get('imdb_id') if ids_data else None
                        if imdb_id and imdb_id != movie_id:
                            return MovieSearchResult(
                                id=imdb_id,
                                title=movie.get('title', ''),
                                release_date=movie.get('release_date', '')[:4] if movie.get('release_date') else None,
                                poster_path=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                                vote_average=movie.get('vote_average'),
                                overview=movie.get('overview') or ""
                            )
                        return None

                    # Use gather for concurrency
                    tasks = [fetch_movie_with_imdb(m) for m in movies_to_process]
                    results_list = await asyncio.gather(*tasks)
                    
                    # Filter out None values
                    results = [r for r in results_list if r]
                    
                    if results:
                        logger.info(f"Successfully returning {len(results)} TMDB recommendations")
                        return results
                else:
                    logger.warning(f"No recommendations found on TMDB for movie: {tmdb_id}")
            else:
                logger.warning(f"Could not find TMDB mapping for IMDb ID: {movie_id}")
        else:
            logger.warning("TMDB_API_KEY is missing, skipping TMDB strategy")

        # 2. ⚡ Strategy B: Language-Aware OMDb Fallback
        logger.info("Falling back to OMDb logic")
        source_data = await omdb_request({"i": movie_id})
        if source_data.get('Response') == 'False':
            return []

        # Detect language from OMDb data
        source_language = source_data.get('Language', '').lower()
        source_country = source_data.get('Country', '').lower()
        source_genres = [g.strip() for g in source_data.get('Genre', '').split(',')]
        
        # Determine language category
        detected_lang = 'en'  # default to English
        if 'hindi' in source_language or 'india' in source_country:
            detected_lang = 'hi'
        elif 'tamil' in source_language:
            detected_lang = 'ta'
        elif 'telugu' in source_language:
            detected_lang = 'te'
        elif 'kannada' in source_language:
            detected_lang = 'kn'
        elif 'malayalam' in source_language:
            detected_lang = 'ml'
        
        logger.info(f"Detected language: {detected_lang} from OMDb data")
        
        results_map = {} 

        # Language-specific curated pools
        language_pools = {
            'hi': {  # Hindi/Bollywood
                "Action": ["tt8178634", "tt15354916", "tt7019842", "tt13751694", "tt12844910"],  # RRR, Jawan, Pathaan, KGF2, Pushpa
                "Drama": ["tt1187043", "tt0169102", "tt5074352", "tt2338151", "tt23849204"],  # 3 Idiots, Lagaan, Dangal, PK, 12th Fail
                "Comedy": ["tt1187043", "tt1620933", "tt1821480", "tt1954470", "tt2283748"],  # 3 Idiots, Munna Bhai, Andhadhun, Queen, Vicky Donor
                "Crime": ["tt6148156", "tt1821480", "tt10280296", "tt8108202", "tt7838252"],  # Gangs of Wasseypur, Andhadhun, Sacred Games, Mirzapur, Article 15
                "Romance": ["tt1039928", "tt0367110", "tt0871510", "tt1954470", "tt0367495"]  # YJHD, Kal Ho Naa Ho, Jab We Met, Queen, DDLJ
            },
            'ta': {  # Tamil
                "Action": ["tt9179430", "tt15097216", "tt9900782", "tt7019842", "tt8178634"],  # Vikram, Leo, Jailer, Pathaan, RRR
                "Drama": ["tt10189514", "tt8108274", "tt1821480", "tt5074352", "tt0169102"],  # Jai Bhim, Soorarai Pottru, Andhadhun, Dangal, Lagaan
                "Comedy": ["tt1187043", "tt1620933", "tt1821480", "tt1954470", "tt2283748"]
            },
            'te': {  # Telugu
                "Action": ["tt8178634", "tt4849438", "tt12844910", "tt7019842", "tt13751694"],  # RRR, Baahubali, Pushpa, Pathaan, KGF2
                "Drama": ["tt8178634", "tt4849438", "tt5074352", "tt0169102", "tt1187043"],
                "Comedy": ["tt1187043", "tt1620933", "tt1821480", "tt1954470", "tt2283748"]
            },
            'kn': {  # Kannada
                "Action": ["tt13751694", "tt12844910", "tt8178634", "tt7019842", "tt15354916"],  # KGF series, RRR, Pathaan, Jawan
                "Drama": ["tt13751694", "tt5074352", "tt0169102", "tt1187043", "tt2338151"]
            },
            'en': {  # English/Hollywood
                "Action": ["tt0468569", "tt1375666", "tt0816692", "tt4154796", "tt10872600"],  # Dark Knight, Inception, Interstellar, Avengers, Spider-Man
                "Drama": ["tt0111161", "tt0068646", "tt0110912", "tt0137523", "tt0109830"],  # Shawshank, Godfather, Pulp Fiction, Fight Club, Forrest Gump
                "Sci-Fi": ["tt0133093", "tt1375666", "tt0816692", "tt0167260", "tt0468569"],  # Matrix, Inception, Interstellar, LOTR, Dark Knight
                "Comedy": ["tt0332280", "tt0113243", "tt0081505", "tt1201607", "tt0110413"],  # Notebook, Braveheart, Raiders, Harry Potter, Leon
                "Crime": ["tt0068646", "tt0110912", "tt0468569", "tt0102926", "tt0114709"],  # Godfather, Pulp Fiction, Dark Knight, Silence, Se7en
                "Animation": ["tt6718170", "tt1323594", "tt0435625", "tt3104988", "tt0462499"]  # Spider-Verse, Toy Story, Ratatouille, Coco, Up
            }
        }

        # Get language-specific pool
        lang_pool = language_pools.get(detected_lang, language_pools['en'])
        
        fallback_ids = []
        for genre in source_genres:
            if genre in lang_pool:
                fallback_ids.extend(lang_pool[genre])
        
        # If no genre match, use all movies from the language pool
        if not fallback_ids:
            for genre_list in lang_pool.values():
                fallback_ids.extend(genre_list)
        
        # Shuffle IDs to make it feel dynamic
        import random
        random.shuffle(fallback_ids)

        if not fallback_ids:
            fallback_ids = ["tt0468569", "tt15398776", "tt0111161"]

        for imdb_id in list(set(fallback_ids)):
            if imdb_id != movie_id and imdb_id not in results_map:
                try:
                    data = await omdb_request({"i": imdb_id})
                    if data.get('Response') != 'False':
                        results_map[imdb_id] = MovieSearchResult(
                            id=data['imdbID'],
                            title=data.get('Title', ''),
                            release_date=data.get('Year'),
                            poster_path=data.get('Poster') if data.get('Poster') != 'N/A' else None,
                            vote_average=float(data['imdbRating']) if data.get('imdbRating') != 'N/A' else None,
                            overview=data.get('Plot') if data.get('Plot') != 'N/A' else ""
                        )
                except: continue
                if len(results_map) >= 10: break

        logger.info(f"Returning {len(results_map)} {detected_lang} language-based recommendations from OMDb")
        return list(results_map.values())
        
    except Exception as e:
        logger.error(f"Failed to fetch recommendations: {e}")
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
