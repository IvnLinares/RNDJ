import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const login = async (credentials) => {
    isLoading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      token.value = response.data.access_token
      localStorage.setItem('token', token.value)
      
      // Obtener información del usuario
      await fetchCurrentUser()
      
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al iniciar sesión'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    error.value = null

    try {
      await api.post('/auth/register', userData)
      
      // Auto-login después del registro
      return await login({
        username: userData.username,
        password: userData.password
      })
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al registrarse'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    if (!token.value) return

    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (err) {
      console.error('Error obteniendo usuario:', err)
      logout()
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const checkAuth = async () => {
    if (token.value) {
      await fetchCurrentUser()
    }
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
    fetchCurrentUser
  }
})
