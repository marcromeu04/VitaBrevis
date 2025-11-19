"""
Modelo de Biomarcadores
Almacena valores de biomarcadores clásicos y avanzados
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class BiomarkerType(str, enum.Enum):
    """Tipo de biomarcador"""
    # Clásicos
    GLUCOSE = "glucose"
    LIPID = "lipid"
    LIVER = "liver"
    KIDNEY = "kidney"
    HORMONE = "hormone"
    INFLAMMATION = "inflammation"
    VITAMIN = "vitamin"
    MINERAL = "mineral"
    THYROID = "thyroid"
    HEMATOLOGY = "hematology"

    # Avanzados
    EPIGENETIC_AGE = "epigenetic_age"
    TELOMERE = "telomere"
    METABOLOMICS = "metabolomics"
    PROTEOMICS = "proteomics"
    ADVANCED_INFLAMMATION = "advanced_inflammation"
    OXIDATIVE_STRESS = "oxidative_stress"
    MITOCHONDRIAL = "mitochondrial"
    GLYCATION = "glycation"


class BiomarkerCategory(Base):
    """
    Categorías de biomarcadores
    Permite organizar y clasificar los biomarcadores
    """
    __tablename__ = "biomarker_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(BiomarkerType), nullable=False)

    # Orden de visualización
    display_order = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<BiomarkerCategory(name={self.name}, type={self.type})>"


class Biomarker(Base):
    """
    Modelo de Biomarcador

    Almacena valores de laboratorio y biomarcadores avanzados
    NO interpreta - solo almacena valores y rangos de referencia
    """
    __tablename__ = "biomarkers"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Categoría
    category_id = Column(Integer, ForeignKey("biomarker_categories.id"), nullable=True)

    # Tipo de biomarcador
    biomarker_type = Column(SQLEnum(BiomarkerType), nullable=False, index=True)

    # Nombre del biomarcador
    name = Column(String(200), nullable=False, index=True)
    # Ejemplos: "Glucosa", "Colesterol Total", "Edad Epigenética GrimAge"

    # Valor
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    # Ejemplos: "mg/dL", "años", "pg/mL"

    # Rango de referencia (proporcionado por laboratorio)
    reference_min = Column(Float, nullable=True)
    reference_max = Column(Float, nullable=True)
    reference_text = Column(String(255), nullable=True)
    # Ejemplo: "Normal: <100 mg/dL, Prediabetes: 100-125, Diabetes: ≥126"

    # Método de medición
    method = Column(String(200), nullable=True)
    # Ejemplo: "Espectrofotometría", "ELISA", "Metilación por microarray"

    # Laboratorio
    laboratory = Column(String(200), nullable=True)

    # Fecha de la muestra
    sample_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Fecha de registro en el sistema
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Usuario que registró el dato
    recorded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Notas adicionales
    notes = Column(Text, nullable=True)

    # Archivo adjunto (PDF del laboratorio)
    file_path = Column(String(500), nullable=True)

    # Flag para marcar como validado por médico
    is_validated = Column(Boolean, default=False)
    validated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    # patient = relationship("Patient", back_populates="biomarkers")
    # category = relationship("BiomarkerCategory")

    def __repr__(self):
        return f"<Biomarker(name={self.name}, value={self.value} {self.unit})>"

    @property
    def is_in_range(self) -> bool:
        """Verifica si el valor está dentro del rango de referencia"""
        if self.reference_min is None and self.reference_max is None:
            return None  # No hay rango definido

        if self.reference_min is not None and self.value < self.reference_min:
            return False

        if self.reference_max is not None and self.value > self.reference_max:
            return False

        return True

    @property
    def deviation_percentage(self) -> float:
        """Calcula la desviación porcentual respecto al rango óptimo"""
        if self.reference_min is None or self.reference_max is None:
            return None

        optimal = (self.reference_min + self.reference_max) / 2
        return ((self.value - optimal) / optimal) * 100
