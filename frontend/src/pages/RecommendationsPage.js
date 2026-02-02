import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import MovieCard from '../components/MovieCard';
import MovieDetailModal from '../components/MovieDetailModal';
import { useSEO } from '../utils/seo';
import { ArrowLeft, Film, Star } from 'lucide-react';
import { Button } from '../components/ui/button';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MovieCardSkeleton = () => (
  <div className="flex flex-col gap-3">
    <div className="aspect-[2/3] w-full bg-white/5 animate-pulse rounded-2xl" />
    <div className="h-4 w-3/4 bg-white/5 animate-pulse rounded" />
    <div className="h-3 w-1/2 bg-white/5 animate-pulse rounded" />
  </div>
);

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

        // Fetch location and source movie details in parallel
        const [geoResponse, movieResponse] = await Promise.all([
          axios.get(`${API}/geolocation`).catch(() => ({ data: { country_code: 'US' } })),
          axios.get(`${API}/movie/${movieId}`)
        ]);

        setUserCountry(geoResponse.data.country_code);
        setSourceMovie(movieResponse.data);

        // Fetch recommendations - this is the long-running one
        const recsResponse = await axios.get(`${API}/movie/${movieId}/recommendations`);
        setRecommendations(recsResponse.data);
      } catch (err) {
        console.error('Error fetching recommendations:', err);
        setError(err.response?.data?.detail || 'Failed to load recommendations.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [movieId]);

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
      <div className="relative h-80 overflow-hidden bg-obsidian">
        {sourceMovie ? (
          <>
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
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1 text-neon-teal">
                    <Star className="w-4 h-4 fill-current" />
                    <span className="font-dm-sans font-bold">{sourceMovie.vote_average}</span>
                  </div>
                  <p className="text-white/60 font-dm-sans">
                    {loading ? "Finding recommendations..." : `${recommendations.length} similar movies for you`}
                  </p>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="max-w-7xl mx-auto p-8 h-full flex flex-col justify-end">
            <div className="h-10 w-1/2 bg-white/5 animate-pulse rounded-lg mb-4" />
            <div className="h-4 w-1/4 bg-white/5 animate-pulse rounded" />
          </div>
        )}
      </div>

      {/* Recommendations Grid */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {loading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {[...Array(10)].map((_, i) => (
              <MovieCardSkeleton key={i} />
            ))}
          </div>
        ) : recommendations.length === 0 ? (
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
