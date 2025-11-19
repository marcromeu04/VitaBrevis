# Guía de Contribución
## VitaBrevis - Plataforma de Gestión para Clínicas de Longevidad

¡Gracias por tu interés en contribuir a VitaBrevis!

---

## 🤝 Cómo Contribuir

### 1. Fork y Clonar

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/tu-usuario/VitaBrevis.git
cd VitaBrevis
```

### 2. Crear una Rama

```bash
# Crear rama feature
git checkout -b feature/nueva-funcionalidad

# Crear rama bugfix
git checkout -b bugfix/corregir-error
```

### 3. Hacer Cambios

- Escribe código limpio y documentado
- Sigue las convenciones de estilo
- Añade tests si es posible
- Actualiza documentación si es necesario

### 4. Commit

```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

**Convención de commits:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formateo, sin cambios de código
- `refactor:` Refactorización
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

### 5. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego abre un Pull Request en GitHub.

---

## 📋 Estándares de Código

### Backend (Python)

- **PEP 8** para estilo
- **Type hints** cuando sea posible
- **Docstrings** en funciones importantes
- **Black** para formateo automático

```bash
# Formatear código
black backend/

# Lint
flake8 backend/
```

### Frontend (JavaScript)

- **ESLint** configurado
- Componentes funcionales con hooks
- Nombres descriptivos de variables
- Comentarios cuando sea necesario

```bash
# Lint
npm run lint
```

---

## 🧪 Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

---

## 🔒 Seguridad

**IMPORTANTE:** Si encuentras una vulnerabilidad de seguridad:

- **NO** abras un issue público
- Envía un email a: security@vitabrevis.com
- Incluye descripción detallada
- Recibirás respuesta en 48 horas

---

## ⚖️ Consideraciones Legales

Al contribuir, ten en cuenta:

- ✅ **GDPR/LOPDGDD compliance** es obligatorio
- ✅ **NO añadir funcionalidades de diagnóstico** (mantener fuera de SaMD)
- ✅ **Cifrado de datos sensibles**
- ✅ **Logging de auditoría** para cambios importantes
- ✅ **No incluir datos reales** de pacientes en ejemplos

---

## 📝 Pull Request Checklist

Antes de enviar tu PR, verifica:

- [ ] El código compila sin errores
- [ ] Los tests pasan
- [ ] La documentación está actualizada
- [ ] Los commits tienen mensajes descriptivos
- [ ] No hay credenciales o secretos en el código
- [ ] Se mantiene compatibilidad con versiones anteriores
- [ ] Se respeta la privacidad de datos (GDPR)

---

## 🎯 Áreas donde Contribuir

### Alto Impacto

- 🔐 Mejoras de seguridad
- 📊 Nuevos tipos de biomarcadores
- 📈 Visualizaciones de datos
- 📱 Responsive design

### Fácil para Comenzar

- 📝 Mejorar documentación
- 🐛 Corregir bugs menores
- 🎨 Mejorar UI/UX
- 🌍 Traducción a otros idiomas

---

## 💬 Comunicación

- **GitHub Issues:** Para bugs y features
- **GitHub Discussions:** Para preguntas generales
- **Email:** contribute@vitabrevis.com

---

## 📜 Licencia

Al contribuir, aceptas que tu código se licencie bajo la misma licencia del proyecto.

---

¡Gracias por contribuir a VitaBrevis! 🎉
