import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import MovieCard from './MovieCard';
import MovieDetailModal from './MovieDetailModal';
import { TrendingUp } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function TrendingSection({ userCountry }) {
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMovie, setSelectedMovie] = useState(null);

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await axios.get(`${API}/trending`);
        setTrending(response.data);
      } catch (error) {
        console.error('Failed to fetch trending movies:', error);
        if (error.response?.status === 401) {
          setError('TMDB API key not configured. Please add your API key to backend/.env to see trending movies.');
        } else {
          setError('Failed to load trending movies. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTrending();
  }, []);

  if (loading) {
    return (
      <div className="py-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-white/50 font-dm-sans">Loading trending movies...</p>
        </div>
      </div>
    );
  }

  return (
    <section className="py-20 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex items-center gap-3 mb-12"
        >
          <TrendingUp className="w-8 h-8 text-neon-teal" />
          <h2 className="text-4xl sm:text-5xl font-outfit font-bold">
            Trending This Week
          </h2>
        </motion.div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {trending.map((movie, index) => (
            <motion.div
              key={movie.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.05 }}
            >
              <MovieCard
                movie={movie}
                onClick={() => setSelectedMovie(movie)}
              />
            </motion.div>
          ))}
        </div>
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
    </section>
  );
}

export default TrendingSection;
