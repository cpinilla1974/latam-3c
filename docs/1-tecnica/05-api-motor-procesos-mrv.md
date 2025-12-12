# API Motor de Procesos MRV Multi-País

**Versión**: 1.0
**Fecha**: 2025-12-10
**Propósito**: Documentar APIs del Motor de Procesos MRV configurable de FICEM CORE

---

## Contexto

FICEM CORE implementa un **Motor de Procesos MRV configurable** que permite a cada país tener múltiples protocolos (PRODUCE Perú, MRV HR Colombia, 4C nacional, etc.) sin necesidad de cambios de código.

---

## Flujo de Aplicaciones

El sistema se compone de **3 aplicaciones** que consumen las mismas APIs de FICEM CORE:

```
┌──────────────────────────────────────────────────────────────┐
│                    FICEM CORE (Backend)                      │
│                    FastAPI + PostgreSQL                      │
│  - APIs REST centralizadas (/api/v1/*)                      │
│  - Motor de procesos MRV (BD procesos_mrv, submissions)     │
│  - Motor de cálculos GCCA                                    │
│  - Autenticación JWT                                         │
└──────────────────────────────────────────────────────────────┘
           ↑                        ↑                    ↑
           │                        │                    │
      consume APIs             consume APIs        consume APIs
           │                        │                    │
┌──────────────────┐   ┌────────────────────┐   ┌──────────────────┐
│  4c-ficem-web    │   │    4c-peru         │   │  4c-colombia     │
│  (Next.js)       │   │    (Next.js)       │   │  (Next.js)       │
│                  │   │                    │   │                  │
│  Rol: Admin      │   │  Rol: País Perú    │   │  Rol: País CO    │
│  FICEM           │   │                    │   │                  │
└──────────────────┘   └────────────────────┘   └──────────────────┘
```

### Responsabilidades por App

| App | Usuarios | Responsabilidad | Endpoints Principales |
|-----|----------|-----------------|----------------------|
| **ficem-core** | Backend (APIs) | Motor de procesos, BD, cálculos | Todos los endpoints |
| **4c-ficem-web** | Operador FICEM | **CREAR** y **CONFIGURAR** procesos, vigilar todos los países | `POST /procesos`, `PATCH /procesos/{id}/estado`, `GET /procesos` (todos) |
| **4c-peru** | Empresas PE, Coordinador PE | **EJECUTAR** procesos del país, crear submissions | `GET /procesos?pais=PE`, `POST /procesos/{id}/submissions`, `POST /submissions/{id}/review` |
| **4c-colombia** | Empresas CO, Coordinador CO | **EJECUTAR** procesos del país, crear submissions | `GET /procesos?pais=CO`, `POST /procesos/{id}/submissions` |

### Flujo de Trabajo Típico

#### 1. Admin FICEM crea proceso (desde 4c-ficem-web)

```typescript
// 4c-ficem-web: Pantalla "Crear Proceso"
POST /api/v1/procesos
{
  "id": "produce-peru-2025",
  "pais_iso": "PE",
  "tipo": "PRODUCE",
  "config": {
    "template_version": "produce_v2.xlsx",
    "validaciones": [...],
    "workflow_steps": [...],
    "deadline_envio": "2026-03-31"
  }
}

// Activar proceso
PATCH /api/v1/procesos/produce-peru-2025/estado
{"estado": "activo"}
```

#### 2. País Perú ejecuta proceso (desde 4c-peru)

```typescript
// 4c-peru: Empresa lista procesos disponibles
GET /api/v1/procesos?pais=PE&estado=activo

// 4c-peru: Empresa crea submission
POST /api/v1/procesos/produce-peru-2025/submissions
{"empresa_id": 123}

// 4c-peru: Empresa sube Excel y envía
POST /api/v1/submissions/{id}/upload
POST /api/v1/submissions/{id}/submit

// 4c-peru: Coordinador PE revisa y aprueba
POST /api/v1/submissions/{id}/review
{"accion": "aprobar"}
```

#### 3. Admin FICEM vigila progreso (desde 4c-ficem-web)

```typescript
// 4c-ficem-web: Dashboard de todos los países
GET /api/v1/procesos  // Sin filtro pais = ve TODOS

// 4c-ficem-web: Ver submissions de un proceso específico
GET /api/v1/procesos/produce-peru-2025/submissions

// 4c-ficem-web: Reporte consolidado
GET /api/v1/procesos/produce-peru-2025/report/agregado
```

---

## Permisos y Acceso

| Endpoint | Empresa | Coordinador País | Operador FICEM |
|----------|---------|------------------|----------------|
| `POST /procesos` (crear) | ❌ | ❌ | ✅ (solo 4c-ficem-web) |
| `GET /procesos?pais=PE` | ✅ | ✅ | ✅ |
| `GET /procesos` (todos) | ❌ | ❌ | ✅ (solo 4c-ficem-web) |
| `POST /submissions` | ✅ (su empresa) | ❌ | ✅ |
| `POST /submissions/{id}/review` | ❌ | ✅ (su país) | ✅ |

---

## Arquitectura del Motor de Procesos

```
┌─────────────────────────────────────────────┐
│           MOTOR DE PROCESOS MRV             │
├─────────────────────────────────────────────┤
│                                             │
│  ProcesoMRV (Registry)                      │
│  ├── id: "produce-peru-2024"                │
│  ├── pais_iso: "PE"                         │
│  ├── tipo: "PRODUCE"                        │
│  ├── config: {...}  ◄── Configurable        │
│  │   ├── template_version                   │
│  │   ├── validaciones[]                     │
│  │   ├── workflow_steps[]                   │
│  │   ├── calculos_habilitados[]             │
│  │   └── deadlines                          │
│  └── estado: "activo"                       │
│                                             │
│  Submission (Envío)                         │
│  ├── proceso_id: "produce-peru-2024"        │
│  ├── empresa_id: 123                        │
│  ├── estado_actual: "en_revision"           │
│  ├── archivo_excel: {...}                   │
│  ├── datos_extraidos: {...}                 │
│  ├── validaciones: [...]                    │
│  └── resultados_calculos: {...}             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Base URL

```
https://api.ficem.org/api/v1
```

Todos los endpoints requieren autenticación JWT:

```http
Authorization: Bearer {access_token}
```

---

## 1. GESTIÓN DE PROCESOS

### 1.1 Listar Procesos Activos de un País

**Uso**: Frontend país muestra procesos disponibles para el usuario

```http
GET /procesos?pais=PE&estado=activo
```

**Query Parameters**:
- `pais` (string, required): Código ISO país ("PE", "CO", "MX")
- `estado` (string, optional): "activo" | "borrador" | "cerrado" | "archivado"
- `tipo` (string, optional): "PRODUCE" | "MRV_HR" | "4C_NACIONAL"

**Response 200**:
```json
{
  "total": 2,
  "items": [
    {
      "id": "produce-peru-2024",
      "pais_iso": "PE",
      "tipo": "PRODUCE",
      "nombre": "Protocolo PRODUCE Perú 2024",
      "descripcion": "Reporte anual huella carbono cemento según PRODUCE",
      "ciclo": "2024",
      "estado": "activo",
      "config": {
        "deadline_envio": "2025-03-31",
        "deadline_revision": "2025-04-30"
      },
      "created_at": "2024-10-01T00:00:00Z"
    },
    {
      "id": "4c-peru-2025",
      "pais_iso": "PE",
      "tipo": "4C_NACIONAL",
      "nombre": "Reporte 4C Nacional Perú 2025",
      "ciclo": "2025",
      "estado": "activo"
    }
  ]
}
```

---

### 1.2 Obtener Detalle de un Proceso

**Uso**: Ver configuración completa (validaciones, workflow, template)

```http
GET /procesos/{proceso_id}
```

**Path Parameters**:
- `proceso_id` (string): ID del proceso (ej: "produce-peru-2024")

**Response 200**:
```json
{
  "id": "produce-peru-2024",
  "pais_iso": "PE",
  "tipo": "PRODUCE",
  "nombre": "Protocolo PRODUCE Perú 2024",
  "descripcion": "Reporte anual huella carbono cemento",
  "ciclo": "2024",
  "estado": "activo",

  "config": {
    "template_version": "produce_peru_v2.1.xlsx",
    "hojas_requeridas": ["Cemento", "Concreto", "Clinker"],

    "validaciones": [
      {
        "tipo": "estructura",
        "nivel": "error",
        "mensaje": "Debe contener hojas requeridas"
      },
      {
        "tipo": "rangos",
        "nivel": "warning",
        "params": {
          "produccion_min": 0,
          "produccion_max": 10000000
        }
      }
    ],

    "workflow_steps": [
      {
        "step": "borrador",
        "roles": ["empresa"],
        "descripcion": "Empresa edita datos"
      },
      {
        "step": "enviado",
        "roles": ["empresa"],
        "notificar": ["coordinador_pais"],
        "descripcion": "Empresa envía para revisión"
      },
      {
        "step": "en_revision",
        "roles": ["coordinador_pais"],
        "descripcion": "Coordinador revisa datos"
      },
      {
        "step": "aprobado",
        "roles": ["coordinador_pais"],
        "triggers": ["ejecutar_calculos"],
        "descripcion": "Datos aprobados y calculados"
      },
      {
        "step": "publicado",
        "roles": ["operador_ficem"],
        "visible": true,
        "descripcion": "Resultados públicos"
      }
    ],

    "deadline_envio": "2025-03-31",
    "deadline_revision": "2025-04-30",

    "calculos_habilitados": ["gcca", "bandas", "benchmarking"],
    "esquema_bd": "peru_data"
  },

  "created_at": "2024-10-01T00:00:00Z",
  "updated_at": "2024-11-15T10:00:00Z"
}
```

---

### 1.3 Descargar Template Excel del Proceso

**Uso**: Usuario descarga plantilla para llenar datos

```http
GET /procesos/{proceso_id}/template
```

**Query Parameters** (opcionales):
- `empresa_id` (integer): Pre-poblar con datos históricos de la empresa

**Response 200**:
```http
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="Plantilla_PRODUCE_Peru_2024.xlsx"

[Archivo Excel binario]
```

**Error 404**:
```json
{
  "error": "Proceso no encontrado",
  "proceso_id": "produce-peru-2024"
}
```

---

## 2. SUBMISSIONS (ENVÍOS)

### 2.1 Crear Submission

**Uso**: Empresa crea nuevo envío para un proceso

```http
POST /procesos/{proceso_id}/submissions
```

**Body** (JSON):
```json
{
  "empresa_id": 123,
  "planta_id": 456  // Opcional
}
```

**Response 201**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "proceso_id": "produce-peru-2024",
  "empresa_id": 123,
  "planta_id": 456,
  "usuario_id": 789,
  "estado_actual": "borrador",
  "workflow_history": [
    {
      "estado": "borrador",
      "fecha": "2024-11-01T10:00:00Z",
      "user_id": 789
    }
  ],
  "created_at": "2024-11-01T10:00:00Z"
}
```

---

### 2.2 Listar Submissions de un Proceso

**Uso**: Ver todos los envíos de una empresa o coordinador revisa todos

```http
GET /procesos/{proceso_id}/submissions
```

**Query Parameters**:
- `empresa_id` (integer, opcional): Filtrar por empresa
- `estado` (string, opcional): "borrador" | "enviado" | "en_revision" | "aprobado"
- `limit` (integer, default=20)
- `offset` (integer, default=0)

**Response 200**:
```json
{
  "total": 5,
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "proceso_id": "produce-peru-2024",
      "empresa_id": 123,
      "empresa_nombre": "Cementos Lima",
      "planta_nombre": "Planta Atocongo",
      "estado_actual": "en_revision",
      "submitted_at": "2024-11-15T14:30:00Z",
      "dias_en_estado": 5
    }
  ]
}
```

---

### 2.3 Obtener Detalle de Submission

```http
GET /submissions/{submission_id}
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "proceso_id": "produce-peru-2024",
  "empresa_id": 123,
  "empresa_nombre": "Cementos Lima",
  "planta_id": 456,
  "planta_nombre": "Planta Atocongo",
  "usuario_id": 789,

  "estado_actual": "en_revision",
  "workflow_history": [
    {
      "estado": "borrador",
      "fecha": "2024-11-01T10:00:00Z",
      "user_id": 789,
      "user_nombre": "Juan Pérez"
    },
    {
      "estado": "enviado",
      "fecha": "2024-11-15T14:30:00Z",
      "user_id": 789,
      "user_nombre": "Juan Pérez"
    },
    {
      "estado": "en_revision",
      "fecha": "2024-11-16T09:00:00Z",
      "user_id": 456,
      "user_nombre": "Coordinador ASOCEM"
    }
  ],

  "archivo_excel": {
    "url": "s3://ficem-uploads/PE/2024/empresa123_20241115.xlsx",
    "filename": "datos_2024.xlsx",
    "size_bytes": 245678,
    "uploaded_at": "2024-11-15T14:30:00Z"
  },

  "validaciones": [
    {
      "tipo": "estructura",
      "status": "ok",
      "mensaje": "Estructura correcta"
    },
    {
      "tipo": "rangos",
      "status": "warning",
      "detalles": [
        "Producción de cemento mayor al histórico (+15%)"
      ]
    }
  ],

  "comentarios": [
    {
      "user_id": 456,
      "user_nombre": "Coordinador ASOCEM",
      "fecha": "2024-11-20T10:00:00Z",
      "texto": "Revisar valor clinker planta Lima"
    }
  ],

  "created_at": "2024-11-01T10:00:00Z",
  "submitted_at": "2024-11-15T14:30:00Z",
  "reviewed_at": "2024-11-20T10:00:00Z"
}
```

---

### 2.4 Subir Archivo Excel

**Uso**: Empresa/usuario carga Excel con datos

```http
POST /submissions/{submission_id}/upload
Content-Type: multipart/form-data
```

**Form Data**:
- `archivo` (file): Archivo Excel

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "archivo_excel": {
    "url": "s3://...",
    "filename": "datos_2024_v2.xlsx",
    "size_bytes": 250000,
    "uploaded_at": "2024-11-16T10:00:00Z"
  },
  "mensaje": "Archivo cargado exitosamente"
}
```

**Error 400**:
```json
{
  "error": "Archivo inválido",
  "detalles": [
    "Formato debe ser .xlsx",
    "Tamaño máximo 10 MB"
  ]
}
```

---

### 2.5 Validar Submission

**Uso**: Ejecutar validaciones antes de enviar

```http
POST /submissions/{submission_id}/validate
```

**Response 200** (válido):
```json
{
  "submission_id": "550e8400-e29b-41d4-a716-446655440000",
  "valido": true,
  "errores": [],
  "advertencias": [
    "Producción 15% mayor que año anterior"
  ],
  "validaciones": [
    {
      "tipo": "estructura",
      "status": "ok"
    },
    {
      "tipo": "rangos",
      "status": "ok"
    },
    {
      "tipo": "consistencia",
      "status": "ok"
    }
  ]
}
```

**Response 200** (inválido):
```json
{
  "submission_id": "550e8400-e29b-41d4-a716-446655440000",
  "valido": false,
  "errores": [
    "Hoja 'Cemento' falta",
    "Campo 'Producción' no puede ser negativo"
  ],
  "advertencias": []
}
```

---

### 2.6 Enviar Submission (Cambiar a "enviado")

**Uso**: Empresa confirma envío para revisión

```http
POST /submissions/{submission_id}/submit
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "estado_actual": "enviado",
  "submitted_at": "2024-11-20T09:00:00Z",
  "proximos_pasos": "Su envío será revisado por el coordinador nacional en los próximos 7 días"
}
```

**Error 400**:
```json
{
  "error": "No se puede enviar",
  "motivo": "Validación fallida",
  "errores": [
    "Campo X falta"
  ]
}
```

---

### 2.7 Revisar Submission (Coordinador)

**Uso**: Coordinador aprueba o rechaza

#### Aprobar:
```http
POST /submissions/{submission_id}/review
Content-Type: application/json

{
  "accion": "aprobar",
  "comentario": "Datos validados correctamente"
}
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "estado_actual": "aprobado",
  "reviewed_at": "2024-11-25T10:00:00Z",
  "proximos_pasos": "Los cálculos se ejecutarán automáticamente"
}
```

#### Rechazar:
```http
POST /submissions/{submission_id}/review
Content-Type: application/json

{
  "accion": "rechazar",
  "comentario": "Falta información en sección Energía"
}
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "estado_actual": "rechazado",
  "reviewed_at": "2024-11-25T10:00:00Z",
  "proximos_pasos": "Corrija los datos y vuelva a enviar"
}
```

---

### 2.8 Agregar Comentario

**Uso**: Cualquier actor agrega comentario al submission

```http
POST /submissions/{submission_id}/comentarios
Content-Type: application/json

{
  "texto": "Por favor verificar valor de clinker planta Lima"
}
```

**Response 201**:
```json
{
  "id": "coment_12345",
  "submission_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 456,
  "user_nombre": "Coordinador ASOCEM",
  "texto": "Por favor verificar...",
  "fecha": "2024-11-20T14:30:00Z"
}
```

---

### 2.9 Obtener Resultados de Cálculos

**Uso**: Ver resultados GCCA, bandas, benchmarking

```http
GET /submissions/{submission_id}/results
```

**Response 200**:
```json
{
  "submission_id": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "aprobado",
  "resultados_calculos": {
    "ejecutado": "2024-11-25T15:00:00Z",

    "gcca": {
      "emision_total_kg_co2e": 97500,
      "emision_unitaria_kg_co2e_tcem": 650,
      "banda": "B",
      "alcances": {
        "alcance_1": 65000,
        "alcance_2": 22500,
        "alcance_3": 10000
      }
    },

    "bandas": {
      "banda_asignada": "B",
      "percentil": 73,
      "rango": "601-700 kg CO2/ton"
    },

    "benchmarking": {
      "promedio_pais": 580,
      "tu_valor": 650,
      "diferencia": 70,
      "posicion": 12,
      "total_empresas": 45
    }
  }
}
```

**Error 404**:
```json
{
  "error": "Resultados no disponibles",
  "estado_actual": "en_revision",
  "mensaje": "Los resultados estarán disponibles cuando el submission sea aprobado"
}
```

---

## 3. REPORTES

### 3.1 Reporte Consolidado de Proceso

**Uso**: Coordinador obtiene reporte agregado de un proceso

```http
GET /procesos/{proceso_id}/report/agregado
```

**Response 200**:
```json
{
  "proceso_id": "produce-peru-2024",
  "pais": "PE",
  "ciclo": "2024",

  "participacion": {
    "total_empresas": 45,
    "submissions_totales": 38,
    "submissions_aprobados": 35,
    "tasa_respuesta": 84.4
  },

  "emision_promedio": {
    "cemento_kg_co2e_tcem": 580,
    "clinker_kg_co2e_tcem": 650
  },

  "distribucion_bandas": {
    "A": 5,
    "B": 12,
    "C": 15,
    "D": 10,
    "E": 3
  }
}
```

---

### 3.2 Exportar Datos de Proceso

**Uso**: Exportar datos para PRODUCE, MRV HR, etc.

```http
GET /procesos/{proceso_id}/export/produce
```

**Query Parameters**:
- `formato` (string): "excel" | "csv" | "json"

**Response 200**:
```http
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="Exportacion_PRODUCE_Peru_2024.xlsx"

[Excel binario con formato específico PRODUCE]
```

---

## 4. GESTIÓN DE PROCESOS (Admin FICEM)

### 4.1 Crear Proceso

**Uso**: Operador FICEM crea nuevo proceso para un país

```http
POST /procesos
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "id": "produce-peru-2025",
  "pais_iso": "PE",
  "tipo": "PRODUCE",
  "nombre": "Protocolo PRODUCE Perú 2025",
  "descripcion": "Reporte anual huella carbono cemento",
  "ciclo": "2025",
  "config": {
    "template_version": "produce_peru_v2.1.xlsx",
    "hojas_requeridas": ["Cemento", "Concreto", "Clinker"],
    "validaciones": [...],
    "workflow_steps": [...],
    "deadline_envio": "2026-03-31",
    "calculos_habilitados": ["gcca", "bandas"]
  }
}
```

**Response 201**:
```json
{
  "id": "produce-peru-2025",
  "pais_iso": "PE",
  "tipo": "PRODUCE",
  "estado": "borrador",
  "created_at": "2024-12-10T10:00:00Z",
  "mensaje": "Proceso creado exitosamente. Cambie estado a 'activo' cuando esté listo."
}
```

---

### 4.2 Actualizar Proceso

```http
PUT /procesos/{proceso_id}
```

### 4.3 Cambiar Estado de Proceso

```http
PATCH /procesos/{proceso_id}/estado
Content-Type: application/json

{
  "estado": "activo"  // borrador | activo | cerrado | archivado
}
```

---

## 5. EJEMPLOS DE INTEGRACIÓN FRONTEND

### React/Next.js - Listar Procesos Activos

```typescript
// hooks/useProcesosMRV.ts
import { useQuery } from '@tanstack/react-query'

export function useProcesosMRV(pais: string) {
  return useQuery({
    queryKey: ['procesos', pais],
    queryFn: async () => {
      const res = await fetch(
        `${API_BASE}/procesos?pais=${pais}&estado=activo`,
        {
          headers: {
            'Authorization': `Bearer ${getToken()}`
          }
        }
      )
      return res.json()
    }
  })
}

// components/SeleccionarProceso.tsx
function SeleccionarProceso() {
  const { data: procesos } = useProcesosMRV('PE')

  return (
    <select>
      {procesos?.items.map(p => (
        <option key={p.id} value={p.id}>
          {p.nombre} ({p.ciclo})
        </option>
      ))}
    </select>
  )
}
```

---

### React - Crear y Subir Submission

```typescript
// hooks/useSubmission.ts
import { useMutation } from '@tanstack/react-query'

export function useCrearSubmission() {
  return useMutation({
    mutationFn: async ({ procesoId, empresaId }) => {
      const res = await fetch(
        `${API_BASE}/procesos/${procesoId}/submissions`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ empresa_id: empresaId })
        }
      )
      return res.json()
    }
  })
}

export function useSubirArchivo() {
  return useMutation({
    mutationFn: async ({ submissionId, archivo }) => {
      const formData = new FormData()
      formData.append('archivo', archivo)

      const res = await fetch(
        `${API_BASE}/submissions/${submissionId}/upload`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${getToken()}`
          },
          body: formData
        }
      )
      return res.json()
    }
  })
}

// Uso en componente
function SubirDatos({ procesoId }) {
  const crearSubmission = useCrearSubmission()
  const subirArchivo = useSubirArchivo()

  const handleSubmit = async (file: File) => {
    // 1. Crear submission
    const submission = await crearSubmission.mutateAsync({
      procesoId,
      empresaId: user.empresa_id
    })

    // 2. Subir archivo
    await subirArchivo.mutateAsync({
      submissionId: submission.id,
      archivo: file
    })

    // 3. Navegar a validación
    router.push(`/submissions/${submission.id}/validar`)
  }

  return <FileUpload onUpload={handleSubmit} />
}
```

---

## 6. ESTADOS Y TRANSICIONES

### Máquina de Estados de Submission

```
┌──────────┐
│ borrador │  ← Estado inicial
└────┬─────┘
     │ submit()
     ▼
┌───────────┐
│  enviado  │
└────┬──────┘
     │ review(aprobar)   │ review(rechazar)
     ▼                    ▼
┌──────────┐         ┌───────────┐
│ aprobado │         │ rechazado │ ──→ volver a borrador
└────┬─────┘         └───────────┘
     │ trigger: ejecutar_calculos
     ▼
┌────────────┐
│ publicado  │  ← Estado final
└────────────┘
```

### Permisos por Rol

| Estado | Empresa | Coordinador País | Operador FICEM |
|--------|---------|------------------|----------------|
| borrador | edit, submit | view | view |
| enviado | view | review, comment | view |
| en_revision | view, comment | approve, reject | view |
| aprobado | view | view | publish |
| publicado | view | view | view |

---

## 7. ERRORES COMUNES

| Código | Error | Solución |
|--------|-------|----------|
| 400 | "Validación fallida" | Verificar que el Excel tenga todas las hojas requeridas |
| 403 | "No autorizado para este proceso" | Usuario no pertenece al país del proceso |
| 404 | "Proceso no encontrado" | Verificar que el proceso esté activo |
| 409 | "Submission ya existe para este ciclo" | Cada empresa puede tener solo 1 submission por proceso/ciclo |

---

## 8. MIGRACIÓN DESDE ENDPOINTS ANTIGUOS

### Mapeo de Endpoints

| Antiguo | Nuevo |
|---------|-------|
| `POST /envios` | `POST /procesos/{proceso_id}/submissions` |
| `GET /envios/{id}` | `GET /submissions/{id}` |
| `POST /envios/{id}/validar` | `POST /submissions/{id}/validate` |
| `POST /envios/{id}/enviar` | `POST /submissions/{id}/submit` |
| `GET /ciclos/actual` | `GET /procesos?pais=PE&estado=activo` |

---

**Documento completado**: 2025-12-10
**Estado**: Listo para uso por frontends
**Contacto**: dev@ficem.org