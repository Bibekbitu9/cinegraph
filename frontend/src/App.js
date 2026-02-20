import { useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Lenis from '@studio-freight/lenis';
import HomePage from './pages/HomePage';
import RecommendationsPage from './pages/RecommendationsPage';

function App() {
  useEffect(() => {
    // Only initialize smooth scrolling on non-touch desktop devices
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    let lenis;
    let rafId;

    if (!isTouchDevice) {
      lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
        smoothTouch: false,
      });

      function raf(time) {
        lenis.raf(time);
        rafId = requestAnimationFrame(raf);
      }

      rafId = requestAnimationFrame(raf);
    }

    return () => {
      if (lenis) {
        lenis.destroy();
        cancelAnimationFrame(rafId);
      }
    };
  }, []);

  return (
    <div className="App">
      <div className="film-grain" />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recommendations/:movieId" element={<RecommendationsPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
