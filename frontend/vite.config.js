import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import frappeui from 'frappe-ui/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [frappeui(), vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      // Proxy API and Frappe endpoints to backend server on port 8000
      '/api': 'http://localhost:8000',
      '/app': 'http://localhost:8000',
      '/assets': 'http://localhost:8000',
    },
  },
  build: {
    outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      output: {
        manualChunks: {
          'frappe-ui': ['frappe-ui'],
        },
      },
    },
  },
  optimizeDeps: {
    include: ['feather-icons', 'showdown', 'engine.io-client'],
  },
})
