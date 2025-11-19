"""
VitaBrevis - Main Application
Plataforma de Gestión para Clínicas de Longevidad
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import engine, Base
from app.api.endpoints import auth, users, patients, biomarkers, genetic, microbiome

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# RATE LIMITER
# ============================================

limiter = Limiter(key_func=get_remote_address)


# ============================================
# LIFESPAN EVENTS
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación
    """
    # Startup
    logger.info("🚀 Starting VitaBrevis API...")

    # Crear tablas si no existen (en producción usar Alembic)
    if settings.ENVIRONMENT == "development":
        logger.info("📊 Creating database tables...")
        Base.metadata.create_all(bind=engine)

    logger.info("✅ VitaBrevis API started successfully")

    yield

    # Shutdown
    logger.info("👋 Shutting down VitaBrevis API...")


# ============================================
# APLICACIÓN FASTAPI
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de Gestión para Clínicas de Longevidad - Cumplimiento GDPR/LOPDGDD",
    version=settings.VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# Añadir rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ============================================
# MIDDLEWARES
# ============================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Request-ID"],
)

# Trusted Host (prevención de Host Header Injection)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.vitabrevis.com", "vitabrevis.com"]
    )


# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para logging de todas las requests
    GDPR: Parte del registro de accesos
    """
    start_time = time.time()

    # Generar ID único para la request
    request_id = f"{int(time.time() * 1000)}"

    # Procesar request
    response = await call_next(request)

    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time

    # Log
    logger.info(
        f"Request: {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.3f}s | "
        f"IP: {request.client.host} | "
        f"ID: {request_id}"
    )

    # Añadir headers de respuesta
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Middleware de seguridad headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Añade headers de seguridad a todas las respuestas
    OWASP Security Headers
    """
    response = await call_next(request)

    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# ============================================
# EXCEPTION HANDLERS
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler personalizado para errores de validación
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Error de validación en los datos enviados"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handler global para excepciones no capturadas
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Error interno del servidor",
            "detail": str(exc) if settings.DEBUG else "Contacte con el administrador"
        }
    )


# ============================================
# ROUTERS
# ============================================

# Importar y registrar routers
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    patients.router,
    prefix="/api/patients",
    tags=["Patients"]
)

app.include_router(
    biomarkers.router,
    prefix="/api/biomarkers",
    tags=["Biomarkers"]
)

app.include_router(
    genetic.router,
    prefix="/api/genetic",
    tags=["Genetic Data"]
)

app.include_router(
    microbiome.router,
    prefix="/api/microbiome",
    tags=["Microbiome"]
)


# ============================================
# ENDPOINTS RAÍZ
# ============================================

@app.get("/")
async def root():
    """
    Endpoint raíz - información de la API
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.ENVIRONMENT != "production" else None,
        "legal_compliance": [
            "GDPR (Reglamento General de Protección de Datos - UE)",
            "LOPDGDD (Ley Orgánica de Protección de Datos - España)",
            "No es Software Médico Regulado (SaMD)"
        ]
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint para monitoring
    """
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/disclaimer")
async def legal_disclaimer():
    """
    Disclaimer legal de la plataforma
    """
    return {
        "disclaimer": {
            "es": (
                f"{settings.APP_NAME} NO es un dispositivo médico regulado (SaMD). "
                "Esta plataforma solo visualiza y almacena datos proporcionados por "
                "profesionales médicos y laboratorios. NO realiza diagnósticos, "
                "NO genera recomendaciones terapéuticas, y NO interpreta resultados clínicos. "
                "El uso clínico de los datos debe ser siempre supervisado por profesionales "
                "sanitarios cualificados."
            ),
            "en": (
                f"{settings.APP_NAME} is NOT a regulated medical device (SaMD). "
                "This platform only visualizes and stores data provided by "
                "medical professionals and laboratories. It does NOT perform diagnoses, "
                "does NOT generate therapeutic recommendations, and does NOT interpret clinical results. "
                "Clinical use of the data must always be supervised by qualified healthcare professionals."
            )
        },
        "data_protection": {
            "gdpr_compliant": True,
            "lopdgdd_compliant": True,
            "encryption": "AES-256",
            "audit_log_retention": "7 years"
        }
    }


# ============================================
# DESARROLLO - Seed data
# ============================================

# TODO: Implementar seed_service para datos de demostración
# if settings.CREATE_DEMO_DATA and settings.ENVIRONMENT == "development":
#     @app.get("/api/dev/seed-data")
#     async def seed_demo_data():
#         """
#         SOLO DESARROLLO: Crea datos de demostración
#         """
#         from app.services.seed_service import create_demo_data
#
#         try:
#             create_demo_data()
#             return {"message": "Demo data created successfully"}
#         except Exception as e:
#             logger.error(f"Error creating demo data: {str(e)}")
#             return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
