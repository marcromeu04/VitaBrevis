"""
Modelo de Composición Corporal
Datos de bioimpedancia, DXA, antropometría
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class MeasurementMethod(str, enum.Enum):
    """Método de medición"""
    BIOIMPEDANCE = "bioimpedance"  # Bioimpedancia
    DXA = "dxa"  # Densitometría ósea (DEXA/DXA)
    SKINFOLD = "skinfold"  # Pliegues cutáneos
    ANTHROPOMETRY = "anthropometry"  # Antropometría manual
    BOD_POD = "bod_pod"  # Bod Pod
    HYDROSTATIC = "hydrostatic"  # Pesaje hidrostático
    OTHER = "other"


class BodyComposition(Base):
    """
    Modelo de Composición Corporal

    Almacena datos de:
    - Bioimpedancia profesional (InBody, Tanita, etc.)
    - DXA (Densitometría)
    - Antropometría
    """
    __tablename__ = "body_compositions"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Fecha de medición
    measurement_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Método utilizado
    measurement_method = Column(SQLEnum(MeasurementMethod), nullable=False)

    # Equipo/dispositivo usado
    device_name = Column(String(200), nullable=True)
    # Ejemplo: "InBody 770", "GE Lunar iDXA"

    # ============================================
    # DATOS BÁSICOS
    # ============================================

    # Peso y altura
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=True)

    # IMC (calculado)
    bmi = Column(Float, nullable=True)

    # ============================================
    # COMPOSICIÓN CORPORAL
    # ============================================

    # Grasa corporal
    body_fat_percentage = Column(Float, nullable=True)  # %
    body_fat_mass_kg = Column(Float, nullable=True)  # kg

    # Masa magra
    lean_body_mass_kg = Column(Float, nullable=True)  # kg
    lean_body_mass_percentage = Column(Float, nullable=True)  # %

    # Masa muscular esquelética
    skeletal_muscle_mass_kg = Column(Float, nullable=True)  # kg
    skeletal_muscle_mass_percentage = Column(Float, nullable=True)  # %

    # Masa ósea
    bone_mass_kg = Column(Float, nullable=True)  # kg

    # ============================================
    # GRASA VISCERAL Y DISTRIBUCIÓN
    # ============================================

    # Grasa visceral (área o nivel)
    visceral_fat_area_cm2 = Column(Float, nullable=True)  # cm²
    visceral_fat_level = Column(Integer, nullable=True)  # Escala 1-20 típicamente

    # Grasa subcutánea
    subcutaneous_fat_kg = Column(Float, nullable=True)

    # ============================================
    # AGUA CORPORAL
    # ============================================

    # Agua corporal total
    total_body_water_kg = Column(Float, nullable=True)  # kg
    total_body_water_percentage = Column(Float, nullable=True)  # %

    # Agua intracelular y extracelular
    intracellular_water_kg = Column(Float, nullable=True)
    extracellular_water_kg = Column(Float, nullable=True)

    # ============================================
    # DENSIDAD ÓSEA (DXA)
    # ============================================

    # Densidad mineral ósea
    bone_mineral_density_g_cm2 = Column(Float, nullable=True)  # g/cm²

    # T-Score (comparación con adulto joven)
    t_score = Column(Float, nullable=True)

    # Z-Score (comparación con misma edad)
    z_score = Column(Float, nullable=True)

    # ============================================
    # METABÓLICOS
    # ============================================

    # Tasa metabólica basal (si viene dada)
    basal_metabolic_rate_kcal = Column(Integer, nullable=True)  # kcal/día

    # ============================================
    # SEGMENTACIÓN (brazos, piernas, tronco)
    # ============================================

    # Músculo por segmento (si disponible)
    muscle_right_arm_kg = Column(Float, nullable=True)
    muscle_left_arm_kg = Column(Float, nullable=True)
    muscle_right_leg_kg = Column(Float, nullable=True)
    muscle_left_leg_kg = Column(Float, nullable=True)
    muscle_trunk_kg = Column(Float, nullable=True)

    # Grasa por segmento
    fat_right_arm_kg = Column(Float, nullable=True)
    fat_left_arm_kg = Column(Float, nullable=True)
    fat_right_leg_kg = Column(Float, nullable=True)
    fat_left_leg_kg = Column(Float, nullable=True)
    fat_trunk_kg = Column(Float, nullable=True)

    # ============================================
    # PERÍMETROS (Antropometría)
    # ============================================

    waist_circumference_cm = Column(Float, nullable=True)
    hip_circumference_cm = Column(Float, nullable=True)
    waist_to_hip_ratio = Column(Float, nullable=True)

    # ============================================
    # OTROS
    # ============================================

    # Archivo del informe
    report_file_path = Column(String(500), nullable=True)

    # Notas
    notes = Column(Text, nullable=True)

    # Validación
    is_validated = Column(Boolean, default=False)
    validated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    # patient = relationship("Patient", back_populates="body_compositions")

    def __repr__(self):
        return (
            f"<BodyComposition(id={self.id}, patient_id={self.patient_id}, "
            f"weight={self.weight_kg}kg, bf%={self.body_fat_percentage})>"
        )
