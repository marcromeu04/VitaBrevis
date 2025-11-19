# VitaBrevis - Plataforma de Gestión para Clínicas de Longevidad

## 🎯 Descripción

VitaBrevis es una plataforma web segura, modular y extensible diseñada específicamente para clínicas de longevidad. Permite gestionar pacientes, biomarcadores, datos genéticos, microbioma y otros parámetros avanzados, cumpliendo estrictamente con GDPR, LOPDGDD y sin ser considerado Software Médico Regulado (SaMD).

## 🚀 Características Principales

### Gestión Avanzada de Pacientes
- Registro completo de datos clínicos
- Historial cronológico de pruebas
- Sistema de fases del programa de longevidad
- Gestión de consentimientos (GDPR, genética, datos biométricos)

### Biomarcadores
- **Clásicos**: Glucosa, lípidos, función hepática, renal, hormonas
- **Avanzados**: Edad epigenética, telómeros, metabolómica, proteómica
- **Composición corporal**: Bioimpedancia, DXA, masa muscular, grasa visceral

### Módulos Especializados
- 🧬 **Genética/ADN**: Solo carga y visualización (sin interpretación médica)
- 🧫 **Microbioma**: Visualización de diversidad y abundancia
- 🧠 **Rendimiento cognitivo**: Tests no clínicos
- 💪 **Actividad física**: Integración con wearables
- 📈 **Timeline integral**: Vista cronológica completa del paciente

### Cumplimiento Legal
- ✅ GDPR (Reglamento General de Protección de Datos - UE)
- ✅ LOPDGDD (Ley Orgánica de Protección de Datos - España)
- ✅ Registro de accesos a historia clínica
- ✅ Cifrado AES-256 en reposo y TLS 1.2+ en tránsito
- ✅ Consentimientos específicos para datos genéticos
- ✅ NO es Software Médico Regulado (solo visualiza, no diagnostica)

### Seguridad
- Cifrado de datos sensibles (AES-256)
- Autenticación robusta con 2FA
- Control de acceso basado en roles (RBAC)
- Registro de auditoría inmutable
- Cumplimiento OWASP Top 10
- Protección contra SQL Injection, XSS, CSRF

## 🏗️ Arquitectura

```
┌─────────────────────────────────┐
│         Frontend (React)         │
│      Tailwind CSS + Vite         │
└─────────────┬───────────────────┘
              │ HTTPS/TLS 1.2+
              ▼
┌─────────────────────────────────┐
│     Backend API (FastAPI)        │
│  - Auth + 2FA                    │
│  - RBAC                          │
│  - Logging/Auditoría             │
│  - Validación                    │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│    PostgreSQL + TimescaleDB      │
│  - Cifrado columnar              │
│  - Auditoría por triggers        │
│  - Pseudonimización              │
└─────────────────────────────────┘
```

## 📦 Stack Tecnológico

### Backend
- **FastAPI** - Framework Python moderno y rápido
- **PostgreSQL 15+** - Base de datos relacional
- **SQLAlchemy 2.0** - ORM
- **Alembic** - Migraciones
- **Pydantic V2** - Validación de datos
- **Passlib + Argon2** - Hashing de contraseñas
- **python-jose** - JWT tokens
- **cryptography** - Cifrado AES-256

### Frontend
- **React 18** - Framework UI
- **Vite** - Build tool
- **Tailwind CSS** - Estilos
- **React Query** - Gestión de estado servidor
- **React Router** - Navegación
- **Chart.js / Recharts** - Visualización de datos
- **Axios** - Cliente HTTP

### DevOps
- **Docker & Docker Compose** - Contenedores
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker 20+
- Docker Compose 2+
- Node.js 18+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/VitaBrevis.git
cd VitaBrevis
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Iniciar con Docker Compose**
```bash
docker-compose up -d
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Desarrollo Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔐 Roles y Permisos

| Rol | Acceso |
|-----|--------|
| **Médico** | Acceso total a pacientes asignados |
| **Enfermería** | Acceso parcial (visualización y registro de datos) |
| **Recepción** | Solo datos administrativos |
| **Paciente** | Solo sus propios datos |
| **Dirección Médica** | Informes globales (datos anonimizados) |

## 📋 Módulos

### Core
- Autenticación y autorización
- Gestión de usuarios
- Auditoría y logging

### Clínicos
- Gestión de pacientes
- Biomarcadores clásicos
- Biomarcadores avanzados
- Composición corporal
- Rendimiento cognitivo
- Actividad física y estilo de vida

### Especializados
- Genética/ADN (solo visualización)
- Microbioma
- Epigenética
- Metabolómica
- Proteómica

### Administrativos
- Consentimientos
- Documentación
- Informes
- Timeline del paciente

## 📄 Documentación Legal Incluida

En `/docs/legal` encontrarás plantillas para:
- ✅ Registro de Actividades de Tratamiento (GDPR Art. 30)
- ✅ Evaluación de Impacto (DPIA)
- ✅ Política de Privacidad
- ✅ Política de Seguridad
- ✅ Procedimiento de Brechas de Seguridad
- ✅ Consentimientos (general, genética, biométricos)
- ✅ Derechos ARSOPL (Acceso, Rectificación, Supresión, Oposición, Portabilidad, Limitación)

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 🚀 Despliegue en Producción

Ver documentación completa en `/docs/technical/deployment.md`

Requisitos mínimos:
- Servidor con 4GB RAM, 2 CPUs
- PostgreSQL 15+ (recomendado managed service)
- Certificado SSL válido
- Backup automático configurado

## 🤝 Contribuir

Este es un proyecto privado para clínicas de longevidad. Si tienes acceso y quieres contribuir:

1. Crea una rama feature
2. Implementa tus cambios
3. Asegúrate de que los tests pasen
4. Crea un Pull Request

## 📜 Licencia

Propietario - Todos los derechos reservados

## 🆘 Soporte

Para soporte técnico o preguntas, contacta a: [tu-email@clinica.com]

## ⚠️ Disclaimer Legal

**VitaBrevis NO es un dispositivo médico regulado (SaMD)**

Esta plataforma:
- ✅ Solo visualiza y almacena datos
- ✅ No realiza diagnósticos
- ✅ No genera recomendaciones terapéuticas
- ✅ No interpreta resultados clínicos
- ✅ No sustituye el criterio médico profesional

El uso clínico de los datos debe ser siempre supervisado por profesionales sanitarios cualificados.

---

**Desarrollado con ❤️ para mejorar la longevidad humana**
