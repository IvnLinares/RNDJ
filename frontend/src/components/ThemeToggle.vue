<script setup>
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
</script>

<template>
  <button
    @click="themeStore.toggleTheme()"
    :class="['theme-toggle', { 'dark': themeStore.theme === 'dark' }]"
    :title="themeStore.theme === 'light' ? 'Cambiar a modo oscuro' : 'Cambiar a modo claro'"
    aria-label="Toggle theme"
  >
    <i class="fas fa-sun theme-icon theme-icon-sun"></i>
    <div class="theme-toggle-slider">
      <i :class="themeStore.theme === 'light' ? 'fas fa-sun' : 'fas fa-moon'"></i>
    </div>
    <i class="fas fa-moon theme-icon theme-icon-moon"></i>
  </button>
</template>
