// Tipos de la API de traduccion (los mismos campos que los modelos Pydantic de backend/ai.py)

// Idiomas destino permitidos. Debe coincidir con el Literal del backend:
// si aqui se anade uno que el backend no acepta, la API respondera 422.
export const LANGUAGES = [
  { code: 'es', name: 'Spanish' },
  { code: 'en', name: 'English' },
  { code: 'de', name: 'German' },
  { code: 'fr', name: 'French' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
] as const

// 'es' | 'en' | ... sacado de la lista de arriba (asi no se escribe dos veces)
export type LanguageCode = (typeof LANGUAGES)[number]['code']

export const MAX_TEXT_LENGTH = 2000

export interface TranslateRequest {
  text: string
  target_language: LanguageCode
}

export interface TranslateResponse {
  translation: string
  detected_language: string
}
