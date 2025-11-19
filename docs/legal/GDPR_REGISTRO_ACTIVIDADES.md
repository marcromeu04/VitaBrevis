# Registro de Actividades de Tratamiento (RAT)
## Artículo 30 GDPR

**Responsable del Tratamiento:** [Nombre de la Clínica de Longevidad]
**Delegado de Protección de Datos (DPO):** [Nombre y contacto]
**Fecha:** 2024
**Versión:** 1.0

---

## 1. Identificación del Responsable

- **Nombre:** [Clínica de Longevidad S.L.]
- **CIF:** [B12345678]
- **Dirección:** [Dirección completa]
- **Teléfono:** [+34 XXX XXX XXX]
- **Email:** [dpo@clinica.com]
- **Representante (si aplicable):** [Nombre]

---

## 2. Actividades de Tratamiento

### 2.1. Gestión de Pacientes

**Finalidad del tratamiento:**
- Prestación de servicios médicos de longevidad
- Gestión de historia clínica digital
- Seguimiento de programas de longevidad

**Base jurídica (Art. 6 GDPR):**
- **Ejecución de contrato** (Art. 6.1.b): Prestación de servicios médicos
- **Consentimiento explícito** (Art. 6.1.a y Art. 9.2.a): Datos de salud
- **Interés vital** (Art. 6.1.d): Protección de intereses vitales
- **Obligación legal** (Art. 6.1.c): Conservación de historia clínica (Ley 41/2002)

**Categorías de datos personales:**

**Datos básicos:**
- Nombre, apellidos
- Fecha de nacimiento
- DNI/NIE
- Dirección, teléfono, email
- Número de historia clínica

**Datos de salud (Art. 9 GDPR - categoría especial):**
- Biomarcadores clínicos (glucosa, lípidos, hormonas, etc.)
- Biomarcadores avanzados (edad epigenética, telómeros, metabolómica)
- Datos de composición corporal (bioimpedancia, DXA)
- Datos genéticos (SNPs, variantes, informes de laboratorios)
- Datos del microbioma
- Tests cognitivos no clínicos
- Datos de estilo de vida (actividad física, sueño)
- Historial médico

**Categorías de interesados:**
- Pacientes de la clínica
- Usuarios del sistema (médicos, enfermeras, recepcionistas)

**Destinatarios:**
- Personal médico autorizado de la clínica
- Laboratorios externos (solo datos necesarios)
- Servicios de hosting (datos pseudonimizados y cifrados)
- Servicios cloud (AWS/Azure con DPA firmado)

**Transferencias internacionales:**
- **NO** se realizan transferencias fuera del EEE
- Si se usan servicios cloud US: Solo con cláusulas contractuales tipo de la UE

**Plazos de conservación:**
- **Historias clínicas:** Mínimo 5 años desde alta del paciente (Ley 41/2002)
- **Datos genéticos:** Hasta revocación de consentimiento
- **Logs de auditoría:** 7 años (requisito LOPDGDD para historia clínica digital)
- **Datos fiscales:** 6 años (Ley tributaria)

**Medidas de seguridad técnicas y organizativas:**

**Cifrado:**
- AES-256 en reposo para datos de salud
- TLS 1.2+ en tránsito
- Hashing de contraseñas con Argon2

**Control de acceso:**
- Autenticación robusta (contraseñas fuertes + 2FA opcional)
- RBAC (Control de acceso basado en roles)
- Registro de todos los accesos (LOPDGDD obligatorio)

**Pseudonimización:**
- Separación de datos identificativos de datos clínicos
- ID internos para relacionar datos

**Copias de seguridad:**
- Backup diario automático
- Cifrado de backups
- Retención de 90 días
- Pruebas de restauración trimestrales

**Auditoría:**
- Logs inmutables de todos los accesos
- Monitorización de actividad sospechosa
- Revisión trimestral de accesos

**Formación del personal:**
- Formación anual en protección de datos
- Acuerdos de confidencialidad firmados
- Política de escritorio limpio
- Política de contraseñas

---

### 2.2. Gestión de Usuarios del Sistema

**Finalidad del tratamiento:**
- Gestión de accesos al sistema
- Autenticación y autorización
- Auditoría de accesos

**Base jurídica:**
- Ejecución de contrato (relación laboral/profesional)
- Obligación legal (registro de accesos)

**Categorías de datos:**
- Nombre, apellidos, email
- Credenciales de acceso (hasheadas)
- Logs de acceso
- Rol profesional

**Plazos de conservación:**
- Datos de usuario: Durante relación laboral + 6 años
- Logs de acceso: 7 años

---

### 2.3. Consentimientos GDPR

**Finalidad del tratamiento:**
- Gestión de consentimientos
- Trazabilidad de permisos otorgados
- Cumplimiento del derecho a retirar consentimiento

**Base jurídica:**
- Obligación legal (Art. 7 GDPR)

**Categorías de datos:**
- Identificación del paciente
- Tipo de consentimiento
- Fecha de otorgamiento/revocación
- IP y user agent (para trazabilidad)
- Versión del documento de consentimiento

**Plazos de conservación:**
- Toda la vida del tratamiento + 7 años
- Nunca se eliminan (evidencia legal)

---

## 3. Evaluación de Impacto (DPIA)

Se ha realizado una Evaluación de Impacto relativa a la Protección de Datos (DPIA) según Art. 35 GDPR.

**Resultado:** Riesgo moderado, mitigado con las medidas de seguridad implementadas.

**Documentación:** Ver `DPIA_VitaBrevis.md`

---

## 4. Registro de Brechas de Seguridad

Se mantiene un registro de todas las brechas de seguridad según Art. 33 y 34 GDPR.

**Procedimiento:** Ver `PROCEDIMIENTO_BRECHAS.md`

---

## 5. Derechos de los Interesados (ARSOPL)

Los interesados pueden ejercer los siguientes derechos:

- **Acceso** (Art. 15): Obtener copia de sus datos
- **Rectificación** (Art. 16): Corregir datos inexactos
- **Supresión** (Art. 17): "Derecho al olvido"
- **Oposición** (Art. 21): Oponerse al tratamiento
- **Portabilidad** (Art. 20): Recibir datos en formato estructurado
- **Limitación** (Art. 18): Solicitar limitación del tratamiento

**Plazo de respuesta:** Máximo 1 mes (prorrogable 2 meses más si es complejo)

**Procedimiento:** Ver `PROCEDIMIENTO_DERECHOS_ARSOPL.md`

---

## 6. Encargados del Tratamiento

### 6.1. Servicios de Hosting

**Proveedor:** [Nombre del proveedor de hosting]
**Ubicación:** UE
**DPA firmado:** Sí
**Fecha:** [Fecha]

**Medidas de seguridad:**
- Cifrado en reposo y en tránsito
- Backup diario
- Certificación ISO 27001

### 6.2. Servicios de Email

**Proveedor:** [Gmail / Otro]
**DPA firmado:** Sí
**Uso:** Solo para notificaciones no sensibles

---

## 7. Revisiones

Este documento debe revisarse:
- **Anualmente**
- Cuando haya cambios en los tratamientos
- Cuando haya cambios normativos

**Última revisión:** [Fecha]
**Próxima revisión:** [Fecha + 1 año]

---

## 8. Aprobación

**Responsable del Tratamiento:**
Nombre: [Nombre]
Cargo: [Cargo]
Firma: _______________
Fecha: _______________

**Delegado de Protección de Datos:**
Nombre: [Nombre DPO]
Firma: _______________
Fecha: _______________
