from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class BadgeBase(BaseModel):
    """Schema base de insignia"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    category: Optional[str] = None
    points_required: int = Field(default=0, ge=0)
    rarity: str = Field(default="common", pattern="^(common|rare|epic|legendary)$")


class BadgeCreate(BadgeBase):
    """Schema para crear insignia"""
    requirements: Optional[Dict[str, Any]] = None


class BadgeResponse(BadgeBase):
    """Schema de respuesta de insignia"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserBadgeResponse(BaseModel):
    """Schema de insignia ganada por usuario"""
    id: int
    user_id: int
    badge_id: int
    earned_at: datetime
    progress: int
    badge: Optional[BadgeResponse] = None
    
    class Config:
        from_attributes = True


class QuestBase(BaseModel):
    """Schema base de misión"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    points_reward: int = Field(default=0, ge=0)
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard|epic)$")
    category: Optional[str] = None


class QuestCreate(QuestBase):
    """Schema para crear misión"""
    badge_reward_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class QuestResponse(QuestBase):
    """Schema de respuesta de misión"""
    id: int
    badge_reward_id: Optional[int] = None
    is_active: bool
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserQuestResponse(BaseModel):
    """Schema de progreso de misión por usuario"""
    id: int
    user_id: int
    quest_id: int
    status: str
    progress: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    quest: Optional[QuestResponse] = None
    
    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    """Schema de entrada en el ranking"""
    id: int
    user_id: int
    total_points: int
    rank_position: Optional[int] = None
    badges_earned: int
    quests_completed: int
    period: str
    last_updated: datetime
    
    # Información del usuario (joined)
    username: Optional[str] = None
    full_name: Optional[str] = None
    scout_group: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """Schema de estadísticas del usuario"""
    user_id: int
    total_points: int
    level: int
    badges_earned: int
    quests_completed: int
    quests_in_progress: int
    rank_position: Optional[int] = None
