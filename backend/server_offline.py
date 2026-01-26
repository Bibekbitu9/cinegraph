from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="CineGraph API (Offline Mode)")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

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

# Sample data for offline mode
SAMPLE_MOVIES = [
    {
        "id": 27205,
        "title": "Inception",
        "release_date": "2010-07-16",
        "poster_path": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "vote_average": 8.4,
        "overview": "Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state."
    },
    {
        "id": 155,
        "title": "The Dark Knight",
        "release_date": "2008-07-18",
        "poster_path": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "vote_average": 9.0,
        "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent."
    },
    {
        "id": 13,
        "title": "Forrest Gump",
        "release_date": "1994-07-06",
        "poster_path": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "vote_average": 8.5,
        "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events."
    },
    {
        "id": 278,
        "title": "The Shawshank Redemption",
        "release_date": "1994-09-23",
        "poster_path": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "vote_average": 9.3,
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "id": 238,
        "title": "The Godfather",
        "release_date": "1972-03-14",
        "poster_path": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "vote_average": 9.2,
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    }
]

# API Routes
@api_router.get("/")
async def root():
    return {"message": "CineGraph API - Offline Mode", "status": "running"}

@api_router.get("/search", response_model=List[MovieSearchResult])
async def search_movies(query: str = Query(..., min_length=1)):
    """Search for movies by title (offline mode with sample data)"""
    results = []
    query_lower = query.lower()
    
    for movie in SAMPLE_MOVIES:
        if query_lower in movie['title'].lower():
            results.append(MovieSearchResult(**movie))
    
    # If no matches, return all sample movies
    if not results:
        results = [MovieSearchResult(**movie) for movie in SAMPLE_MOVIES]
    
    return results[:10]

@api_router.get("/movie/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: int):
    """Get detailed information about a specific movie"""
    for movie in SAMPLE_MOVIES:
        if movie['id'] == movie_id:
            return MovieDetail(
                **movie,
                runtime=120,
                genres=[{"id": 1, "name": "Action"}, {"id": 2, "name": "Drama"}],
                tagline="A mind-bending thriller"
            )
    
    # Default movie if not found
    return MovieDetail(
        id=movie_id,
        title="Sample Movie",
        overview="This is a sample movie in offline mode.",
        release_date="2024-01-01",
        vote_average=7.5,
        runtime=120,
        genres=[{"id": 1, "name": "Drama"}],
        tagline="Sample tagline"
    )

@api_router.get("/movie/{movie_id}/recommendations", response_model=List[MovieSearchResult])
async def get_recommendations(movie_id: int):
    """Get movie recommendations (offline mode)"""
    # Return other sample movies as recommendations
    recommendations = [movie for movie in SAMPLE_MOVIES if movie['id'] != movie_id]
    return [MovieSearchResult(**movie) for movie in recommendations[:10]]

@api_router.get("/movie/{movie_id}/streaming", response_model=StreamingAvailability)
async def get_streaming_availability(movie_id: int, country: str = "US"):
    """Get streaming availability (offline mode)"""
    return StreamingAvailability(
        country=country.upper(),
        subscription=[
            StreamingProvider(
                provider_id=8,
                provider_name="Netflix",
                logo_path="https://image.tmdb.org/t/p/w92/t2yyOv40HZeVlLjYsCsPHnWLk4W.jpg",
                link="https://www.netflix.com"
            )
        ],
        rent=[
            StreamingProvider(
                provider_id=2,
                provider_name="Apple TV",
                logo_path="https://image.tmdb.org/t/p/w92/peURlLlr8jggOwK53fJ5wdQl05y.jpg",
                link="https://tv.apple.com"
            )
        ]
    )

@api_router.get("/trending", response_model=List[MovieSearchResult])
async def get_trending():
    """Get trending movies (offline mode)"""
    return [MovieSearchResult(**movie) for movie in SAMPLE_MOVIES]

@api_router.get("/geolocation", response_model=GeolocationResponse)
async def get_geolocation():
    """Detect user's country (offline mode)"""
    return GeolocationResponse(
        country_code='US',
        country_name='United States'
    )

@api_router.get("/api-info")
async def get_api_info():
    """API Information"""
    return {
        "name": "CineGraph API",
        "version": "1.0.0",
        "mode": "offline",
        "description": "Movie recommendation API running in offline mode with sample data",
        "note": "This is offline mode. For full functionality, ensure internet connectivity to TMDB API."
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)