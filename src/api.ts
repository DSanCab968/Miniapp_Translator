// Todas las llamadas al backend pasan por aqui.
// Asi, lo comun (cabeceras, manejo de errores) solo se programa en un sitio.
// Las rutas protegidas reciben el token de sesion de Clerk y lo envian en la
// cabecera "Authorization: Bearer <token>", que es donde lo busca backend/auth.py.
import type { TranslateRequest, TranslateResponse } from './types/translate'

// Mensajes comprensibles para el usuario segun el codigo HTTP.
// No se muestra el "detail" del backend: puede ser tecnico.
const ERROR_MESSAGES: Record<number, string> = {
  401: 'Your session has expired. Please sign in again.',
  422: 'The text or the language is not valid. Please check the form.',
  502: 'The translation service failed. Please try again in a few seconds.',
  503: 'The translation service is not available right now.',
}

async function request<T>(path: string, options: RequestInit = {}, token: string | null = null): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  let response: Response
  try {
    // Ruta relativa (/api/...): mismo origen, sin CORS (proxy de Vite / rewrites de Vercel)
    response = await fetch(`/api${path}`, { ...options, headers })
  } catch {
    // fetch solo lanza error si no hay respuesta (sin red, servidor apagado...)
    throw new Error('Cannot connect to the server.')
  }

  if (!response.ok) {
    throw new Error(ERROR_MESSAGES[response.status] ?? `Unexpected server error (${response.status}).`)
  }
  return response.json() as Promise<T>
}

export const api = {
  translate: (data: TranslateRequest, token: string | null) =>
    request<TranslateResponse>('/translate', { method: 'POST', body: JSON.stringify(data) }, token),
}
