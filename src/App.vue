<script setup lang="ts">
// La unica pantalla de la app: formulario de traduccion + resultado.
import { computed, ref } from 'vue'
import { api } from './api'
import { LANGUAGES, MAX_TEXT_LENGTH, type LanguageCode, type TranslateResponse } from './types/translate'

// Estado del formulario
const text = ref('')
const targetLanguage = ref<LanguageCode>('en')

// Estado de la peticion
const loading = ref(false)
const errorMessage = ref('')
const result = ref<TranslateResponse | null>(null)

// Validacion en la UI (el backend lo vuelve a validar: doble validacion)
const trimmedLength = computed(() => text.value.trim().length)
const tooLong = computed(() => text.value.length > MAX_TEXT_LENGTH)
const canSubmit = computed(() => trimmedLength.value > 0 && !tooLong.value && !loading.value)

async function translate(): Promise<void> {
  if (!canSubmit.value) return
  loading.value = true
  errorMessage.value = ''
  result.value = null
  try {
    result.value = await api.translate({ text: text.value, target_language: targetLanguage.value })
  } catch (error) {
    // api.ts siempre lanza Error con un mensaje ya pensado para el usuario
    errorMessage.value = error instanceof Error ? error.message : 'Unexpected error.'
  } finally {
    // finally se ejecuta haya ido bien o mal: siempre se quita el "cargando"
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <main class="mx-auto max-w-2xl px-4 py-10">
      <h1 class="text-2xl font-extrabold tracking-tight">Miniapp <span class="text-indigo-400">Translator</span></h1>
      <p class="mt-1 text-sm text-slate-400">Write in any language: the AI detects it and translates it.</p>

      <!-- @submit.prevent: evita que el navegador recargue la pagina al enviar -->
      <form class="mt-6 space-y-4" @submit.prevent="translate">
        <div>
          <label for="text" class="mb-1 block text-sm font-medium text-slate-300">Text</label>
          <textarea
            id="text"
            v-model="text"
            rows="6"
            placeholder="Type the text to translate..."
            class="w-full resize-y rounded-xl border border-slate-700 bg-slate-900 p-3 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
          <!-- Contador: en rojo si se pasa del limite -->
          <p class="mt-1 text-right text-xs" :class="tooLong ? 'text-red-400' : 'text-slate-500'">
            {{ text.length }} / {{ MAX_TEXT_LENGTH }}
          </p>
        </div>

        <div class="flex flex-wrap items-end gap-3">
          <div>
            <label for="language" class="mb-1 block text-sm font-medium text-slate-300">Translate to</label>
            <select
              id="language"
              v-model="targetLanguage"
              class="rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            >
              <option v-for="language in LANGUAGES" :key="language.code" :value="language.code">
                {{ language.name }}
              </option>
            </select>
          </div>

          <button
            type="submit"
            :disabled="!canSubmit"
            class="rounded-xl bg-indigo-600 px-5 py-2 font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ loading ? 'Translating...' : 'Translate' }}
          </button>
        </div>
      </form>

      <!-- role="alert": los lectores de pantalla anuncian el error -->
      <p v-if="errorMessage" role="alert" class="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
        {{ errorMessage }}
      </p>

      <section v-if="result" class="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-4">
        <p class="text-xs uppercase tracking-wide text-slate-500">
          Detected language: <span class="text-indigo-300">{{ result.detected_language }}</span>
        </p>
        <!-- whitespace-pre-wrap: respeta los saltos de linea de la traduccion -->
        <p class="mt-2 whitespace-pre-wrap text-slate-100">{{ result.translation }}</p>
      </section>
    </main>
  </div>
</template>
