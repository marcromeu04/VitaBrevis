"""
Modelo de Paciente
Datos clínicos y personales del paciente
ALTA SENSIBILIDAD - Datos de salud (Artículo 9 GDPR)
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Enum as SQLEnum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date, datetime
import enum

from app.db.database import Base


class Sex(str, enum.Enum):
    """Sexo biológico del paciente"""
    MALE = "male"
    FEMALE = "female"
    INTERSEX = "intersex"
    UNKNOWN = "unknown"


class BloodType(str, enum.Enum):
    """Grupo sanguíneo"""
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
    UNKNOWN = "unknown"


class ProgramPhase(str, enum.Enum):
    """Fase del programa de longevidad"""
    INITIAL_ASSESSMENT = "initial_assessment"  # Evaluación inicial
    BASELINE = "baseline"  # Línea base establecida
    ACTIVE_INTERVENTION = "active_intervention"  # Intervención activa
    MAINTENANCE = "maintenance"  # Mantenimiento
    MONITORING = "monitoring"  # Solo monitoreo
    COMPLETED = "completed"  # Programa completado
    INACTIVE = "inactive"  # Inactivo


class Patient(Base):
    """
    Modelo de Paciente

    GDPR Artículo 9: Datos especiales (salud)
    - Requiere consentimiento EXPLÍCITO
    - Cifrado obligatorio
    - Minimización de datos
    - Derecho al olvido

    LOPDGDD: Historia clínica digital
    - Cumple con Instrucción 1/2009 AEPD
    - Registro de accesos obligatorio
    """
    __tablename__ = "patients"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # ID de usuario si el paciente tiene cuenta
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)

    # Identificación clínica
    # CIFRADO: Este campo debe cifrarse (contiene PII)
    medical_record_number = Column(String(50), unique=True, index=True, nullable=False)

    # Datos personales (CIFRADOS en producción)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex = Column(SQLEnum(Sex), nullable=False)

    # Contacto (CIFRADO)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)

    # Datos clínicos básicos
    blood_type = Column(SQLEnum(BloodType), nullable=True)
    height_cm = Column(Integer, nullable=True)  # Altura en cm

    # Médico responsable
    responsible_doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Estado del programa
    program_phase = Column(
        SQLEnum(ProgramPhase),
        nullable=False,
        default=ProgramPhase.INITIAL_ASSESSMENT
    )
    program_start_date = Column(Date, nullable=True)

    # Notas médicas generales
    medical_notes = Column(Text, nullable=True)

    # Estado
    is_active = Column(Boolean, default=True, nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    # user = relationship("User", foreign_keys=[user_id])
    # responsible_doctor = relationship("User", foreign_keys=[responsible_doctor_id])
    # consents = relationship("Consent", back_populates="patient")
    # biomarkers = relationship("Biomarker", back_populates="patient")
    # genetic_data = relationship("GeneticData", back_populates="patient")
    # microbiome_data = relationship("MicrobiomeData", back_populates="patient")
    # body_compositions = relationship("BodyComposition", back_populates="patient")
    # cognitive_tests = relationship("CognitiveTest", back_populates="patient")
    # lifestyle_data = relationship("LifestyleData", back_populates="patient")

    def __repr__(self):
        return f"<Patient(id={self.id}, mrn={self.medical_record_number})>"

    @property
    def full_name(self) -> str:
        """Retorna nombre completo"""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calcula edad actual"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
