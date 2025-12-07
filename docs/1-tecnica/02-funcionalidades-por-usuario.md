# Funcionalidades por Grupo de Usuarios

**Fecha**: 2025-12-07
**Estado**: Documento base para decisiones de arquitectura

---

## Grupos de Usuarios

| Grupo | Alcance | Descripción |
|-------|---------|-------------|
| **FICEM** | Regional (LATAM) | Equipo técnico regional, gestiona datos de todos los países |
| **País** | Nacional | Stakeholders nacionales (gremio, gobierno, coordinadores) |
| **Empresas** | Individual | Personal de empresas cementeras con diferentes roles |
| **IA/Analítica** | Transversal | Servicio consumido por todos los grupos |

---

## 1. FICEM (Equipo Regional)

**Roles posibles**: Operador, Administrador, Analista

| # | Funcionalidad |
|---|--------------|
| 1 | Cargar archivos Excel de empresas |
| 2 | Validar datos (estructura, formato, coherencia) |
| 3 | Ejecutar cálculos A1-A3 (clinker, cemento, concreto) |
| 4 | Clasificar GCCA (bandas A-G, AA-F) |
| 5 | Gestionar factores de emisión por país/año |
| 6 | Generar plantillas Excel personalizadas |
| 7 | Ver resultados consolidados LATAM |
| 8 | Gestionar empresas/plantas |
| 9 | Monitorear procesamiento |
| 10 | Benchmarking regional (anónimo) |

**Interfaz requerida**: Sí (app completa con frontend)

---

## 2. País (ej: Perú - ASOCEM + PRODUCE + particularidades)

**Roles posibles**: Coordinador gremio, Funcionario gobierno, Analista país, Observador

| # | Funcionalidad |
|---|--------------|
| 1 | Dashboard métricas país |
| 2 | Listado empresas del país |
| 3 | Descargar plantillas Excel |
| 4 | Ver resultados cálculos empresas |
| 5 | Benchmarking nacional |
| 6 | Generar reportes país |
| 7 | Coordinación con FICEM para validación |
| 8 | Funcionalidades específicas según TDR local |

**Nota**: Cada país tendrá sus propios stakeholders (gobierno, gremio, etc.) con requisitos específicos. Ejemplo Perú: ASOCEM (gremio) + PRODUCE (gobierno) + TDR específico.

**Interfaz requerida**: Sí (app específica por país)

---

## 3. Empresas Cementeras

**Roles posibles**: Editor (carga datos), Supervisor (revisa/aprueba), Observador (solo lectura)

| # | Funcionalidad |
|---|--------------|
| 1 | Descargar plantilla Excel |
| 2 | Cargar datos de la empresa |
| 3 | Ver sus resultados de cálculos |
| 4 | Ver su posición en benchmarking (anónimo) |
| 5 | Recibir reporte individual |
| 6 | Aprobar/rechazar envíos (supervisores) |

**Interfaz requerida**: Acceso limitado (dentro de app país o portal futuro)

---

## 4. IA/Analítica (knowledge-api)

**Nota**: No es un grupo de usuarios, es un servicio transversal consumido por los otros grupos.

| # | Funcionalidad |
|---|--------------|
| 1 | Chat sobre datos (RAG) |
| 2 | Generación de insights automáticos |
| 3 | Predicción de huella |
| 4 | Generación de reportes IA |
| 5 | Módulo de usuarios/autenticación |

**Interfaz requerida**: No (servicio API consumido por otras apps)

---

## Arquitectura Resultante

Basado en las funcionalidades y considerando que es un solo desarrollador:

### Decisión: Backend Centralizado + Frontends por App

| Repo | Tipo | Tecnología | Estado |
|------|------|------------|--------|
| **4c-ficem-core** | Backend centralizado + Frontend operador | FastAPI + PostgreSQL + Streamlit | Activo |
| **4c-peru** | Frontend país | Next.js | Activo |
| **4c-{pais}** | Frontend país (futuro) | Next.js | Futuro |
| **knowledge-api** | Servicio IA | FastAPI + Vector DB | En espera (POC existe) |
| **latam-3c** | Documentación | Markdown | Mantenimiento |

### Justificación

1. **Backend centralizado en ficem-core**: Menos código que mantener, un solo lugar para usuarios/sesiones, datos por país en esquemas separados
2. **knowledge-api separado**: No está contratado aún, debe poder crecer/venderse independiente cuando se contrate
3. **Frontends en Next.js**: Mejor manejo de usuarios/sesiones que Streamlit, interfaces más flexibles

---

## Diagrama de Relaciones

```
                    ┌─────────────────────────┐
                    │     knowledge-api       │
                    │  (IA, RAG - en espera)  │
                    └───────────┬─────────────┘
                                │ APIs (futuro)
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
        │              4c-ficem-core                    │
        │         (Backend Centralizado)                │
        │                                               │
        │  ┌─────────────────────────────────────────┐ │
        │  │ FastAPI:                                │ │
        │  │  • APIs datos/cálculos                  │ │
        │  │  • APIs por país (datos PE, CO...)      │ │
        │  │  • Usuarios/sesiones                    │ │
        │  └─────────────────────────────────────────┘ │
        │  ┌─────────────────────────────────────────┐ │
        │  │ PostgreSQL:                             │ │
        │  │  • Esquemas por país                    │ │
        │  │  • Datos regionales                     │ │
        │  └─────────────────────────────────────────┘ │
        │  ┌─────────────────────────────────────────┐ │
        │  │ Streamlit (Operador FICEM):             │ │
        │  │  • Carga Excel, validación, cálculos    │ │
        │  │  • Gestión empresas/plantas             │ │
        │  └─────────────────────────────────────────┘ │
        └───────────────────┬───────────────────────────┘
                            │ APIs REST
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
    ┌──────────────────┐       ┌──────────────────┐
    │    4c-peru       │       │   4c-colombia    │
    │    (Next.js)     │       │    (futuro)      │
    │                  │       │                  │
    │ • Dashboard PE   │       │ • Dashboard CO   │
    │ • Empresas PE    │       │ • Empresas CO    │
    │ • Reportes PE    │       │ • Reportes CO    │
    │ • TDR PRODUCE    │       │ • TDR local      │
    └──────────────────┘       └──────────────────┘
```

---

## Autenticación

**Decisión: JWT centralizado en ficem-core**

- ficem-core emite y valida tokens JWT
- Los frontends (4c-peru, etc.) no gestionan usuarios, solo consumen el token
- Sin dependencias externas (Auth0, etc.)

**Flujo:**
```
Usuario → Frontend (login form)
              ↓
         POST /api/auth/login → ficem-core
              ↓
         ficem-core valida credenciales en PostgreSQL
              ↓
         Retorna JWT + refresh token
              ↓
         Frontend guarda en cookie httpOnly
              ↓
         Cada request incluye JWT en header Authorization
```

**Contenido del JWT:**
- user_id
- email
- rol (operador, coordinador, editor, etc.)
- grupo (ficem, pais, empresa)
- pais_code (PE, CO, etc.) - para usuarios de país/empresa
- empresa_id - para usuarios de empresa

---

## Notas

1. **FICEM Core es el único backend**: Centraliza datos, cálculos, usuarios y sesiones
2. **Cada país es solo frontend**: Consume APIs de ficem-core, sin backend propio
3. **Datos por país**: Almacenados en ficem-core con esquemas/tablas separadas
4. **knowledge-api crece después**: Cuando se contrate, se integra como servicio adicional
5. **Las empresas acceden vía app país**: No tienen app propia

---

**Última actualización**: 2025-12-07
**Decisión tomada**: 2025-12-07
