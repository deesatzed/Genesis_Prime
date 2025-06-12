const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  distDir: process.env.NEXT_DIST_DIR || '.next',
  output: process.env.NEXT_OUTPUT_MODE,

  // Move outputFileTracingRoot here (top level)
  outputFileTracingRoot: path.join(__dirname, '../'),

  experimental: {
    // (remove outputFileTracingRoot from here)
    // you can add other experimental flags here if needed
  },

  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  images: { unoptimized: true },
};

module.exports = nextConfig;
