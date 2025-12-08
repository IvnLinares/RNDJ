import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useUserStore = defineStore('user', () => {
  const users = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchUsers = async (skip = 0, limit = 100) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.get('/users/', {
        params: { skip, limit }
      })
      users.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar usuarios'
    } finally {
      isLoading.value = false
    }
  }

  const getUserById = async (userId) => {
    try {
      const response = await api.get(`/users/${userId}`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar usuario'
      return null
    }
  }

  const updateUser = async (userData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.put('/users/me', userData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al actualizar usuario'
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    users,
    isLoading,
    error,
    fetchUsers,
    getUserById,
    updateUser
  }
})
