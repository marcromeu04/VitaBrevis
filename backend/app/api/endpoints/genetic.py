"""
Endpoints de Datos Genéticos
IMPORTANTE: Solo visualización, sin interpretación (evitar SaMD)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_genetic_data():
    """Listar datos genéticos - TODO"""
    return {"message": "Genetic data endpoint - To be implemented"}


@router.post("/upload")
async def upload_genetic_report():
    """Subir informe genético - TODO"""
    return {"message": "Upload genetic report - To be implemented"}
