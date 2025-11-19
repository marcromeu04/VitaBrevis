"""
Modelo de Auditoría
Registro inmutable de todos los accesos y cambios
CRÍTICO para cumplimiento GDPR y LOPDGDD
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.db.database import Base


class AuditLog(Base):
    """
    Registro de Auditoría

    LOPDGDD (España): Artículo requerido
    - Registro de TODOS los accesos a historias clínicas
    - Retención: 7 años mínimo (2555 días)
    - INMUTABLE: No se pueden editar ni eliminar

    GDPR: Artículo 30 - Registro de actividades de tratamiento
    """
    __tablename__ = "audit_logs"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    # Usuario que realiza la acción
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_email = Column(String(255), nullable=False)  # Denormalizado para inmutabilidad
    user_role = Column(String(50), nullable=False)

    # Acción realizada
    action = Column(String(100), nullable=False, index=True)
    # Ejemplos: "LOGIN", "LOGOUT", "VIEW_PATIENT", "UPDATE_BIOMARKER",
    #           "DOWNLOAD_REPORT", "DELETE_CONSENT", "EXPORT_DATA"

    # Recurso afectado
    resource_type = Column(String(100), nullable=True, index=True)
    # Ejemplos: "Patient", "Biomarker", "GeneticData", "Report"

    resource_id = Column(Integer, nullable=True, index=True)

    # Detalles de la acción (JSON para flexibilidad)
    details = Column(JSON, nullable=True)
    # Ejemplo: {"patient_id": 123, "fields_modified": ["weight", "height"]}

    # Contexto de la request
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    endpoint = Column(String(255), nullable=True)
    http_method = Column(String(10), nullable=True)

    # Resultado de la acción
    status = Column(String(20), nullable=False)
    # "SUCCESS", "FAILED", "UNAUTHORIZED", "FORBIDDEN"

    error_message = Column(Text, nullable=True)

    # Relaciones
    # user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, action={self.action}, "
            f"user={self.user_email}, status={self.status})>"
        )

    class Config:
        """No permitir modificaciones después de creación"""
        # En SQLAlchemy, esto se maneja a nivel de aplicación
        # Los triggers de DB previenen UPDATE/DELETE
        pass


# ============================================
# Funciones auxiliares para logging
# ============================================

def log_action(
    db,
    user_id: int,
    user_email: str,
    user_role: str,
    action: str,
    status: str = "SUCCESS",
    resource_type: str = None,
    resource_id: int = None,
    details: dict = None,
    ip_address: str = None,
    user_agent: str = None,
    endpoint: str = None,
    http_method: str = None,
    error_message: str = None
):
    """
    Crea un registro de auditoría

    Esta función SIEMPRE debe ser llamada para acciones importantes
    """
    audit_entry = AuditLog(
        user_id=user_id,
        user_email=user_email,
        user_role=user_role,
        action=action,
        status=status,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint,
        http_method=http_method,
        error_message=error_message
    )

    db.add(audit_entry)
    db.commit()

    return audit_entry
