<template>
  <div>
    <Navbar />
    
    <div class="py-5 px-4 px-md-5">
      <div class="container" style="max-width: 1000px;">
        <!-- Header -->
        <div class="mb-4">
          <h1 class="h3 fw-bold mb-0" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            Mi Perfil
          </h1>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="card border-0 shadow-sm text-center py-5" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
          <div class="fs-1 mb-3"><i class="fas fa-spinner fa-spin"></i></div>
          <p class="text-muted">Cargando perfil...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger" role="alert">
          <i class="fas fa-exclamation-circle me-2"></i>
          <strong>Error:</strong> {{ error }}
          <button @click="loadProfile" class="btn btn-sm btn-outline-danger mt-2 ms-2">
            <i class="fas fa-redo"></i> Reintentar
          </button>
        </div>

        <!-- Profile Content -->
        <div v-else class="space-y-4">
          <!-- Profile Header Card -->
          <div class="card border-0 shadow-sm mb-4" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <h2 class="h4 fw-bold mb-1">{{ user.full_name || user.username }}</h2>
                  <p class="text-muted mb-1">@{{ user.username }}</p>
                  <p class="text-muted small">{{ user.email }}</p>
                </div>
                <div class="text-end">
                  <!-- Nivel deshabilitado temporalmente -->
                  <!-- <div class="h2 fw-bold mb-1" style="background: linear-gradient(135deg, #a855f7 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {{ user.level }}
                  </div>
                  <p class="text-muted small">Nivel Scout</p> -->
                </div>
              </div>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="row g-3 mb-4">
            <!-- Puntos deshabilitados temporalmente -->
            <!-- <div class="col-md-4">
              <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                <div class="card-body">
                  <div class="h5 fw-bold mb-1" style="color: #a855f7;">{{ user.points }}</div>
                  <p class="text-muted small mb-0">Puntos</p>
                </div>
              </div>
            </div> -->
            <!-- Insignias deshabilitadas temporalmente -->
            <!-- <div class="col-md-4">
              <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                <div class="card-body">
                  <div class="h5 fw-bold mb-1" style="color: #f97316;">{{ user.badges_count }}</div>
                  <p class="text-muted small mb-0">Insignias</p>
                </div>
              </div>
            </div> -->
            <div class="col-md-4">
              <div class="card border-0 shadow-sm text-center" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                <div class="card-body">
                  <div class="h5 mb-1" style="color: #4b9ea6;">
                    <i :class="user.is_active ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                  </div>
                  <p class="text-muted small mb-0">Estado</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Form Card -->
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
            <div class="card-header bg-transparent border-bottom d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Información Personal</h5>
              <div v-if="!editMode">
                <button @click="enterEditMode" class="btn btn-sm btn-primary">
                  <i class="fas fa-edit me-1"></i>Editar
                </button>
              </div>
              <div v-else class="gap-2 d-flex">
                <button @click="cancelEdit" class="btn btn-sm btn-outline-secondary">
                  Cancelar
                </button>
                <button @click="saveProfile" :disabled="savingProfile" class="btn btn-sm btn-primary">
                  {{ savingProfile ? 'Guardando...' : 'Guardar' }}
                </button>
              </div>
            </div>

            <div class="card-body">
              <!-- Form Fields -->
              <form @submit.prevent>
                <!-- Full Name -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Nombre Completo</label>
                  <input
                    v-model="formData.full_name"
                    :readonly="!editMode"
                    type="text"
                    class="form-control"
                    :class="{ 'bg-light': !editMode }"
                    placeholder="Tu nombre completo"
                  />
                </div>

                <!-- Username -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Nombre de Usuario</label>
                  <input
                    v-model="formData.username"
                    :readonly="!editMode"
                    type="text"
                    class="form-control"
                    :class="{ 'bg-light': !editMode }"
                    placeholder="Tu nombre de usuario"
                  />
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Email</label>
                  <input
                    v-model="formData.email"
                    :readonly="!editMode"
                    type="email"
                    class="form-control"
                    :class="{ 'bg-light': !editMode }"
                    placeholder="tu@email.com"
                  />
                </div>

                <!-- Scout Group -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Grupo Scout</label>
                  <input
                    v-model="formData.scout_group"
                    :readonly="!editMode"
                    type="text"
                    class="form-control"
                    :class="{ 'bg-light': !editMode }"
                    placeholder="Tu grupo scout"
                  />
                </div>

                <!-- Scout Region -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Región Scout</label>
                  <input
                    v-model="formData.scout_region"
                    :readonly="!editMode"
                    type="text"
                    class="form-control"
                    :class="{ 'bg-light': !editMode }"
                    placeholder="Tu región scout"
                  />
                </div>

                <!-- Scout Rank -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">Rango Scout</label>
                  <select
                    v-model="formData.scout_rank"
                    :disabled="!editMode"
                    class="form-select"
                    :class="{ 'bg-light': !editMode }"
                  >
                    <option value="">Seleccionar rango</option>
                    <option value="Scout">Scout</option>
                    <option value="Guía">Guía</option>
                    <option value="Pionero">Pionero</option>
                    <option value="Rover">Rover</option>
                    <option value="Dirigente">Dirigente</option>
                  </select>
                </div>
              </form>

              <!-- Account Info (Read-only) -->
              <div class="mt-4 pt-4 border-top">
                <h6 class="fw-bold mb-3">Información de Cuenta</h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                      <div class="card-body">
                        <p class="text-muted small mb-1">ID de Usuario</p>
                        <p class="fw-bold">{{ user.id }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                      <div class="card-body">
                        <p class="text-muted small mb-1">Creada el</p>
                        <p class="fw-bold">{{ formatDate(user.created_at) }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                      <div class="card-body">
                        <p class="text-muted small mb-1">Última actualización</p>
                        <p class="fw-bold">{{ user.updated_at ? formatDate(user.updated_at) : 'N/A' }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.6);">
                      <div class="card-body">
                        <p class="text-muted small mb-1">Cuenta Activa</p>
                        <p class="fw-bold">
                          <i :class="user.is_active ? 'fas fa-check-circle text-success' : 'fas fa-times-circle text-danger'"></i> 
                          {{ user.is_active ? 'Sí' : 'No' }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import api from '../services/api'

const user = ref({
  id: null,
  email: '',
  username: '',
  full_name: '',
  scout_group: '',
  scout_region: '',
  scout_rank: '',
  points: 0,
  level: 1,
  badges_count: 0,
  is_active: false,
  created_at: '',
  updated_at: null
})

const formData = ref({
  email: '',
  username: '',
  full_name: '',
  scout_group: '',
  scout_region: '',
  scout_rank: ''
})

const loading = ref(true)
const error = ref(null)
const editMode = ref(false)
const savingProfile = ref(false)

// Load user profile on component mount
onMounted(() => {
  loadProfile()
})

// Load profile from API
const loadProfile = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await api.get('/users/me')
    user.value = response.data
    // Initialize form data with user data
    Object.keys(formData.value).forEach(key => {
      formData.value[key] = user.value[key] || ''
    })
  } catch (err) {
    console.error('Error loading profile:', err)
    error.value = err.response?.data?.detail || 'Error al cargar el perfil'
  } finally {
    loading.value = false
  }
}

// Enter edit mode
const enterEditMode = () => {
  editMode.value = true
}

// Cancel edit mode
const cancelEdit = () => {
  editMode.value = false
  // Reset form data
  Object.keys(formData.value).forEach(key => {
    formData.value[key] = user.value[key] || ''
  })
}

// Save profile changes
const saveProfile = async () => {
  try {
    savingProfile.value = true
    error.value = null
    
    const response = await api.put('/users/me', formData.value)
    user.value = response.data
    editMode.value = false
    
    // Show success message
    alert('Perfil actualizado exitosamente')
  } catch (err) {
    console.error('Error updating profile:', err)
    error.value = err.response?.data?.detail || 'Error al actualizar el perfil'
  } finally {
    savingProfile.value = false
  }
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
