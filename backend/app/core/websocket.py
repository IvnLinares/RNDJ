from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import logging
import json

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Gestor de conexiones WebSocket para chat en tiempo real"""
    
    def __init__(self):
        # Diccionario: room_id -> Set de WebSockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Diccionario: WebSocket -> user_id
        self.user_connections: Dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Conectar un usuario a una sala de chat"""
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        
        self.active_connections[room_id].add(websocket)
        self.user_connections[websocket] = user_id
        
        logger.info(f"👤 Usuario {user_id} conectado a sala {room_id}")
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        """Desconectar un usuario de una sala"""
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            
            # Eliminar sala si está vacía
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
        
        user_id = self.user_connections.pop(websocket, None)
        logger.info(f"👋 Usuario {user_id} desconectado de sala {room_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Enviar mensaje a una conexión específica"""
        await websocket.send_text(message)
    
    async def broadcast_to_room(self, message: dict, room_id: str, exclude: WebSocket = None):
        """
        Enviar mensaje a todos los usuarios de una sala
        
        Args:
            message: Diccionario con el mensaje a enviar
            room_id: ID de la sala
            exclude: WebSocket a excluir (ej: el emisor)
        """
        if room_id not in self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections[room_id]:
            if connection != exclude:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    logger.error(f"Error enviando mensaje: {e}")
                    disconnected.append(connection)
        
        # Limpiar conexiones fallidas
        for conn in disconnected:
            self.disconnect(conn, room_id)
    
    def get_room_users_count(self, room_id: str) -> int:
        """Obtener cantidad de usuarios conectados a una sala"""
        return len(self.active_connections.get(room_id, set()))


# Instancia global del gestor de conexiones
manager = ConnectionManager()
