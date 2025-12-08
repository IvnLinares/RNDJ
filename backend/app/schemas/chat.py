from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRoomBase(BaseModel):
    """Schema base de sala de chat"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    room_type: str = Field(default="public", pattern="^(public|private|group)$")


class ChatRoomCreate(ChatRoomBase):
    """Schema para crear sala de chat"""
    pass


class ChatRoomResponse(ChatRoomBase):
    """Schema de respuesta de sala de chat"""
    id: int
    created_by: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    """Schema base de mensaje de chat"""
    content: str = Field(..., min_length=1)
    message_type: str = Field(default="text", pattern="^(text|image|file|system)$")


class ChatMessageCreate(ChatMessageBase):
    """Schema para crear mensaje"""
    room_id: int


class ChatMessageResponse(ChatMessageBase):
    """Schema de respuesta de mensaje"""
    id: int
    room_id: int
    user_id: int
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    edited_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ChatMessageWebSocket(BaseModel):
    """Schema para mensajes via WebSocket"""
    type: str = "message"  # message, user_joined, user_left, typing
    room_id: int
    user_id: int
    username: str
    content: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
