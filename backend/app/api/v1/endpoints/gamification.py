from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List

from app.database import get_db
from app.schemas.gamification import (
    BadgeCreate,
    BadgeResponse,
    UserBadgeResponse,
    QuestCreate,
    QuestResponse,
    UserQuestResponse,
    LeaderboardEntry,
    UserStatsResponse
)
from app.models.gamification import Badge, UserBadge, Quest, UserQuest, Leaderboard
from app.models.user import User
from app.api.v1.endpoints.users import get_current_user_from_token
from datetime import datetime

router = APIRouter()


# ==================== BADGES ====================

@router.post("/badges", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
async def create_badge(
    badge_data: BadgeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Crear nueva insignia (solo admin)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear insignias"
        )
    
    new_badge = Badge(**badge_data.model_dump())
    db.add(new_badge)
    await db.commit()
    await db.refresh(new_badge)
    
    return new_badge


@router.get("/badges", response_model=List[BadgeResponse])
async def get_badges(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener todas las insignias disponibles
    """
    result = await db.execute(
        select(Badge)
        .where(Badge.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    badges = result.scalars().all()
    return badges


@router.get("/badges/my", response_model=List[UserBadgeResponse])
async def get_my_badges(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener insignias del usuario actual
    """
    result = await db.execute(
        select(UserBadge)
        .where(UserBadge.user_id == current_user.id)
        .order_by(UserBadge.earned_at.desc())
    )
    user_badges = result.scalars().all()
    return user_badges


@router.post("/badges/{badge_id}/award/{user_id}", response_model=UserBadgeResponse)
async def award_badge(
    badge_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Otorgar insignia a un usuario (solo admin o sistema)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para otorgar insignias"
        )
    
    # Verificar que la insignia existe
    result = await db.execute(select(Badge).where(Badge.id == badge_id))
    badge = result.scalar_one_or_none()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insignia no encontrada"
        )
    
    # Verificar que el usuario existe
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el usuario no tiene ya esta insignia
    result = await db.execute(
        select(UserBadge).where(
            and_(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya tiene esta insignia"
        )
    
    # Otorgar insignia
    user_badge = UserBadge(
        user_id=user_id,
        badge_id=badge_id,
        progress=100
    )
    db.add(user_badge)
    
    # Actualizar contador de insignias del usuario
    user.badges_count += 1
    
    await db.commit()
    await db.refresh(user_badge)
    
    return user_badge


# ==================== QUESTS ====================

@router.post("/quests", response_model=QuestResponse, status_code=status.HTTP_201_CREATED)
async def create_quest(
    quest_data: QuestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Crear nueva misión (solo admin)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear misiones"
        )
    
    new_quest = Quest(**quest_data.model_dump())
    db.add(new_quest)
    await db.commit()
    await db.refresh(new_quest)
    
    return new_quest


@router.get("/quests", response_model=List[QuestResponse])
async def get_quests(
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener todas las misiones
    """
    query = select(Quest)
    if active_only:
        query = query.where(Quest.is_active == True)
    
    result = await db.execute(query.offset(skip).limit(limit))
    quests = result.scalars().all()
    return quests


@router.get("/quests/my", response_model=List[UserQuestResponse])
async def get_my_quests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener misiones del usuario actual
    """
    result = await db.execute(
        select(UserQuest)
        .where(UserQuest.user_id == current_user.id)
        .order_by(UserQuest.started_at.desc())
    )
    user_quests = result.scalars().all()
    return user_quests


@router.post("/quests/{quest_id}/start", response_model=UserQuestResponse)
async def start_quest(
    quest_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Iniciar una misión
    """
    # Verificar que la misión existe
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = result.scalar_one_or_none()
    if not quest or not quest.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misión no encontrada o inactiva"
        )
    
    # Verificar que el usuario no ha iniciado ya esta misión
    result = await db.execute(
        select(UserQuest).where(
            and_(
                UserQuest.user_id == current_user.id,
                UserQuest.quest_id == quest_id,
                UserQuest.status != "failed"
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya has iniciado esta misión"
        )
    
    # Iniciar misión
    user_quest = UserQuest(
        user_id=current_user.id,
        quest_id=quest_id,
        status="in_progress",
        progress=0
    )
    db.add(user_quest)
    await db.commit()
    await db.refresh(user_quest)
    
    return user_quest


@router.put("/quests/{quest_id}/complete", response_model=UserQuestResponse)
async def complete_quest(
    quest_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Completar una misión
    """
    # Buscar la misión del usuario
    result = await db.execute(
        select(UserQuest).where(
            and_(
                UserQuest.user_id == current_user.id,
                UserQuest.quest_id == quest_id,
                UserQuest.status == "in_progress"
            )
        )
    )
    user_quest = result.scalar_one_or_none()
    
    if not user_quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misión no iniciada o ya completada"
        )
    
    # Obtener detalles de la misión
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = result.scalar_one_or_none()
    
    # Completar misión
    user_quest.status = "completed"
    user_quest.progress = 100
    user_quest.completed_at = datetime.utcnow()
    
    # Otorgar recompensas
    current_user.points += quest.points_reward
    
    await db.commit()
    await db.refresh(user_quest)
    
    return user_quest


# ==================== LEADERBOARD ====================

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    period: str = "all_time",
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener tabla de clasificación
    
    - **period**: all_time, monthly, weekly
    """
    result = await db.execute(
        select(Leaderboard)
        .where(Leaderboard.period == period)
        .order_by(Leaderboard.rank_position.asc())
        .offset(skip)
        .limit(limit)
    )
    leaderboard = result.scalars().all()
    return leaderboard


@router.get("/stats/me", response_model=UserStatsResponse)
async def get_my_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obtener estadísticas del usuario actual
    """
    # Contar quests completadas
    result = await db.execute(
        select(func.count(UserQuest.id)).where(
            and_(
                UserQuest.user_id == current_user.id,
                UserQuest.status == "completed"
            )
        )
    )
    quests_completed = result.scalar()
    
    # Contar quests en progreso
    result = await db.execute(
        select(func.count(UserQuest.id)).where(
            and_(
                UserQuest.user_id == current_user.id,
                UserQuest.status == "in_progress"
            )
        )
    )
    quests_in_progress = result.scalar()
    
    # Obtener ranking
    result = await db.execute(
        select(Leaderboard).where(
            and_(
                Leaderboard.user_id == current_user.id,
                Leaderboard.period == "all_time"
            )
        )
    )
    leaderboard_entry = result.scalar_one_or_none()
    rank_position = leaderboard_entry.rank_position if leaderboard_entry else None
    
    return UserStatsResponse(
        user_id=current_user.id,
        total_points=current_user.points,
        level=current_user.level,
        badges_earned=current_user.badges_count,
        quests_completed=quests_completed or 0,
        quests_in_progress=quests_in_progress or 0,
        rank_position=rank_position
    )
