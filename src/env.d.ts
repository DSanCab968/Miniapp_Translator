/// <reference types="vite/client" />

// Le dice a TypeScript que los archivos .vue son componentes de Vue
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<object, object, unknown>
  export default component
}
