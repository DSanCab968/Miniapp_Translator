"""
Aplicacion FastAPI del traductor: aqui se juntan todas las rutas.

Todas las rutas empiezan por /api para que frontend y backend compartan origen
(mismo dominio): asi no hace falta CORS ni en local, ni en Vercel, ni en EC2.

En el contenedor unico (Dockerfile) esta app sirve TAMBIEN la SPA compilada (dist/).
"""

import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend import ai

# Formato basico de los logs (se ven con "docker compose logs api" y en los logs de Vercel)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="Miniapp Translator API",
    description="Traduce un texto a un idioma destino con IA (Groq)",
    version="1.0.0",
    # La documentacion automatica tambien cuelga de /api para que funcione
    # a traves del proxy de Vite y de los rewrites de Vercel
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(ai.router)


@app.get("/api/health", tags=["System"])
def health_check() -> dict:
    """
    Indica si la API esta viva. Es PUBLICA (sin login) y no devuelve datos
    sensibles: sirve para comprobar el despliegue y para monitorizar.
    """
    return {"status": "ok"}


# --- SPA compilada (solo en el contenedor) ---------------------------------
# El Dockerfile define FRONTEND_DIST=/app/dist. En Vercel (que sirve la SPA el mismo)
# y en el compose de desarrollo (Vite) no existe, asi que esto no se activa.
# Se monta AL FINAL: las rutas /api/... ya definidas arriba tienen prioridad.
frontend_dist = os.getenv("FRONTEND_DIST")
if frontend_dist:
    # html=True: al pedir "/" devuelve index.html
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="spa")
