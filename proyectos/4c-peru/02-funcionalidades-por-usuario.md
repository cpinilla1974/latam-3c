# Funcionalidades por Grupo de Usuarios

**Fecha**: 2025-12-11
**Estado**: Esquema definitivo de roles y permisos

---

## Roles del Sistema

| # | Rol | Valor BD | Quién es | Qué puede ver | Qué puede hacer |
|---|-----|----------|----------|---------------|-----------------|
| 1 | Root | `ROOT` | Superadmin FICEM | Todo | Todo |
| 2 | Admin Proceso | `ADMIN_PROCESO` | Staff FICEM | Todo | Gestionar procesos, aprobar submissions |
| 3 | Ejecutivo FICEM | `EJECUTIVO_FICEM` | Directivo FICEM | Todo | Solo ver |
| 4 | Amigo FICEM | `AMIGO_FICEM` | Académico, consultor | Público + Amigos FICEM | Solo ver + API |
| 5 | Coordinador País | `COORDINADOR_PAIS` | Asociación nacional | Todo de su país | Solo ver + enviar recordatorios |
| 6 | Supervisor Empresa | `SUPERVISOR_EMPRESA` | Jefe en empresa | Su empresa + Amigos FICEM | Aprobar antes de enviar |
| 7 | Informante Empresa | `INFORMANTE_EMPRESA` | Empleado empresa | Su empresa + Amigos FICEM | Cargar datos |
| 8 | Visor Empresa | `VISOR_EMPRESA` | Empleado empresa | Su empresa + Amigos FICEM | Solo ver |

---

## 1. FICEM (Equipo Regional)

**Roles**: `ROOT`, `ADMIN_PROCESO`, `EJECUTIVO_FICEM`, `AMIGO_FICEM`

| # | Funcionalidad | ROOT | ADMIN_PROCESO | EJECUTIVO | AMIGO |
|---|--------------|------|---------------|-----------|-------|
| 1 | Gestionar usuarios | ✓ | ✓ | - | - |
| 2 | Gestionar procesos MRV | ✓ | ✓ | - | - |
| 3 | Aprobar submissions (final) | ✓ | ✓ | - | - |
| 4 | Ejecutar cálculos A1-A3 | ✓ | ✓ | - | - |
| 5 | Gestionar factores de emisión | ✓ | ✓ | - | - |
| 6 | Ver resultados LATAM | ✓ | ✓ | ✓ | - |
| 7 | Benchmarking regional | ✓ | ✓ | ✓ | ✓ |
| 8 | Eliminar procesos | ✓ | - | - | - |

**Interfaz requerida**: Sí (Streamlit en ficem-core + API REST)

---

## 2. País

**Rol**: `COORDINADOR_PAIS`

| # | Funcionalidad |
|---|--------------|
| 1 | Dashboard métricas país |
| 2 | Listado empresas del país |
| 3 | Ver estado de envíos (solo observar, NO aprueba) |
| 4 | Ver resultados cálculos empresas |
| 5 | Benchmarking nacional |
| 6 | Enviar recordatorios a empresas |

**Nota importante**: El coordinador país **observa** pero **no aprueba** envíos. La aprobación va: Empresa → FICEM directamente.

**Interfaz requerida**: Sí (4c-peru en Next.js)

---

## 3. Empresas Cementeras

**Roles**: `SUPERVISOR_EMPRESA`, `INFORMANTE_EMPRESA`, `VISOR_EMPRESA`

| # | Funcionalidad | SUPERVISOR | INFORMANTE | VISOR |
|---|--------------|------------|------------|-------|
| 1 | Descargar plantilla Excel | ✓ | ✓ | ✓ |
| 2 | Cargar Excel con datos | - | ✓ | - |
| 3 | Ver estado del envío | ✓ | ✓ | ✓ |
| 4 | Enviar a supervisor | - | ✓ | - |
| 5 | Aprobar envío interno | ✓ | - | - |
| 6 | Ver resultados de cálculos | ✓ | ✓ | ✓ |
| 7 | Descargar reporte individual | ✓ | ✓ | ✓ |
| 8 | Benchmarking (posición anónima) | ✓ | ✓ | ✓ |

**Interfaz requerida**: Acceso vía app país (4c-peru)

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
        │  │  • Revisar envíos, ejecutar cálculos    │ │
        │  │  • Gestión empresas/plantas/usuarios    │ │
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
    │ • Login empresa  │       │ • Login empresa  │
    │ • Carga Excel    │       │ • Carga Excel    │
    │ • Dashboard PE   │       │ • Dashboard CO   │
    │ • Revisión envíos│       │ • Revisión envíos│
    │ • Reportes PE    │       │ • Reportes CO    │
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
- rol (`ROOT`, `ADMIN_PROCESO`, `COORDINADOR_PAIS`, `INFORMANTE_EMPRESA`, etc.)
- pais (código país o "regional" para FICEM)
- empresa_id (para usuarios de empresa, null para otros)

---

## Notas

1. **FICEM Core es el único backend**: Centraliza datos, cálculos, usuarios y sesiones
2. **Cada país es solo frontend**: Consume APIs de ficem-core, sin backend propio
3. **Datos por país**: Almacenados en ficem-core con esquemas/tablas separadas
4. **knowledge-api crece después**: Cuando se contrate, se integra como servicio adicional
5. **Las empresas acceden vía app país**: No tienen app propia
6. **Coordinador país solo observa**: No aprueba envíos, la aprobación es Empresa → FICEM

---

**Última actualización**: 2025-12-11
**Decisión tomada**: 2025-12-10
