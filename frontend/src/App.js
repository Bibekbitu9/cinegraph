import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '/api';

function App() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const searchMovies = async (query) => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Search failed:', error);
      setMovies([]);
    }
    setLoading(false);
  };

  const loadTrending = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/trending`);
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Failed to load trending:', error);
      setMovies([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadTrending();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    searchMovies(searchQuery);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎬 CineGraph</h1>
        <p>AI-Powered Movie Recommendations</p>
        
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for movies..."
            className="search-input"
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>

        <button onClick={loadTrending} className="trending-button">
          Show Trending Movies
        </button>

        {loading && <p>Loading...</p>}

        <div className="movies-grid">
          {movies.map((movie) => (
            <div key={movie.id} className="movie-card">
              {movie.poster_path && (
                <img 
                  src={movie.poster_path} 
                  alt={movie.title}
                  className="movie-poster"
                />
              )}
              <h3>{movie.title}</h3>
              <p>⭐ {movie.vote_average}/10</p>
              <p>{movie.release_date}</p>
              <p className="overview">{movie.overview?.substring(0, 100)}...</p>
            </div>
          ))}
        </div>

        {movies.length === 0 && !loading && (
          <p>No movies found. Try searching or loading trending movies!</p>
        )}
      </header>
    </div>
  );
}

export default App;