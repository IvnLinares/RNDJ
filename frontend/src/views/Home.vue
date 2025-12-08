<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-blue-900 text-white shadow-lg">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold">🏕️ RNJ-Connect</h1>
            <p class="text-blue-200 text-sm">Red Nacional de Jóvenes Scouts</p>
          </div>
          <nav class="space-x-4">
            <RouterLink 
              to="/login" 
              class="bg-white text-blue-900 px-6 py-2 rounded-lg font-semibold hover:bg-blue-50 transition"
            >
              Iniciar Sesión
            </RouterLink>
          </nav>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <main class="flex-1 bg-gradient-to-br from-blue-50 to-green-50">
      <div class="container mx-auto px-4 py-20">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="text-5xl font-bold text-gray-900 mb-6">
            Conecta, Compite, Crece
          </h2>
          <p class="text-xl text-gray-700 mb-12">
            Plataforma de gamificación para scouts. Completa misiones, 
            gana insignias y alcanza la cima del ranking nacional.
          </p>

          <div class="grid md:grid-cols-3 gap-8 mb-12">
            <!-- Feature 1 -->
            <div class="bg-white p-6 rounded-xl shadow-md">
              <div class="text-4xl mb-4">🎯</div>
              <h3 class="text-xl font-bold mb-2">Misiones</h3>
              <p class="text-gray-600">
                Completa desafíos y gana puntos para tu grupo scout
              </p>
            </div>

            <!-- Feature 2 -->
            <div class="bg-white p-6 rounded-xl shadow-md">
              <div class="text-4xl mb-4">💬</div>
              <h3 class="text-xl font-bold mb-2">Chat en Vivo</h3>
              <p class="text-gray-600">
                Conéctate con scouts de todo el país en tiempo real
              </p>
            </div>

            <!-- Feature 3 -->
            <div class="bg-white p-6 rounded-xl shadow-md">
              <div class="text-4xl mb-4">🏆</div>
              <h3 class="text-xl font-bold mb-2">Ranking</h3>
              <p class="text-gray-600">
                Compite en el ranking nacional y regional
              </p>
            </div>
          </div>

          <RouterLink 
            to="/login" 
            class="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition shadow-lg"
          >
            Comenzar Ahora
          </RouterLink>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-8">
      <div class="container mx-auto px-4 text-center">
        <p>&copy; 2025 RNJ-Connect - Red Nacional de Jóvenes Scouts</p>
        <p class="text-gray-400 text-sm mt-2">Siempre Listos 🏕️</p>
      </div>
    </footer>
  </div>
</template>
