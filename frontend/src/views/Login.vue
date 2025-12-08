<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const form = ref({
  username: '',
  email: '',
  password: '',
  full_name: ''
})

const handleSubmit = async () => {
  if (isLogin.value) {
    // Login
    const success = await authStore.login({
      username: form.value.username,
      password: form.value.password
    })
    
    if (success) {
      router.push('/dashboard')
    }
  } else {
    // Registro
    const success = await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      full_name: form.value.full_name
    })
    
    if (success) {
      router.push('/dashboard')
    }
  }
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  authStore.error = null
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-500 to-green-500 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          🏕️ RNJ-Connect
        </h1>
        <p class="text-gray-600">
          {{ isLogin ? 'Inicia sesión en tu cuenta' : 'Crea tu cuenta de scout' }}
        </p>
      </div>

      <!-- Error Message -->
      <div v-if="authStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ authStore.error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ isLogin ? 'Usuario o Email' : 'Nombre de Usuario' }}
          </label>
          <input
            v-model="form.username"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            :placeholder="isLogin ? 'usuario o email' : 'miusuario'"
          />
        </div>

        <!-- Email (solo registro) -->
        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="scout@ejemplo.com"
          />
        </div>

        <!-- Full Name (solo registro) -->
        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
          <input
            v-model="form.full_name"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Juan Pérez"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input
            v-model="form.password"
            type="password"
            required
            :minlength="isLogin ? 1 : 8"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="••••••••"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
        >
          {{ authStore.isLoading ? 'Cargando...' : (isLogin ? 'Iniciar Sesión' : 'Registrarse') }}
        </button>
      </form>

      <!-- Toggle Mode -->
      <div class="mt-6 text-center">
        <button
          @click="toggleMode"
          class="text-blue-600 hover:text-blue-700 font-medium"
        >
          {{ isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión' }}
        </button>
      </div>

      <!-- Back to Home -->
      <div class="mt-4 text-center">
        <RouterLink to="/" class="text-gray-600 hover:text-gray-700 text-sm">
          ← Volver al inicio
        </RouterLink>
      </div>
    </div>
  </div>
</template>
