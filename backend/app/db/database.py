"""
Configuración de la base de datos
SQLAlchemy setup con soporte para sync y async
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import Generator

from app.core.config import settings


# ============================================
# SQLAlchemy Engine (Sync)
# ============================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexión antes de usarla
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,  # Log SQL queries en desarrollo
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================
# SQLAlchemy Engine (Async) - Para operaciones async
# ============================================

async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


# ============================================
# Base declarativa
# ============================================

Base = declarative_base()


# ============================================
# Dependency para obtener sesión de DB
# ============================================

def get_db() -> Generator:
    """
    Dependency que proporciona una sesión de base de datos
    Se cierra automáticamente al finalizar la request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    """
    Dependency que proporciona una sesión asíncrona
    """
    async with AsyncSessionLocal() as session:
        yield session


# ============================================
# Event listeners para seguridad
# ============================================

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """
    Configuraciones de seguridad al conectar a PostgreSQL
    """
    cursor = dbapi_conn.cursor()

    # Establecer timezone UTC
    cursor.execute("SET timezone='UTC'")

    # Configurar statement timeout (30 segundos)
    cursor.execute("SET statement_timeout='30s'")

    cursor.close()
