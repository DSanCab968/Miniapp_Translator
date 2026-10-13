# Imagen para usar la Vercel CLI SIN instalar nada en el PC (solo herramienta local).
# Es node:24-alpine + curl: "vercel curl" (probar despliegues protegidos) llama al
# programa curl del sistema, y la imagen de Node no lo trae.
FROM node:24-alpine
RUN apk add --no-cache curl
