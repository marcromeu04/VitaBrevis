"""
Schemas Pydantic para Patient
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date, datetime
from app.models.patient import Sex, BloodType, ProgramPhase


class PatientBase(BaseModel):
    """Schema base de paciente"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    sex: Sex
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    blood_type: Optional[BloodType] = None
    height_cm: Optional[int] = Field(None, ge=50, le=250)
    medical_notes: Optional[str] = None


class PatientCreate(PatientBase):
    """Schema para crear paciente"""
    responsible_doctor_id: Optional[int] = None
    program_phase: ProgramPhase = ProgramPhase.INITIAL_ASSESSMENT


class PatientUpdate(BaseModel):
    """Schema para actualizar paciente"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    blood_type: Optional[BloodType] = None
    height_cm: Optional[int] = Field(None, ge=50, le=250)
    medical_notes: Optional[str] = None
    program_phase: Optional[ProgramPhase] = None
    is_active: Optional[bool] = None


class Patient(PatientBase):
    """Schema de respuesta de paciente"""
    id: int
    medical_record_number: str
    user_id: Optional[int]
    responsible_doctor_id: Optional[int]
    program_phase: ProgramPhase
    program_start_date: Optional[date]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    # Propiedades calculadas
    age: Optional[int] = None

    class Config:
        from_attributes = True


class PatientList(BaseModel):
    """Lista de pacientes con paginación"""
    total: int
    items: list[Patient]
    page: int
    page_size: int
