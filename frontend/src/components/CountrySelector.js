import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, Check, X } from 'lucide-react';
import { Button } from './ui/button';

const COUNTRIES = [
  { code: 'US', name: 'United States', flag: '🇺🇸' },
  { code: 'IN', name: 'India', flag: '🇮🇳' },
  { code: 'GB', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'CA', name: 'Canada', flag: '🇨🇦' },
  { code: 'AU', name: 'Australia', flag: '🇦🇺' },
  { code: 'DE', name: 'Germany', flag: '🇩🇪' },
  { code: 'FR', name: 'France', flag: '🇫🇷' },
  { code: 'ES', name: 'Spain', flag: '🇪🇸' },
  { code: 'IT', name: 'Italy', flag: '🇮🇹' },
  { code: 'BR', name: 'Brazil', flag: '🇧🇷' },
  { code: 'MX', name: 'Mexico', flag: '🇲🇽' },
  { code: 'JP', name: 'Japan', flag: '🇯🇵' },
  { code: 'KR', name: 'South Korea', flag: '🇰🇷' },
  { code: 'SG', name: 'Singapore', flag: '🇸🇬' },
  { code: 'AE', name: 'United Arab Emirates', flag: '🇦🇪' },
  { code: 'NL', name: 'Netherlands', flag: '🇳🇱' },
  { code: 'SE', name: 'Sweden', flag: '🇸🇪' },
  { code: 'NO', name: 'Norway', flag: '🇳🇴' },
  { code: 'DK', name: 'Denmark', flag: '🇩🇰' },
  { code: 'FI', name: 'Finland', flag: '🇫🇮' },
  { code: 'PL', name: 'Poland', flag: '🇵🇱' },
  { code: 'TR', name: 'Turkey', flag: '🇹🇷' },
  { code: 'ZA', name: 'South Africa', flag: '🇿🇦' },
  { code: 'AR', name: 'Argentina', flag: '🇦🇷' },
  { code: 'CL', name: 'Chile', flag: '🇨🇱' },
  { code: 'CO', name: 'Colombia', flag: '🇨🇴' },
  { code: 'ID', name: 'Indonesia', flag: '🇮🇩' },
  { code: 'TH', name: 'Thailand', flag: '🇹🇭' },
  { code: 'MY', name: 'Malaysia', flag: '🇲🇾' },
  { code: 'PH', name: 'Philippines', flag: '🇵🇭' },
  { code: 'NZ', name: 'New Zealand', flag: '🇳🇿' },
  { code: 'IE', name: 'Ireland', flag: '🇮🇪' },
  { code: 'PT', name: 'Portugal', flag: '🇵🇹' },
  { code: 'GR', name: 'Greece', flag: '🇬🇷' },
  { code: 'CZ', name: 'Czech Republic', flag: '🇨🇿' },
  { code: 'HU', name: 'Hungary', flag: '🇭🇺' },
  { code: 'RO', name: 'Romania', flag: '🇷🇴' },
  { code: 'AT', name: 'Austria', flag: '🇦🇹' },
  { code: 'CH', name: 'Switzerland', flag: '🇨🇭' },
  { code: 'BE', name: 'Belgium', flag: '🇧🇪' },
  { code: 'HK', name: 'Hong Kong', flag: '🇭🇰' },
];

function CountrySelector({ currentCountry, onCountryChange, isOpen, onClose }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCountry, setSelectedCountry] = useState(currentCountry);

  const filteredCountries = COUNTRIES.filter(
    (country) =>
      country.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      country.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelect = (countryCode) => {
    setSelectedCountry(countryCode);
    onCountryChange(countryCode);
    onClose();
  };

  const currentCountryData = COUNTRIES.find(c => c.code === currentCountry);

  if (!isOpen) {
    return (
      <button
        onClick={onClose}
        className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full transition-all"
        data-testid="country-selector-trigger"
      >
        <MapPin className="w-4 h-4 text-neon-teal" />
        <span className="text-sm font-dm-sans">
          {currentCountryData?.flag} {currentCountryData?.name || currentCountry}
        </span>
      </button>
    );
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/80 backdrop-blur-sm"
            data-testid="country-modal-backdrop"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', damping: 25 }}
            className="relative w-full max-w-2xl max-h-[80vh] glass-panel rounded-2xl shadow-2xl overflow-hidden"
            data-testid="country-selector-modal"
          >
            {/* Header */}
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <MapPin className="w-6 h-6 text-neon-teal" />
                  <h2 className="text-2xl font-outfit font-bold">Select Your Country</h2>
                </div>
                <button
                  onClick={onClose}
                  className="w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors"
                  data-testid="close-country-modal"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-white/60 font-dm-sans text-sm mb-4">
                Choose your location to see streaming availability in your region
              </p>
              {/* Search */}
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search countries..."
                className="w-full bg-white/5 border border-white/10 focus:border-electric-violet/50 text-white placeholder:text-white/30 rounded-lg px-4 py-3 font-dm-sans outline-none transition-all"
                data-testid="country-search-input"
              />
            </div>

            {/* Country List */}
            <div className="overflow-y-auto max-h-96 p-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {filteredCountries.map((country) => (
                  <button
                    key={country.code}
                    onClick={() => handleSelect(country.code)}
                    className={`flex items-center justify-between p-3 rounded-lg transition-all ${
                      selectedCountry === country.code || currentCountry === country.code
                        ? 'bg-electric-violet/20 border-2 border-electric-violet/50'
                        : 'bg-white/5 hover:bg-white/10 border-2 border-transparent'
                    }`}
                    data-testid={`country-option-${country.code}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{country.flag}</span>
                      <span className="font-dm-sans text-left">{country.name}</span>
                    </div>
                    {(selectedCountry === country.code || currentCountry === country.code) && (
                      <Check className="w-5 h-5 text-neon-teal" />
                    )}
                  </button>
                ))}
              </div>

              {filteredCountries.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-white/50 font-dm-sans">No countries found</p>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

export default CountrySelector;
