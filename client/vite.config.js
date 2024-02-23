import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/', 
  server: {
      port: 8080,
  },
  build: {
    outDir: '../static/dist', // Output directory relative to Django's static directory
    manifest: true, // Generate a manifest.json file for Django
    assetsDir: 'static/assets',
    emptyOutDir: true, // Clean the output directory before building
    rollupOptions: {
      input: {
        main: './src/main.js', // Entry point of your Vue app
      },
    },
  },
})
