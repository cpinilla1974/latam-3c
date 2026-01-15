# Flujo de Datos - Sistema 4C

**Fecha**: 2025-12-11
**Estado**: Vigente

> **Nota histórica**: Este documento reemplaza a `docs/4-historico/v1/03-flujo-datos_HASTA_2025-12-11.md`.

---

## Resumen

Las empresas cargan sus datos directamente a través de la app país (4c-peru, etc.), que actúa como frontend. El backend centralizado (ficem-core) procesa, valida y calcula. **Flujo de doble aprobación**: Empresa → FICEM (el coordinador país solo observa).

---

## Actores

| Actor | Rol BD | Descripción | App que usa |
|-------|--------|-------------|-------------|
| **Informante** | `INFORMANTE_EMPRESA` | Carga datos de la empresa | 4c-peru |
| **Supervisor** | `SUPERVISOR_EMPRESA` | Aprueba envío interno | 4c-peru |
| **Visor** | `VISOR_EMPRESA` | Solo lectura | 4c-peru |
| **Coordinador País** | `COORDINADOR_PAIS` | Observa (no aprueba) | 4c-peru |
| **Admin Proceso** | `ADMIN_PROCESO` | Aprueba final, ejecuta cálculos | ficem-core |
| **Root** | `ROOT` | Superadmin | ficem-core |

---

## Estados del Submission

| Estado | Descripción | Quién actúa siguiente |
|--------|-------------|----------------------|
| `BORRADOR` | Informante trabajando | Informante Empresa |
| `ENVIADO` | Informante envió a supervisor | Supervisor Empresa |
| `APROBADO_EMPRESA` | Supervisor empresa aprobó | Admin FICEM |
| `EN_REVISION_FICEM` | Admin FICEM revisando | Admin FICEM |
| `APROBADO_FICEM` | Admin FICEM aprobó (final) | Sistema (cálculos) |
| `RECHAZADO_EMPRESA` | Supervisor rechazó | Informante (corrige) |
| `RECHAZADO_FICEM` | Admin FICEM rechazó | Supervisor (corrige) |
| `PUBLICADO` | Visible públicamente | - |
| `ARCHIVADO` | Histórico | - |

---

## Flujo de Aprobación (Doble)

```
Informante carga datos
       ↓
    [BORRADOR]
       ↓
Informante envía a supervisor
       ↓
    [ENVIADO]
       ↓
Supervisor Empresa aprueba
       ↓
 [APROBADO_EMPRESA]
       ↓
Admin Proceso FICEM aprueba
       ↓
  [APROBADO_FICEM]
       ↓
   [PUBLICADO]

Coordinador País observa todo el flujo (no aprueba)
```

## Flujo Técnico Completo

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ INFORMANTE  │     │  4c-peru    │     │ ficem-core  │     │ADMIN_PROCESO│
│  (empresa)  │     │ (frontend)  │     │  (backend)  │     │   (FICEM)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │ 1. Login          │                   │                   │
       │──────────────────>│                   │                   │
       │                   │ POST /auth/login  │                   │
       │                   │──────────────────>│                   │
       │                   │<── JWT ───────────│                   │
       │                   │                   │                   │
       │ 2. Descarga template                  │                   │
       │──────────────────>│ GET /templates    │                   │
       │                   │──────────────────>│                   │
       │<── Excel ─────────│<── Excel ─────────│                   │
       │                   │                   │                   │
       │ 3. Completa offline                   │                   │
       │ (...tiempo...)    │                   │                   │
       │                   │                   │                   │
       │ 4. Sube Excel     │                   │                   │
       │──────────────────>│ POST /uploads     │                   │
       │                   │──────────────────>│ [BORRADOR]        │
       │                   │<── validación ────│                   │
       │<── errores/ok ────│                   │                   │
       │                   │                   │                   │
       │ 5. Envía a supervisor                 │                   │
       │──────────────────>│ POST /submit      │                   │
       │                   │──────────────────>│ [ENVIADO]         │
       │                   │                   │                   │
       │                   │                   │                   │
┌──────┴──────┐            │                   │                   │
│ SUPERVISOR  │            │                   │                   │
│  (empresa)  │            │                   │                   │
└──────┬──────┘            │                   │                   │
       │ 6. Aprueba interno│                   │                   │
       │──────────────────>│ POST /approve     │                   │
       │                   │──────────────────>│[APROBADO_EMPRESA] │
       │                   │                   │                   │
       │                   │                   │ 7. Admin revisa   │
       │                   │                   │──────────────────>│
       │                   │                   │                   │
       │                   │                   │ 8. Aprueba final  │
       │                   │                   │<──────────────────│
       │                   │                   │ [APROBADO_FICEM]  │
       │                   │                   │                   │
       │                   │                   │ 9. Cálculos       │
       │                   │                   │ (A1-A3, GCCA)     │
       │                   │                   │ [PUBLICADO]       │
       │                   │                   │                   │
       │ 10. Ve resultados │                   │                   │
       │──────────────────>│ GET /results      │                   │
       │                   │──────────────────>│                   │
       │<── dashboard ─────│<── datos ─────────│                   │
```

---

## Pasos Detallados

### 1. Login
- Empresa accede a 4c-peru
- Ingresa credenciales
- ficem-core valida y retorna JWT
- Frontend guarda token en cookie httpOnly

### 2. Descarga Template
- Empresa solicita plantilla Excel
- ficem-core genera Excel personalizado según perfil (integrada/molienda/concreto)
- Empresa descarga

### 3. Completado Offline
- Empresa completa Excel con datos de producción
- No requiere conexión a internet
- Validación interna por la empresa

### 4. Carga de Excel
- Empresa sube archivo a 4c-peru
- ficem-core ejecuta validaciones automáticas:
  - Estructura (hojas, campos requeridos)
  - Formato (tipos de datos, rangos)
  - Coherencia (composiciones al 100%, consistencia volumen/densidad)
- Si hay errores, se muestran inmediatamente
- Estado: `borrador`

### 5. Envío (Confirmación)
- Empresa confirma que los datos son correctos
- Estado cambia a `enviado`
- Ya no puede modificar

### 6. Notificación
- Sistema notifica al Coordinador País
- Aparece en su bandeja de pendientes

### 7. Revisión País
- Coordinador revisa el envío
- Puede aprobar (`validado`) o rechazar (`rechazado`)
- Si rechaza, empresa recibe notificación con motivo

### 8. Procesamiento
- FICEM (o automático) ejecuta cálculos:
  - Emisiones A1-A3 (clinker, cemento, concreto)
  - Clasificación bandas GCCA
  - Agregación para benchmarking
- Estado: `procesado` → `publicado`

### 9. Consulta de Resultados
- Empresa accede a dashboard en 4c-peru
- Ve sus resultados y clasificación GCCA
- Ve su posición en benchmarking (anónimo)
- Puede descargar reportes

---

## APIs Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/auth/login` | POST | Autenticación, retorna JWT |
| `/templates/{tipo}` | GET | Genera y descarga template Excel |
| `/uploads` | POST | Carga archivo Excel |
| `/uploads/{id}/validate` | GET | Ejecuta validaciones |
| `/uploads/{id}/submit` | POST | Confirma envío |
| `/uploads/{id}/review` | POST | Coordinador aprueba/rechaza |
| `/results/{empresa_id}` | GET | Resultados de cálculos |
| `/reports/{empresa_id}` | GET | Genera reporte PDF/Excel |
| `/benchmarking/{pais}` | GET | Datos de benchmarking anónimos |

---

## Permisos por Rol

| Acción | INFORMANTE | SUPERVISOR | VISOR | COORD_PAIS | ADMIN_PROCESO | ROOT |
|--------|------------|------------|-------|------------|---------------|------|
| Descargar template | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cargar Excel | ✓ | - | - | - | ✓ | ✓ |
| Enviar a supervisor | ✓ | - | - | - | - | - |
| Aprobar (empresa) | - | ✓ | - | - | - | - |
| Ver envíos país | - | - | - | ✓ | ✓ | ✓ |
| Aprobar (FICEM) | - | - | - | - | ✓ | ✓ |
| Ejecutar cálculos | - | - | - | - | ✓ | ✓ |
| Ver resultados propios | ✓ | ✓ | ✓ | - | - | - |
| Ver resultados país | - | - | - | ✓ | ✓ | ✓ |
| Ver resultados LATAM | - | - | - | - | ✓ | ✓ |
| Gestionar procesos | - | - | - | - | ✓ | ✓ |
| Eliminar procesos | - | - | - | - | - | ✓ |

---

**Última actualización**: 2025-12-11
