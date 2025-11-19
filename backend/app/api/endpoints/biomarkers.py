"""
Endpoints de Biomarcadores
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_biomarkers():
    """Listar biomarcadores - TODO"""
    return {"message": "Biomarkers endpoint - To be implemented"}


@router.post("/")
async def create_biomarker():
    """Crear biomarcador - TODO"""
    return {"message": "Create biomarker - To be implemented"}
