import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';


export default defineConfig({
  plugins: [vue()],
  test: {
    testMatch: ['**/*.test.js'],
    files: 'src/**/*.test.js',
    extensions: ['js', 'vue'],
  }
});