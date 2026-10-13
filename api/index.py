"""
Puerta de entrada del backend SOLO para Vercel.

Vercel convierte CADA archivo .py de la carpeta api/ en una funcion serverless.
Por eso aqui solo hay este archivo, y todo el codigo real vive en backend/.
vercel.json redirige todas las rutas /api/* a esta funcion.

(En local y en Docker no se usa: uvicorn arranca directamente "backend.main:app".)
"""

from backend.main import app  # noqa: F401
