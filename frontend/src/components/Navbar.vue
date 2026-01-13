<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const isActive = (path) => {
  return route.path === path
}
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-light bg-white shadow-sm sticky-top" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.4) !important;">
    <div class="container-fluid px-3 px-md-5">
      <!-- Logo & Brand -->
      <RouterLink to="/dashboard" class="navbar-brand d-flex align-items-center gap-2">
        <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 40px; height: 40px; background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <i class="fas fa-campground text-white" style="font-size: 14px;"></i>
        </div>
        <span class="fw-bold" style="font-size: 18px; color: #1a1a1a;">RNDJ</span>
      </RouterLink>

      <!-- Toggle Button -->
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation Menu -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto gap-1">
          <li class="nav-item">
            <RouterLink 
              to="/dashboard" 
              :class="['nav-link', { active: isActive('/dashboard') }]"
              style="font-weight: 500; color: #4b5563;"
            >
              <i class="fas fa-home me-2"></i>Dashboard
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink 
              to="/chat" 
              :class="['nav-link', { active: isActive('/chat') }]"
              style="font-weight: 500; color: #4b5563;"
            >
              <i class="fas fa-comments me-2"></i>Chat
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink 
              to="/foro" 
              :class="['nav-link', { active: isActive('/foro') }]"
              style="font-weight: 500; color: #4b5563;"
            >
              <i class="fas fa-users me-2"></i>5to Foro
            </RouterLink>
          </li>
          <!-- Gamification deshabilitada temporalmente -->
          <!-- <li class="nav-item">
            <RouterLink 
              to="/gamification" 
              :class="['nav-link', { active: isActive('/gamification') }]"
              style="font-weight: 500; color: #4b5563;"
            >
              <i class="fas fa-trophy me-2"></i>Misiones
            </RouterLink>
          </li> -->
        </ul>

        <!-- Right Section -->
        <div class="d-flex align-items-center gap-2 ms-3">
          <ThemeToggle />

          <RouterLink 
            to="/profile"
            :class="['btn btn-link', { active: isActive('/profile') }]"
            style="text-decoration: none; color: #4b5563; font-weight: 500; font-size: 14px;"
          >
            <i class="fas fa-user me-1"></i>
            <span class="d-none d-lg-inline">{{ authStore.user?.username || 'Perfil' }}</span>
          </RouterLink>

          <button 
            @click="handleLogout"
            class="btn btn-link"
            style="text-decoration: none; color: #dc2626; font-weight: 500; padding: 0; border: none;"
          >
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  border-bottom: 1px solid rgba(200, 200, 200, 0.2) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.navbar-light .navbar-nav .nav-link {
  color: #4b5563 !important;
  transition: color 0.3s ease;
  border-bottom: 2px solid transparent;
}

.navbar-light .navbar-nav .nav-link:hover {
  color: #7c3aed !important;
}

.navbar-light .navbar-nav .nav-link.active {
  color: #7c3aed !important;
  border-bottom: 2px solid #7c3aed;
}

.btn-link {
  color: #4b5563 !important;
  transition: color 0.3s ease;
}

.btn-link:hover {
  color: #7c3aed !important;
}

.btn-link.active {
  color: #7c3aed !important;
}

@media (prefers-color-scheme: dark) {
  .navbar {
    background-color: rgba(30, 41, 59, 0.4) !important;
  }

  .navbar-light .navbar-nav .nav-link {
    color: #d1d5db !important;
  }

  .navbar-light .navbar-nav .nav-link:hover,
  .navbar-light .navbar-nav .nav-link.active {
    color: #c084fc !important;
  }

  .btn-link {
    color: #d1d5db !important;
  }

  .btn-link:hover,
  .btn-link.active {
    color: #c084fc !important;
  }

  .navbar-brand {
    color: #f3f4f6 !important;
  }
}
</style>
