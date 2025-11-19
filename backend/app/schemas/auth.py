"""
Schemas Pydantic para Autenticación
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Schema de respuesta de token"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos contenidos en el token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str
    totp_code: Optional[str] = None  # Para 2FA


class RefreshTokenRequest(BaseModel):
    """Schema para refresh token"""
    refresh_token: str


class Enable2FAResponse(BaseModel):
    """Respuesta al habilitar 2FA"""
    secret: str
    qr_code_url: str
    backup_codes: list[str]
