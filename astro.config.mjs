import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://ash-hun.github.io',
  base: '/ash-world',
  integrations: [
    mdx(),
    react(),
    sitemap(),
    tailwind({ applyBaseStyles: false }),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: false,
    },
  },
});
