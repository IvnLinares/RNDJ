<template>
  <!-- 🎨 EJEMPLO COMPLETO DE USO DEL DESIGN SYSTEM -->
  
  <div style="background-color: var(--bg-secondary); min-height: 100vh; padding: var(--spacing-8);">
    <div class="container">
      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 1: HEADER CON TÍTULO
           ═══════════════════════════════════════════════════════════════ -->
      
      <div class="card card-gradient mb-8" style="padding: var(--spacing-8);">
        <h1 style="color: white; font-size: var(--font-size-5xl); margin: 0;">
          🎨 Design System
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-size: var(--font-size-lg); margin: var(--spacing-4) 0 0 0;">
          Sistema de estilos unificado para RNDJ-Connect
        </p>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 2: ALERTAS
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          📢 Alertas
        </h2>
        
        <div style="display: grid; gap: var(--spacing-4);">
          <div class="alert alert-success">
            <div class="alert-icon">✅</div>
            <div class="alert-content">
              <div class="alert-title">¡Éxito!</div>
              <p style="margin: 0; font-size: var(--font-size-sm);">
                Tu operación se completó correctamente
              </p>
            </div>
          </div>

          <div class="alert alert-error">
            <div class="alert-icon">❌</div>
            <div class="alert-content">
              <div class="alert-title">Error</div>
              <p style="margin: 0; font-size: var(--font-size-sm);">
                Ocurrió un error al procesar tu solicitud
              </p>
            </div>
          </div>

          <div class="alert alert-warning">
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
              <div class="alert-title">Advertencia</div>
              <p style="margin: 0; font-size: var(--font-size-sm);">
                Debes revisar esta información
              </p>
            </div>
          </div>

          <div class="alert alert-info">
            <div class="alert-icon">ℹ️</div>
            <div class="alert-content">
              <div class="alert-title">Información</div>
              <p style="margin: 0; font-size: var(--font-size-sm);">
                Información importante que debes saber
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 3: BOTONES
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          🔘 Botones
        </h2>
        
        <div class="card p-8">
          <!-- Botones por color -->
          <div style="margin-bottom: var(--spacing-8);">
            <h4 style="margin-bottom: var(--spacing-4);">Variantes de Color</h4>
            <div style="display: flex; gap: var(--spacing-4); flex-wrap: wrap;">
              <button class="btn btn-primary">Primary</button>
              <button class="btn btn-secondary">Secondary</button>
              <button class="btn btn-success">Success</button>
              <button class="btn btn-danger">Danger</button>
              <button class="btn btn-outline">Outline</button>
              <button class="btn btn-ghost">Ghost</button>
            </div>
          </div>

          <!-- Botones por tamaño -->
          <div style="margin-bottom: var(--spacing-8);">
            <h4 style="margin-bottom: var(--spacing-4);">Tamaños</h4>
            <div style="display: flex; gap: var(--spacing-4); align-items: center;">
              <button class="btn btn-primary btn-sm">Pequeño</button>
              <button class="btn btn-primary">Normal</button>
              <button class="btn btn-primary btn-lg">Grande</button>
            </div>
          </div>

          <!-- Botones deshabilitados -->
          <div>
            <h4 style="margin-bottom: var(--spacing-4);">Estados</h4>
            <div style="display: flex; gap: var(--spacing-4);">
              <button class="btn btn-primary" disabled>Deshabilitado</button>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 4: TARJETAS
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          📦 Tarjetas
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--spacing-6);">
          <!-- Tarjeta Simple -->
          <div class="card">
            <div class="card-header">
              <h3>Tarjeta Simple</h3>
            </div>
            <div class="card-body">
              <p style="margin: 0;">
                Esta es una tarjeta básica con header, body y footer.
              </p>
            </div>
            <div class="card-footer">
              <button class="btn btn-outline btn-sm">Cancelar</button>
              <button class="btn btn-primary btn-sm">Aceptar</button>
            </div>
          </div>

          <!-- Tarjeta Elevada -->
          <div class="card card-elevated">
            <div class="card-header">
              <h3>Tarjeta Elevada</h3>
            </div>
            <div class="card-body">
              <p style="margin: 0;">
                Esta tarjeta tiene una sombra más pronunciada.
              </p>
            </div>
            <div class="card-footer">
              <button class="btn btn-primary btn-sm">Más info</button>
            </div>
          </div>

          <!-- Tarjeta Gradiente -->
          <div class="card card-gradient">
            <h3 style="margin: 0; color: white;">Tarjeta Gradiente</h3>
            <p style="margin: var(--spacing-2) 0 0 0; color: rgba(255,255,255,0.9);">
              Con fondo degradado automático.
            </p>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 5: FORMULARIOS
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          📋 Formularios
        </h2>
        
        <div class="card">
          <div class="card-header">
            <h3>Formulario de Ejemplo</h3>
          </div>
          
          <div class="card-body">
            <form style="display: grid; gap: var(--spacing-6);">
              <!-- Input de texto -->
              <div class="form-group">
                <label class="form-label">Nombre Completo</label>
                <input 
                  type="text" 
                  class="form-input" 
                  placeholder="Tu nombre completo"
                  value="Juan Pérez"
                >
                <div class="form-helper">Ingresa tu nombre completo</div>
              </div>

              <!-- Input de email -->
              <div class="form-group">
                <label class="form-label">Email</label>
                <input 
                  type="email" 
                  class="form-input" 
                  placeholder="tu@email.com"
                  value="juan@scouts.com"
                >
              </div>

              <!-- Select -->
              <div class="form-group">
                <label class="form-label">Rango Scout</label>
                <select class="form-select">
                  <option>Seleccionar...</option>
                  <option selected>Scout</option>
                  <option>Guía</option>
                  <option>Pionero</option>
                  <option>Rover</option>
                </select>
              </div>

              <!-- Textarea -->
              <div class="form-group">
                <label class="form-label">Descripción</label>
                <textarea 
                  class="form-textarea" 
                  placeholder="Cuéntanos más sobre ti..."
                >Soy un Scout apasionado por la naturaleza</textarea>
              </div>

              <!-- Con validación de error -->
              <div class="form-group">
                <label class="form-label">Campo con Error</label>
                <input 
                  type="text" 
                  class="form-input" 
                  placeholder="Este campo tiene error"
                >
                <div class="form-error">Este campo es obligatorio</div>
              </div>
            </form>
          </div>

          <div class="card-footer">
            <button class="btn btn-outline">Cancelar</button>
            <button class="btn btn-primary">Guardar</button>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 6: BADGES
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          🏷️ Badges
        </h2>
        
        <div class="card p-8">
          <div style="display: flex; gap: var(--spacing-4); flex-wrap: wrap;">
            <span class="badge badge-primary">Primary</span>
            <span class="badge badge-success">Activo</span>
            <span class="badge badge-danger">Inactivo</span>
            <span class="badge badge-warning">Pendiente</span>
            <span class="badge badge-primary">Scout</span>
            <span class="badge badge-success">Verificado</span>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 7: ANIMACIONES
           ═══════════════════════════════════════════════════════════════ -->
      
      <section class="mb-12">
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          ✨ Animaciones
        </h2>
        
        <div class="card p-8">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--spacing-8);">
            <div 
              class="animate-fadeIn"
              style="background: linear-gradient(135deg, var(--color-primary), var(--color-secondary)); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              fadeIn
            </div>

            <div 
              class="animate-slideInLeft"
              style="background: var(--color-success); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              slideInLeft
            </div>

            <div 
              class="animate-slideInRight"
              style="background: var(--color-warning); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              slideInRight
            </div>

            <div 
              class="animate-slideInUp"
              style="background: var(--color-danger); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              slideInUp
            </div>

            <div 
              class="animate-pulse"
              style="background: var(--color-accent); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              pulse
            </div>

            <div 
              class="animate-bounce"
              style="background: var(--color-info); color: white; padding: var(--spacing-6); border-radius: var(--radius-lg); text-align: center;"
            >
              bounce
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════════════
           SECCIÓN 8: PALETA DE COLORES
           ═══════════════════════════════════════════════════════════════ -->
      
      <section>
        <h2 style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-6);">
          🎨 Paleta de Colores
        </h2>
        
        <div class="card p-8">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--spacing-4);">
            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-primary); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Primary</small>
            </div>
            
            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-secondary); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Secondary</small>
            </div>

            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-success); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Success</small>
            </div>

            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-danger); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Danger</small>
            </div>

            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-warning); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Warning</small>
            </div>

            <div style="text-align: center;">
              <div style="width: 100%; height: 80px; background-color: var(--color-accent); border-radius: var(--radius-lg); margin-bottom: var(--spacing-2);"></div>
              <small style="color: var(--color-gray-600);">Accent</small>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// Este componente es solo demostrativo
// Muestra todos los componentes y estilos disponibles en el Design System
</script>

<style scoped>
/* Estilos locales opcionales */
section {
  animation: fadeIn var(--transition-base);
}
</style>
