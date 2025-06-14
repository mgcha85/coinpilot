import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';
const config: UserConfig = {
  plugins: [sveltekit()],
  css: {
    postcss: './postcss.config.js'
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: { usePolling: true }
  }
};
export default config;
