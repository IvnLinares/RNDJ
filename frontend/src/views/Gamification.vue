<template>
  <div>
    <Navbar />
    
    <div class="py-5 px-4 px-md-5">
      <div class="container" style="max-width: 1200px;">
        <!-- Header -->
        <div class="mb-4">
          <h1 class="h3 fw-bold mb-0" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            Gamificación
          </h1>
        </div>

        <!-- Main Card -->
        <div class="card border-0 shadow-sm mb-4" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
          <div class="card-header bg-transparent border-bottom">
            <h5 class="card-title mb-0">Sistema de Gamificación</h5>
          </div>
          <div class="card-body text-center py-5">
            <div class="fs-1 mb-3" style="color: #a855f7;">
              <i class="fas fa-bullseye"></i>
            </div>
            <h3 class="h5 fw-bold mb-3">Misiones e Insignias</h3>
            <p class="text-muted mb-3" style="max-width: 600px; margin-left: auto; margin-right: auto;">
              Completa misiones épicas, gana insignias exclusivas y sube de nivel.
              ¡El sistema de gamificación estará disponible muy pronto!
            </p>
            <div class="d-flex gap-2 justify-content-center flex-wrap">
              <span class="badge bg-primary">Misiones</span>
              <span class="badge bg-danger">Insignias</span>
              <span class="badge bg-success">Rankings</span>
              <span class="badge bg-secondary">Próximamente</span>
            </div>
          </div>
        </div>

        <!-- Features Preview -->
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #a855f7;">
                  <i class="fas fa-bullseye"></i>
                </div>
                <h6 class="card-title fw-bold">Misiones Épicas</h6>
                <p class="card-text text-muted small">Completa desafíos individuales y en equipo</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #f97316;">
                  <i class="fas fa-medal"></i>
                </div>
                <h6 class="card-title fw-bold">Insignias</h6>
                <p class="card-text text-muted small">Desbloquea insignias exclusivas por tus logros</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
              <div class="card-body">
                <div class="fs-1 mb-3" style="color: #4b9ea6;">
                  <i class="fas fa-trophy"></i>
                </div>
                <h6 class="card-title fw-bold">Rankings</h6>
                <p class="card-text text-muted small">Compite en rankings nacionales y regionales</p>
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
