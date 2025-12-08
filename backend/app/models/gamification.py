from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func

from app.database import Base


class Badge(Base):
    """Modelo de Insignia/Badge"""
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon_url = Column(String(500))
    
    # Requisitos
    category = Column(String(100))  # leadership, community, skills, etc.
    points_required = Column(Integer, default=0)
    requirements = Column(JSON)  # Criterios para obtener la insignia
    
    # Metadata
    rarity = Column(String(50), default="common")  # common, rare, epic, legendary
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Badge {self.name}>"


class UserBadge(Base):
    """Modelo de relación Usuario-Insignia"""
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    
    # Metadata
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    progress = Column(Integer, default=100)  # Porcentaje de completitud
    
    def __repr__(self):
        return f"<UserBadge User:{self.user_id} Badge:{self.badge_id}>"


class Quest(Base):
    """Modelo de Misión/Quest"""
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Recompensas
    points_reward = Column(Integer, default=0)
    badge_reward_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    
    # Configuración
    difficulty = Column(String(50), default="medium")  # easy, medium, hard, epic
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Quest {self.title}>"


class UserQuest(Base):
    """Modelo de progreso de misión por usuario"""
    __tablename__ = "user_quests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    
    # Progreso
    status = Column(String(50), default="in_progress")  # in_progress, completed, failed
    progress = Column(Integer, default=0)  # Porcentaje 0-100
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<UserQuest User:{self.user_id} Quest:{self.quest_id}>"


class Leaderboard(Base):
    """Modelo de Ranking/Tabla de Posiciones"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Estadísticas
    total_points = Column(Integer, default=0)
    rank_position = Column(Integer)
    badges_earned = Column(Integer, default=0)
    quests_completed = Column(Integer, default=0)
    
    # Periodo
    period = Column(String(50), default="all_time")  # all_time, monthly, weekly
    
    # Timestamps
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Leaderboard User:{self.user_id} Rank:{self.rank_position}>"
