#!/usr/bin/env python3
"""
Script para crear usuario administrador inicial
"""

import sys
import os
from getpass import getpass

# Añadir directorio padre al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password


def create_admin():
    """Crea un usuario administrador"""

    print("=" * 50)
    print("CREAR USUARIO ADMINISTRADOR - VitaBrevis")
    print("=" * 50)
    print()

    # Solicitar datos
    email = input("Email del administrador: ").strip()
    username = input("Username: ").strip()
    first_name = input("Nombre: ").strip()
    last_name = input("Apellido: ").strip()

    # Validar email
    if not email or '@' not in email:
        print("❌ Email inválido")
        return

    # Validar username
    if not username or len(username) < 3:
        print("❌ Username debe tener al menos 3 caracteres")
        return

    # Solicitar contraseña
    password = getpass("Contraseña (mínimo 8 caracteres): ")
    password_confirm = getpass("Confirmar contraseña: ")

    if password != password_confirm:
        print("❌ Las contraseñas no coinciden")
        return

    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        return

    # Crear sesión
    db = SessionLocal()

    try:
        # Verificar si ya existe el email
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ Ya existe un usuario con el email {email}")
            return

        # Verificar si ya existe el username
        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            print(f"❌ Ya existe un usuario con el username {username}")
            return

        # Hash de la contraseña
        hashed_password = hash_password(password)

        # Crear administrador
        admin = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print()
        print("✅ Usuario administrador creado exitosamente!")
        print()
        print(f"Email: {admin.email}")
        print(f"Username: {admin.username}")
        print(f"Rol: {admin.role.value}")
        print(f"ID: {admin.id}")
        print()
        print("Ya puedes iniciar sesión en la plataforma.")

    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
