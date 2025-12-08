import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { createWebSocket } from '@/services/websocket'

export const useChatStore = defineStore('chat', () => {
  const rooms = ref([])
  const currentRoom = ref(null)
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const ws = ref(null)

  const fetchRooms = async () => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.get('/chat/rooms')
      rooms.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar salas'
    } finally {
      isLoading.value = false
    }
  }

  const fetchMessages = async (roomId, skip = 0, limit = 100) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.get(`/chat/rooms/${roomId}/messages`, {
        params: { skip, limit }
      })
      messages.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar mensajes'
    } finally {
      isLoading.value = false
    }
  }

  const createRoom = async (roomData) => {
    try {
      const response = await api.post('/chat/rooms', roomData)
      rooms.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al crear sala'
      return null
    }
  }

  const connectToRoom = (roomId, token, onMessage) => {
    ws.value = createWebSocket(roomId, token, onMessage)
    return ws.value
  }

  const sendMessage = (content) => {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      ws.value.send(content)
    }
  }

  const disconnectFromRoom = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  const setCurrentRoom = (room) => {
    currentRoom.value = room
  }

  return {
    rooms,
    currentRoom,
    messages,
    isLoading,
    error,
    fetchRooms,
    fetchMessages,
    createRoom,
    connectToRoom,
    sendMessage,
    disconnectFromRoom,
    setCurrentRoom
  }
})
