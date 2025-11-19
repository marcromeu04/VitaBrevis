"""
Modelo de Usuario
Gestión de usuarios del sistema (médicos, enfermeras, recepción, pacientes)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.db.database import Base


class UserRole(str, enum.Enum):
    """Roles de usuario con permisos específicos"""
    ADMIN = "admin"  # Administrador del sistema
    MEDICO = "medico"  # Médico - acceso total a pacientes asignados
    ENFERMERIA = "enfermeria"  # Enfermería - acceso parcial
    RECEPCION = "recepcion"  # Recepción - solo administrativo
    PACIENTE = "paciente"  # Paciente - solo sus datos
    DIRECCION_MEDICA = "direccion_medica"  # Dirección - informes globales


class User(Base):
    """
    Modelo de Usuario del sistema

    GDPR: Este modelo contiene datos personales
    - Nombre, email, teléfono son datos personales
    - Se debe obtener consentimiento para procesarlos
    - El usuario puede ejercer derechos ARSOPL
    """
    __tablename__ = "users"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)

    # Credenciales (hasheadas con Argon2)
    hashed_password = Column(String(255), nullable=False)

    # Datos personales
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)

    # Rol y permisos
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.PACIENTE)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # 2FA (Two-Factor Authentication)
    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    totp_secret = Column(String(32), nullable=True)  # Secret para TOTP

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Si el usuario es paciente, referencia a su registro de paciente
    patient_id = Column(Integer, nullable=True)  # FK se añadirá después

    # Relaciones
    # audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    @property
    def full_name(self) -> str:
        """Retorna nombre completo"""
        return f"{self.first_name} {self.last_name}"

    def has_permission(self, required_role: UserRole) -> bool:
        """
        Verifica si el usuario tiene permisos suficientes

        Jerarquía de roles:
        admin > direccion_medica > medico > enfermeria > recepcion > paciente
        """
        role_hierarchy = {
            UserRole.ADMIN: 6,
            UserRole.DIRECCION_MEDICA: 5,
            UserRole.MEDICO: 4,
            UserRole.ENFERMERIA: 3,
            UserRole.RECEPCION: 2,
            UserRole.PACIENTE: 1,
        }

        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level
