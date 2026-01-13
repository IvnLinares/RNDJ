<template>
  <div>
    <Navbar />
    
    <!-- Modern Hero Section -->
    <div class="foro-hero">
      <div class="container">
        <div class="hero-content">
          <div class="hero-icon">
            <i class="fas fa-users"></i>
          </div>
          <h1 class="hero-title">5to Foro Nacional de Jóvenes</h1>
          <p class="hero-subtitle">Sistema integral de gestión de participantes · RNDJ 2025</p>
          <div class="hero-stats">
            <div class="stat-item">
              <i class="fas fa-user-check"></i>
              <span>{{ participants.length }} Registrados</span>
            </div>
            <div class="stat-item">
              <i class="fas fa-trophy"></i>
              <span>Foro Nacional</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="foro-container">
      <div class="container">
        <!-- Modern Tabs Navigation -->
        <div class="modern-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab-button', { active: activeTab === tab.id }]"
            @click="switchTab(tab.id)"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
            <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
          </button>
        </div>

      <!-- Contenido de tabs -->
      <div class="tab-content">
        <!-- Tab: Registrar Participante -->
        <div class="tab-pane fade show active" id="registro" role="tabpanel">
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95);">
            <div class="card-body p-5">
              <h5 class="card-title fw-bold mb-4">Registrar nuevo participante</h5>
              
              <form @submit.prevent="submitForm" v-if="!formSubmitting">
                <div class="row">
                  <!-- Nombre -->
                  <div class="col-md-6 mb-4">
                    <label for="fullName" class="form-label fw-600 text-dark">Nombre Completo *</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="fullName" 
                      v-model="formData.full_name"
                      placeholder="Nombre y Apellido"
                      required
                      style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 16px;"
                    >
                  </div>

                  <!-- NIS -->
                  <div class="col-md-6 mb-4">
                    <label for="nis" class="form-label fw-600 text-dark">NIS (Número de Identificación Scout) *</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="nis" 
                      v-model="formData.nis"
                      placeholder="Ej: NIS123456"
                      required
                      style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 16px;"
                    >
                  </div>

                  <!-- Email -->
                  <div class="col-md-6 mb-4">
                    <label for="email" class="form-label fw-600 text-dark">Email *</label>
                    <input 
                      type="email" 
                      class="form-control" 
                      id="email" 
                      v-model="formData.email"
                      placeholder="correo@ejemplo.com"
                      required
                      style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 16px;"
                    >
                  </div>

                  <!-- Rama -->
                  <div class="col-md-6 mb-4">
                    <label for="rama" class="form-label fw-600 text-dark">Rama Scout *</label>
                    <select 
                      class="form-select" 
                      id="rama" 
                      v-model="formData.rama"
                      required
                      style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 16px;"
                    >
                      <option value="">Selecciona una rama</option>
                      <option value="Caminantes">Caminantes (15-18 años)</option>
                      <option value="Rovers">Rovers (18-22 años)</option>
                      <option value="Dirigente Joven">Dirigente Joven (22-25 años)</option>
                      <option value="Dirigente">Dirigente (25+ años)</option>
                    </select>
                  </div>

                  <!-- Notas -->
                  <div class="col-12 mb-4">
                    <label for="notes" class="form-label fw-600 text-dark">Notas Adicionales</label>
                    <textarea 
                      class="form-control" 
                      id="notes" 
                      v-model="formData.notes"
                      placeholder="Información adicional sobre el participante..."
                      rows="3"
                      style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 16px;"
                    ></textarea>
                  </div>
                </div>

                <!-- Botón enviar -->
                <div class="d-flex gap-3">
                  <button 
                    type="submit" 
                    class="btn fw-bold px-4 py-2"
                    style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); color: white; border: none; border-radius: 10px;"
                  >
                    <i class="fas fa-save me-2"></i>Guardar Participante
                  </button>
                  <button 
                    type="button" 
                    @click="resetForm"
                    class="btn fw-bold px-4 py-2"
                    style="background-color: #f1f5f9; color: #4b5563; border: none; border-radius: 10px;"
                  >
                    <i class="fas fa-redo me-2"></i>Limpiar
                  </button>
                </div>

                <!-- Mensajes -->
                <div v-if="successMessage" class="alert alert-success mt-4" role="alert" style="animation: slideDown 0.3s ease-out;">
                  <i class="fas fa-check-circle me-2"></i>{{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger mt-4" role="alert" style="animation: slideDown 0.3s ease-out;">
                  <i class="fas fa-exclamation-circle me-2"></i>{{ errorMessage }}
                </div>
              </form>

              <!-- Cargando -->
              <div v-else class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-3 text-muted">Registrando participante...</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Importar XLSX -->
        <div class="tab-pane fade" id="importar" role="tabpanel">
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95);">
            <div class="card-body p-5">
              <h5 class="card-title fw-bold mb-4">Importar participantes desde XLSX</h5>

              <!-- Instrucciones -->
              <div class="alert alert-info" role="alert" style="background-color: rgba(168, 85, 247, 0.1); border: 2px solid #a855f7; color: #333;">
                <h6 class="fw-bold mb-3">
                  <i class="fas fa-info-circle me-2" style="color: #a855f7;"></i>Formato del archivo Excel
                </h6>
                <p class="mb-0 small">El archivo debe tener las siguientes columnas en este orden:</p>
                <ul class="small mt-2 mb-0">
                  <li><strong>Columna A:</strong> Nombre completo (requerido)</li>
                  <li><strong>Columna B:</strong> NIS - Número de Identificación Scout (requerido)</li>
                  <li><strong>Columna C:</strong> Email (requerido)</li>
                  <li><strong>Columna D:</strong> Rama Scout - Caminantes, Rovers, Dirigente Joven, Dirigente (requerido)</li>
                  <li><strong>Columna E:</strong> Notas (opcional)</li>
                </ul>
              </div>

              <!-- Upload area -->
              <div 
                @drop="handleDrop" 
                @dragover.prevent="isDragging = true" 
                @dragleave="isDragging = false"
                :style="isDragging ? 'background-color: rgba(168, 85, 247, 0.1); border-color: #a855f7;' : ''"
                style="border: 3px dashed #e2e8f0; border-radius: 15px; padding: 40px; text-align: center; cursor: pointer; transition: all 0.3s;"
              >
                <div class="mb-4">
                  <i class="fas fa-file-excel" style="font-size: 3rem; color: #f97316;"></i>
                </div>
                <h6 class="fw-bold mb-2">Arrastra tu archivo Excel aquí</h6>
                <p class="text-muted mb-4">o haz clic para seleccionar</p>
                <input 
                  type="file" 
                  ref="fileInput" 
                  @change="handleFileSelect"
                  accept=".xlsx,.xls"
                  style="display: none;"
                >
                <button 
                  type="button" 
                  @click="$refs.fileInput.click()"
                  class="btn fw-bold px-4 py-2"
                  style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; border: none; border-radius: 10px;"
                >
                  <i class="fas fa-search me-2"></i>Seleccionar archivo
                </button>
              </div>

              <!-- Estado de carga -->
              <div v-if="importFile" class="mt-4 p-3" style="background-color: #f1f5f9; border-radius: 10px;">
                <p class="mb-0">
                  <i class="fas fa-file me-2" style="color: #4b9ea6;"></i>
                  <strong>{{ importFile.name }}</strong>
                </p>
              </div>

              <!-- Botón importar -->
              <div class="mt-4">
                <button 
                  type="button" 
                  @click="submitImport"
                  :disabled="!importFile || isImporting"
                  class="btn fw-bold px-4 py-2"
                  style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); color: white; border: none; border-radius: 10px;"
                >
                  <span v-if="!isImporting">
                    <i class="fas fa-cloud-upload-alt me-2"></i>Importar participantes
                  </span>
                  <span v-else>
                    <i class="fas fa-spinner fa-spin me-2"></i>Importando...
                  </span>
                </button>
              </div>

              <!-- Resultado de importación -->
              <div v-if="importResult" class="mt-4 p-4" style="background-color: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; border-radius: 10px;">
                <h6 class="fw-bold mb-3" style="color: #059669;">
                  <i class="fas fa-check-circle me-2"></i>Importación completada
                </h6>
                <div class="row g-3">
                  <div class="col-md-3">
                    <div class="text-center">
                      <div class="h3 fw-bold" style="color: #a855f7;">{{ importResult.total_records }}</div>
                      <small class="text-muted">Total registros</small>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="text-center">
                      <div class="h3 fw-bold" style="color: #10b981;">{{ importResult.successful_records }}</div>
                      <small class="text-muted">Exitosos</small>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="text-center">
                      <div class="h3 fw-bold" style="color: #ef4444;">{{ importResult.failed_records }}</div>
                      <small class="text-muted">Fallidos</small>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="text-center">
                      <div class="h3 fw-bold" style="color: #f59e0b;">{{ importResult.import_id }}</div>
                      <small class="text-muted">ID Importación</small>
                    </div>
                  </div>
                </div>

                <!-- Errores detallados -->
                <div v-if="importResult.errors && importResult.errors.length > 0" class="mt-4">
                  <h6 class="fw-bold mb-3" style="color: #ef4444;">Errores encontrados:</h6>
                  <div class="list-group">
                    <div 
                      v-for="(error, idx) in importResult.errors.slice(0, 5)" 
                      :key="idx"
                      class="list-group-item"
                      style="background-color: rgba(239, 68, 68, 0.05); border-color: #fca5a5;"
                    >
                      <p class="mb-1"><strong>Fila {{ error.row }}:</strong> {{ error.error }}</p>
                    </div>
                  </div>
                  <p v-if="importResult.errors.length > 5" class="mt-3 text-muted small">
                    ... y {{ importResult.errors.length - 5 }} errores más
                  </p>
                </div>
              </div>

              <!-- Mensajes -->
              <div v-if="importError" class="alert alert-danger mt-4" role="alert" style="animation: slideDown 0.3s ease-out;">
                <i class="fas fa-exclamation-circle me-2"></i>{{ importError }}
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Listado de Participantes -->
        <div class="tab-pane fade" id="listado" role="tabpanel">
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95);">
            <div class="card-body p-5">
              <h5 class="card-title fw-bold mb-4">Listado de Participantes</h5>

              <!-- Filtros -->
              <div class="row g-3 mb-4">
                <div class="col-md-4">
                  <label class="form-label fw-600">Filtrar por Rama</label>
                  <select v-model="filterRama" class="form-select" style="border: 2px solid #e2e8f0; border-radius: 10px;">
                    <option value="">Todas las ramas</option>
                    <option value="Caminantes">Caminantes (15-18)</option>
                    <option value="Rovers">Rovers (18-22)</option>
                    <option value="Dirigente Joven">Dirigente Joven (22-25)</option>
                    <option value="Dirigente">Dirigente (25+)</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-600">Confirmación</label>
                  <select v-model="filterConfirmed" class="form-select" style="border: 2px solid #e2e8f0; border-radius: 10px;">
                    <option value="">Todos</option>
                    <option value="true">Confirmados</option>
                    <option value="false">No confirmados</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-600">Buscar por nombre</label>
                  <input 
                    type="text" 
                    v-model="searchText" 
                    placeholder="Nombre o email..."
                    class="form-control"
                    style="border: 2px solid #e2e8f0; border-radius: 10px;"
                  >
                </div>
              </div>

              <!-- Tabla -->
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead style="background-color: #f1f5f9;">
                    <tr>
                      <th class="fw-bold">Nombre</th>
                      <th class="fw-bold">NIS</th>
                      <th class="fw-bold">Email</th>
                      <th class="fw-bold">Rama</th>
                      <th class="fw-bold">Confirmado</th>
                      <th class="fw-bold">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="participant in filteredParticipants" :key="participant.id">
                      <td class="fw-600">{{ participant.full_name }}</td>
                      <td>{{ participant.nis }}</td>
                      <td>{{ participant.email }}</td>
                      <td>
                        <span 
                          class="badge" 
                          :style="getBadgeColor(participant.rama)"
                        >
                          {{ participant.rama }}
                        </span>
                      </td>
                      <td>
                        <span v-if="participant.is_confirmed" class="badge bg-success">
                          <i class="fas fa-check me-1"></i>Sí
                        </span>
                        <span v-else class="badge bg-warning">
                          <i class="fas fa-hourglass me-1"></i>Pendiente
                        </span>
                      </td>
                      <td>
                        <button 
                          @click="editParticipant(participant)"
                          class="btn btn-sm fw-bold"
                          style="background-color: #a855f7; color: white; border-radius: 6px;"
                        >
                          <i class="fas fa-edit me-1"></i>Ver
                        </button>
                      </td>
                    </tr>
                    <tr v-if="filteredParticipants.length === 0">
                      <td colspan="6" class="text-center py-5 text-muted">
                        <i class="fas fa-inbox me-2" style="font-size: 2rem;"></i>
                        <p class="mt-2">No hay participantes registrados</p>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Paginación -->
              <div v-if="totalParticipants > 0" class="d-flex justify-content-between align-items-center mt-4">
                <small class="text-muted">
                  Mostrando {{ participants.length }} de {{ totalParticipants }} participantes
                </small>
                <nav>
                  <ul class="pagination mb-0">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <button class="page-link" @click="currentPage--">Anterior</button>
                    </li>
                    <li class="page-item active">
                      <span class="page-link">{{ currentPage }}</span>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage * 100 >= totalParticipants }">
                      <button class="page-link" @click="currentPage++">Siguiente</button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Estadísticas -->
        <div class="tab-pane fade" id="estadisticas" role="tabpanel">
          <div class="row g-4">
            <!-- Cards de estadísticas -->
            <div class="col-md-6">
              <div class="card border-0 shadow-sm h-100 hover-lift" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%); box-shadow: 0 4px 20px rgba(168, 85, 247, 0.1);">
                <div class="card-body p-5 text-center">
                  <div class="fs-1 mb-3" style="color: #a855f7;">
                    <i class="fas fa-users"></i>
                  </div>
                  <div class="h2 fw-bold mb-1">{{ statistics.total_participants }}</div>
                  <p class="text-muted">Participantes totales</p>
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <div class="card border-0 shadow-sm h-100 hover-lift" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%); box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);">
                <div class="card-body p-5 text-center">
                  <div class="fs-1 mb-3" style="color: #10b981;">
                    <i class="fas fa-check-circle"></i>
                  </div>
                  <div class="h2 fw-bold mb-1">{{ statistics.confirmed_participants }}</div>
                  <p class="text-muted">Confirmados ({{ confirmationRate }}%)</p>
                </div>
              </div>
            </div>

            <!-- Gráfico de distribución por rama -->
            <div class="col-12">
              <div class="card border-0 shadow-sm" style="backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.7) 100%);">
                <div class="card-body p-5">
                  <h6 class="card-title fw-bold mb-4">Distribución por Rama Scout</h6>
                  <div class="row g-4">
                    <div v-for="(count, rama) in statistics.by_rama" :key="rama" class="col-md-4">
                      <div class="text-center p-4" style="background-color: #f1f5f9; border-radius: 10px;">
                        <div class="h4 fw-bold mb-2" :style="getRamaColor(rama)">{{ count }}</div>
                        <p class="text-muted mb-0">{{ rama }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Carnets -->
        <div class="tab-pane fade" id="carnets" role="tabpanel">
          <div class="card border-0 shadow-sm" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95);">
            <div class="card-body p-5">
              <h5 class="card-title fw-bold mb-4">Generar y Gestionar Carnets</h5>
              
              <!-- Opciones de filtrado -->
              <div class="row mb-4 g-3">
                <div class="col-md-3">
                  <label class="form-label fw-600 text-dark">Rama</label>
                  <select v-model="carnetFilterRama" class="form-select" style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 10px 12px;">
                    <option value="">Todas las ramas</option>
                    <option value="Caminantes">Caminantes (15-18)</option>
                    <option value="Rovers">Rovers (18-22)</option>
                    <option value="Dirigente Joven">Dirigente Joven (22-25)</option>
                    <option value="Dirigente">Dirigente (25+)</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-600 text-dark">Estado</label>
                  <select v-model="carnetFilterConfirmed" class="form-select" style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 10px 12px;">
                    <option value="">Todos</option>
                    <option value="true">Confirmados</option>
                    <option value="false">No confirmados</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-600 text-dark">Buscar</label>
                  <input 
                    v-model="carnetSearchText" 
                    type="text" 
                    class="form-control" 
                    placeholder="Por nombre o NIS..."
                    style="border: 2px solid #e2e8f0; border-radius: 10px; padding: 10px 12px;"
                  >
                </div>
                <div class="col-md-3 d-flex align-items-end gap-2">
                  <button @click="printAllCarnets" class="btn btn-primary w-100" style="border-radius: 8px; padding: 10px 12px; font-weight: 600;">
                    <i class="fas fa-print me-2"></i>Imprimir Todo
                  </button>
                </div>
              </div>

              <!-- Carnets -->
              <div v-if="filteredCarnets.length > 0" class="carnets-container">
                <div class="row">
                  <div v-for="participant in filteredCarnets" :key="participant.id" class="col-md-6 col-lg-4 mb-4">
                    <div class="carnet-wrapper">
                      <ParticipantCard 
                        :participant="participant"
                        @click="openParticipantDetail(participant)"
                        style="cursor: pointer;"
                      />
                      <div class="carnet-actions">
                        <button 
                          @click="printCarnet(participant)" 
                          class="btn btn-sm btn-outline-primary"
                          title="Imprimir"
                        >
                          <i class="fas fa-print"></i> Imprimir
                        </button>
                        <button 
                          @click="downloadCarnetPDF(participant)" 
                          class="btn btn-sm btn-outline-success"
                          title="Descargar"
                        >
                          <i class="fas fa-download"></i> PDF
                        </button>
                        <button 
                          @click="openParticipantDetail(participant)" 
                          class="btn btn-sm btn-outline-info"
                          title="Ver detalles"
                        >
                          <i class="fas fa-eye"></i> Detalles
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                No hay participantes para mostrar. Carga participantes primero.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

      <!-- Modal de detalles del participante -->
      <ParticipantDetailModal 
        v-if="selectedParticipant"
        :participant="selectedParticipant"
        :is-open="showDetailModal"
        @close="closeParticipantDetail"
        @print="printParticipantDetail"
        @download="downloadParticipantPDF"
      />
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/Navbar.vue'
import ParticipantCard from '@/components/ParticipantCard.vue'
import ParticipantDetailModal from '@/components/ParticipantDetailModal.vue'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const authStore = useAuthStore()

// Verificar autenticación al montar
onMounted(async () => {
  // Si no hay usuario, intentar recuperarlo del token
  if (!authStore.user && authStore.token) {
    await authStore.fetchCurrentUser()
  }
})

// Estados del formulario de registro
const formData = ref({
  full_name: '',
  nis: '',
  email: '',
  rama: '',
  notes: ''
})

const formSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Estados de importación
const fileInput = ref(null)
const importFile = ref(null)
const isDragging = ref(false)
const isImporting = ref(false)
const importError = ref('')
const importResult = ref(null)

// Estados del listado
const participants = ref([])
const totalParticipants = ref(0)
const currentPage = ref(1)
const filterRama = ref('')
const filterConfirmed = ref('')
const searchText = ref('')
const isLoadingParticipants = ref(false)

// Estados de estadísticas
const statistics = ref({
  total_participants: 0,
  confirmed_participants: 0,
  by_rama: {},
  registration_rate: 0
})

// Estados de carnets
const carnetFilterRama = ref('')
const carnetFilterConfirmed = ref('')
const carnetSearchText = ref('')
const carnetsList = ref([])
const selectedParticipant = ref(null)
const showDetailModal = ref(false)

// Métodos del formulario
const submitForm = async () => {
  formSubmitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch('/api/v1/foro/participants', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(formData.value)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al registrar participante')
    }

    successMessage.value = '¡Participante registrado exitosamente!'
    resetForm()
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    formSubmitting.value = false
  }
}

const resetForm = () => {
  formData.value = {
    full_name: '',
    nis: '',
    email: '',
    rama: '',
    notes: ''
  }
  successMessage.value = ''
  errorMessage.value = ''
}

// Métodos de importación
const handleFileSelect = (event) => {
  importFile.value = event.target.files[0]
  importError.value = ''
  importResult.value = null
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  if (event.dataTransfer.files.length > 0) {
    importFile.value = event.dataTransfer.files[0]
  }
}

const submitImport = async () => {
  if (!importFile.value) return

  isImporting.value = true
  importError.value = ''
  importResult.value = null

  try {
    const formData = new FormData()
    formData.append('file', importFile.value)

    const response = await fetch('/api/v1/foro/import-xlsx', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al importar archivo')
    }

    const result = await response.json()
    importResult.value = result
    importFile.value = null
  } catch (error) {
    importError.value = error.message
  } finally {
    isImporting.value = false
  }
}

// Métodos del listado
const loadParticipants = async () => {
  if (isLoadingParticipants.value) return
  
  isLoadingParticipants.value = true
  try {
    const params = new URLSearchParams()
    params.append('skip', (currentPage.value - 1) * 100)
    params.append('limit', 100)
    if (filterRama.value) params.append('rama', filterRama.value)
    if (filterConfirmed.value !== '') params.append('is_confirmed', filterConfirmed.value === 'true')

    const response = await fetch(`/api/v1/foro/participants?${params}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) throw new Error('Error al cargar participantes')
    participants.value = await response.json()
    totalParticipants.value = participants.value.length
  } catch (error) {
    console.error('Error:', error)
  } finally {
    isLoadingParticipants.value = false
  }
}

// Métodos de estadísticas
const loadStatistics = async () => {
  try {
    const response = await fetch('/api/v1/foro/statistics', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) throw new Error('Error al cargar estadísticas')
    statistics.value = await response.json()
  } catch (error) {
    console.error('Error:', error)
  }
}

const editParticipant = (participant) => {
  // Placeholder para editar participante
  alert(`Editar: ${participant.full_name}`)
}

// Computados
const filteredParticipants = computed(() => {
  return participants.value.filter(p => {
    const matchRama = !filterRama.value || p.rama === filterRama.value
    const matchSearch = !searchText.value || 
      p.full_name.toLowerCase().includes(searchText.value.toLowerCase()) ||
      p.email.toLowerCase().includes(searchText.value.toLowerCase())
    return matchRama && matchSearch
  })
})

const confirmationRate = computed(() => {
  if (statistics.value.total_participants === 0) return 0
  return Math.round((statistics.value.confirmed_participants / statistics.value.total_participants) * 100)
})

// Filtrado de carnets
const filteredCarnets = computed(() => {
  return carnetsList.value.filter(p => {
    const matchRama = !carnetFilterRama.value || p.rama === carnetFilterRama.value
    const matchConfirmed = carnetFilterConfirmed.value === '' || 
      (carnetFilterConfirmed.value === 'true' ? p.is_confirmed : !p.is_confirmed)
    const matchSearch = !carnetSearchText.value || 
      p.full_name.toLowerCase().includes(carnetSearchText.value.toLowerCase()) ||
      p.nis.toLowerCase().includes(carnetSearchText.value.toLowerCase())
    return matchRama && matchConfirmed && matchSearch
  })
})

// Helper functions
const getBadgeColor = (rama) => {
  const colors = {
    'Caminantes': 'background: linear-gradient(135deg, #4b9ea6 0%, #2d6b74 100%); color: white;',
    'Rovers': 'background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;',
    'Dirigente Joven': 'background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white;',
    'Dirigente': 'background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); color: white;'
  }
  return colors[rama] || 'background-color: #e5e7eb; color: #4b5563;'
}

const getRamaColor = (rama) => {
  const colors = {
    'Caminantes': 'color: #4b9ea6;',
    'Rovers': 'color: #10b981;',
    'Dirigente Joven': 'color: #f97316;',
    'Dirigente': 'color: #a855f7;'
  }
  return colors[rama] || 'color: #4b5563;'
}

// Funciones de carnets
const loadCarnets = async () => {
  try {
    isLoadingParticipants.value = true
    const response = await fetch('/api/v1/foro/participants', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    if (!response.ok) throw new Error('Error cargando participantes')
    
    const data = await response.json()
    carnetsList.value = data.data || data
  } catch (error) {
    console.error('Error:', error)
    errorMessage.value = 'Error cargando los carnets'
  } finally {
    isLoadingParticipants.value = false
  }
}

const openParticipantDetail = (participant) => {
  selectedParticipant.value = participant
  showDetailModal.value = true
}

const closeParticipantDetail = () => {
  showDetailModal.value = false
  selectedParticipant.value = null
}

const printCarnet = (participant) => {
  const printWindow = window.open('', '', 'height=600,width=800')
  const carnetElement = document.querySelector(`[data-participant-id="${participant.id}"]`)
  
  if (!carnetElement) {
    alert('Error: No se puede encontrar el carnet')
    return
  }

  html2canvas(carnetElement, {
    backgroundColor: '#ffffff',
    scale: 2,
    allowTaint: true,
    useCORS: true
  }).then(canvas => {
    const imgData = canvas.toDataURL('image/png')
    printWindow.document.write(`
      <html>
        <head>
          <title>Imprimir Carnet - ${participant.full_name}</title>
          <style>
            body { margin: 0; padding: 20px; }
            img { max-width: 100%; height: auto; display: block; margin: auto; }
            @media print {
              body { margin: 0; padding: 0; }
              img { max-width: 100%; }
            }
          </style>
        </head>
        <body>
          <img src="${imgData}" />
        </body>
      </html>
    `)
    printWindow.document.close()
    setTimeout(() => printWindow.print(), 500)
  })
}

const downloadCarnetPDF = (participant) => {
  const carnetElement = document.querySelector(`[data-participant-id="${participant.id}"]`)
  
  if (!carnetElement) {
    alert('Error: No se puede encontrar el carnet')
    return
  }

  html2canvas(carnetElement, {
    backgroundColor: '#ffffff',
    scale: 2,
    allowTaint: true,
    useCORS: true
  }).then(canvas => {
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: [88, 55] // Tamaño de carnet estándar
    })
    
    const imgWidth = 88
    const imgHeight = 55
    
    pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight)
    pdf.save(`carnet-${participant.full_name.replace(/\s+/g, '_')}.pdf`)
  })
}

const printAllCarnets = () => {
  if (filteredCarnets.value.length === 0) {
    alert('No hay carnets para imprimir')
    return
  }

  const printWindow = window.open('', '', 'height=800,width=1000')
  let html = `
    <html>
      <head>
        <title>Imprimir Todos los Carnets</title>
        <style>
          body { margin: 10px; padding: 0; font-family: Arial, sans-serif; }
          .carnet-page { 
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 10px;
            text-align: center;
          }
          .carnet-page img { 
            max-width: 350px; 
            height: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
          }
          @media print {
            body { margin: 0; padding: 5px; }
            .carnet-page { margin-bottom: 5px; }
          }
        </style>
      </head>
      <body>
  `

  // Procesar cada carnet
  let processedCount = 0
  filteredCarnets.value.forEach((participant, index) => {
    const carnetElement = document.querySelector(`[data-participant-id="${participant.id}"]`)
    if (carnetElement) {
      html2canvas(carnetElement, {
        backgroundColor: '#ffffff',
        scale: 1.5,
        allowTaint: true,
        useCORS: true
      }).then(canvas => {
        const imgData = canvas.toDataURL('image/png')
        html += `
          <div class="carnet-page">
            <img src="${imgData}" alt="Carnet ${participant.full_name}" />
          </div>
        `
        processedCount++
        
        if (processedCount === filteredCarnets.value.length) {
          html += `
          </body>
        </html>
          `
          printWindow.document.write(html)
          printWindow.document.close()
          setTimeout(() => printWindow.print(), 500)
        }
      })
    }
  })
}

const downloadParticipantPDF = () => {
  if (!selectedParticipant.value) return
  
  const pdf = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  })

  const participant = selectedParticipant.value
  const pageWidth = pdf.internal.pageSize.getWidth()
  const pageHeight = pdf.internal.pageSize.getHeight()
  let yPos = 20

  // Header
  pdf.setFontSize(18)
  pdf.setFont(undefined, 'bold')
  pdf.text('Información del Participante', 15, yPos)
  yPos += 15

  // Divider
  pdf.setDrawColor(102, 126, 234)
  pdf.line(15, yPos, pageWidth - 15, yPos)
  yPos += 10

  // Información
  pdf.setFontSize(11)
  pdf.setFont(undefined, 'normal')

  const info = [
    [`Nombre:`, participant.full_name],
    [`NIS:`, participant.nis],
    [`Email:`, participant.email],
    [`Rama:`, participant.rama],
    [`Estado:`, participant.is_confirmed ? 'Confirmado' : 'No confirmado'],
    [`Registrado:`, new Date(participant.registration_date).toLocaleDateString('es-ES')],
    [`Notas:`, participant.notes || 'Sin notas']
  ]

  info.forEach(([label, value]) => {
    pdf.setFont(undefined, 'bold')
    pdf.text(label, 15, yPos)
    pdf.setFont(undefined, 'normal')
    const textWidth = pageWidth - 60
    const splitText = pdf.splitTextToSize(String(value), textWidth)
    pdf.text(splitText, 45, yPos)
    yPos += Math.max(7, splitText.length * 5) + 3
  })

  pdf.save(`participante-${participant.full_name.replace(/\s+/g, '_')}.pdf`)
}

const printParticipantDetail = () => {
  if (!selectedParticipant.value) return
  window.print()
}
</script>

<style scoped>
.hover-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(168, 85, 247, 0.15) !important;
}

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

/* Carnets Container */
.carnets-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.carnet-wrapper {
  position: relative;
  animation: slideDown 0.3s ease;
}

.carnet-wrapper:hover .carnet-actions {
  opacity: 1;
  visibility: visible;
}

.carnet-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0 0 12px 12px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 10;
}

.carnet-actions .btn {
  flex: 1;
  font-size: 12px;
  padding: 8px 10px;
  border-radius: 6px;
}

.btn-outline-primary {
  color: #667eea;
  border-color: #667eea;
}

.btn-outline-primary:hover {
  background-color: #667eea;
  color: white;
}

.btn-outline-success {
  color: #10b981;
  border-color: #10b981;
}

.btn-outline-success:hover {
  background-color: #10b981;
  color: white;
}

.btn-outline-info {
  color: #0891b2;
  border-color: #0891b2;
}

.btn-outline-info:hover {
  background-color: #0891b2;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .carnets-container {
    grid-template-columns: 1fr;
  }

  .carnet-actions {
    opacity: 1;
    visibility: visible;
    background: rgba(0, 0, 0, 0.9);
  }
}

@media print {
  .carnet-actions {
    display: none !important;
  }
}
</style>
