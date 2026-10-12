"""
Tests del backend. NUNCA llaman a Groq: el cliente real se sustituye por uno falso
(MagicMock) que devuelve la respuesta que queramos. Asi no se gastan tokens y
se pueden probar tambien los casos de error.
"""

import json
from unittest.mock import MagicMock

import httpx2
import openai
import pytest
from fastapi.testclient import TestClient

from backend.ai import get_ai_client
from backend.main import app

client = TestClient(app)


def fake_ai_client(content: str) -> MagicMock:
    """Cliente falso cuya respuesta (choices[0].message.content) es 'content'."""
    ai = MagicMock()
    choice = MagicMock(message=MagicMock(content=content), finish_reason="stop")
    ai.chat.completions.create.return_value = MagicMock(choices=[choice])
    return ai


@pytest.fixture
def use_ai():
    """
    Devuelve una funcion para elegir que respondera la "IA" en cada test.
    Uso: ai = use_ai(json.dumps({...}))  -> ai es el cliente falso (para inspeccionarlo)
    "dependency_overrides": donde la API pida get_ai_client, se le da el falso.
    """

    def set_response(content: str) -> MagicMock:
        ai = fake_ai_client(content)
        app.dependency_overrides[get_ai_client] = lambda: ai
        return ai

    yield set_response
    app.dependency_overrides.clear()  # dejar la app limpia para el siguiente test


def test_translate_ok(use_ai):
    ai = use_ai(json.dumps({"translation": "Hello world", "detected_language": "Spanish"}))

    response = client.post("/api/translate", json={"text": "Hola mundo", "target_language": "en"})

    assert response.status_code == 200
    assert response.json() == {"translation": "Hello world", "detected_language": "Spanish"}
    # Se comprueba tambien QUE se le envio a la IA: texto delimitado e idioma destino
    messages = ai.chat.completions.create.call_args.kwargs["messages"]
    assert "English" in messages[0]["content"]
    assert messages[1]["content"] == "<text>\nHola mundo\n</text>"


@pytest.mark.parametrize(
    "body",
    [
        {"text": "", "target_language": "en"},  # texto vacio
        {"text": "   ", "target_language": "en"},  # solo espacios
        {"text": "a" * 2001, "target_language": "en"},  # demasiado largo
        {"text": "Hola", "target_language": "ru"},  # idioma no permitido
        {"text": "Hola"},  # falta el idioma
    ],
)
def test_invalid_input_returns_422(use_ai, body):
    ai = use_ai("{}")
    assert client.post("/api/translate", json=body).status_code == 422
    ai.chat.completions.create.assert_not_called()  # con entrada invalida no se gastan tokens


@pytest.mark.parametrize(
    "ai_response",
    [
        "this is not JSON",  # texto libre
        json.dumps({"other": 1}),  # JSON sin los campos pedidos
        json.dumps(["not", "an", "object"]),  # JSON pero no es un objeto
        None,  # error de conexion con el proveedor (ver abajo)
    ],
)
def test_provider_error_returns_502(use_ai, ai_response):
    ai = use_ai(ai_response or "")
    if ai_response is None:
        # Simular que Groq no responde. Ojo: el SDK openai 3.x usa httpx2
        ai.chat.completions.create.side_effect = openai.APIConnectionError(request=httpx2.Request("POST", "https://groq"))

    response = client.post("/api/translate", json={"text": "Hola", "target_language": "en"})

    assert response.status_code == 502
    # Mensaje generico: nunca se filtran detalles tecnicos al usuario
    assert response.json()["detail"] == "The translation service failed. Please try again later."
