# Guía de Despliegue - VitaBrevis
## Plataforma de Gestión para Clínicas de Longevidad

---

## 🚀 Inicio Rápido con Docker

### Prerrequisitos

- Docker 20+
- Docker Compose 2+
- 4GB RAM mínimo
- 20GB espacio en disco

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/VitaBrevis.git
cd VitaBrevis
```

### Paso 2: Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` y configura:

```bash
# CRÍTICO: Cambia estos valores en producción
SECRET_KEY=<genera_con_openssl_rand_-hex_32>
ENCRYPTION_KEY=<genera_con_python_fernet>
DB_PASSWORD=<contraseña_segura>

# Email (opcional, para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=<app-password>

# Clínica
CLINIC_NAME=Mi Clínica de Longevidad
CLINIC_EMAIL=info@clinica.com
```

### Paso 3: Generar Claves de Seguridad

```bash
# Generar SECRET_KEY
openssl rand -hex 32

# Generar ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Paso 4: Iniciar con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL (puerto 5432)
- Backend FastAPI (puerto 8000)
- Frontend React (puerto 3000)

### Paso 5: Acceder a la Aplicación

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Paso 6: Crear Usuario Admin

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Ejecutar script de creación de admin
python3 scripts/create_admin.py
```

---

## 🖥️ Desarrollo Local (sin Docker)

### Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar PostgreSQL local
createdb vitabrevis_db

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar desarrollo
npm run dev
```

---

## 🌐 Despliegue en Producción

### Opción 1: VPS (Recomendado para Europa)

**Proveedores compatibles GDPR:**
- Hetzner (Alemania)
- OVH (Francia)
- Scaleway (Francia)
- DigitalOcean (Frankfurt)

**Requisitos mínimos:**
- 4GB RAM
- 2 vCPUs
- 50GB SSD
- Ubuntu 22.04 LTS

### Configuración del Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar certbot para SSL
sudo apt install certbot python3-certbot-nginx -y

# Configurar firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/VitaBrevis.git
cd VitaBrevis

# Configurar .env
cp .env.example .env
nano .env
```

**Configuración de producción en `.env`:**

```bash
ENVIRONMENT=production
DEBUG=false

# Base de datos
DB_PASSWORD=<contraseña_muy_segura>

# Seguridad
SECRET_KEY=<clave_generada>
ENCRYPTION_KEY=<clave_generada>

# CORS
CORS_ORIGINS=https://vitabrevis.tudominio.com

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=noreply@tudominio.com
SMTP_PASSWORD=<app-password>

# Backup
BACKUP_ENABLED=true
```

### Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/vitabrevis
```

```nginx
server {
    listen 80;
    server_name vitabrevis.tudominio.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name vitabrevis.tudominio.com;

    # SSL certificates (certbot los generará)
    ssl_certificate /etc/letsencrypt/live/vitabrevis.tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vitabrevis.tudominio.com/privkey.pem;

    # Seguridad SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Headers de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Tamaño máximo de upload (para informes PDF)
    client_max_body_size 50M;
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/vitabrevis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Obtener certificado SSL
sudo certbot --nginx -d vitabrevis.tudominio.com
```

### Iniciar Aplicación

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Configurar Backups Automáticos

```bash
# Crear script de backup
sudo nano /usr/local/bin/backup-vitabrevis.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/vitabrevis"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup de base de datos
docker-compose exec -T db pg_dump -U vitabrevis vitabrevis_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup de uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C /path/to/vitabrevis backend/uploads

# Eliminar backups antiguos (más de 90 días)
find $BACKUP_DIR -name "*.gz" -mtime +90 -delete

echo "Backup completado: $DATE"
```

```bash
# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/backup-vitabrevis.sh

# Programar con cron (diario a las 2 AM)
sudo crontab -e
```

Añadir:
```
0 2 * * * /usr/local/bin/backup-vitabrevis.sh >> /var/log/vitabrevis-backup.log 2>&1
```

---

## 📊 Monitorización

### Logs

```bash
# Ver logs del backend
docker-compose logs -f backend

# Ver logs del frontend
docker-compose logs -f frontend

# Ver logs de base de datos
docker-compose logs -f db
```

### Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Base de datos
docker-compose exec db pg_isready
```

---

## 🔒 Seguridad Post-Despliegue

### Checklist de Seguridad

- [ ] Variables de entorno configuradas con valores únicos
- [ ] Certificado SSL válido (HTTPS)
- [ ] Firewall configurado
- [ ] Backups automáticos funcionando
- [ ] Contraseñas de base de datos seguras (>20 caracteres)
- [ ] SECRET_KEY y ENCRYPTION_KEY únicos
- [ ] CORS configurado solo con dominios permitidos
- [ ] Logs de auditoría habilitados
- [ ] Acceso SSH solo con clave (no password)
- [ ] Fail2ban instalado y configurado
- [ ] Actualizaciones automáticas de seguridad

### Actualizar Aplicación

```bash
cd VitaBrevis

# Hacer backup antes de actualizar
/usr/local/bin/backup-vitabrevis.sh

# Pull de cambios
git pull

# Reconstruir contenedores
docker-compose build

# Reiniciar con downtime mínimo
docker-compose up -d

# Verificar migraciones
docker-compose exec backend alembic upgrade head
```

---

## 🆘 Troubleshooting

### Error: No se puede conectar a la base de datos

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps db

# Ver logs de PostgreSQL
docker-compose logs db

# Verificar conectividad
docker-compose exec backend pg_isready -h db -U vitabrevis
```

### Error: CORS

Verifica que `CORS_ORIGINS` en `.env` incluye tu dominio:

```bash
CORS_ORIGINS=https://vitabrevis.tudominio.com,http://localhost:3000
```

### Error: Certificado SSL expirado

```bash
# Renovar certificado
sudo certbot renew

# Reiniciar nginx
sudo systemctl restart nginx
```

---

## 📞 Soporte

Para soporte técnico:
- Email: support@vitabrevis.com
- Documentación: https://docs.vitabrevis.com
- Issues: https://github.com/tu-usuario/VitaBrevis/issues

---

## ⚖️ Cumplimiento Legal

Recuerda que al desplegar esta plataforma debes:

✅ Completar el **Registro de Actividades de Tratamiento** (ver `docs/legal/GDPR_REGISTRO_ACTIVIDADES.md`)
✅ Realizar la **DPIA** (ver `docs/legal/DPIA_EVALUACION_IMPACTO.md`)
✅ Publicar la **Política de Privacidad**
✅ Obtener **consentimientos** de los pacientes
✅ Configurar **backups cifrados**
✅ Mantener **logs de auditoría** durante 7 años

---

© 2024 VitaBrevis - Cumplimiento GDPR/LOPDGDD
