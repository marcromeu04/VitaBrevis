"""
Configuración de la aplicación
Carga variables de entorno y define configuración global
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, Field


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings
    Carga automáticamente desde variables de entorno
    """

    # General
    APP_NAME: str = "VitaBrevis"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # Database
    DB_USER: str = "vitabrevis"
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "vitabrevis_db"

    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL de conexión a PostgreSQL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Construye la URL de conexión asíncrona"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str  # Para cifrado AES-256 de datos sensibles

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parsea los orígenes CORS desde string a lista"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Email (para notificaciones y 2FA)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@vitabrevis.com"
    SMTP_FROM_NAME: str = "VitaBrevis"

    # Archivos
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    # Logging y auditoría
    LOG_LEVEL: str = "INFO"
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 años (requisito legal)
    ENABLE_AUDIT_LOG: bool = True

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # Backup
    BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"
    BACKUP_RETENTION_DAYS: int = 90

    # Clínica
    CLINIC_NAME: str = "Mi Clínica de Longevidad"
    CLINIC_ADDRESS: str = "Dirección de la clínica"
    CLINIC_PHONE: str = "+34 912 345 678"
    CLINIC_EMAIL: str = "info@clinica.com"
    CLINIC_LOGO_URL: str = "/assets/logo.png"

    # Datos de prueba
    CREATE_DEMO_DATA: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
