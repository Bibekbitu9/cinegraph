// craco.config.js
const path = require("path");
require("dotenv").config();

module.exports = {
  style: {
    postcss: {
      loaderOptions: (postcssLoaderOptions) => {
        postcssLoaderOptions.postcssOptions = {
          plugins: [
            require('tailwindcss'),
            require('autoprefixer'),
          ],
        };
        return postcssLoaderOptions;
      },
    },
  },
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig) => {
      // Add ignored patterns to reduce watched directories
      webpackConfig.watchOptions = {
        ...webpackConfig.watchOptions,
        ignored: [
          '**/node_modules/**',
          '**/.git/**',
          '**/build/**',
          '**/dist/**',
          '**/coverage/**',
        ],
      };
      return webpackConfig;
    },
  },
};
