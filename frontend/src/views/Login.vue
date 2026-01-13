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
  <div class="d-flex align-items-center justify-content-center" style="min-height: 100vh; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 1rem;">
    <div style="width: 100%; max-width: 450px;">
      <!-- Logo y Header -->
      <div class="text-center mb-5">
        <div class="d-inline-flex align-items-center justify-content-center mb-4 rounded-3" style="width: 80px; height: 80px; background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); box-shadow: 0 8px 25px rgba(168, 85, 247, 0.3);">
          <i class="fas fa-campground" style="font-size: 36px; color: white;"></i>
        </div>
        <h1 class="h3 fw-bold mb-2" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.8rem;">
          RNDJ-Connect
        </h1>
        <p class="text-muted mb-0 fw-500">
          {{ isLogin ? 'Bienvenido de vuelta' : 'Únete a la aventura scout' }}
        </p>
      </div>

      <!-- Card Principal Premium -->
      <div class="card border-0" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.85) 100%); box-shadow: 0 20px 40px rgba(168, 85, 247, 0.12); border-radius: 20px;">
        <div class="card-body p-5">
          <!-- Error Message -->
          <div v-if="authStore.error" class="alert alert-danger d-flex align-items-center mb-4" role="alert" style="border-radius: 12px; border: none; animation: slideDown 0.3s ease-out;">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <span>{{ authStore.error }}</span>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit">
            <!-- Username -->
            <div class="mb-4">
              <label class="form-label fw-semibold mb-2" style="color: #334155;">
                {{ isLogin ? 'Usuario o Email' : 'Nombre de Usuario' }}
              </label>
              <input
                v-model="form.username"
                type="text"
                required
                class="form-control"
                :placeholder="isLogin ? 'usuario o email' : 'miusuario'"
                style="border-radius: 12px; border: 2px solid #e2e8f0; padding: 12px 16px; font-size: 1rem;"
              />
            </div>

            <!-- Email (solo registro) -->
            <div v-if="!isLogin" class="mb-4">
              <label class="form-label fw-semibold mb-2" style="color: #334155;">Email</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="form-control"
                placeholder="scout@ejemplo.com"
                style="border-radius: 12px; border: 2px solid #e2e8f0; padding: 12px 16px; font-size: 1rem;"
              />
            </div>

            <!-- Full Name (solo registro) -->
            <div v-if="!isLogin" class="mb-4">
              <label class="form-label fw-semibold mb-2" style="color: #334155;">Nombre Completo</label>
              <input
                v-model="form.full_name"
                type="text"
                class="form-control"
                placeholder="Juan Pérez"
                style="border-radius: 12px; border: 2px solid #e2e8f0; padding: 12px 16px; font-size: 1rem;"
              />
            </div>

            <!-- Password -->
            <div class="mb-5">
              <label class="form-label fw-semibold mb-2" style="color: #334155;">Contraseña</label>
              <input
                v-model="form.password"
                type="password"
                required
                :minlength="isLogin ? 1 : 8"
                class="form-control"
                placeholder="••••••••"
                style="border-radius: 12px; border: 2px solid #e2e8f0; padding: 12px 16px; font-size: 1rem;"
              />
              <small v-if="!isLogin" class="text-muted d-block mt-2">
                Mínimo 8 caracteres
              </small>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="btn btn-primary w-100 fw-bold py-3"
              style="border-radius: 12px; font-size: 1rem; background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);"
            >
              <i v-if="authStore.isLoading" class="fas fa-spinner fa-spin me-2"></i>
              <span>{{ isLogin ? 'Iniciar Sesión' : 'Crear Cuenta' }}</span>
            </button>
          </form>

          <!-- Toggle Mode -->
          <div class="mt-5 pt-4 text-center border-top" style="border-color: #e2e8f0 !important;">
            <p class="text-muted mb-3">{{ isLogin ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?' }}</p>
            <button
              @click="toggleMode"
              class="btn btn-link fw-bold"
              style="color: #a855f7; text-decoration: none; padding: 0;"
            >
              {{ isLogin ? 'Regístrate aquí' : 'Inicia sesión aquí' }}
            </button>
          </div>

          <!-- Back to Home -->
          <div class="mt-4 text-center">
            <RouterLink to="/" class="btn btn-link btn-sm text-decoration-none text-muted fw-500">
              <i class="fas fa-arrow-left me-1"></i>Volver al inicio
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Info Footer -->
      <div class="alert mt-4 mb-0" style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.05) 0%, rgba(249, 115, 22, 0.05) 100%); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 12px; color: #475569;">
        <small class="fw-500">
          <i class="fas fa-info-circle me-1"></i>
          Demo: usuario: <strong>testuser</strong> | contraseña: <strong>123456</strong>
        </small>
      </div>
    </div>
  </div>
</template>
