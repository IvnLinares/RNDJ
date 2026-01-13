<template>
  <div>
    <Navbar />
    
    <div class="py-5 px-4 px-md-5">
      <div class="container" style="max-width: 1200px;">
        <!-- Header -->
        <div class="mb-4">
          <h1 class="h3 fw-bold mb-0" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            Chat en Vivo
          </h1>
        </div>

        <!-- Main Chat Card -->
        <div class="card border-0 shadow-sm mb-4" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
          <div class="card-header bg-transparent border-bottom">
            <h5 class="card-title mb-0">En Desarrollo</h5>
          </div>
          <div class="card-body text-center py-5">
            <div class="fs-1 mb-3" style="color: #f97316;">
              <i class="fas fa-comments"></i>
            </div>
            <h3 class="h5 fw-bold mb-3">Chat en Tiempo Real</h3>
            <p class="text-muted mb-3" style="max-width: 600px; margin-left: auto; margin-right: auto;">
              Pronto podrás conectarte con scouts de todo el país en tiempo real.
              ¡Estamos trabajando en esta increíble funcionalidad!
            </p>
            <div class="d-flex gap-2 justify-content-center flex-wrap">
              <span class="badge bg-primary">WebSocket</span>
              <span class="badge bg-success">Tiempo Real</span>
              <span class="badge bg-danger">Próximamente</span>
            </div>
          </div>
          <div class="card-footer bg-transparent border-top">
            <RouterLink to="/dashboard" class="btn btn-sm btn-primary">
              Volver al Dashboard
            </RouterLink>
          </div>
        </div>

        <!-- Features Preview -->
        <div class="row g-4 mt-3">
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #a855f7;">
                  <i class="fas fa-users"></i>
                </div>
                <h6 class="card-title fw-bold">Salas de Grupo</h6>
                <p class="card-text text-muted small">Crea o únete a salas de chat por grupo scout</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #f97316;">
                  <i class="fas fa-bell"></i>
                </div>
                <h6 class="card-title fw-bold">Notificaciones</h6>
                <p class="card-text text-muted small">Recibe notificaciones instantáneas de mensajes</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #4b9ea6;">
                  <i class="fas fa-paperclip"></i>
                </div>
                <h6 class="card-title fw-bold">Multimedia</h6>
                <p class="card-text text-muted small">Comparte imágenes y archivos con tu equipo</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { RouterLink } from 'vue-router'
</script>
