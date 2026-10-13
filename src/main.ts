// Punto de entrada del frontend: crea la app de Vue y la monta en <div id="app">
import { createApp } from 'vue'
import { clerkPlugin } from '@clerk/vue'
import App from './App.vue'
import './style.css'

// Clave PUBLICA de Clerk. Vite solo expone al navegador las variables que empiezan
// por VITE_, y las mete en el bundle AL COMPILAR: si cambia, hay que recompilar/redesplegar.
// (La clave secreta CLERK_SECRET_KEY no empieza por VITE_, asi que nunca llega aqui.)
const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
if (!publishableKey) {
  throw new Error('Missing VITE_CLERK_PUBLISHABLE_KEY (see .env.example)')
}

// clerkPlugin da la sesion y el usuario a los componentes (Show, SignInButton...) y a useAuth
createApp(App).use(clerkPlugin, { publishableKey }).mount('#app')
