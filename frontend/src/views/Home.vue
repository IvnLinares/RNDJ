<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThemeToggle from '@/components/ThemeToggle.vue'

const authStore = useAuthStore()
</script>

<style scoped>
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

<template>
  <div class="d-flex flex-column" style="min-height: 100vh; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);">
    <!-- Header Premium -->
    <header class="sticky-top" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background-color: rgba(255, 255, 255, 0.85); border-bottom: 1px solid rgba(200, 200, 200, 0.15); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
      <div class="container-fluid px-4 px-md-5">
        <div class="d-flex align-items-center justify-content-between py-3">
          <div class="d-flex align-items-center gap-3">
            <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 45px; height: 45px; background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);">
              <i class="fas fa-campground text-white" style="font-size: 22px;"></i>
            </div>
            <h1 class="h4 mb-0 fw-bold" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">RNDJ-Connect</h1>
          </div>
          <nav class="d-flex align-items-center gap-3">
            <ThemeToggle />
            <RouterLink to="/login" class="btn btn-primary btn-sm fw-bold">
              Iniciar Sesión
            </RouterLink>
          </nav>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <main class="flex-grow-1 container-fluid px-4 px-md-5 py-5">
      <div class="container" style="max-width: 1200px; animation: fadeIn 0.6s ease-out;">
        <!-- Hero Title -->
        <div class="text-center mb-5">
          <h2 class="display-3 fw-bold mb-4" style="line-height: 1.2;">
            <span style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Conecta</span>,
            <br>
            <span style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Compite</span>,
            <br>
            <span style="background: linear-gradient(135deg, #4b9ea6 0%, #2d6b74 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Crece</span>
          </h2>
          <!-- <p class="lead text-muted mb-5" style="max-width: 650px; margin-left: auto; margin-right: auto; font-weight: 500;">
            Plataforma de gamificación para scouts. Completa misiones épicas, 
            gana insignias exclusivas y alcanza la cima del ranking nacional.
          </p> -->
          <p class="lead text-muted mb-5" style="max-width: 650px; margin-left: auto; margin-right: auto; font-weight: 500;">
            Plataforma de conexión para scouts. Conéctate con otros scouts y colabora en proyectos de grupo.
          </p>
          <RouterLink to="/login" class="btn btn-primary btn-lg fw-bold px-5 py-3" style="border-radius: 12px; font-size: 1.1rem;">
            Comenzar Ahora
            <i class="fas fa-arrow-right ms-2"></i>
          </RouterLink>
        </div>

        <!-- Feature Cards Premium -->
        <div class="row g-4 mt-5 mb-5">
          <!-- Feature 1 - Misiones deshabilitadas temporalmente -->
          <!-- <div class="col-md-4">
            <div class="card border-0 h-100 hover-lift" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%); box-shadow: 0 4px 20px rgba(168, 85, 247, 0.1);">
              <div class="card-body p-5">
                <div class="fs-1 mb-4" style="color: #a855f7; animation: slideDown 0.6s ease-out;">
                  <i class="fas fa-bullseye"></i>
                </div>
                <h5 class="card-title fw-bold mb-3" style="color: #1a1a1a; font-size: 1.2rem;">Misiones Épicas</h5>
                <p class="card-text text-muted" style="line-height: 1.6;">
                  Completa desafíos emocionantes y gana puntos para tu grupo scout
                </p>
              </div>
            </div>
          </div> -->

          <!-- Feature 2 -->
          <div class="col-md-6">
            <div class="card border-0 h-100 hover-lift" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%); box-shadow: 0 4px 20px rgba(249, 115, 22, 0.1); animation: slideDown 0.7s ease-out;">
              <div class="card-body p-5">
                <div class="fs-1 mb-4" style="color: #f97316;">
                  <i class="fas fa-comments"></i>
                </div>
                <h5 class="card-title fw-bold mb-3" style="color: #1a1a1a; font-size: 1.2rem;">Chat en Vivo</h5>
                <p class="card-text text-muted" style="line-height: 1.6;">
                  Conéctate con scouts de todo el país en tiempo real
                </p>
              </div>
            </div>
          </div>

          <!-- Feature 3 -->
          <div class="col-md-6">
            <div class="card border-0 h-100 hover-lift" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%); box-shadow: 0 4px 20px rgba(75, 158, 166, 0.1); animation: slideDown 0.8s ease-out;">
              <div class="card-body p-5">
                <div class="fs-1 mb-4" style="color: #4b9ea6;">
                  <i class="fas fa-trophy"></i>
                </div>
                <h5 class="card-title fw-bold mb-3" style="color: #1a1a1a; font-size: 1.2rem;">Ranking Nacional</h5>
                <p class="card-text text-muted" style="line-height: 1.6;">
                  Compite en el ranking nacional y regional
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Section Premium -->
        <div class="card border-0 mt-5 hover-glow" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.8) 100%); box-shadow: 0 10px 30px rgba(168, 85, 247, 0.12);">
          <div class="card-body p-5">
            <h3 class="fw-bold mb-5 text-center" style="font-size: 1.5rem; background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
              <i class="fas fa-users me-2"></i>Únete a la Comunidad Scout
            </h3>
            <div class="row g-4">
              <div class="col-md-4">
                <div class="text-center">
                  <div class="fs-2 fw-bold mb-2" style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">1,000+</div>
                  <div class="text-muted fw-500">Scouts Activos</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="text-center">
                  <div class="fs-2 fw-bold mb-2" style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">50+</div>
                  <div class="text-muted fw-500">Grupos Scouts</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="text-center">
                  <div class="fs-2 fw-bold mb-2" style="background: linear-gradient(135deg, #4b9ea6 0%, #2d6b74 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">20+</div>
                  <div class="text-muted fw-500">Conexiones Diarias</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer Premium -->
    <footer class="border-top text-center py-5 mt-5" style="border-color: rgba(200, 200, 200, 0.15) !important; background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(248, 250, 252, 0.3) 100%); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);">
      <div class="container">
        <p class="mb-2 fw-500 text-muted">© 2024 RNDJ-Connect - Red Nacional de Jóvenes Scouts</p>
        <p class="mb-0 text-muted small">Siempre Listos</p>
      </div>
    </footer>
  </div>
</template>
