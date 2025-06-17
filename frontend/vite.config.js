import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
        proxy: {
            '/api': {
                target: 'https://localhost:8000', // FastAPI server
                changeOrigin: true,
            }
        },
		fs: {
			allow: [
				// Allow serving files from the project root
				'..',
				// Allow serving files from node_modules
				'../node_modules',
				// Allow serving SvelteKit files
				'../node_modules/@sveltejs'
			]
		}
	}
});