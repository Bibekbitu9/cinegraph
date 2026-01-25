import { motion } from 'framer-motion';
import { Star, Calendar } from 'lucide-react';

function MovieCard({ movie, onClick }) {
  const posterUrl = movie.poster_path || 'https://via.placeholder.com/300x450/0A0A0C/7C3AED?text=No+Poster';
  const releaseYear = movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A';

  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="group relative overflow-hidden rounded-xl bg-charcoal border border-white/5 transition-all duration-500 hover:border-electric-violet/30 hover:shadow-2xl cursor-pointer"
      data-testid={`movie-card-${movie.id}`}
    >
      {/* Movie Poster */}
      <div className="relative aspect-[2/3] overflow-hidden">
        <img
          src={posterUrl}
          alt={movie.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 card-overlay opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Rating Badge */}
        {movie.vote_average > 0 && (
          <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-sm rounded-full px-2 py-1 flex items-center gap-1">
            <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
            <span className="text-xs font-dm-sans font-semibold">
              {movie.vote_average.toFixed(1)}
            </span>
          </div>
        )}
      </div>

      {/* Movie Info */}
      <div className="p-4">
        <h3 className="font-outfit font-semibold text-white mb-2 line-clamp-2 group-hover:text-electric-violet transition-colors">
          {movie.title}
        </h3>
        {movie.release_date && (
          <div className="flex items-center gap-1 text-white/50 text-sm font-dm-sans">
            <Calendar className="w-3 h-3" />
            <span>{releaseYear}</span>
          </div>
        )}
      </div>

      {/* Hover Action */}
      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
        <div className="bg-electric-violet text-white px-6 py-2 rounded-full font-outfit font-semibold text-sm">
          View Details
        </div>
      </div>
    </motion.div>
  );
}

export default MovieCard;
