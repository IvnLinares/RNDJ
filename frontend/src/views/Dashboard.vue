<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchCurrentUser()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Bar -->
    <nav class="bg-white shadow-md">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-8">
            <h1 class="text-2xl font-bold text-blue-900">🏕️ RNJ-Connect</h1>
            <div class="hidden md:flex space-x-4">
              <RouterLink to="/dashboard" class="text-gray-700 hover:text-blue-600 font-medium">
                Dashboard
              </RouterLink>
              <RouterLink to="/chat" class="text-gray-700 hover:text-blue-600 font-medium">
                Chat
              </RouterLink>
              <RouterLink to="/gamification" class="text-gray-700 hover:text-blue-600 font-medium">
                Gamificación
              </RouterLink>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <RouterLink to="/profile" class="text-gray-700 hover:text-blue-600">
              👤 {{ authStore.user?.username || 'Perfil' }}
            </RouterLink>
            <button
              @click="handleLogout"
              class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
            >
              Salir
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <div v-if="authStore.user" class="max-w-6xl mx-auto">
        <!-- Welcome Section -->
        <div class="bg-white rounded-xl shadow-md p-8 mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">
            ¡Bienvenido, {{ authStore.user.full_name || authStore.user.username }}! 👋
          </h2>
          <p class="text-gray-600">
            {{ authStore.user.scout_group ? `Grupo Scout: ${authStore.user.scout_group}` : 'Completa tu perfil para conectar con tu grupo' }}
          </p>
        </div>

        <!-- Stats Cards -->
        <div class="grid md:grid-cols-4 gap-6 mb-8">
          <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl p-6 shadow-lg">
            <div class="text-4xl mb-2">⭐</div>
            <div class="text-3xl font-bold">{{ authStore.user.points || 0 }}</div>
            <div class="text-blue-100">Puntos</div>
          </div>

          <div class="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl p-6 shadow-lg">
            <div class="text-4xl mb-2">📊</div>
            <div class="text-3xl font-bold">Nivel {{ authStore.user.level || 1 }}</div>
            <div class="text-green-100">Tu Nivel</div>
          </div>

          <div class="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
            <div class="text-4xl mb-2">🏅</div>
            <div class="text-3xl font-bold">{{ authStore.user.badges_count || 0 }}</div>
            <div class="text-purple-100">Insignias</div>
          </div>

          <div class="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-xl p-6 shadow-lg">
            <div class="text-4xl mb-2">🎯</div>
            <div class="text-3xl font-bold">0</div>
            <div class="text-orange-100">Misiones</div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid md:grid-cols-3 gap-6">
          <RouterLink
            to="/chat"
            class="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition block"
          >
            <div class="text-4xl mb-4">💬</div>
            <h3 class="text-xl font-bold mb-2">Chat en Vivo</h3>
            <p class="text-gray-600">Conéctate con otros scouts</p>
          </RouterLink>

          <RouterLink
            to="/gamification"
            class="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition block"
          >
            <div class="text-4xl mb-4">🎮</div>
            <h3 class="text-xl font-bold mb-2">Misiones</h3>
            <p class="text-gray-600">Completa desafíos y gana puntos</p>
          </RouterLink>

          <RouterLink
            to="/profile"
            class="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition block"
          >
            <div class="text-4xl mb-4">👤</div>
            <h3 class="text-xl font-bold mb-2">Mi Perfil</h3>
            <p class="text-gray-600">Actualiza tu información</p>
          </RouterLink>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">⏳</div>
        <p class="text-gray-600">Cargando...</p>
      </div>
    </main>
  </div>
</template>
