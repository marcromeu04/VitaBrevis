"""
Endpoints de Pacientes
GDPR: Datos de salud - Artículo 9
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import secrets

from app.db.database import get_db
from app.schemas.patient import Patient, PatientCreate, PatientUpdate, PatientList
from app.models.patient import Patient as PatientModel
from app.models.user import User as UserModel
from app.api.endpoints.auth import get_current_user
from app.models.audit_log import log_action

router = APIRouter()


def generate_medical_record_number() -> str:
    """Genera un número de historia clínica único"""
    prefix = "VB"  # VitaBrevis
    random_part = secrets.token_hex(4).upper()
    return f"{prefix}-{random_part}"


@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo paciente

    GDPR: Requiere consentimiento explícito
    """
    # Solo médicos y admin pueden crear pacientes
    if current_user.role.value not in ["admin", "medico", "recepcion"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear pacientes"
        )

    # Generar medical record number
    mrn = generate_medical_record_number()

    # Crear paciente
    new_patient = PatientModel(
        **patient_data.dict(),
        medical_record_number=mrn
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    # Audit log
    log_action(
        db=db,
        user_id=current_user.id,
        user_email=current_user.email,
        user_role=current_user.role.value,
        action="CREATE_PATIENT",
        status="SUCCESS",
        resource_type="Patient",
        resource_id=new_patient.id
    )

    return new_patient


@router.get("/", response_model=PatientList)
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar pacientes"""
    query = db.query(PatientModel)

    # Filtro por búsqueda
    if search:
        query = query.filter(
            (PatientModel.first_name.ilike(f"%{search}%")) |
            (PatientModel.last_name.ilike(f"%{search}%")) |
            (PatientModel.medical_record_number.ilike(f"%{search}%"))
        )

    # Si es médico, solo sus pacientes
    if current_user.role.value == "medico":
        query = query.filter(PatientModel.responsible_doctor_id == current_user.id)

    total = query.count()
    patients = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "items": patients,
        "page": skip // limit + 1,
        "page_size": limit
    }


@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener paciente por ID

    LOPDGDD: Registrar acceso a historia clínica
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )

    # Verificar permisos
    if current_user.role.value == "medico":
        if patient.responsible_doctor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este paciente"
            )

    # Registrar acceso
    log_action(
        db=db,
        user_id=current_user.id,
        user_email=current_user.email,
        user_role=current_user.role.value,
        action="VIEW_PATIENT",
        status="SUCCESS",
        resource_type="Patient",
        resource_id=patient.id
    )

    return patient


@router.put("/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar paciente"""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )

    # Actualizar
    update_data = patient_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    # Audit log
    log_action(
        db=db,
        user_id=current_user.id,
        user_email=current_user.email,
        user_role=current_user.role.value,
        action="UPDATE_PATIENT",
        status="SUCCESS",
        resource_type="Patient",
        resource_id=patient.id,
        details=update_data
    )

    return patient
