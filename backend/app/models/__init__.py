"""
Database Models
Importar todos los modelos aquí para Alembic
"""

from app.db.database import Base
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.patient import Patient
from app.models.consent import Consent
from app.models.biomarker import Biomarker, BiomarkerCategory
from app.models.genetic_data import GeneticData
from app.models.microbiome import MicrobiomeData
from app.models.body_composition import BodyComposition
from app.models.cognitive import CognitiveTest
from app.models.lifestyle import LifestyleData

__all__ = [
    "Base",
    "User",
    "AuditLog",
    "Patient",
    "Consent",
    "Biomarker",
    "BiomarkerCategory",
    "GeneticData",
    "MicrobiomeData",
    "BodyComposition",
    "CognitiveTest",
    "LifestyleData",
]
