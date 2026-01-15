# LATAM-3C: Centro de Coordinación de Proyectos FICEM

Este repositorio es el **centro de comando y coordinación** para todos los proyectos/contratos con FICEM relacionados con la plataforma de medición y reporte de emisiones en la industria cementera de Latinoamérica.

## Estructura del Repositorio

### `/contratos/`
Gestión comercial y administrativa de contratos con FICEM.

- **peru-2025/** - Contrato vigente: 4C-Peru + FICEM Core + Web FICEM
  - `admin/` - TDRs, propuestas técnicas, planes de trabajo

- **cognos-2026/** - Nuevo contrato (a formular): Módulos de conocimiento con IA

### `/proyectos/`
Documentación técnica específica de cada proyecto de software.

- **4c-peru/** - Especificaciones técnicas del frontend Perú
  - Funcionalidades por usuario
  - Estructura de contenidos
  - Metodología MRV Perú
  - [Repo: github.com/cpinilla1974/4c-peru](https://github.com/cpinilla1974/4c-peru)

- **ficem-core/** - Especificaciones del backend centralizado
  - Arquitectura técnica
  - APIs y endpoints
  - Motor de procesos MRV
  - [Repo: github.com/cpinilla1974/4c-ficem-core](https://github.com/cpinilla1974/4c-ficem-core)

- **ficem-cognos/** - Módulos de conocimiento con IA
  - Documentación de pilotos IA
  - Casos de uso RAG
  - Optimización de modelos

### `/prototipos/`
Código experimental y prototipos temporales.

- **v0/** - Prototipo inicial (Streamlit básico)
- **v1/** - Segunda iteración (Streamlit + IA + Base datos)
- **data_peru/** - Sistema de análisis de datos del sector cemento Perú (TDR Item 2)
- **data/** - Datos de ejemplo (ACME, Cementos Andinos)

### `/docs/`
Recursos compartidos entre todos los proyectos.

- **arquitectura-global/** - Arquitectura transversal de la plataforma
  - Modelo de datos unificado
  - Flujo de datos general
  - Validaciones del sistema
  - Axiomas y decisiones arquitectónicas

- **metodologia/** - Metodología y procesos
  - Diagramas de flujo (Mermaid)
  - Características del sistema
  - Scripts y herramientas

- **referencias/** - Material de consulta
  - Análisis e informes
  - Benchmarking GCCA
  - Documentación técnica externa
  - Versiones históricas

### Sesiones de Trabajo

Las sesiones de trabajo se documentan en:
```
/home/cpinilla/projects/gestion/proyectos/latam-3c/sesiones/
```

Formato: `YYYY-MM-DD.md`

## Arquitectura Multi-Repositorio

Este proyecto coordina múltiples repositorios de software:

```
latam-3c (este repo)          ← Centro de coordinación
    ├── Documentación
    ├── Gestión de contratos
    └── Decisiones de arquitectura

4c-ficem-core                 ← Backend centralizado
    ├── Motor de cálculos MRV
    ├── APIs REST
    └── Base de datos

4c-peru                       ← Frontend Perú
    ├── Dashboards
    ├── Reportes
    └── Visualizaciones
```

## Metodología de Documentación

### Principios
1. **Solo lo esencial** - Documentar únicamente lo discutido y acordado
2. **Bloques de construcción** - Cada documento debe ser necesario y suficiente
3. **Sin opciones** - Las opciones son para discusión, no para documentar
4. **Conciso y efectivo** - Evitar documentos extensos

### Qué documentar
- ✅ Estructuras de datos acordadas
- ✅ Decisiones técnicas tomadas
- ✅ Especificaciones funcionales definidas
- ✅ Código y configuraciones necesarias

### Qué NO documentar
- ❌ Listas de opciones no decididas
- ❌ Planes tentativos sin discutir
- ❌ Recomendaciones no solicitadas
- ❌ Información redundante o especulativa

## Convenciones

### Política de Comunicación
- NUNCA usar regionalismos argentinos
- SIEMPRE usar español neutro profesional

### Política de Commits
- NUNCA incluir a Claude como autor
- Los commits deben aparecer como del usuario únicamente

## Navegación Rápida

- Contrato Peru actual: [contratos/peru-2025/admin/](contratos/peru-2025/admin/)
- Arquitectura global: [docs/arquitectura-global/](docs/arquitectura-global/)
- Specs 4C-Peru: [proyectos/4c-peru/](proyectos/4c-peru/)
- Specs FICEM Core: [proyectos/ficem-core/](proyectos/ficem-core/)
- Prototipos: [prototipos/](prototipos/)
