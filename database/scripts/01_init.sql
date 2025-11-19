-- ============================================
-- VitaBrevis - Inicialización de Base de Datos
-- ============================================

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Configurar timezone UTC
SET timezone = 'UTC';

-- ============================================
-- Triggers para Auditoría
-- ============================================

-- Función para prevenir modificación de audit_logs
CREATE OR REPLACE FUNCTION prevent_audit_log_modification()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'No se pueden modificar o eliminar registros de auditoría';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Se aplicará cuando se cree la tabla audit_logs
-- CREATE TRIGGER prevent_update_audit_logs
--     BEFORE UPDATE OR DELETE ON audit_logs
--     FOR EACH ROW EXECUTE FUNCTION prevent_audit_log_modification();

-- ============================================
-- Función para updated_at automático
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Configuración de Roles (opcional)
-- ============================================

-- Crear rol de solo lectura para informes
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'vitabrevis_readonly') THEN
        CREATE ROLE vitabrevis_readonly;
    END IF;
END
$$;

-- ============================================
-- Comentarios
-- ============================================

COMMENT ON DATABASE vitabrevis_db IS 'Base de datos de VitaBrevis - Plataforma de Gestión de Clínicas de Longevidad';
COMMENT ON EXTENSION pgcrypto IS 'Extensión para cifrado de datos sensibles';

-- ============================================
-- Configuración de Performance
-- ============================================

-- Aumentar shared_buffers si es posible (debe configurarse en postgresql.conf)
-- shared_buffers = 256MB

-- Statement timeout para prevenir queries largas
ALTER DATABASE vitabrevis_db SET statement_timeout = '30s';

-- ============================================
-- Logging
-- ============================================

ALTER DATABASE vitabrevis_db SET log_statement = 'mod'; -- Log INSERT, UPDATE, DELETE
ALTER DATABASE vitabrevis_db SET log_duration = on;

-- ============================================
-- Fin de Inicialización
-- ============================================

SELECT 'VitaBrevis Database Initialized Successfully!' AS status;
