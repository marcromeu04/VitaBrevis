"""
Modelo de Datos Genéticos
Solo almacenamiento y visualización - SIN interpretación
CRÍTICO: No generar recomendaciones ni diagnósticos (evitar SaMD)
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class GeneticData(Base):
    """
    Modelo de Datos Genéticos

    IMPORTANTE - Compliance:
    - Solo almacena y visualiza datos
    - NO interpreta variantes
    - NO calcula riesgos
    - NO genera recomendaciones
    - NO usa modelos poligénicos (PRS)

    Ley 14/2007 (España): Investigación Biomédica
    - Requiere consentimiento ESPECÍFICO
    - Prohibida discriminación genética

    GDPR Artículo 9: Categoría especial de datos
    - Requiere consentimiento explícito
    - Cifrado obligatorio
    """
    __tablename__ = "genetic_data"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Información del test
    test_name = Column(String(200), nullable=False)
    # Ejemplo: "23andMe Health + Ancestry", "Whole Genome Sequencing"

    test_provider = Column(String(200), nullable=True)
    # Ejemplo: "23andMe", "AncestryDNA", "Nebula Genomics"

    test_date = Column(DateTime(timezone=True), nullable=True, index=True)

    # Tipo de test
    test_type = Column(String(100), nullable=True)
    # Ejemplos: "SNP Genotyping", "WGS", "WES", "Panel específico"

    # Archivo del informe original (PDF)
    report_file_path = Column(String(500), nullable=True)

    # Datos raw (opcional - puede ser muy grande)
    # Formato: JSON con SNPs o variantes
    raw_data = Column(JSON, nullable=True)
    # Ejemplo: {"rs7412": "C/C", "rs429358": "T/T", ...}

    # Resumen organizado por categorías (solo descriptivo)
    # NO debe contener interpretaciones médicas
    summary_data = Column(JSON, nullable=True)
    # Ejemplo estructura (solo datos, sin interpretación):
    # {
    #   "metabolism": {
    #     "caffeine": {"gene": "CYP1A2", "variant": "rs762551", "genotype": "A/A"},
    #     "lactose": {"gene": "LCT", "variant": "rs4988235", "genotype": "C/T"}
    #   },
    #   "vitamins": {
    #     "vitamin_d": {"gene": "VDR", "variant": "rs2228570", "genotype": "C/C"}
    #   }
    # }

    # Frecuencias poblacionales (si vienen en el informe)
    population_frequencies = Column(JSON, nullable=True)

    # Notas del profesional
    clinical_notes = Column(Text, nullable=True)

    # Validación
    is_validated = Column(Boolean, default=False)
    validated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    # patient = relationship("Patient", back_populates="genetic_data")

    def __repr__(self):
        return f"<GeneticData(id={self.id}, test={self.test_name}, patient_id={self.patient_id})>"

    @staticmethod
    def get_disclaimer() -> str:
        """
        Disclaimer legal para mostrar con datos genéticos
        """
        return (
            "AVISO LEGAL: Estos datos genéticos son solo informativos y descriptivos. "
            "NO constituyen un diagnóstico médico. "
            "NO se deben tomar decisiones de salud basándose únicamente en esta información. "
            "Consulte siempre con un profesional médico cualificado. "
            "Esta plataforma NO interpreta datos genéticos ni calcula riesgos de enfermedad."
        )
