# Evaluación de Impacto sobre la Protección de Datos (DPIA)
## Data Protection Impact Assessment - VitaBrevis

**Artículo 35 GDPR**

---

## 1. Información General

**Proyecto:** VitaBrevis - Plataforma de Gestión para Clínicas de Longevidad
**Responsable del Tratamiento:** [Nombre de la Clínica]
**Delegado de Protección de Datos:** [Nombre y contacto]
**Fecha de evaluación:** [Fecha]
**Versión:** 1.0

---

## 2. ¿Es necesaria una DPIA?

**SÍ**, porque el tratamiento cumple con los siguientes criterios del Art. 35.3 GDPR:

✅ **Evaluación sistemática y exhaustiva** de aspectos personales basada en tratamiento automatizado
✅ **Tratamiento a gran escala de categorías especiales de datos** (datos de salud - Art. 9 GDPR)
✅ **Tratamiento de datos genéticos** (Art. 9 GDPR)
✅ **Uso de nuevas tecnologías** (sistema digital de gestión de salud)

---

## 3. Descripción del Tratamiento

### 3.1. Naturaleza del Tratamiento

**Tipo de sistema:** Plataforma web de gestión clínica

**Tratamientos realizados:**
- Almacenamiento de historia clínica digital
- Gestión de biomarcadores clínicos y avanzados
- Almacenamiento de datos genéticos (sin interpretación)
- Gestión de datos del microbioma
- Seguimiento de composición corporal
- Tests cognitivos no clínicos
- Datos de estilo de vida

**Volumen de datos:**
- Aproximadamente [X] pacientes
- [X] registros de biomarcadores al mes
- Datos almacenados durante mínimo 5 años

### 3.2. Finalidad del Tratamiento

- Prestación de servicios médicos de longevidad
- Seguimiento longitudinal de pacientes
- Visualización de tendencias de salud
- Generación de informes descriptivos

**IMPORTANTE:** El sistema NO realiza:
- Diagnósticos médicos automatizados
- Recomendaciones terapéuticas
- Interpretación de datos genéticos
- Cálculo de riesgos de enfermedad

Por tanto, **NO es un Software Médico Regulado (SaMD)**.

### 3.3. Contexto del Tratamiento

- **Relación médico-paciente:** Sí, existe consentimiento informado
- **Expectativas razonables:** Los pacientes esperan que sus datos de salud estén seguros
- **Vulnerabilidad:** Datos de salud son especialmente sensibles
- **Número de interesados:** Aproximadamente [X] pacientes

---

## 4. Identificación de Riesgos

### 4.1. Riesgos para los Derechos y Libertades

| Riesgo | Probabilidad | Impacto | Nivel |
|--------|-------------|---------|-------|
| **Acceso no autorizado a datos de salud** | Media | Alto | **ALTO** |
| **Fuga de datos genéticos** | Baja | Muy Alto | **ALTO** |
| **Uso indebido de datos para discriminación** | Baja | Alto | **MEDIO** |
| **Pérdida de datos por fallo técnico** | Media | Alto | **ALTO** |
| **Suplantación de identidad** | Baja | Medio | **MEDIO** |
| **Violación de confidencialidad por empleados** | Baja | Alto | **MEDIO** |

### 4.2. Desglose de Riesgos Principales

#### Riesgo 1: Acceso no autorizado a datos de salud

**Descripción:**
Un atacante externo o interno podría acceder a datos de salud de pacientes sin autorización.

**Daños potenciales:**
- Violación de privacidad
- Discriminación (seguro, empleo)
- Daño psicológico
- Pérdida de confianza

**Fuentes del riesgo:**
- Vulnerabilidades en el sistema
- Credenciales comprometidas
- Ataques de fuerza bruta
- Ingeniería social

#### Riesgo 2: Fuga de datos genéticos

**Descripción:**
Datos genéticos podrían ser filtrados o hackeados.

**Daños potenciales:**
- Discriminación genética (prohibida por ley pero posible)
- Uso por terceros (aseguradoras, empleadores)
- Identificación de familiares (información indirecta)
- Imposible cambiar datos genéticos (permanentes)

**Fuentes del riesgo:**
- Backup no cifrado
- Transferencia insegura
- Acceso de proveedores externos

#### Riesgo 3: Pérdida de datos

**Descripción:**
Pérdida permanente de datos médicos por fallo técnico o desastre.

**Daños potenciales:**
- Interrupción de tratamiento médico
- Pérdida de histórico clínico
- Imposibilidad de ejercer derechos

**Fuentes del riesgo:**
- Fallo de hardware
- Corrupción de base de datos
- Desastre natural
- Ransomware

---

## 5. Medidas de Mitigación Implementadas

### 5.1. Medidas Técnicas

#### Cifrado
✅ **AES-256** para datos en reposo
✅ **TLS 1.2+** para datos en tránsito
✅ **Hashing Argon2** para contraseñas
✅ **Cifrado de backups**

#### Control de Acceso
✅ **RBAC** (Control basado en roles)
✅ **Autenticación robusta** (contraseñas fuertes)
✅ **2FA opcional**
✅ **Timeouts de sesión** (30 minutos)
✅ **Registro de todos los accesos** (obligatorio LOPDGDD)

#### Seguridad de la Aplicación
✅ **Cumplimiento OWASP Top 10**
✅ **Protección SQL Injection** (ORM SQLAlchemy)
✅ **Protección XSS** (sanitización de inputs)
✅ **Protección CSRF** (tokens)
✅ **Rate limiting** (anti-abuso)
✅ **Security headers** (X-Frame-Options, CSP, etc.)

#### Backups y Recuperación
✅ **Backup diario automático**
✅ **Retención 90 días**
✅ **Backups cifrados**
✅ **Pruebas de restauración trimestrales**
✅ **Almacenamiento en ubicación separada**

#### Auditoría
✅ **Logs inmutables** de todos los accesos
✅ **Retención logs: 7 años** (requisito legal)
✅ **Alertas de actividad sospechosa**
✅ **Revisión trimestral de logs**

### 5.2. Medidas Organizativas

#### Políticas y Procedimientos
✅ **Política de Privacidad** publicada
✅ **Política de Seguridad de la Información**
✅ **Procedimiento de Brechas de Seguridad**
✅ **Procedimiento de Derechos ARSOPL**
✅ **Política de Retención de Datos**

#### Personal
✅ **Formación anual en protección de datos**
✅ **Acuerdos de confidencialidad** firmados
✅ **Principio de mínimo privilegio**
✅ **Política de escritorio limpio**
✅ **Controles de acceso físico** a servidores

#### Contratos
✅ **DPA** (Data Processing Agreement) con proveedores
✅ **Cláusulas de confidencialidad**
✅ **Auditorías a encargados** (anuales)

#### Consentimiento
✅ **Consentimiento informado y explícito**
✅ **Consentimiento específico para datos genéticos**
✅ **Granularidad de consentimientos** (por tipo de dato)
✅ **Fácil revocación** (online)
✅ **Registro de consentimientos** con trazabilidad

### 5.3. Medidas de Privacidad por Diseño

✅ **Minimización de datos:** Solo se recogen datos necesarios
✅ **Pseudonimización:** Separación de datos identificativos
✅ **Anonimización:** Informes agregados sin identificación
✅ **Cifrado por defecto:** Todos los datos sensibles cifrados
✅ **Limitación de acceso:** Solo personal autorizado
✅ **Transparencia:** Información clara al paciente

---

## 6. Evaluación de Riesgos Residuales

Después de implementar las medidas de mitigación:

| Riesgo Original | Riesgo Residual |
|----------------|-----------------|
| Acceso no autorizado (ALTO) | **BAJO** |
| Fuga de datos genéticos (ALTO) | **BAJO** |
| Uso indebido (MEDIO) | **MUY BAJO** |
| Pérdida de datos (ALTO) | **BAJO** |
| Suplantación de identidad (MEDIO) | **MUY BAJO** |
| Violación por empleados (MEDIO) | **BAJO** |

**Conclusión:** Los riesgos residuales son **ACEPTABLES** con las medidas implementadas.

---

## 7. Consulta a Interesados

Se ha informado a los interesados mediante:
- ✅ Política de Privacidad accesible
- ✅ Información en formularios de consentimiento
- ✅ Comunicación directa en primera visita

Los pacientes han tenido oportunidad de:
- Hacer preguntas sobre el tratamiento
- Solicitar información adicional
- Ejercer sus derechos

---

## 8. Aprobación y Revisión

### 8.1. Aprobación

**Responsable del Tratamiento:**
Nombre: [Nombre]
Firma: _______________
Fecha: _______________

**Delegado de Protección de Datos:**
Nombre: [Nombre DPO]
Firma: _______________
Fecha: _______________

### 8.2. Revisión

Esta DPIA debe revisarse:
- **Anualmente**
- Cuando cambien los riesgos
- Cuando se añadan nuevas funcionalidades
- Cuando cambien las medidas de seguridad

**Próxima revisión:** [Fecha + 1 año]

---

## 9. Conclusión

✅ **La DPIA ha sido completada satisfactoriamente**

✅ **Los riesgos han sido identificados y mitigados**

✅ **No es necesaria consulta previa a la autoridad de control** (Art. 36 GDPR) porque los riesgos residuales son bajos

✅ **El proyecto puede proceder** con las medidas de seguridad implementadas

❗ **Es obligatorio revisar esta DPIA periódicamente**
