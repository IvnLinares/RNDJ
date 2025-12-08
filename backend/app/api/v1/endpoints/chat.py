from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.database import get_db
from app.schemas.chat import (
    ChatRoomCreate,
    ChatRoomResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatMessageWebSocket
)
from app.models.chat import ChatRoom, ChatMessage
from app.models.user import User
from app.api.v1.endpoints.users import get_current_user_from_token
from app.core.websocket import manager
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/rooms", response_model=ChatRoomResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_room(
    room_data: ChatRoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Crear nueva sala de chat
    """
    new_room = ChatRoom(
        name=room_data.name,
        description=room_data.description,
        room_type=room_data.room_type,
        created_by=current_user.id
    )
    
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    
    return new_room


@router.get("/rooms", response_model=List[ChatRoomResponse])
async def get_chat_rooms(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener lista de salas de chat
    """
    result = await db.execute(
        select(ChatRoom)
        .where(ChatRoom.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    rooms = result.scalars().all()
    return rooms


@router.get("/rooms/{room_id}", response_model=ChatRoomResponse)
async def get_chat_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener detalles de una sala de chat
    """
    result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala de chat no encontrada"
        )
    
    return room


@router.get("/rooms/{room_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener mensajes de una sala de chat
    """
    # Verificar que la sala existe
    result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala de chat no encontrada"
        )
    
    # Obtener mensajes
    result = await db.execute(
        select(ChatMessage)
        .where(
            ChatMessage.room_id == room_id,
            ChatMessage.is_deleted == False
        )
        .order_by(ChatMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    messages = result.scalars().all()
    
    return list(reversed(messages))  # Retornar en orden cronológico


@router.post("/rooms/{room_id}/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    room_id: int,
    message_data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Crear mensaje en una sala de chat (REST endpoint)
    
    Para chat en tiempo real, usar WebSocket endpoint
    """
    # Verificar que la sala existe
    result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala de chat no encontrada"
        )
    
    # Crear mensaje
    new_message = ChatMessage(
        room_id=room_id,
        user_id=current_user.id,
        content=message_data.content,
        message_type=message_data.message_type
    )
    
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    return new_message


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    token: str
):
    """
    WebSocket endpoint para chat en tiempo real
    
    Uso desde frontend:
    ```javascript
    const ws = new WebSocket(`ws://localhost:8000/api/v1/chat/ws/${roomId}?token=${authToken}`)
    ```
    """
    # Validar token y obtener usuario
    from app.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    user_id = int(payload.get("sub"))
    username = payload.get("username", "Usuario")
    
    # Conectar usuario
    await manager.connect(websocket, str(room_id), str(user_id))
    
    # Notificar ingreso
    join_message = ChatMessageWebSocket(
        type="user_joined",
        room_id=room_id,
        user_id=user_id,
        username=username,
        content=f"{username} se unió al chat"
    )
    await manager.broadcast_to_room(join_message.model_dump(), str(room_id))
    
    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_text()
            
            # Crear mensaje en DB (opcional, dependiendo de si quieres persistencia)
            # Aquí puedes agregar lógica para guardar en BD
            
            # Broadcast del mensaje
            message = ChatMessageWebSocket(
                type="message",
                room_id=room_id,
                user_id=user_id,
                username=username,
                content=data,
                timestamp=datetime.utcnow()
            )
            
            await manager.broadcast_to_room(message.model_dump(), str(room_id))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, str(room_id))
        
        # Notificar salida
        leave_message = ChatMessageWebSocket(
            type="user_left",
            room_id=room_id,
            user_id=user_id,
            username=username,
            content=f"{username} abandonó el chat"
        )
        await manager.broadcast_to_room(leave_message.model_dump(), str(room_id))
