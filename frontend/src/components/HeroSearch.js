import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Search, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function HeroSearch({ userCountry }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const searchMovies = async () => {
      if (query.trim().length < 2) {
        setResults([]);
        return;
      }

      setLoading(true);
      try {
        const response = await axios.get(`${API}/search`, {
          params: { query: query.trim() },
        });
        setResults(response.data);
        setShowResults(true);
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    const debounce = setTimeout(searchMovies, 300);
    return () => clearTimeout(debounce);
  }, [query]);

  const handleMovieSelect = (movie) => {
    navigate(`/recommendations/${movie.id}`);
    setQuery('');
    setShowResults(false);
  };

  const clearSearch = () => {
    setQuery('');
    setResults([]);
    setShowResults(false);
  };

  return (
    <div ref={searchRef} className="relative w-full">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-6 top-1/2 transform -translate-y-1/2 w-6 h-6 text-white/30" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a movie..."
          className="w-full bg-white/5 border border-white/10 focus:border-electric-violet/50 text-white placeholder:text-white/30 rounded-full pl-16 pr-16 py-6 text-lg font-dm-sans transition-all focus:bg-white/10 focus:shadow-[0_0_30px_rgba(124,58,237,0.15)] outline-none"
          data-testid="movie-search-input"
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute right-6 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white transition-colors"
            data-testid="clear-search-btn"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Search Results Dropdown */}
      <AnimatePresence>
        {showResults && results.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute top-full mt-4 w-full glass-panel rounded-2xl shadow-2xl overflow-hidden z-50"
            data-testid="search-results-dropdown"
          >
            <div className="max-h-96 overflow-y-auto">
              {results.map((movie) => (
                <button
                  key={movie.id}
                  onClick={() => handleMovieSelect(movie)}
                  className="w-full flex items-start gap-4 p-4 hover:bg-white/5 transition-colors border-b border-white/5 last:border-b-0"
                  data-testid={`search-result-${movie.id}`}
                >
                  {movie.poster_path ? (
                    <img
                      src={movie.poster_path}
                      alt={movie.title}
                      className="w-16 h-24 object-cover rounded-lg flex-shrink-0"
                    />
                  ) : (
                    <div className="w-16 h-24 bg-charcoal rounded-lg flex-shrink-0 flex items-center justify-center">
                      <Search className="w-6 h-6 text-white/20" />
                    </div>
                  )}
                  <div className="flex-1 text-left">
                    <h3 className="font-outfit font-semibold text-white mb-1">
                      {movie.title}
                    </h3>
                    <p className="text-sm text-white/50 font-dm-sans">
                      {movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}
                      {movie.vote_average && (
                        <span className="ml-2">⭐ {movie.vote_average.toFixed(1)}</span>
                      )}
                    </p>
                    {movie.overview && (
                      <p className="text-xs text-white/40 mt-1 line-clamp-2 font-dm-sans">
                        {movie.overview}
                      </p>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading State */}
      {loading && query.length >= 2 && (
        <div className="absolute top-full mt-4 w-full glass-panel rounded-2xl p-4 text-center">
          <p className="text-white/50 font-dm-sans">Searching...</p>
        </div>
      )}

      {/* No Results */}
      {showResults && !loading && query.length >= 2 && results.length === 0 && (
        <div className="absolute top-full mt-4 w-full glass-panel rounded-2xl p-4 text-center">
          <p className="text-white/50 font-dm-sans">No movies found. Try a different title.</p>
        </div>
      )}
    </div>
  );
}

export default HeroSearch;
