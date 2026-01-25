import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// SEO Helper to update meta tags dynamically
export const useSEO = ({ title, description, image, url }) => {
  const location = useLocation();

  useEffect(() => {
    if (title) {
      document.title = `${title} | CineGraph`;
      
      // Update Open Graph
      updateMetaTag('og:title', title);
      updateMetaTag('twitter:title', title);
    }

    if (description) {
      updateMetaTag('description', description);
      updateMetaTag('og:description', description);
      updateMetaTag('twitter:description', description);
    }

    if (image) {
      updateMetaTag('og:image', image);
      updateMetaTag('twitter:image', image);
    }

    if (url) {
      updateMetaTag('og:url', url);
      updateMetaTag('twitter:url', url);
      updateLinkTag('canonical', url);
    }
  }, [title, description, image, url, location]);
};

const updateMetaTag = (property, content) => {
  if (!content) return;
  
  let element = document.querySelector(`meta[property="${property}"]`) ||
                document.querySelector(`meta[name="${property}"]`);
  
  if (element) {
    element.setAttribute('content', content);
  } else {
    element = document.createElement('meta');
    if (property.startsWith('og:') || property.startsWith('twitter:')) {
      element.setAttribute('property', property);
    } else {
      element.setAttribute('name', property);
    }
    element.setAttribute('content', content);
    document.head.appendChild(element);
  }
};

const updateLinkTag = (rel, href) => {
  if (!href) return;
  
  let element = document.querySelector(`link[rel="${rel}"]`);
  
  if (element) {
    element.setAttribute('href', href);
  } else {
    element = document.createElement('link');
    element.setAttribute('rel', rel);
    element.setAttribute('href', href);
    document.head.appendChild(element);
  }
};

// Structured data helper for movies
export const addMovieStructuredData = (movie) => {
  if (!movie) return;

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Movie",
    "name": movie.title,
    "description": movie.overview,
    "datePublished": movie.release_date,
    "aggregateRating": movie.vote_average ? {
      "@type": "AggregateRating",
      "ratingValue": movie.vote_average,
      "bestRating": "10",
      "worstRating": "0"
    } : undefined,
    "image": movie.poster_path,
    "genre": movie.genres?.map(g => g.name),
    "duration": movie.runtime ? `PT${movie.runtime}M` : undefined
  };

  let script = document.getElementById('movie-structured-data');
  if (!script) {
    script = document.createElement('script');
    script.id = 'movie-structured-data';
    script.type = 'application/ld+json';
    document.head.appendChild(script);
  }
  script.textContent = JSON.stringify(structuredData);
};

export const removeMovieStructuredData = () => {
  const script = document.getElementById('movie-structured-data');
  if (script) {
    script.remove();
  }
};
