<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/Navbar.vue'

const authStore = useAuthStore()

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchCurrentUser()
  }
})
</script>

<template>
  <div>
    <Navbar />

    <!-- Main Content -->
    <main class="container-fluid px-4 px-md-5 py-5">
      <div v-if="authStore.user" class="container" style="max-width: 1400px;">
        <!-- Welcome Section -->
        <div class="card border-0 shadow-sm mb-4" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
          <div class="card-body">
            <h2 class="h4 fw-bold mb-1">
              ¡Hola, {{ authStore.user.full_name || authStore.user.username }}!
            </h2>
            <p class="text-muted mb-0">
              {{ authStore.user.scout_group ? `Grupo Scout: ${authStore.user.scout_group}` : 'Completa tu perfil para conectar con tu grupo' }}
            </p>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="row g-3 mb-4">
          <!-- Puntos deshabilitados temporalmente -->
          <!-- <div class="col-md-3">
            <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-2 mb-2" style="color: #a855f7;">
                  <i class="fas fa-star"></i>
                </div>
                <div class="h5 fw-bold mb-1">{{ authStore.user.points || 0 }}</div>
                <small class="text-muted">Puntos Totales</small>
              </div>
            </div>
          </div> -->

          <!-- Nivel deshabilitado temporalmente -->
          <!-- <div class="col-md-3">
            <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-2 mb-2" style="color: #f97316;">
                  <i class="fas fa-chart-line"></i>
                </div>
                <div class="h5 fw-bold mb-1">Nivel {{ authStore.user.level || 1 }}</div>
                <small class="text-muted">Tu Nivel Actual</small>
              </div>
            </div>
          </div> -->

          <!-- Insignias deshabilitadas temporalmente -->
          <!-- <div class="col-md-3">
            <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-2 mb-2" style="color: #4b9ea6;">
                  <i class="fas fa-medal"></i>
                </div>
                <div class="h5 fw-bold mb-1">{{ authStore.user.badges_count || 0 }}</div>
                <small class="text-muted">Insignias</small>
              </div>
            </div>
          </div> -->

          <div class="col-md-3">
            <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <!-- Misiones deshabilitadas temporalmente -->
              <!-- <div class="fs-2 mb-2" style="color: #a855f7;">
                  <i class="fas fa-bullseye"></i>
                </div>
                <div class="h5 fw-bold mb-1">0</div>
                <small class="text-muted">Misiones Activas</small> -->
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mb-4">
          <h5 class="fw-bold mb-3">Acciones Rápidas</h5>
          <div class="row g-3">
            <div class="col-md-4">
              <RouterLink to="/chat" class="card border-0 shadow-sm text-decoration-none" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6); color: inherit; transition: transform 0.3s;">
                <div class="card-body">
                  <div class="fs-2 mb-3" style="color: #a855f7;">
                    <i class="fas fa-comments"></i>
                  </div>
                  <h6 class="card-title fw-bold">Chat en Vivo</h6>
                  <p class="card-text small text-muted">Conéctate con otros scouts</p>
                </div>
              </RouterLink>
            </div>

            <!-- Misiones deshabilitadas temporalmente -->
            <!-- <div class="col-md-4">
              <RouterLink to="/gamification" class="card border-0 shadow-sm text-decoration-none" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6); color: inherit; transition: transform 0.3s;">
                <div class="card-body">
                  <div class="fs-2 mb-3" style="color: #f97316;">
                    <i class="fas fa-gamepad"></i>
                  </div>
                  <h6 class="card-title fw-bold">Misiones</h6>
                  <p class="card-text small text-muted">Completa desafíos</p>
                </div>
              </RouterLink>
            </div> -->

            <div class="col-md-4">
              <RouterLink to="/profile" class="card border-0 shadow-sm text-decoration-none" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6); color: inherit; transition: transform 0.3s;">
                <div class="card-body">
                  <div class="fs-2 mb-3" style="color: #4b9ea6;">
                    <i class="fas fa-user"></i>
                  </div>
                  <h6 class="card-title fw-bold">Mi Perfil</h6>
                  <p class="card-text small text-muted">Actualiza tu información</p>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>

        <!-- Progress Section -->
        <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
          <div class="card-header border-0 bg-transparent">
            <h6 class="card-title fw-bold mb-0">
              <i class="fas fa-chart-line me-2" style="color: #a855f7;"></i>Tu Progreso
            </h6>
          </div>
          <div class="card-body">
            <!-- Progreso de Nivel deshabilitado temporalmente -->
            <!-- <div class="mb-4">
              <div class="d-flex justify-content-between mb-2">
                <span class="fw-semibold">Próximo Nivel</span>
                <span class="fw-bold" style="color: #a855f7;">{{ authStore.user.points || 0 }} / {{ (authStore.user.level || 1) * 100 }}</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div 
                  class="progress-bar" 
                  style="background: linear-gradient(90deg, #a855f7 0%, #7c3aed 100%); width: 65%"
                ></div>
              </div>
            </div> -->
            <p class="text-muted text-center">Funcionalidad de progreso deshabilitada temporalmente</p>

            <!-- Progress Bar 2 - Insignias deshabilitadas temporalmente -->
            <!-- <div>
              <div class="d-flex justify-content-between mb-2">
                <span class="fw-semibold">Insignias Desbloqueadas</span>
                <span class="fw-bold" style="color: #f97316;">{{ authStore.user.badges_count || 0 }} / 20</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div 
                  class="progress-bar" 
                  style="background: linear-gradient(90deg, #f97316 0%, #facc15 100%); width: 35%"
                ></div>
              </div>
            </div> -->
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <div class="fs-1 mb-3">
          <i class="fas fa-spinner fa-spin"></i>
        </div>
        <p class="text-muted">Cargando tu aventura...</p>
      </div>
    </main>
  </div>
</template>
