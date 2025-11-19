"""
Schemas Pydantic para User
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# ============================================
# BASE SCHEMAS
# ============================================

class UserBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.PACIENTE


# ============================================
# CREATE / UPDATE
# ============================================

class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=8, max_length=100)

    @validator("password")
    def validate_password(cls, v):
        """Validar fortaleza de contraseña"""
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        # Verificar complejidad
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "La contraseña debe contener mayúsculas, minúsculas y números"
            )

        return v


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


class UserChangePassword(BaseModel):
    """Schema para cambiar contraseña"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @validator("new_password")
    def validate_password(cls, v):
        """Validar fortaleza de contraseña"""
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "La contraseña debe contener mayúsculas, minúsculas y números"
            )

        return v


# ============================================
# RESPONSE
# ============================================

class User(UserBase):
    """Schema de respuesta de usuario"""
    id: int
    is_active: bool
    is_verified: bool
    is_2fa_enabled: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserInDB(User):
    """Schema de usuario en DB (incluye password hash)"""
    hashed_password: str
