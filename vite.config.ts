import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Direccion del backend a la que el proxy reenvia las llamadas a /api.
// - Dentro de Docker Compose vale "http://api:8000" ("api" es el nombre del servicio).
// - Si algun dia se ejecuta fuera de Docker, se usa localhost.
const apiTarget = process.env.API_TARGET ?? 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    // Escuchar en todas las interfaces (0.0.0.0): necesario para que el
    // servidor de Vite sea accesible desde fuera del contenedor
    host: true,
    port: 5173,
    strictPort: true,
    // Proxy: el navegador llama a /api/... en el MISMO origen (localhost:5173)
    // y Vite lo reenvia al backend. En Vercel hara lo mismo vercel.json,
    // y en EC2 FastAPI servira la SPA y la API desde el mismo contenedor.
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
})
