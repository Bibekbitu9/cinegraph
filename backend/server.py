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
from openai import AsyncOpenAI
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env', override=True)

# OMDb Configuration
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')
OMDB_BASE_URL = "http://www.omdbapi.com"

# Groq AI Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

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
    """Search for movies by title or theme using Semantic AI Search"""
    try:
        if GROQ_API_KEY:
            client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
            prompt = f"User searched for movies related to: '{query}'. Provide the top 10 best matching films in cinematic history. Combine exact matches and strong thematic matches. CRITICAL INSTRUCTION: You MUST respond ONLY with a raw comma-separated list of EXACT IMDb IDs (e.g. tt1234567,tt7654321). No text, no titles, no markdown."
            chat_completion = await client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.5
            )
            response_text = chat_completion.choices[0].message.content.strip()
            ai_imdb_ids = re.findall(r'tt\d+', response_text)
            
            if ai_imdb_ids:
                async def fetch_result(rec_id):
                    try:
                        data = await omdb_request({"i": rec_id})
                        if data.get('Response') != 'False' and data.get('Poster') and data.get('Poster') != 'N/A':
                            return MovieSearchResult(
                                id=data['imdbID'],
                                title=data.get('Title', ''),
                                release_date=data.get('Year')[:4] if data.get('Year') else None,
                                poster_path=data.get('Poster'),
                                vote_average=float(data['imdbRating']) if data.get('imdbRating') and data.get('imdbRating') != 'N/A' else None,
                                overview=data.get('Plot') if data.get('Plot') != 'N/A' else None
                            )
                    except: pass
                    return None
                
                ai_tasks = [fetch_result(rec_id) for rec_id in list(dict.fromkeys(ai_imdb_ids))]
                results = [r for r in await asyncio.gather(*ai_tasks) if r]
                if results:
                    return results[:12]
    except Exception as e:
        logger.error(f"Groq AI Search failed: {e}")
        
    return []

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
        
        # 1. 🚀 Strategy A: Groq AI Recommendations (Highly Contextual)
        if GROQ_API_KEY:
            logger.info("Attempting Groq AI recommendation strategy")
            try:
                # Need source movie details to prompt the AI
                source_data = await omdb_request({"i": movie_id})
                if source_data.get('Response') != 'False':
                    title = source_data.get('Title', '')
                    genre = source_data.get('Genre', '')
                    plot = source_data.get('Plot', '')
                    
                    if title:
                        client = AsyncOpenAI(
                            api_key=GROQ_API_KEY,
                            base_url="https://api.groq.com/openai/v1"
                        )
                        
                        prompt = f"""You are an elite cinema recommendation engine. I am a user who just finished watching the movie '{title}' (Genres: {genre}, Plot summary: {plot}). 
Your task is to recommend exactly 12 incredible, highly similar companion films that capture the precise mood, cinematic style, pacing, and core thematic concepts of '{title}'. 
DO NOT just match basic genres, focus heavily on the 'vibe'. Combine popular hits with hidden gems.

CRITICAL INSTRUCTION: You MUST respond ONLY with a raw comma-separated list of EXACT IMDb IDs (e.g. tt1234567,tt7654321). 
Do NOT include any conversational text, no movies titles, no explanations, no JSON formatting, no markdown, no quotes. Just the raw comma-separated IDs."""

                        chat_completion = await client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": prompt
                                }
                            ],
                            model="llama-3.3-70b-versatile",
                            temperature=0.7,
                        )
                        
                        response_text = chat_completion.choices[0].message.content.strip()
                        ai_imdb_ids = re.findall(r'tt\d+', response_text)
                        
                        if ai_imdb_ids:
                            logger.info(f"Groq AI highly contextual suggested IDs: {ai_imdb_ids}")
                            results_map = {}
                            
                            async def fetch_ai_recommendation(rec_id):
                                if rec_id == movie_id: return None
                                try:
                                    data = await omdb_request({"i": rec_id})
                                    if data.get('Response') != 'False' and data.get('Poster') and data.get('Poster') != 'N/A':
                                        vote_average = None
                                        if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
                                            try: vote_average = float(data['imdbRating'])
                                            except: pass
                                        
                                        return MovieSearchResult(
                                            id=data['imdbID'],
                                            title=data.get('Title', ''),
                                            release_date=data.get('Year')[:4] if data.get('Year') else None,
                                            poster_path=data.get('Poster'),
                                            vote_average=vote_average,
                                            overview=data.get('Plot') if data.get('Plot') != 'N/A' else ""
                                        )
                                except: pass
                                return None

                            # Fetch all AI recommendations concurrently
                            ai_tasks = [fetch_ai_recommendation(rec_id) for rec_id in list(dict.fromkeys(ai_imdb_ids))]
                            ai_results = await asyncio.gather(*ai_tasks)
                            
                            valid_results = [r for r in ai_results if r]
                            if len(valid_results) >= 4:
                                return valid_results[:10]
            except Exception as e:
                logger.error(f"Groq AI Recommendations failed: {e}")
                return []
        
        logger.warning("GROQ_API_KEY is missing. Cannot fetch recommendations.")
        return []
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
    Get dynamic trending movies using TMDB (if available) or randomly from OMDb pool.
    """
    try:
        # 1. 🚀 Strategy A: Groq AI Real-Time Trending (Highly Dynamic)
        if GROQ_API_KEY:
            logger.info("Attempting Groq AI for trending movies")
            client = AsyncOpenAI(
                api_key=GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )
            
            prompt = """You are an elite cinema engine. Your task is to provide the absolute top 10 most popular, trending, and highly discussed movies globally right now (this week). 
Mix massive new blockbusters, critically acclaimed recent releases, and viral hits.

CRITICAL INSTRUCTION: You MUST respond ONLY with a raw comma-separated list of EXACT IMDb IDs (e.g. tt1234567,tt7654321). 
Do NOT include any text, titles, or explanations. Just the raw comma-separated IDs."""

            chat_completion = await client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.8,
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            logger.info(f"Groq Raw Response: {response_text}")
            ai_imdb_ids = re.findall(r'tt\d+', response_text)
            logger.info(f"Extracted IDs: {ai_imdb_ids}")
            
            if ai_imdb_ids:
                logger.info(f"Groq AI trending suggested IDs: {ai_imdb_ids}")
                
                async def fetch_ai_trending(rec_id):
                    try:
                        data = await omdb_request({"i": rec_id})
                        if data.get('Response') != 'False' and data.get('Poster') and data.get('Poster') != 'N/A':
                            vote_average = None
                            if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
                                try: vote_average = float(data['imdbRating'])
                                except: pass
                            
                            return MovieSearchResult(
                                id=data['imdbID'],
                                title=data.get('Title', ''),
                                release_date=data.get('Year')[:4] if data.get('Year') else None,
                                poster_path=data.get('Poster'),
                                vote_average=vote_average,
                                overview=data.get('Plot') if data.get('Plot') != 'N/A' else ""
                            )
                    except: pass
                    return None

                ai_tasks = [fetch_ai_trending(rec_id) for rec_id in list(dict.fromkeys(ai_imdb_ids))]
                ai_results = await asyncio.gather(*ai_tasks)
                
                valid_results = [r for r in ai_results if r]
                if len(valid_results) >= 5:
                    return valid_results[:10]
    except Exception as e:
        logger.error(f"Groq AI Trending failed: {e}")
        return []

    logger.warning("GROQ_API_KEY is missing. Cannot fetch trending movies.")
    return []

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
