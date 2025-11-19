"""
Modelo de Consentimientos
Gestión de consentimientos GDPR
CRÍTICO para cumplimiento legal
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class ConsentType(str, enum.Enum):
    """Tipos de consentimiento"""
    GDPR_GENERAL = "gdpr_general"  # Consentimiento general GDPR
    GENETIC_DATA = "genetic_data"  # Específico para datos genéticos (Ley 14/2007)
    BIOMETRIC_DATA = "biometric_data"  # Datos biométricos
    DATA_SHARING = "data_sharing"  # Compartir datos con terceros
    RESEARCH = "research"  # Uso de datos para investigación
    MARKETING = "marketing"  # Comunicaciones comerciales


class Consent(Base):
    """
    Modelo de Consentimiento

    GDPR Artículo 7: Condiciones para el consentimiento
    - Debe ser libre, específico, informado e inequívoco
    - Debe poder retirarse en cualquier momento
    - Registro de fecha y versión del texto

    Ley 14/2007 (España): Investigación Biomédica
    - Consentimiento ESPECÍFICO para datos genéticos
    """
    __tablename__ = "consents"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Tipo de consentimiento
    consent_type = Column(SQLEnum(ConsentType), nullable=False, index=True)

    # Estado del consentimiento
    is_granted = Column(Boolean, nullable=False, default=False)

    # Versión del documento de consentimiento
    # Importante: si cambia el texto legal, debe incrementarse
    consent_version = Column(String(20), nullable=False)

    # Texto del consentimiento (almacenar snapshot)
    consent_text = Column(Text, nullable=False)

    # Firma digital / aceptación
    accepted_by_ip = Column(String(45), nullable=True)
    accepted_by_user_agent = Column(Text, nullable=True)

    # Timestamps
    granted_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Usuario que registró el consentimiento (puede ser médico o el paciente)
    registered_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Observaciones
    notes = Column(Text, nullable=True)

    # Relaciones
    # patient = relationship("Patient", back_populates="consents")

    def __repr__(self):
        status = "granted" if self.is_granted else "revoked"
        return f"<Consent(id={self.id}, type={self.consent_type}, status={status})>"

    def revoke(self):
        """Revocar consentimiento"""
        self.is_granted = False
        self.revoked_at = func.now()

    @property
    def is_active(self) -> bool:
        """Verifica si el consentimiento está activo"""
        return self.is_granted and self.revoked_at is None
