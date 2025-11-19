"""
Modelo de Tests Cognitivos
Datos de rendimiento cognitivo NO clínico
IMPORTANTE: No son tests de diagnóstico neurológico
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class CognitiveTestType(str, enum.Enum):
    """Tipo de test cognitivo"""
    REACTION_TIME = "reaction_time"  # Tiempo de reacción
    WORKING_MEMORY = "working_memory"  # Memoria de trabajo
    ATTENTION = "attention"  # Atención simple
    PROCESSING_SPEED = "processing_speed"  # Velocidad de procesamiento
    EXECUTIVE_FUNCTION = "executive_function"  # Función ejecutiva
    VERBAL_FLUENCY = "verbal_fluency"  # Fluidez verbal
    PATTERN_RECOGNITION = "pattern_recognition"  # Reconocimiento de patrones
    OTHER = "other"


class CognitiveTest(Base):
    """
    Modelo de Test Cognitivo

    IMPORTANTE - NO es diagnóstico médico:
    - Tests sencillos de rendimiento cognitivo
    - NO sustituye evaluación neuropsicológica
    - Solo para tracking de rendimiento en programas de longevidad

    Ejemplos:
    - Tests de tiempo de reacción
    - Tareas simples de memoria
    - Tests de atención sostenida
    """
    __tablename__ = "cognitive_tests"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Tipo de test
    test_type = Column(SQLEnum(CognitiveTestType), nullable=False, index=True)

    # Nombre del test
    test_name = Column(String(200), nullable=False)
    # Ejemplo: "Simple Reaction Time", "N-Back Task", "Stroop Test"

    # Fecha del test
    test_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Duración del test (en segundos)
    duration_seconds = Column(Integer, nullable=True)

    # ============================================
    # RESULTADOS PRINCIPALES
    # ============================================

    # Score principal (normalizado 0-100 si es posible)
    score = Column(Float, nullable=True)

    # Tiempo de respuesta promedio (ms)
    average_response_time_ms = Column(Float, nullable=True)

    # Precisión (%)
    accuracy_percentage = Column(Float, nullable=True)

    # Número de intentos correctos
    correct_attempts = Column(Integer, nullable=True)

    # Número de intentos incorrectos
    incorrect_attempts = Column(Integer, nullable=True)

    # Total de intentos
    total_attempts = Column(Integer, nullable=True)

    # ============================================
    # DATOS DETALLADOS (JSON)
    # ============================================

    # Resultados completos del test
    detailed_results = Column(JSON, nullable=True)
    # Ejemplo para test de reacción:
    # {
    #   "trials": [245, 198, 223, ...],  # tiempos en ms
    #   "median": 215,
    #   "std_dev": 45,
    #   "fastest": 178,
    #   "slowest": 289
    # }

    # ============================================
    # CONTEXTO
    # ============================================

    # Condiciones del test
    conditions = Column(JSON, nullable=True)
    # Ejemplo: {"time_of_day": "morning", "fasted": true, "sleep_hours": 7}

    # Plataforma/dispositivo
    platform = Column(String(100), nullable=True)
    # Ejemplo: "Web", "Mobile App", "Tablet"

    # ============================================
    # NOTAS Y VALIDACIÓN
    # ============================================

    # Notas del profesional
    clinical_notes = Column(Text, nullable=True)

    # Validación
    is_validated = Column(Boolean, default=False)
    validated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    # patient = relationship("Patient", back_populates="cognitive_tests")

    def __repr__(self):
        return (
            f"<CognitiveTest(id={self.id}, type={self.test_type}, "
            f"score={self.score}, date={self.test_date})>"
        )

    @staticmethod
    def get_disclaimer() -> str:
        """Disclaimer legal para tests cognitivos"""
        return (
            "AVISO: Estos tests cognitivos son solo para seguimiento de rendimiento. "
            "NO son diagnósticos médicos ni neuropsicológicos. "
            "NO sustituyen una evaluación profesional. "
            "Si tiene preocupaciones sobre su salud cognitiva, consulte con un especialista."
        )
