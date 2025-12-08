const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const createWebSocket = (roomId, token, onMessage) => {
  const ws = new WebSocket(`${WS_BASE_URL}/api/v1/chat/ws/${roomId}?token=${token}`)

  ws.onopen = () => {
    console.log('WebSocket conectado')
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (onMessage) {
        onMessage(data)
      }
    } catch (error) {
      console.error('Error al parsear mensaje:', error)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  ws.onclose = () => {
    console.log('WebSocket desconectado')
  }

  return ws
}
