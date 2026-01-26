/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'electric-violet': '#7C3AED',
        'neon-teal': '#2DD4BF',
        'cinema-red': '#E11D48',
        'obsidian': '#030305',
      },
      fontFamily: {
        'outfit': ['Outfit', 'sans-serif'],
        'dm-sans': ['DM Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}