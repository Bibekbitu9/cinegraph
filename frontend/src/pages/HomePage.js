import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import HeroSearch from '../components/HeroSearch';
import TrendingSection from '../components/TrendingSection';
import CountrySelector from '../components/CountrySelector';
import axios from 'axios';
import { Film } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function HomePage() {
  const [userCountry, setUserCountry] = useState(() => {
    // Try to get saved country from localStorage
    return localStorage.getItem('userCountry') || 'US';
  });
  const [showCountrySelector, setShowCountrySelector] = useState(false);

  useEffect(() => {
    // Detect user's location only if not already set
    const detectLocation = async () => {
      const savedCountry = localStorage.getItem('userCountry');
      if (savedCountry) {
        return; // User has already chosen a country
      }
      
      try {
        const response = await axios.get(`${API}/geolocation`);
        const detectedCountry = response.data.country_code;
        setUserCountry(detectedCountry);
        localStorage.setItem('userCountry', detectedCountry);
      } catch (error) {
        console.error('Failed to detect location:', error);
      }
    };
    detectLocation();
  }, []);

  const handleCountryChange = (newCountry) => {
    setUserCountry(newCountry);
    localStorage.setItem('userCountry', newCountry);
  };

  return (
    <div className="min-h-screen bg-obsidian">
      {/* Country Selector Modal */}
      <CountrySelector
        currentCountry={userCountry}
        onCountryChange={setUserCountry}
        isOpen={showCountrySelector}
        onClose={() => setShowCountrySelector(false)}
      />

      {/* Hero Section */}
      <div className="hero-glow relative min-h-screen flex flex-col items-center justify-center px-6">
        {/* Country Selector Trigger */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="absolute top-6 right-6"
        >
          <button
            onClick={() => setShowCountrySelector(true)}
            className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full transition-all"
            data-testid="country-selector-trigger"
          >
            <span className="text-sm font-dm-sans">
              {userCountry === 'IN' ? '🇮🇳' : userCountry === 'US' ? '🇺🇸' : userCountry === 'GB' ? '🇬🇧' : '🌍'} {userCountry}
            </span>
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center gap-3 mb-6">
            <Film className="w-12 h-12 text-electric-violet" />
            <h1 className="text-6xl sm:text-7xl lg:text-8xl font-outfit font-bold tracking-tight">
              CineGraph
            </h1>
          </div>
          <p className="text-lg sm:text-xl text-white/60 font-dm-sans max-w-2xl mx-auto">
            Discover your next favorite movie with AI-powered recommendations
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="w-full max-w-4xl"
        >
          <HeroSearch userCountry={userCountry} />
        </motion.div>
      </div>

      {/* Trending Section */}
      <TrendingSection userCountry={userCountry} />

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-white/40 text-sm font-dm-sans">
            Powered by TMDB • Built with ❤️ for movie enthusiasts
          </p>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
