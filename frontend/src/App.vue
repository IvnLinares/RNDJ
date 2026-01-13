<script setup>
import { RouterView } from 'vue-router'
import { onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // Inicializar autenticación si hay token guardado
  if (authStore.token && !authStore.user) {
    authStore.checkAuth()
  }
})

// Monitorear cambios en el token
watch(() => authStore.token, async (newToken) => {
  if (newToken && !authStore.user) {
    await authStore.fetchCurrentUser()
  }
})
</script>

<template>
  <div id="app" class="min-h-screen">
    <RouterView />
  </div>
</template>

<style scoped>
/* Estilos globales específicos si son necesarios */
</style>
