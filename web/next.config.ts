import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export: `next build` writes plain HTML/CSS/JS to out/ (docs/specs/02, ADR-06)
  output: "export",
  // Thumbnails are already optimized WebP files produced by the pipeline
  images: { unoptimized: true },
  // /plots/<id> is emitted as /plots/<id>/index.html, so no host rewrites are needed
  trailingSlash: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
