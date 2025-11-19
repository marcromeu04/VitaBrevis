"""
Modelo de Datos de Estilo de Vida
Actividad física, sueño, y otros parámetros de estilo de vida
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date

from app.db.database import Base


class LifestyleData(Base):
    """
    Modelo de Datos de Estilo de Vida

    Almacena datos de:
    - Actividad física (pasos, ejercicio)
    - Sueño
    - Peso diario
    - Frecuencia cardíaca en reposo
    - Datos de wearables (si el paciente autoriza)

    GDPR: Requiere consentimiento para integración con wearables
    """
    __tablename__ = "lifestyle_data"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Fecha del registro
    record_date = Column(Date, nullable=False, index=True)

    # ============================================
    # ACTIVIDAD FÍSICA
    # ============================================

    # Pasos diarios
    steps = Column(Integer, nullable=True)

    # Distancia recorrida (km)
    distance_km = Column(Float, nullable=True)

    # Calorías activas quemadas
    active_calories = Column(Integer, nullable=True)

    # Minutos de actividad moderada
    moderate_activity_minutes = Column(Integer, nullable=True)

    # Minutos de actividad vigorosa
    vigorous_activity_minutes = Column(Integer, nullable=True)

    # Entrenamientos específicos
    workouts = Column(JSON, nullable=True)
    # Ejemplo: [
    #   {"type": "running", "duration_min": 30, "distance_km": 5.2, "avg_hr": 145},
    #   {"type": "strength", "duration_min": 45, "exercises": 8}
    # ]

    # ============================================
    # SUEÑO
    # ============================================

    # Horas de sueño total
    sleep_hours = Column(Float, nullable=True)

    # Calidad del sueño (1-10 o porcentaje)
    sleep_quality_score = Column(Float, nullable=True)

    # Fases del sueño (si disponible)
    sleep_stages = Column(JSON, nullable=True)
    # Ejemplo: {
    #   "deep_sleep_hours": 1.5,
    #   "light_sleep_hours": 4.2,
    #   "rem_sleep_hours": 2.1,
    #   "awake_hours": 0.2
    # }

    # Hora de acostarse y levantarse
    bedtime = Column(DateTime(timezone=True), nullable=True)
    wake_time = Column(DateTime(timezone=True), nullable=True)

    # ============================================
    # DATOS FISIOLÓGICOS
    # ============================================

    # Peso diario
    weight_kg = Column(Float, nullable=True)

    # Frecuencia cardíaca en reposo
    resting_heart_rate = Column(Integer, nullable=True)

    # Variabilidad de la frecuencia cardíaca (HRV)
    heart_rate_variability_ms = Column(Float, nullable=True)

    # Presión arterial (si se registra diariamente)
    systolic_bp = Column(Integer, nullable=True)
    diastolic_bp = Column(Integer, nullable=True)

    # Saturación de oxígeno (SpO2)
    oxygen_saturation = Column(Float, nullable=True)

    # ============================================
    # NUTRICIÓN (básico)
    # ============================================

    # Calorías consumidas (si se trackea)
    calories_consumed = Column(Integer, nullable=True)

    # Vasos de agua
    water_glasses = Column(Integer, nullable=True)

    # ============================================
    # BIENESTAR SUBJETIVO
    # ============================================

    # Nivel de energía percibido (1-10)
    energy_level = Column(Integer, nullable=True)

    # Nivel de estrés percibido (1-10)
    stress_level = Column(Integer, nullable=True)

    # Estado de ánimo (1-10)
    mood_score = Column(Integer, nullable=True)

    # ============================================
    # FUENTE DE DATOS
    # ============================================

    # Fuente de los datos
    data_source = Column(String(100), nullable=True)
    # Ejemplo: "Apple Health", "Google Fit", "Strava", "Manual", "Garmin", "Whoop"

    # Datos raw de la integración (si aplicable)
    raw_integration_data = Column(JSON, nullable=True)

    # ============================================
    # NOTAS
    # ============================================

    # Notas del paciente
    patient_notes = Column(Text, nullable=True)

    # Notas del profesional
    clinical_notes = Column(Text, nullable=True)

    # ============================================
    # METADATA
    # ============================================

    # Validación
    is_validated = Column(Boolean, default=False)
    validated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Registro
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    # patient = relationship("Patient", back_populates="lifestyle_data")

    def __repr__(self):
        return (
            f"<LifestyleData(id={self.id}, patient_id={self.patient_id}, "
            f"date={self.record_date}, steps={self.steps})>"
        )

    @property
    def total_active_minutes(self) -> int:
        """Calcula minutos totales de actividad"""
        moderate = self.moderate_activity_minutes or 0
        vigorous = self.vigorous_activity_minutes or 0
        return moderate + vigorous

    @property
    def sleep_efficiency(self) -> float:
        """
        Calcula eficiencia del sueño
        (Tiempo dormido / Tiempo en cama) * 100
        """
        if not self.bedtime or not self.wake_time or not self.sleep_hours:
            return None

        time_in_bed = (self.wake_time - self.bedtime).total_seconds() / 3600
        if time_in_bed <= 0:
            return None

        return (self.sleep_hours / time_in_bed) * 100
