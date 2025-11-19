"""
Módulo de seguridad
Maneja autenticación, autorización, cifrado y hashing
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

from app.core.config import settings


# ============================================
# PASSWORD HASHING (Argon2)
# ============================================

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=4,
)


def hash_password(password: str) -> str:
    """
    Hash de contraseña usando Argon2

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado

    Returns:
        True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# JWT TOKENS
# ============================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un JWT access token

    Args:
        data: Datos a incluir en el payload
        expires_delta: Tiempo de expiración (opcional)

    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un JWT refresh token

    Args:
        data: Datos a incluir en el payload
        expires_delta: Tiempo de expiración (opcional)

    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica y verifica un JWT token

    Args:
        token: Token JWT

    Returns:
        Payload del token o None si es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# ============================================
# CIFRADO AES-256 (para datos sensibles)
# ============================================

class DataEncryption:
    """
    Clase para cifrado/descifrado de datos sensibles
    Usa AES-256 mediante Fernet (implementación de cryptography)
    """

    def __init__(self):
        """Inicializa el cipher con la clave de cifrado"""
        # Derivar clave de 32 bytes desde la clave configurada
        key = settings.ENCRYPTION_KEY.encode()

        # Si la clave no es exactamente 32 bytes, derivarla con PBKDF2
        if len(key) != 32:
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'vitabrevis_salt_2024',  # En producción, usar salt único
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(key))
        else:
            key = base64.urlsafe_b64encode(key)

        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        """
        Cifra datos sensibles

        Args:
            data: Datos en texto plano

        Returns:
            Datos cifrados en base64
        """
        if not data:
            return ""

        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Descifra datos

        Args:
            encrypted_data: Datos cifrados en base64

        Returns:
            Datos descifrados en texto plano
        """
        if not encrypted_data:
            return ""

        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception:
            # Si falla el descifrado, retornar vacío (puede ser dato corrupto)
            return ""


# Instancia global para uso en toda la aplicación
data_encryption = DataEncryption()


# ============================================
# UTILIDADES DE SEGURIDAD
# ============================================

def generate_random_token(length: int = 32) -> str:
    """
    Genera un token aleatorio seguro

    Args:
        length: Longitud del token en bytes

    Returns:
        Token en formato hexadecimal
    """
    return os.urandom(length).hex()


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo para prevenir path traversal

    Args:
        filename: Nombre de archivo original

    Returns:
        Nombre de archivo seguro
    """
    # Remover caracteres peligrosos
    dangerous_chars = ['/', '\\', '..', '\0']
    safe_filename = filename

    for char in dangerous_chars:
        safe_filename = safe_filename.replace(char, '_')

    # Limitar longitud
    if len(safe_filename) > 255:
        name, ext = os.path.splitext(safe_filename)
        safe_filename = name[:250] + ext

    return safe_filename
