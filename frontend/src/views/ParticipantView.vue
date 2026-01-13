<template>
  <div class="participant-view" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); min-height: 100vh;">
    <div class="container py-5">
      <!-- Back Button -->
      <div class="mb-4">
        <RouterLink to="/foro" class="btn btn-outline-secondary">
          <i class="fas fa-arrow-left me-2"></i>Volver al Foro
        </RouterLink>
      </div>

      <!-- Información del Participante -->
      <div v-if="participant" class="row g-4">
        <!-- Carnet -->
        <div class="col-lg-5">
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95); position: sticky; top: 20px;">
            <div class="card-body p-0">
              <ParticipantCard :participant="participant" />
            </div>
          </div>
        </div>

        <!-- Detalles -->
        <div class="col-lg-7">
          <ParticipantDetailModal 
            :participant="participant"
            :is-open="true"
          />
        </div>
      </div>

      <!-- Cargando -->
      <div v-else-if="isLoading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="mt-3 text-muted">Buscando participante...</p>
      </div>

      <!-- Error -->
      <div v-else class="alert alert-danger" role="alert">
        <i class="fas fa-exclamation-circle me-2"></i>
        <strong>Error:</strong> No se pudo encontrar al participante
        <div class="mt-3">
          <p class="mb-2">Posibles razones:</p>
          <ul>
            <li>El código QR puede estar dañado o no válido</li>
            <li>El participante puede haber sido eliminado</li>
            <li>Es posible que no tengas permisos para ver este participante</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import ParticipantCard from '@/components/ParticipantCard.vue'
import ParticipantDetailModal from '@/components/ParticipantDetailModal.vue'

const route = useRoute()
const router = useRouter()

const participant = ref(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    const participantId = route.params.id
    
    if (!participantId) {
      throw new Error('ID de participante no válido')
    }

    const response = await fetch(`/api/v1/foro/participants/${participantId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (!response.ok) {
      throw new Error('Participante no encontrado')
    }

    const data = await response.json()
    participant.value = data
  } catch (error) {
    console.error('Error:', error)
    participant.value = null
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.participant-view {
  min-height: 100vh;
}

@media (max-width: 992px) {
  .card {
    position: relative !important;
    top: auto !important;
  }
}
</style>
