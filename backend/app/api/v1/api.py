from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, chat, foro  # gamification deshabilitada temporalmente

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(foro.router, prefix="/foro", tags=["Foro Nacional"])
# Gamificación deshabilitada temporalmente
# api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamificación"])
