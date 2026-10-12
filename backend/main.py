"""
Aplicacion FastAPI del traductor: aqui se juntan todas las rutas.

Todas las rutas empiezan por /api para que frontend y backend compartan origen
(mismo dominio): asi no hace falta CORS ni en local, ni en Vercel, ni en EC2.
"""

import logging

from fastapi import FastAPI

from backend import ai

# Formato basico de los logs (se ven con "docker compose logs api" y en los logs de Vercel)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="Miniapp Translator API",
    description="Traduce un texto a un idioma destino con IA (Groq)",
    version="0.1.0",
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
