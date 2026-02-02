import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import MovieCard from '../components/MovieCard';
import MovieDetailModal from '../components/MovieDetailModal';
import { useSEO } from '../utils/seo';
import { ArrowLeft, Film } from 'lucide-react';
import { Button } from '../components/ui/button';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function RecommendationsPage() {
  const { movieId } = useParams();
  const navigate = useNavigate();
  const [sourceMovie, setSourceMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [userCountry, setUserCountry] = useState(() => {
    return localStorage.getItem('userCountry') || 'US';
  });



  // SEO optimization
  useSEO({
    title: sourceMovie ? `Movies Like ${sourceMovie.title} - Similar Recommendations` : 'Movie Recommendations',
    description: sourceMovie ? `Discover ${recommendations.length} movies similar to ${sourceMovie.title}. AI-powered recommendations based on genre, theme, and style. Find where to watch in ${userCountry}.` : 'Find similar movies with AI recommendations',
    image: sourceMovie?.backdrop_path,
    url: window.location.href
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch location
        try {
          const geoResponse = await axios.get(`${API}/geolocation`);
          setUserCountry(geoResponse.data.country_code);
        } catch (err) {
          console.error('Failed to detect location:', err);
        }

        // Fetch source movie details
        const movieResponse = await axios.get(`${API}/movie/${movieId}`);
        setSourceMovie(movieResponse.data);

        // Fetch recommendations
        const recsResponse = await axios.get(`${API}/movie/${movieId}/recommendations`);
        setRecommendations(recsResponse.data);
      } catch (err) {
        console.error('Error fetching recommendations:', err);
        setError(err.response?.data?.detail || 'Failed to load recommendations. Please check if your OMDb API key is configured.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [movieId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-obsidian flex items-center justify-center">
        <div className="text-center">
          <Film className="w-16 h-16 text-electric-violet mx-auto mb-4 animate-pulse" />
          <p className="text-white/60 font-dm-sans">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-obsidian flex items-center justify-center px-6">
        <div className="text-center max-w-md">
          <Film className="w-16 h-16 text-cinema-red mx-auto mb-4" />
          <h2 className="text-2xl font-outfit font-bold mb-2">Oops!</h2>
          <p className="text-white/60 font-dm-sans mb-6">{error}</p>
          <Button
            onClick={() => navigate('/')}
            className="bg-electric-violet hover:bg-electric-violet/90 text-white rounded-full px-8 py-3"
            data-testid="back-home-error-btn"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-obsidian">
      {/* Header */}
      <header className="sticky top-0 z-50 glass-panel border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Button
            onClick={() => navigate('/')}
            variant="ghost"
            className="text-white/70 hover:text-white hover:bg-white/5"
            data-testid="back-home-btn"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Search
          </Button>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Film className="w-6 h-6 text-electric-violet" />
              <span className="text-xl font-outfit font-bold">CineGraph</span>
            </div>
          </div>
        </div>
      </header>

      {/* Source Movie Banner */}
      {sourceMovie && (
        <div className="relative h-80 overflow-hidden">
          {sourceMovie.backdrop_path && (
            <img
              src={sourceMovie.backdrop_path}
              alt={sourceMovie.title}
              className="w-full h-full object-cover"
            />
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-obsidian via-obsidian/80 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-8">
            <div className="max-w-7xl mx-auto">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-4xl sm:text-5xl font-outfit font-bold mb-2"
              >
                Movies like {sourceMovie.title}
              </motion.h1>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-white/60 font-dm-sans"
              >
                {recommendations.length} recommendations based on your selection
              </motion.p>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations Grid */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {recommendations.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-white/60 font-dm-sans text-lg">
              No recommendations found for this movie. Try searching for another title.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {recommendations.map((movie, index) => (
              <motion.div
                key={movie.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <MovieCard
                  movie={movie}
                  onClick={() => setSelectedMovie(movie)}
                />
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Movie Detail Modal */}
      {selectedMovie && (
        <MovieDetailModal
          movieId={selectedMovie.id}
          isOpen={!!selectedMovie}
          onClose={() => setSelectedMovie(null)}
          userCountry={userCountry}
        />
      )}
    </div>
  );
}

export default RecommendationsPage;
