# Flujo de Datos - Sistema 4C

**Fecha**: 2025-12-07
**Estado**: Vigente

> **Nota histórica**: Este documento reemplaza a `docs/4-historico/v1/06-flujo-proceso_HASTA_2025-12-07.md` que describía el flujo centralizado vía email.

---

## Resumen

Las empresas cargan sus datos directamente a través de la app país (4c-peru, etc.), que actúa como frontend. El backend centralizado (ficem-core) procesa, valida y calcula.

---

## Actores

| Actor | Descripción | App que usa |
|-------|-------------|-------------|
| **Empresa** | Usuario de empresa cementera (editor, supervisor) | 4c-peru |
| **Coordinador País** | Coordinador del gremio o gobierno | 4c-peru |
| **Operador FICEM** | Equipo técnico regional | ficem-core (Streamlit) |

---

## Estados del Envío

| Estado | Descripción | Quién actúa siguiente |
|--------|-------------|----------------------|
| `borrador` | Empresa subió archivo, puede modificar | Empresa |
| `enviado` | Empresa confirmó envío | Coordinador País |
| `en_revision` | Coordinador revisando | Coordinador País |
| `rechazado` | Errores encontrados | Empresa (corrige) |
| `validado` | País aprobó, listo para procesar | FICEM |
| `procesado` | Cálculos ejecutados | - |
| `publicado` | Resultados disponibles | Empresa (consulta) |

---

## Flujo Completo

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EMPRESA   │     │  4c-peru    │     │ ficem-core  │     │   FICEM     │
│  (usuario)  │     │ (frontend)  │     │  (backend)  │     │ (operador)  │
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
       │                   │──────────────────>│                   │
       │                   │<── validación ────│                   │
       │<── errores/ok ────│                   │                   │
       │                   │                   │                   │
       │ 5. Envía (confirma)                   │                   │
       │──────────────────>│ POST /submit      │                   │
       │                   │──────────────────>│ estado: enviado   │
       │                   │                   │                   │
       │                   │                   │ 6. Notifica       │
       │                   │                   │──────────────────>│
       │                   │                   │                   │
       │                   │                   │ 7. Coordinador    │
       │                   │                   │    revisa/valida  │
       │                   │                   │<──────────────────│
       │                   │                   │                   │
       │                   │                   │ 8. Procesa        │
       │                   │                   │ (cálculos A1-A3)  │
       │                   │                   │                   │
       │ 9. Ve resultados  │                   │                   │
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

| Acción | Empresa Editor | Empresa Supervisor | Coordinador País | FICEM |
|--------|----------------|-------------------|------------------|-------|
| Descargar template | ✓ | ✓ | ✓ | ✓ |
| Cargar Excel | ✓ | ✓ | - | ✓ |
| Enviar | ✓ | ✓ | - | - |
| Aprobar envío empresa | - | ✓ | - | - |
| Revisar envíos país | - | - | ✓ | ✓ |
| Aprobar/Rechazar | - | - | ✓ | ✓ |
| Ejecutar cálculos | - | - | - | ✓ |
| Ver resultados propios | ✓ | ✓ | - | - |
| Ver resultados país | - | - | ✓ | ✓ |
| Ver resultados LATAM | - | - | - | ✓ |

---

**Última actualización**: 2025-12-07
