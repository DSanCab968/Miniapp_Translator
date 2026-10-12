# Imagen del backend SOLO para DESARROLLO LOCAL (con recarga automatica).
# No es la imagen que se entrega: la de produccion sera el Dockerfile de la raiz (Fase 5).
# python:3.12 coincide con la version que usa el runtime de Python de Vercel.
FROM python:3.12-slim

# No crear archivos .pyc y mostrar los logs al momento (sin buffer)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Se copian primero solo los requirements: asi Docker reutiliza esta capa
# (y no reinstala todo) mientras no cambien las dependencias
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# El codigo NO se copia: docker-compose monta la carpeta del proyecto en /app,
# y --reload reinicia el servidor cada vez que cambia un archivo de backend/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "backend"]
