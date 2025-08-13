import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  kit: {
    adapter: adapter({
      pages: 'dist',
      assets: 'dist',
      fallback: undefined
    }),
    prerender: {
      handleHttpError: ({ path, message }) => {
        // Ignore missing favicon
        if (path === '/favicon.png') return;
        throw new Error(message);
      }
    }
  },
  preprocess: vitePreprocess()
};