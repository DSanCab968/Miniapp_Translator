# ---------------------------------------------------------------
# Imagen de PRODUCCION: UN SOLO CONTENEDOR con la SPA y la API.
# (Es la que se entrega y la que se llevara a EC2. Para desarrollar
#  se sigue usando docker-compose.yml.)
#
# "Multi-stage": dos etapas. La primera compila Vue con Node; la segunda
# es la imagen final, solo con Python, el backend y el resultado (dist/).
# Node y node_modules se quedan en la primera etapa y NO llegan a la final.
#
# Construir:
#   docker build --build-arg VITE_CLERK_PUBLISHABLE_KEY=pk_test_... -t miniapp-translator:0.5 .
# Ejecutar (los secretos se pasan AL ARRANCAR, nunca dentro de la imagen):
#   docker run -d --name miniapp-translator --env-file .env -p 127.0.0.1:8080:8000 miniapp-translator:0.5
# ---------------------------------------------------------------

# ===== Etapa 1: compilar el frontend (Vue + TypeScript + Tailwind) =====
FROM node:24-alpine AS frontend
WORKDIR /build

# Primero solo los package*.json: mientras no cambien las dependencias,
# Docker reutiliza esta capa y no vuelve a ejecutar "npm ci" (build mas rapido)
COPY package.json package-lock.json ./
# npm ci instala EXACTAMENTE las versiones de package-lock.json
RUN npm ci --no-audit --no-fund

# Despues, el codigo y la configuracion del frontend
COPY index.html vite.config.ts tsconfig.json tailwind.config.js postcss.config.js ./
COPY src ./src

# Clave PUBLICA de Clerk: Vite la mete en el JavaScript AL COMPILAR, por eso
# es un ARG (dato de construccion) y no una variable de ejecucion.
# No es un secreto: cualquiera puede verla en el navegador.
ARG VITE_CLERK_PUBLISHABLE_KEY
# "npm run build" = vue-tsc (comprueba tipos) + vite build -> genera /build/dist
RUN npm run build


# ===== Etapa 2: imagen final (Python + FastAPI + dist/) =====
FROM python:3.12-slim

# No crear archivos .pyc y mostrar los logs al momento (sin buffer)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias de produccion (capa cacheada mientras no cambie requirements.txt)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Codigo del backend (los tests no entran: estan excluidos en .dockerignore)
COPY backend ./backend
# Solo el RESULTADO de la etapa 1: HTML, CSS y JS ya compilados
COPY --from=frontend /build/dist ./dist

# Le dice a backend/main.py que sirva la SPA desde esta carpeta
ENV FRONTEND_DIST=/app/dist

# Usuario sin privilegios: si alguien llegara a explotar un fallo de la app,
# no tendria permisos de root dentro del contenedor
RUN useradd --create-home --uid 10001 app
USER app

# Puerto en el que escucha uvicorn DENTRO del contenedor (documentacion;
# el que se abre de verdad se elige con "docker run -p")
EXPOSE 8000

# Docker comprueba cada 30 s que la app responde (estado "healthy" en "docker ps").
# Se usa Python para no instalar curl solo para esto.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4)"

# 0.0.0.0 = escuchar en todas las interfaces del contenedor. Con 127.0.0.1
# solo se podria llamar desde dentro y el "-p" de docker run no funcionaria.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
