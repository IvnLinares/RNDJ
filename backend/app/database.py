from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Crear engine asíncrono para SQL Server
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    poolclass=NullPool,  # Para evitar problemas con SQL Server y async
)

# Crear session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Clase base para todos los modelos"""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obtener sesión de base de datos
    
    Uso en endpoints:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Inicializar base de datos - crear todas las tablas"""
    try:
        async with engine.begin() as conn:
            # Importar todos los modelos aquí para que SQLAlchemy los detecte
            from app.models import user, chat, gamification  # noqa
            
            # Crear todas las tablas
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Tablas de base de datos creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {e}")
        raise


async def close_db():
    """Cerrar conexiones de base de datos"""
    await engine.dispose()
    logger.info("🔒 Conexiones de base de datos cerradas")
