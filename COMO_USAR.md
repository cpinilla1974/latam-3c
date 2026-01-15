# Cómo Usar Este Repositorio

Este repositorio **NO contiene código ejecutable**. Es el centro de coordinación para gestionar múltiples proyectos/contratos con FICEM.

## Para qué sirve este repo

### ✅ SÍ usar este repo para:
- Gestionar contratos y propuestas con FICEM
- Documentar decisiones de arquitectura global
- Coordinar entre proyectos (4c-peru, ficem-core, cognos)
- Mantener referencias técnicas compartidas
- Documentar sesiones de trabajo

### ❌ NO usar este repo para:
- Ejecutar código (usar repos de software específicos)
- Desarrollo de features (ir a 4c-ficem-core o 4c-peru)
- Deployment (cada proyecto tiene su propio deployment)

---

## Estructura y Navegación

### 1. Gestión de Contratos

**Dónde:** [contratos/](contratos/)

**Para qué:**
- Revisar TDRs y términos de referencia
- Consultar propuestas técnico-económicas
- Ver planes de trabajo aprobados
- Preparar nuevos contratos

**Ejemplo:**
```bash
# Ver TDR del contrato Perú vigente
cat contratos/peru-2025/admin/TDR_FICEM_ASOCEM_Proyecto_MRV_Peru_3.pdf

# Ver propuesta técnica
cat contratos/peru-2025/admin/propuesta-tecnico-economica-etapa1.md
```

### 2. Documentación Técnica de Proyectos

**Dónde:** [proyectos/](proyectos/)

**Para qué:**
- Entender especificaciones técnicas de cada proyecto
- Ver funcionalidades definidas
- Consultar APIs y arquitectura

**Estructura:**
```
proyectos/
├── 4c-peru/          # Specs del frontend Perú
├── ficem-core/       # Specs del backend centralizado
└── ficem-cognos/     # Specs de módulos IA
```

**Ejemplo:**
```bash
# Ver funcionalidades de 4C-Peru
cat proyectos/4c-peru/02-funcionalidades-por-usuario.md

# Ver arquitectura del core
cat proyectos/ficem-core/01-arquitectura-ficem-4c.md
```

### 3. Arquitectura Global

**Dónde:** [docs/arquitectura-global/](docs/arquitectura-global/)

**Para qué:**
- Entender el modelo de datos unificado
- Ver flujo de datos entre sistemas
- Consultar validaciones transversales
- Revisar axiomas del proyecto

**Ejemplo:**
```bash
# Ver modelo de datos
cat docs/arquitectura-global/04-modelo-datos.md

# Ver flujo de datos
cat docs/arquitectura-global/03-flujo-datos.md
```

### 4. Prototipos y Experimentación

**Dónde:** [prototipos/](prototipos/)

**Para qué:**
- Consultar código experimental
- Ver prototipos históricos (v0, v1)
- Acceder a scripts de análisis de datos

**Ejemplo:**
```bash
# Ver análisis de datos Perú
cd prototipos/data_peru/
python scripts/calcular_agregados_nacionales.py
```

### 5. Referencias Técnicas

**Dónde:** [docs/referencias/](docs/referencias/)

**Para qué:**
- Consultar estándares GCCA
- Ver análisis previos
- Acceder a documentación externa

---

## Flujos de Trabajo Comunes

### Iniciar un nuevo contrato

1. Crear carpeta en `contratos/NOMBRE-AÑO/`
2. Agregar TDR y propuesta inicial
3. Documentar en sesión usando `/documentar-sesion`

### Tomar decisiones de arquitectura global

1. Revisar `docs/arquitectura-global/axiomas-proyecto.md`
2. Discutir cambio propuesto
3. Actualizar documento correspondiente
4. Documentar decisión en sesión

### Coordinar entre proyectos

1. Identificar qué proyectos se afectan
2. Documentar cambio en `proyectos/PROYECTO/`
3. Si afecta a todos, documentar en `docs/arquitectura-global/`
4. Notificar en sesión

### Consultar estado de un proyecto

1. Revisar sesiones recientes: `/home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/`
2. Ver docs del proyecto: `proyectos/PROYECTO/`
3. Revisar contrato relacionado: `contratos/NOMBRE/`

---

## Documentación de Sesiones

**Ubicación:**
```
/home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/
```

**Cómo documentar:**
```bash
# Al finalizar trabajo
/documentar-sesion
```

La skill `/documentar-sesion` automáticamente:
- Detecta la fecha actual
- Crea o actualiza el archivo de sesión
- Mantiene historial incremental
- Documenta lo trabajado en el día

**Formato de archivo:** `YYYY-MM-DD.md`

**Qué incluye:**
- Qué se hizo
- Por qué se hizo
- Decisiones tomadas
- Contexto del problema
- Estado actual

---

## Relación con Otros Repositorios

### 4c-ficem-core
**URL:** https://github.com/cpinilla1974/4c-ficem-core

**Qué tiene:**
- Código del backend (FastAPI/Django)
- Motor de cálculos MRV
- APIs REST
- Base de datos

**Cuándo trabajar ahí:**
- Implementar nuevos cálculos
- Desarrollar APIs
- Modificar modelo de datos
- Corregir bugs del backend

### 4c-peru
**URL:** https://github.com/cpinilla1974/4c-peru

**Qué tiene:**
- Código del frontend (React/Streamlit)
- Dashboards interactivos
- Reportes MRV
- Visualizaciones

**Cuándo trabajar ahí:**
- Crear nuevas vistas
- Modificar dashboards
- Agregar reportes
- Corregir bugs del frontend

### latam-3c (este repo)
**Qué tiene:**
- Documentación de coordinación
- Gestión de contratos
- Arquitectura global
- Sesiones de trabajo

**Cuándo trabajar aquí:**
- Preparar propuestas
- Documentar decisiones globales
- Coordinar entre proyectos
- Mantener referencias

---

## Buenas Prácticas

### ✅ Hacer
- Documentar decisiones importantes
- Mantener contratos actualizados
- Usar `/documentar-sesion` regularmente
- Consultar arquitectura antes de implementar
- Mantener sesiones concisas y útiles

### ❌ No hacer
- Copiar código de otros repos aquí
- Duplicar documentación entre repos
- Documentar opciones no decididas
- Crear propuestas sin discutir primero

---

## Comandos Útiles

```bash
# Ver estructura del repo
tree -L 2 -d

# Buscar en documentación
grep -r "palabra" docs/

# Ver última sesión documentada
ls -lt /home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/ | head -5

# Ver commits recientes
git log --oneline -10

# Buscar archivo específico
find . -name "*arquitectura*"
```

---

## Preguntas Frecuentes

**P: ¿Dónde está el código para ejecutar?**
R: En los repos específicos: 4c-ficem-core (backend) o 4c-peru (frontend)

**P: ¿Dónde documento una nueva feature?**
R: Si es específica de un proyecto: en su repo. Si afecta a todos: aquí en arquitectura-global/

**P: ¿Cómo sé qué se trabajó ayer?**
R: Revisa `/home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/YYYY-MM-DD.md`

**P: ¿Dónde están los entregables para FICEM?**
R: En `contratos/NOMBRE/admin/` (propuestas, TDRs, planes)

**P: ¿Puedo ejecutar prototipos?**
R: Sí, están en `prototipos/v0/` o `prototipos/v1/` pero son código experimental

---

## Ayuda

Para más información, consulta:
- [README.md](README.md) - Visión general del repo
- [CLAUDE.md](CLAUDE.md) - Metodología de trabajo con Claude
- Sesiones recientes en `/home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/`
