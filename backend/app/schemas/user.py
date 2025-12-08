from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    scout_group: Optional[str] = None
    scout_region: Optional[str] = None
    scout_rank: Optional[str] = None


class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    scout_group: Optional[str] = None
    scout_region: Optional[str] = None
    scout_rank: Optional[str] = None


class UserInDB(UserBase):
    """Schema de usuario en base de datos"""
    id: int
    points: int = 0
    level: int = 1
    badges_count: int = 0
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Schema de respuesta de usuario (sin datos sensibles)"""
    id: int
    points: int
    level: int
    badges_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema de token de autenticación"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de datos dentro del token"""
    user_id: Optional[int] = None
