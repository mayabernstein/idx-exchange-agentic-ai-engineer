import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  preview: {
    allowedHosts: ['real-estate-recommendation-system-production.up.railway.app'],
  },
})
