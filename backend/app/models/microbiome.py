"""
Modelo de Datos de Microbioma
Almacena resultados de análisis de microbiota intestinal
Solo visualización - sin interpretación médica
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class MicrobiomeData(Base):
    """
    Modelo de Datos del Microbioma

    Almacena resultados de análisis de microbiota intestinal
    - Solo muestra lo que el laboratorio ya calculó
    - NO interpreta ni genera recomendaciones
    """
    __tablename__ = "microbiome_data"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)

    # Paciente
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    # Información del test
    test_name = Column(String(200), nullable=False)
    # Ejemplo: "Microbiome Test Complete", "Gut Health Analysis"

    test_provider = Column(String(200), nullable=True)
    # Ejemplo: "Viome", "Thorne", "BiomeFx", "DayTwo"

    sample_date = Column(DateTime(timezone=True), nullable=True, index=True)
    sample_type = Column(String(100), nullable=True)
    # Ejemplo: "Stool", "Oral swab"

    # Archivo del informe original
    report_file_path = Column(String(500), nullable=True)

    # Diversidad alfa (valor dado por el laboratorio)
    alpha_diversity = Column(Float, nullable=True)
    alpha_diversity_index = Column(String(50), nullable=True)
    # Ejemplo: "Shannon", "Simpson"

    # Diversidad beta (si viene en el informe)
    beta_diversity_notes = Column(Text, nullable=True)

    # Abundancia relativa por phylum (nivel superior)
    phylum_abundance = Column(JSON, nullable=True)
    # Ejemplo: {
    #   "Firmicutes": 65.2,
    #   "Bacteroidetes": 28.5,
    #   "Proteobacteria": 4.1,
    #   "Actinobacteria": 2.2
    # }

    # Géneros principales encontrados
    genus_abundance = Column(JSON, nullable=True)
    # Ejemplo: {
    #   "Faecalibacterium": 12.5,
    #   "Bacteroides": 10.2,
    #   "Prevotella": 8.3,
    #   ...
    # }

    # Especies principales (si están disponibles)
    species_abundance = Column(JSON, nullable=True)

    # Marcadores específicos (dados por el laboratorio)
    markers = Column(JSON, nullable=True)
    # Ejemplo: {
    #   "butyrate_producers": 15.2,
    #   "lactate_producers": 8.5,
    #   "pathobionts": 0.3
    # }

    # Funciones metabólicas (si vienen en el informe)
    metabolic_functions = Column(JSON, nullable=True)
    # Ejemplo: {
    #   "short_chain_fatty_acids": "moderate",
    #   "vitamin_synthesis": "high"
    # }

    # Ratio Firmicutes/Bacteroidetes (comúnmente reportado)
    firmicutes_bacteroidetes_ratio = Column(Float, nullable=True)

    # Notas del laboratorio
    lab_notes = Column(Text, nullable=True)

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
    # patient = relationship("Patient", back_populates="microbiome_data")

    def __repr__(self):
        return f"<MicrobiomeData(id={self.id}, test={self.test_name}, patient_id={self.patient_id})>"

    @staticmethod
    def get_disclaimer() -> str:
        """Disclaimer legal para datos de microbioma"""
        return (
            "AVISO: Los datos del microbioma son solo informativos. "
            "Esta plataforma muestra únicamente los resultados proporcionados por el laboratorio. "
            "NO se generan interpretaciones ni recomendaciones terapéuticas. "
            "Consulte con un profesional de la salud para interpretación clínica."
        )
