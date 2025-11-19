"""
Endpoints de Microbioma
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_microbiome_data():
    """Listar datos de microbioma - TODO"""
    return {"message": "Microbiome data endpoint - To be implemented"}


@router.post("/upload")
async def upload_microbiome_report():
    """Subir informe de microbioma - TODO"""
    return {"message": "Upload microbiome report - To be implemented"}
