"""Inicialización de schemas"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
    UserResponse,
    Token,
    TokenData
)
from app.schemas.chat import (
    ChatRoomBase,
    ChatRoomCreate,
    ChatRoomResponse,
    ChatMessageBase,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatMessageWebSocket
)
from app.schemas.gamification import (
    BadgeBase,
    BadgeCreate,
    BadgeResponse,
    UserBadgeResponse,
    QuestBase,
    QuestCreate,
    QuestResponse,
    UserQuestResponse,
    LeaderboardEntry,
    UserStatsResponse
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    "Token",
    "TokenData",
    
    # Chat schemas
    "ChatRoomBase",
    "ChatRoomCreate",
    "ChatRoomResponse",
    "ChatMessageBase",
    "ChatMessageCreate",
    "ChatMessageResponse",
    "ChatMessageWebSocket",
    
    # Gamification schemas
    "BadgeBase",
    "BadgeCreate",
    "BadgeResponse",
    "UserBadgeResponse",
    "QuestBase",
    "QuestCreate",
    "QuestResponse",
    "UserQuestResponse",
    "LeaderboardEntry",
    "UserStatsResponse"
]
