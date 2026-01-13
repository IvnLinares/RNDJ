<template>
  <teleport to="body" v-if="isOpen">
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <!-- Close Button -->
        <button class="btn-close-modal" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>

        <div class="participant-detail">
          <!-- Header -->
          <div class="detail-header" :style="{ background: ramaGradient }">
            <div class="rama-info">
              <span class="rama-emoji">{{ getRamaEmoji() }}</span>
              <div class="rama-text">
                <h2>{{ participant.full_name }}</h2>
                <p class="rama-label">{{ participant.rama }}</p>
              </div>
            </div>
            <div class="confirmed-badge" v-if="participant.is_confirmed">
              <i class="fas fa-check-circle"></i> Confirmado
            </div>
          </div>

          <!-- Content Tabs -->
          <div class="detail-tabs">
            <button
              v-for="tab in tabs"
              :key="tab"
              :class="['tab-btn', { active: activeTab === tab }]"
              @click="activeTab = tab"
            >
              <i :class="getTabIcon(tab)"></i> {{ tab }}
            </button>
          </div>

          <!-- Tab Content -->
          <div class="detail-body">
            <!-- Información General -->
            <div v-show="activeTab === 'Información'" class="tab-content">
              <div class="info-grid">
                <div class="info-item">
                  <span class="label">🆔 NIS (ID Scout)</span>
                  <span class="value">{{ participant.nis }}</span>
                </div>
                <div class="info-item">
                  <span class="label">📧 Email</span>
                  <span class="value">
                    <a :href="`mailto:${participant.email}`">{{ participant.email }}</a>
                  </span>
                </div>
                <div class="info-item">
                  <span class="label">🏕️ Rama</span>
                  <span class="value">
                    <span class="rama-badge" :style="{ background: ramaColor }">
                      {{ participant.rama }}
                    </span>
                  </span>
                </div>
                <div class="info-item">
                  <span class="label">📅 Registrado</span>
                  <span class="value">{{ formatDate(participant.registration_date) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">⏰ Actualizado</span>
                  <span class="value">{{ formatDate(participant.updated_date) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">🔢 ID Sistema</span>
                  <span class="value mono">{{ participant.id }}</span>
                </div>
              </div>
            </div>

            <!-- Notas -->
            <div v-show="activeTab === 'Notas'" class="tab-content">
              <div class="notes-section">
                <div v-if="participant.notes" class="notes-content">
                  {{ participant.notes }}
                </div>
                <div v-else class="no-data">
                  <i class="fas fa-sticky-note"></i>
                  <p>Sin notas registradas</p>
                </div>
              </div>
            </div>

            <!-- Documentos -->
            <div v-show="activeTab === 'Documentos'" class="tab-content">
              <div class="documents-grid">
                <div class="doc-item" :class="{ 'has-file': participant.medical_file }">
                  <div class="doc-icon">
                    <i class="fas fa-file-medical"></i>
                  </div>
                  <div class="doc-info">
                    <h4>Ficha Médica</h4>
                    <p v-if="participant.medical_file" class="status success">
                      <i class="fas fa-check-circle"></i> Adjunto
                    </p>
                    <p v-else class="status pending">
                      <i class="fas fa-clock"></i> Pendiente
                    </p>
                  </div>
                  <button
                    v-if="participant.medical_file"
                    class="btn-download"
                    @click="downloadFile(participant.id, 'medical-file')"
                    title="Descargar"
                  >
                    <i class="fas fa-download"></i>
                  </button>
                </div>

                <div class="doc-item" :class="{ 'has-file': participant.grow_together_cert }">
                  <div class="doc-icon">
                    <i class="fas fa-scroll"></i>
                  </div>
                  <div class="doc-info">
                    <h4>Crecer Juntos</h4>
                    <p v-if="participant.grow_together_cert" class="status success">
                      <i class="fas fa-check-circle"></i> Adjunto
                    </p>
                    <p v-else class="status pending">
                      <i class="fas fa-clock"></i> Pendiente
                    </p>
                  </div>
                  <button
                    v-if="participant.grow_together_cert"
                    class="btn-download"
                    @click="downloadFile(participant.id, 'grow-together-cert')"
                    title="Descargar"
                  >
                    <i class="fas fa-download"></i>
                  </button>
                </div>

                <div class="doc-item" :class="{ 'has-file': participant.safe_from_harm_cert }">
                  <div class="doc-icon">
                    <i class="fas fa-shield-alt"></i>
                  </div>
                  <div class="doc-info">
                    <h4>Safe from Harm</h4>
                    <p v-if="participant.safe_from_harm_cert" class="status success">
                      <i class="fas fa-check-circle"></i> Adjunto
                    </p>
                    <p v-else class="status pending">
                      <i class="fas fa-clock"></i> Pendiente
                    </p>
                  </div>
                  <button
                    v-if="participant.safe_from_harm_cert"
                    class="btn-download"
                    @click="downloadFile(participant.id, 'safe-from-harm-cert')"
                    title="Descargar"
                  >
                    <i class="fas fa-download"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- QR -->
            <div v-show="activeTab === 'QR'" class="tab-content qr-tab">
              <div class="qr-display">
                <qrcode-vue
                  :value="qrValue"
                  :options="qrOptions"
                  tag="div"
                  class="qr-large"
                />
                <p class="qr-text">Escanea este código QR para acceder a los detalles</p>
                <code class="qr-url">{{ qrValue }}</code>
              </div>
            </div>
          </div>

          <!-- Footer Actions -->
          <div class="detail-footer">
            <button class="btn btn-secondary" @click="closeModal">
              <i class="fas fa-times"></i> Cerrar
            </button>
            <button class="btn btn-primary" @click="printParticipant">
              <i class="fas fa-print"></i> Imprimir Carnet
            </button>
            <button class="btn btn-success" @click="downloadCarnet">
              <i class="fas fa-download"></i> Descargar PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import QrcodeVue from 'qrcode.vue'

const props = defineProps({
  participant: {
    type: Object,
    default: null
  },
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'print', 'download'])

const activeTab = ref('Información')
const tabs = ['Información', 'Notas', 'Documentos', 'QR']

const ramaColors = {
  'Caminantes': '#4b9ea6',
  'Rovers': '#10b981',
  'Dirigente Joven': '#f97316',
  'Dirigente': '#a855f7'
}

const ramaGradient = computed(() => {
  const color = ramaColors[props.participant?.rama] || '#667eea'
  return `linear-gradient(135deg, ${color}, ${color}dd)`
})

const ramaColor = computed(() => {
  return ramaColors[props.participant?.rama] || '#667eea'
})

const qrValue = computed(() => {
  return `${window.location.origin}/foro/participant/${props.participant?.id}`
})

const qrOptions = {
  errorCorrectionLevel: 'H',
  type: 'image/png',
  quality: 0.95,
  width: 300,
  margin: 2,
  color: {
    dark: '#000000',
    light: '#FFFFFF'
  }
}

const closeModal = () => {
  emit('close')
}

const getRamaEmoji = () => {
  const emojis = {
    'Caminantes': '🏔️',
    'Rovers': '🧭',
    'Dirigente Joven': '⚜️',
    'Dirigente': '🎖️'
  }
  return emojis[props.participant?.rama] || '👤'
}

const getTabIcon = (tab) => {
  const icons = {
    'Información': 'fas fa-info-circle',
    'Notas': 'fas fa-sticky-note',
    'Documentos': 'fas fa-file-pdf',
    'QR': 'fas fa-qrcode'
  }
  return icons[tab] || 'fas fa-circle'
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const downloadFile = async (participantId, fileType) => {
  try {
    const response = await fetch(
      `/api/v1/foro/participants/${participantId}/${fileType}`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }
    )

    if (!response.ok) throw new Error('Error descargando archivo')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.participant.full_name}-${fileType}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    a.remove()
  } catch (error) {
    console.error('Error:', error)
    alert('Error descargando archivo')
  }
}

const printParticipant = () => {
  emit('print')
}

const downloadCarnet = () => {
  emit('download')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.btn-close-modal {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: #333;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.2s ease;
}

.btn-close-modal:hover {
  background: rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

/* Detail Header */
.detail-header {
  padding: 24px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.rama-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.rama-emoji {
  font-size: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

.rama-text h2 {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 700;
}

.rama-label {
  margin: 0;
  font-size: 12px;
  font-weight: 500;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.confirmed-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  backdrop-filter: blur(10px);
}

/* Tabs */
.detail-tabs {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(248, 249, 250, 0.5);
  padding: 0;
  overflow-x: auto;
}

.tab-btn {
  flex: 1;
  padding: 14px 16px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #666;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  white-space: nowrap;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.tab-btn:hover {
  color: #333;
  background: rgba(0, 0, 0, 0.02);
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

/* Body Content */
.detail-body {
  padding: 24px;
}

.tab-content {
  animation: fadeIn 0.2s ease;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-item .label {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.info-item .value {
  font-size: 14px;
  color: #333;
  word-break: break-all;
}

.info-item a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.2s;
}

.info-item a:hover {
  color: #5568d3;
  text-decoration: underline;
}

.rama-badge {
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  width: fit-content;
}

.mono {
  font-family: 'Courier New', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

/* Notes */
.notes-section {
  min-height: 200px;
}

.notes-content {
  background: rgba(248, 249, 250, 0.5);
  padding: 16px;
  border-radius: 8px;
  line-height: 1.6;
  color: #333;
  word-break: break-word;
  border-left: 4px solid #667eea;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #999;
  gap: 12px;
}

.no-data i {
  font-size: 48px;
  opacity: 0.5;
}

.no-data p {
  margin: 0;
  font-size: 14px;
}

/* Documents */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.doc-item.has-file {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.3);
}

.doc-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.doc-item.has-file .doc-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.doc-info {
  flex: 1;
}

.doc-info h4 {
  margin: 0 0 4px 0;
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.status {
  margin: 0;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status.success {
  color: #10b981;
  font-weight: 500;
}

.status.pending {
  color: #f59e0b;
  font-weight: 500;
}

.btn-download {
  background: none;
  border: 1px solid rgba(0, 0, 0, 0.2);
  color: #667eea;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.btn-download:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* QR Tab */
.qr-tab {
  display: flex;
  justify-content: center;
}

.qr-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 8px;
}

.qr-large {
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.qr-text {
  margin: 0;
  color: #666;
  font-size: 13px;
  text-align: center;
}

.qr-url {
  display: block;
  background: rgba(0, 0, 0, 0.05);
  padding: 12px;
  border-radius: 6px;
  font-size: 11px;
  color: #666;
  word-break: break-all;
  text-align: center;
  font-family: 'Courier New', monospace;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Footer */
.detail-footer {
  padding: 16px 24px;
  background: rgba(248, 249, 250, 0.5);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
  min-width: 120px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.btn-secondary {
  background: rgba(0, 0, 0, 0.05);
  color: #333;
}

.btn-secondary:hover {
  background: rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 10px;
  }

  .detail-header {
    flex-direction: column;
    gap: 12px;
  }

  .rama-info {
    width: 100%;
  }

  .confirmed-badge {
    width: 100%;
    justify-content: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .detail-tabs {
    overflow-x: auto;
  }

  .tab-btn {
    font-size: 12px;
    padding: 12px 12px;
  }

  .documents-grid {
    grid-template-columns: 1fr;
  }

  .detail-footer {
    flex-direction: column;
  }

  .btn {
    min-width: 100%;
  }
}

/* Scrollbar */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

.modal-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>
