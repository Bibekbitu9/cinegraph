import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { X, Star, Calendar, Clock, PlayCircle, MapPin, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function MovieDetailModal({ movieId, isOpen, onClose, userCountry }) {
  const [movie, setMovie] = useState(null);
  const [streaming, setStreaming] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isOpen) return;

    const fetchMovieDetails = async () => {
      try {
        setLoading(true);
        const [movieResponse, streamingResponse] = await Promise.all([
          axios.get(`${API}/movie/${movieId}`),
          axios.get(`${API}/movie/${movieId}/streaming`, {
            params: { country: userCountry },
          }),
        ]);
        setMovie(movieResponse.data);
        setStreaming(streamingResponse.data);
      } catch (error) {
        console.error('Failed to fetch movie details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMovieDetails();
  }, [movieId, isOpen, userCountry]); // Added userCountry to dependencies

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      // Lock the body scroll
      document.body.style.overflow = 'hidden';
      document.body.style.paddingRight = '0px'; // Prevent layout shift
    }

    return () => {
      // Restore body scroll
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    };
  }, [isOpen]);

  const handleGetRecommendations = () => {
    onClose();
    navigate(`/recommendations/${movieId}`);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 pointer-events-none"
        >
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/80 backdrop-blur-sm pointer-events-auto"
            data-testid="modal-backdrop"
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', damping: 25 }}
            onClick={(e) => e.stopPropagation()}
            data-lenis-prevent
            style={{ overflowY: 'auto' }}
            className="relative w-full max-w-4xl max-h-[90vh] glass-panel rounded-2xl shadow-2xl pointer-events-auto"
            data-testid="movie-detail-modal"
          >
            {loading ? (
              <div className="p-12 text-center">
                <p className="text-white/50 font-dm-sans">Loading movie details...</p>
              </div>
            ) : movie ? (
              <>
                {/* Close Button */}
                <button
                  onClick={onClose}
                  className="absolute top-4 right-4 z-10 w-10 h-10 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/70 transition-colors"
                  data-testid="close-modal-btn"
                >
                  <X className="w-5 h-5" />
                </button>

                {/* Backdrop Image */}
                {movie.backdrop_path && (
                  <div className="relative h-72 overflow-hidden rounded-t-2xl">
                    <img
                      src={movie.backdrop_path}
                      alt={movie.title}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-obsidian to-transparent" />
                  </div>
                )}

                <div className="p-8">
                  {/* Title & Meta */}
                  <div className="mb-6">
                    <h2 className="text-4xl font-outfit font-bold mb-2">{movie.title}</h2>
                    {movie.tagline && (
                      <p className="text-neon-teal text-lg font-dm-sans italic mb-4">"{movie.tagline}"</p>
                    )}
                    <div className="flex flex-wrap items-center gap-4 text-white/60 font-dm-sans">
                      {movie.release_date && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          <span>{new Date(movie.release_date).getFullYear()}</span>
                        </div>
                      )}
                      {movie.runtime && (
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4" />
                          <span>{movie.runtime} min</span>
                        </div>
                      )}
                      {movie.vote_average > 0 && (
                        <div className="flex items-center gap-2">
                          <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                          <span className="text-white font-semibold">{movie.vote_average.toFixed(1)}/10</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Genres */}
                  {movie.genres.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-6">
                      {movie.genres.map((genre) => (
                        <span
                          key={genre.id}
                          className="px-3 py-1 bg-electric-violet/20 border border-electric-violet/30 rounded-full text-sm font-dm-sans"
                        >
                          {genre.name}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Overview */}
                  {movie.overview && (
                    <div className="mb-6">
                      <h3 className="text-xl font-outfit font-semibold mb-3">Synopsis</h3>
                      <p className="text-white/80 font-dm-sans leading-relaxed">{movie.overview}</p>
                    </div>
                  )}

                  {/* Streaming Availability */}
                  {streaming && (
                    <div className="mb-6">
                      <div className="flex items-center gap-2 mb-4">
                        <MapPin className="w-5 h-5 text-neon-teal" />
                        <h3 className="text-xl font-outfit font-semibold">
                          Where to Watch ({streaming.country})
                        </h3>
                      </div>

                      {streaming.subscription.length === 0 && streaming.rent.length === 0 && streaming.buy.length === 0 ? (
                        <div className="glass-panel rounded-xl p-6">
                          <p className="text-white/50 font-dm-sans mb-4">No streaming options available in your region.</p>
                          {streaming.imdb_link && (
                            <a
                              href={streaming.imdb_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-2 text-electric-violet hover:text-electric-violet/80 text-sm font-dm-sans transition-colors"
                            >
                              View more on IMDb
                              <PlayCircle className="w-4 h-4" />
                            </a>
                          )}
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {streaming.subscription.length > 0 && (
                            <div>
                              <h4 className="text-sm font-outfit font-semibold text-neon-teal mb-2">STREAM</h4>
                              <div className="flex flex-wrap gap-3">
                                {streaming.subscription.map((provider) => (
                                  <a
                                    key={provider.provider_id}
                                    href={provider.link || '#'}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-2 bg-white/5 hover:bg-white/10 rounded-lg p-2 transition-all hover:scale-105 cursor-pointer group"
                                    title={`Watch on ${provider.provider_name}`}
                                  >
                                    {provider.logo_path && (
                                      <img
                                        src={provider.logo_path}
                                        alt={provider.provider_name}
                                        className="w-10 h-10 rounded"
                                      />
                                    )}
                                    <div className="flex flex-col">
                                      <span className="text-sm font-dm-sans">{provider.provider_name}</span>
                                      <span className="text-xs text-neon-teal opacity-0 group-hover:opacity-100 transition-opacity">
                                        Click to watch →
                                      </span>
                                    </div>
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}

                          {streaming.rent.length > 0 && (
                            <div>
                              <h4 className="text-sm font-outfit font-semibold text-electric-violet mb-2">RENT</h4>
                              <div className="flex flex-wrap gap-3">
                                {streaming.rent.map((provider) => (
                                  <a
                                    key={provider.provider_id}
                                    href={provider.link || '#'}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-2 bg-white/5 hover:bg-white/10 rounded-lg p-2 transition-all hover:scale-105 cursor-pointer group"
                                    title={`Rent on ${provider.provider_name}`}
                                  >
                                    {provider.logo_path && (
                                      <img
                                        src={provider.logo_path}
                                        alt={provider.provider_name}
                                        className="w-10 h-10 rounded"
                                      />
                                    )}
                                    <div className="flex flex-col">
                                      <span className="text-sm font-dm-sans">{provider.provider_name}</span>
                                      <span className="text-xs text-electric-violet opacity-0 group-hover:opacity-100 transition-opacity">
                                        Click to rent →
                                      </span>
                                    </div>
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}

                          {streaming.buy.length > 0 && (
                            <div>
                              <h4 className="text-sm font-outfit font-semibold text-cinema-red mb-2">BUY</h4>
                              <div className="flex flex-wrap gap-3">
                                {streaming.buy.map((provider) => (
                                  <a
                                    key={provider.provider_id}
                                    href={provider.link || '#'}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-2 bg-white/5 hover:bg-white/10 rounded-lg p-2 transition-all hover:scale-105 cursor-pointer group"
                                    title={`Buy on ${provider.provider_name}`}
                                  >
                                    {provider.logo_path && (
                                      <img
                                        src={provider.logo_path}
                                        alt={provider.provider_name}
                                        className="w-10 h-10 rounded"
                                      />
                                    )}
                                    <div className="flex flex-col">
                                      <span className="text-sm font-dm-sans">{provider.provider_name}</span>
                                      <span className="text-xs text-cinema-red opacity-0 group-hover:opacity-100 transition-opacity">
                                        Click to buy →
                                      </span>
                                    </div>
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}

                          {streaming.imdb_link && (
                            <div className="pt-2 border-t border-white/10">
                              <a
                                href={streaming.imdb_link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 text-white/50 hover:text-white text-sm font-dm-sans transition-colors"
                              >
                                View on IMDb
                                <PlayCircle className="w-4 h-4" />
                              </a>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Action Button */}
                  <div className="flex gap-4">
                    <Button
                      onClick={handleGetRecommendations}
                      className="bg-electric-violet hover:bg-electric-violet/90 text-white rounded-full px-8 py-3 font-outfit font-semibold transition-all hover:shadow-[0_0_20px_rgba(124,58,237,0.4)] flex-1"
                      data-testid="get-recommendations-btn"
                    >
                      <TrendingUp className="w-5 h-5 mr-2" />
                      Get Similar Movies
                    </Button>
                  </div>
                </div>
              </>
            ) : (
              <div className="p-12 text-center">
                <p className="text-white/50 font-dm-sans">Failed to load movie details</p>
              </div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

export default MovieDetailModal;
