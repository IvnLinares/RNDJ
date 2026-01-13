<template>
  <div class="participant-carnet-container" ref="cardElement">
    <!-- Carnet - Estilo Profesional -->
    <div class="carnet-wrapper" :class="{ flipped: isFlipped }">
      <!-- FRENTE DEL CARNET -->
      <div class="carnet-front" v-if="!isFlipped">
        <div class="carnet-card">
          <!-- Decoración izquierda superior -->
          <div class="carnet-wave-top"></div>
          
          <!-- Contenido Frente -->
          <div class="carnet-content">
            <!-- Logo y Header -->
            <div class="carnet-logo-section">
              <div class="carnet-logo" :style="{ background: primaryRamaColor }">
                <span class="logo-text">RNDJ</span>
              </div>
              <div class="carnet-title-small">5to Foro</div>
            </div>

            <!-- Foto del participante -->
            <div class="carnet-photo-section">
              <div class="carnet-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            </div>

            <!-- Información del Participante -->
            <div class="carnet-info-section">
              <h3 class="carnet-name">{{ participant.full_name }}</h3>
              
              <div class="carnet-rama-badge" :style="{ background: primaryRamaColor }">
                {{ participant.rama }}
              </div>

              <div class="carnet-detail-row">
                <span class="detail-label">NIS:</span>
                <span class="detail-value">{{ participant.nis }}</span>
              </div>

              <div class="carnet-detail-row">
                <span class="detail-label">Email:</span>
                <span class="detail-value email-small">{{ participant.email }}</span>
              </div>
            </div>

            <!-- Fecha de validez -->
            <div class="carnet-footer-section">
              <div class="validity-date">
                <span class="date-label">Válido hasta:</span>
                <span class="date-value">{{ formatDateShort(new Date(new Date().getFullYear() + 1, 11, 31)) }}</span>
              </div>
            </div>
          </div>

          <!-- Decoración derecha inferior -->
          <div class="carnet-wave-bottom"></div>
        </div>
      </div>

      <!-- REVERSO DEL CARNET -->
      <div class="carnet-back" v-else>
        <div class="carnet-card carnet-back-card">
          <!-- Decoración izquierda -->
          <div class="carnet-wave-top"></div>

          <!-- Contenido Reverso -->
          <div class="carnet-content-back">
            <!-- QR Code -->
            <div class="carnet-qr-section">
              <qrcode-vue
                :value="qrValue"
                :options="qrOptions"
                tag="div"
                class="carnet-qr-code"
              />
            </div>

            <!-- Información de Advertencia -->
            <div class="carnet-info-back">
              <h5 class="info-back-title">Información</h5>
              <p class="info-back-text">
                Este carnet es personal e intransferible, el uso inadecuado de este documento es responsabilidad del titular.
              </p>

              <!-- Datos de contacto/ubicación -->
              <div class="carnet-contact-info">
                <div class="contact-row">
                  <span class="contact-label">Foro:</span>
                  <span class="contact-value">5to Foro Nacional 2026</span>
                </div>
                <div class="contact-row" v-if="participant.notes">
                  <span class="contact-label">Notas:</span>
                  <span class="contact-value">{{ truncateText(participant.notes, 30) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Decoración derecha -->
          <div class="carnet-wave-bottom"></div>
        </div>
      </div>
    </div>
    <!-- Botones de Acción -->
    <div class="carnet-button-section">
      <button 
        class="btn-action btn-flip"
        @click="toggleFlip"
        title="Voltear carnet"
      >
        <i class="fas fa-repeat"></i> Voltear
      </button>
      
      <button 
        class="btn-action btn-download"
        @click="downloadCard"
        :disabled="isDownloading"
        title="Descargar frente y reverso"
      >
        <i class="fas fa-download"></i> 
        {{ isDownloading ? 'Descargando...' : 'Descargar Ambos' }}
      </button>

      <button 
        class="btn-action btn-print"
        @click="printCard"
        title="Imprimir carnet"
      >
        <i class="fas fa-print"></i> Imprimir
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import QrcodeVue from 'qrcode.vue'
import html2canvas from 'html2canvas'

const props = defineProps({
  participant: {
    type: Object,
    required: true
  }
})

const isFlipped = ref(false)
const cardElement = ref(null)
const isDownloading = ref(false)

const ramaColors = {
  'Caminantes': '#4b9ea6',
  'Rovers': '#10b981',
  'Dirigente Joven': '#f97316',
  'Dirigente': '#a855f7'
}

const primaryRamaColor = computed(() => {
  return ramaColors[props.participant.rama] || '#4b9ea6'
})

const qrValue = computed(() => {
  return `${window.location.origin}/foro/participant/${props.participant.id}`
})

const qrOptions = {
  errorCorrectionLevel: 'H',
  type: 'image/png',
  quality: 0.95,
  width: 140,
  margin: 0,
  color: {
    dark: '#000000',
    light: '#FFFFFF'
  }
}

const toggleFlip = () => {
  isFlipped.value = !isFlipped.value
}

const formatDateShort = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('es-ES', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit'
  })
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const downloadCard = async () => {
  try {
    isDownloading.value = true
    
    // Obtener el wrapper y remover temporalmente la transformación
    const wrapper = cardElement.value.querySelector('.carnet-wrapper')
    const originalTransform = wrapper.style.transform
    const wasFlipped = isFlipped.value
    
    // Asegurar que no esté volteado
    isFlipped.value = false
    wrapper.style.transform = 'none'
    
    // Pequeña pausa para que el navegador procese el cambio
    await new Promise(resolve => setTimeout(resolve, 150))

    // Capturar el FRENTE
    const frontElement = cardElement.value.querySelector('.carnet-front')
    const canvasFront = await html2canvas(frontElement, {
      backgroundColor: '#ffffff',
      scale: 3,
      logging: false,
      useCORS: true,
      allowTaint: true,
      imageTimeout: 0
    })

    // Ahora voltear para capturar el REVERSO
    isFlipped.value = true
    await new Promise(resolve => setTimeout(resolve, 150))

    const backElement = cardElement.value.querySelector('.carnet-back')
    const canvasBack = await html2canvas(backElement, {
      backgroundColor: '#ffffff',
      scale: 3,
      logging: false,
      useCORS: true,
      allowTaint: true,
      imageTimeout: 0
    })

    // Restaurar estado original
    isFlipped.value = wasFlipped
    wrapper.style.transform = originalTransform

    // Crear un canvas combinado (lado a lado)
    const combinedCanvas = document.createElement('canvas')
    const ctx = combinedCanvas.getContext('2d')
    
    // Dimensiones: colocar ambos carnets lado a lado con separación
    const gap = 60 // Espacio entre carnets
    const padding = 40 // Margen alrededor
    combinedCanvas.width = canvasFront.width + canvasBack.width + gap + (padding * 2)
    combinedCanvas.height = Math.max(canvasFront.height, canvasBack.height) + (padding * 2)
    
    // Fondo blanco
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, combinedCanvas.width, combinedCanvas.height)
    
    // Dibujar frente
    ctx.drawImage(canvasFront, padding, padding)
    
    // Dibujar reverso
    ctx.drawImage(canvasBack, canvasFront.width + gap + padding, padding)
    
    // Agregar etiquetas
    ctx.fillStyle = '#666666'
    ctx.font = 'bold 36px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('FRENTE', canvasFront.width / 2 + padding, padding - 10)
    ctx.fillText('REVERSO', canvasFront.width + gap + padding + canvasBack.width / 2, padding - 10)
    
    // Convertir a blob y descargar
    combinedCanvas.toBlob((blob) => {
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      const timestamp = new Date().toISOString().split('T')[0]
      link.download = `carnet-completo-${props.participant.nis}-${timestamp}.png`
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }, 'image/png')
  } catch (error) {
    console.error('Error al descargar el carnet:', error)
    alert('Error al descargar el carnet. Intenta de nuevo.')
  } finally {
    isDownloading.value = false
  }
}

const printCard = async () => {
  try {
    // Seleccionar el elemento del carnet
    const carnetElement = isFlipped.value 
      ? cardElement.value.querySelector('.carnet-back')
      : cardElement.value.querySelector('.carnet-front')
    
    if (!carnetElement) {
      console.error('No se encontró el elemento del carnet')
      return
    }

    // Crear una ventana de impresión
    const printWindow = window.open('', '_blank')
    
    const htmlContent = `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Imprimir Carnet</title>
          <style>
            body {
              margin: 0;
              padding: 20px;
              background: white;
              font-family: Arial, sans-serif;
            }
            @media print {
              body {
                margin: 0;
                padding: 0;
              }
            }
          </style>
        </head>
        <body>
          ${carnetElement.outerHTML}
        </body>
      </html>
    `
    
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    
    // Esperar a que el documento cargue antes de imprimir
    setTimeout(() => {
      printWindow.print()
    }, 250)
  } catch (error) {
    console.error('Error al imprimir el carnet:', error)
  }
}
</script>

<style scoped>
.participant-carnet-container {
  width: 100%;
  max-width: 500px;
  margin: 20px auto;
  perspective: 1200px;
}

.carnet-wrapper {
  width: 100%;
  height: 320px;
  position: relative;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.carnet-wrapper.flipped {
  transform: rotateY(180deg);
}

.carnet-front,
.carnet-back {
  width: 100%;
  height: 100%;
  position: absolute;
  backface-visibility: hidden;
}

.carnet-back {
  transform: rotateY(180deg);
}

.carnet-card {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Estilos para descarga/impresión */
@media print, (max-width: 0px) {
  .carnet-card {
    box-shadow: none;
  }
}

.carnet-wave-top {
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: v-bind(primaryRamaColor);
  border-radius: 50%;
  opacity: 0.15;
  pointer-events: none;
}

.carnet-wave-bottom {
  position: absolute;
  bottom: -80px;
  left: -80px;
  width: 250px;
  height: 250px;
  background: v-bind(primaryRamaColor);
  border-radius: 50%;
  opacity: 0.1;
  pointer-events: none;
}

/* FRENTE DEL CARNET */
.carnet-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 30px 25px;
  position: relative;
  z-index: 1;
  justify-content: space-between;
}

.carnet-logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.carnet-logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.carnet-logo-text {
  font-size: 11px;
  color: #999;
  font-weight: 600;
  margin-top: 4px;
}

.carnet-photo-section {
  display: flex;
  justify-content: center;
  margin: 15px 0;
}

.carnet-photo-placeholder {
  width: 100px;
  height: 120px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e5e7eb;
  color: #d1d5db;
  font-size: 40px;
}

.carnet-info-section {
  text-align: center;
}

.carnet-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 10px 0 12px 0;
  line-height: 1.2;
}

.carnet-rama-badge {
  display: inline-block;
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.carnet-detail-row {
  display: flex;
  justify-content: center;
  gap: 8px;
  font-size: 11px;
  margin: 5px 0;
}

.detail-label {
  font-weight: 700;
  color: #666;
  min-width: 35px;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

.email-small {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.carnet-footer-section {
  text-align: center;
  margin-top: 15px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.validity-date {
  display: flex;
  justify-content: center;
  gap: 6px;
  font-size: 10px;
}

.date-label {
  color: #999;
  font-weight: 600;
}

.date-value {
  color: #333;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

/* REVERSO DEL CARNET */
.carnet-back-card {
  padding: 20px;
}

.carnet-content-back {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  gap: 15px;
}

.carnet-qr-section {
  display: flex;
  justify-content: center;
  padding: 10px;
}

.carnet-qr-code {
  padding: 6px;
  background: white;
  border-radius: 8px;
  border: 2px solid #f3f4f6;
}

.carnet-info-back {
  background: linear-gradient(135deg, rgba(248, 249, 250, 0.8) 0%, rgba(243, 244, 246, 0.8) 100%);
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid v-bind(primaryRamaColor);
}

.info-back-title {
  font-size: 12px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-back-text {
  font-size: 10px;
  line-height: 1.4;
  color: #555;
  margin: 0 0 8px 0;
}

.carnet-contact-info {
  font-size: 9px;
}

.contact-row {
  display: flex;
  gap: 6px;
  margin: 3px 0;
  align-items: flex-start;
}

.contact-label {
  font-weight: 700;
  color: #666;
  min-width: 40px;
}

.contact-value {
  color: #333;
  flex: 1;
}

/* Botones de Acción */
.carnet-button-section {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.btn-action {
  border: none;
  color: white;
  padding: 10px 16px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-action i {
  font-size: 14px;
}

.btn-flip {
  background: linear-gradient(135deg, v-bind(primaryRamaColor) 0%, rgba(75, 158, 166, 0.8) 100%);
}

.btn-flip:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.btn-download {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.btn-download:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.btn-print {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.btn-print:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.btn-action:active:not(:disabled) {
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
  .participant-carnet-container {
    max-width: 100%;
    padding: 0 10px;
  }

  .carnet-card {
    border-radius: 12px;
  }

  .carnet-content {
    padding: 25px 20px;
  }

  .carnet-name {
    font-size: 15px;
  }

  .carnet-photo-placeholder {
    width: 90px;
    height: 110px;
    font-size: 35px;
  }
}

@media print {
  .btn-flip,
  .carnet-button-section {
    display: none !important;
  }
}
</style>
