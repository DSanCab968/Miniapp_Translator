/// <reference types="vite/client" />

// Le dice a TypeScript que los archivos .vue son componentes de Vue
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<object, object, unknown>
  export default component
}

// Tipos de las variables de entorno que usa el frontend (import.meta.env)
interface ImportMetaEnv {
  readonly VITE_CLERK_PUBLISHABLE_KEY: string
}
