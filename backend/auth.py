"""
Autenticacion con Clerk: la API solo atiende a usuarios con sesion iniciada.

Como funciona:
    1. El usuario inicia sesion en la SPA con los componentes de Clerk.
    2. La SPA pide a Clerk un token de sesion (un JWT de vida corta) y lo envia
       en cada llamada: cabecera "Authorization: Bearer <token>".
    3. Esta dependencia valida el token con el SDK oficial de Clerk (clerk-backend-api):
         - firma RS256 con la clave publica de la instancia (JWKS, se descarga y se guarda en cache)
         - caducidad (exp / nbf)
         - azp ("authorized party"): el origen de la web que pidio el token debe estar
           en CLERK_AUTHORIZED_PARTIES. Asi un token emitido para otra web no vale aqui.
    4. Si algo falla -> 401. El motivo va al log (nunca el token).

Ocultar el formulario en la SPA NO protege nada: cualquiera puede llamar a la API con curl.
Lo que protege es esta comprobacion en el servidor.
"""

import logging
import os

from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from fastapi import HTTPException, Request, status

logger = logging.getLogger("translator.auth")


def get_authorized_parties() -> list[str]:
    """Lee CLERK_AUTHORIZED_PARTIES ("origen1,origen2") y la convierte en lista."""
    value = os.getenv("CLERK_AUTHORIZED_PARTIES", "")
    # strip() quita espacios; rstrip("/") evita que "https://web.app/" no coincida con "https://web.app"
    return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]


def require_user(request: Request) -> dict:
    """
    Dependencia de FastAPI: devuelve los datos del token (payload) si la sesion es valida.
    Se anade a las rutas protegidas; si lanza HTTPException, la ruta no se ejecuta.
    """
    secret_key = os.getenv("CLERK_SECRET_KEY")
    authorized_parties = get_authorized_parties()
    if not secret_key or not authorized_parties:
        # Falla "cerrado": si falta configuracion, NO se deja pasar a nadie
        logger.error("Clerk is not configured (CLERK_SECRET_KEY or CLERK_AUTHORIZED_PARTIES missing)")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication is not configured.")

    # Solo se acepta el token en la cabecera Authorization (asi es explicito y facil de probar).
    # Sin esto, el SDK tambien buscaria la cookie "__session".
    if not request.headers.get("Authorization", "").startswith("Bearer "):
        raise unauthorized("missing bearer token")

    state = authenticate_request(
        request,  # el SDK solo necesita request.headers, que FastAPI tiene
        AuthenticateRequestOptions(
            secret_key=secret_key,  # para descargar la clave publica (JWKS) de la instancia
            authorized_parties=authorized_parties,
            accepts_token=["session_token"],  # solo tokens de sesion de usuario
        ),
    )
    if not state.is_signed_in:
        raise unauthorized(str(state.reason))
    return state.payload or {}


def unauthorized(reason: str) -> HTTPException:
    """401 con mensaje generico; el motivo concreto solo va al log."""
    logger.warning("Request rejected: %s", reason)
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must be signed in.",
        # Cabecera estandar que indica que tipo de credencial se espera
        headers={"WWW-Authenticate": "Bearer"},
    )
