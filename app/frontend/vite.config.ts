import { defineConfig } from 'vite';

export default defineConfig({
  base: '/static/react/',
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  build: {
    outDir: '../static/react',
    emptyOutDir: true,
  },
});
