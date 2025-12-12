# API Endpoints Prioritarios - 4C Perú

**Versión**: 1.0
**Fecha**: 2025-12-07
**Propósito**: Definir endpoints de ficem-core ordenados por prioridad de implementación

---

## FASE 1: AUTENTICACIÓN + DATOS BÁSICOS

**Timeline**: Semana 1-2
**Propósito**: Login funcional y obtener datos de empresa

### 1.1 Autenticación

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@empresa.com",
  "password": "password123"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "user": {
    "id": "usr_12345",
    "email": "usuario@empresa.com",
    "nombre": "Juan Pérez",
    "rol": "editor",
    "grupo": "empresa",
    "empresa_id": "emp_999",
    "pais_code": "PE"
  }
}

Error 401:
{
  "error": "Invalid credentials"
}
```

### 1.2 Validar Token

```http
GET /api/auth/me
Authorization: Bearer {access_token}

Response 200:
{
  "id": "usr_12345",
  "email": "usuario@empresa.com",
  "nombre": "Juan Pérez",
  "rol": "editor",
  "grupo": "empresa",
  "empresa_id": "emp_999",
  "pais_code": "PE"
}
```

### 1.3 Refresh Token

```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer"
}
```

### 1.4 Obtener Datos de Empresa (para empresa)

```http
GET /api/empresas/mi-empresa
Authorization: Bearer {access_token}

Response 200:
{
  "id": "emp_999",
  "nombre": "Cementos Perú S.A.",
  "ruc": "20123456789",
  "contacto": "Juan Pérez",
  "email_contacto": "usuario@empresa.com",
  "telefono": "01-2345678",
  "ubicacion": "Lima, Perú",
  "tipos_producto": ["cemento", "concreto"],
  "foto_logo": "url"
}
```

### 1.5 Obtener Datos de Empresa (para coordinador)

```http
GET /api/empresas/{empresa_id}
Authorization: Bearer {access_token}

Response 200:
{
  "id": "emp_999",
  "nombre": "Cementos Perú S.A.",
  "ruc": "20123456789",
  "contacto": "Juan Pérez",
  "email_contacto": "usuario@empresa.com",
  "telefono": "01-2345678",
  "ubicacion": "Lima, Perú",
  "tipos_producto": ["cemento", "concreto"],
  "usuarios": [
    {
      "id": "usr_12345",
      "email": "usuario@empresa.com",
      "nombre": "Juan Pérez",
      "rol": "editor"
    }
  ]
}
```

### 1.6 Listar Empresas Perú (para coordinador)

```http
GET /api/empresas?pais=PE
Authorization: Bearer {access_token}

Query parameters:
  - pais: "PE" (required)

Response 200:
{
  "total": 45,
  "items": [
    {
      "id": "emp_999",
      "nombre": "Cementos Perú S.A.",
      "ubicacion": "Lima",
      "tipos_producto": ["cemento", "concreto"],
      "estado_ciclo": "ENVIADO"
    },
    ...
  ]
}
```

---

## FASE 2: CICLO Y PLANTILLAS

**Timeline**: Semana 2-3
**Propósito**: Obtener ciclo abierto y generar plantillas Excel

### 2.1 Obtener Ciclo Actual

```http
GET /api/ciclos/actual?pais=PE
Authorization: Bearer {access_token}

Response 200:
{
  "id": "ciclo_2025",
  "año": 2025,
  "pais": "PE",
  "estado": "ABIERTO",
  "fecha_inicio": "2025-01-01",
  "fecha_fin": "2025-12-31",
  "deadline_envio": "2025-03-31",
  "deadline_validacion": "2025-04-30",
  "fecha_publicacion": "2025-05-31"
}
```

### 2.2 Listar Ciclos Históricos

```http
GET /api/ciclos?pais=PE
Authorization: Bearer {access_token}

Response 200:
{
  "total": 5,
  "items": [
    {
      "id": "ciclo_2025",
      "año": 2025,
      "estado": "ABIERTO",
      "fecha_inicio": "2025-01-01"
    },
    {
      "id": "ciclo_2024",
      "año": 2024,
      "estado": "PUBLICADO",
      "fecha_inicio": "2024-01-01"
    }
  ]
}
```

### 2.3 Descargar Plantilla Excel

```http
GET /api/plantillas/{tipo}?ciclo_id={id}&empresa_id={id}
Authorization: Bearer {access_token}

Path parameters:
  - tipo: "clinker" | "cemento" | "concreto"

Query parameters:
  - ciclo_id: ID del ciclo actual (ej: "ciclo_2025")
  - empresa_id: ID de la empresa (optional, para pre-popular datos)

Response 200:
  Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  Content-Disposition: attachment; filename="Plantilla_Cemento_2025.xlsx"

  [archivo Excel binario]

Error 404:
{
  "error": "Ciclo no encontrado"
}
```

### 2.4 Obtener Estructura de Plantilla (como JSON)

```http
GET /api/plantillas/{tipo}/estructura
Authorization: Bearer {access_token}

Path parameters:
  - tipo: "cemento"

Response 200:
{
  "tipo_producto": "cemento",
  "hojas": [
    {
      "nombre": "Datos Producción",
      "campos": [
        {
          "nombre": "produccion_toneladas",
          "tipo": "number",
          "requerido": true,
          "descripcion": "Producción anual en toneladas"
        }
      ]
    },
    {
      "nombre": "Energía",
      "campos": [...]
    }
  ],
  "instrucciones": "url a PDF"
}
```

---

## FASE 3: ENVÍOS Y VALIDACIÓN

**Timeline**: Semana 3-4
**Propósito**: Cargar Excel, validar, enviar

### 3.1 Crear Envío (Subir Excel)

```http
POST /api/envios
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Form data:
  - ciclo_id: "ciclo_2025"
  - empresa_id: "emp_999" (optional si es empresa)
  - archivo: [archivo Excel binario]
  - tipo_producto: "cemento"

Response 201:
{
  "id": "envio_12345",
  "empresa_id": "emp_999",
  "ciclo_id": "ciclo_2025",
  "tipo_producto": "cemento",
  "estado": "BORRADOR",
  "archivo_nombre": "Plantilla_Cemento_2025.xlsx",
  "fecha_carga": "2025-02-15T10:30:00Z",
  "datos_resumen": {
    "produccion_toneladas": 150000,
    "campos_completados": 28,
    "campos_totales": 35
  }
}

Error 400:
{
  "error": "Ciclo cerrado",
  "mensaje": "No se pueden crear nuevos envíos para este ciclo"
}
```

### 3.2 Obtener Envío

```http
GET /api/envios/{envio_id}
Authorization: Bearer {access_token}

Response 200:
{
  "id": "envio_12345",
  "empresa_id": "emp_999",
  "empresa_nombre": "Cementos Perú S.A.",
  "ciclo_id": "ciclo_2025",
  "tipo_producto": "cemento",
  "estado": "BORRADOR",
  "archivo_nombre": "Plantilla_Cemento_2025.xlsx",
  "fecha_carga": "2025-02-15T10:30:00Z",
  "fecha_envio": null,
  "datos_resumen": {
    "produccion_toneladas": 150000,
    "consumo_energia_kwh": 450000
  }
}
```

### 3.3 Validar Localmente

```http
POST /api/envios/{envio_id}/validar
Authorization: Bearer {access_token}

Response 200:
{
  "valido": true,
  "errores": [],
  "advertencias": [
    "Resistencia cemento inusualmente alta (comparado con histórico)"
  ],
  "resumen": {
    "estructura": "OK",
    "campos_completados": 35,
    "campos_totales": 35,
    "coherencia": "OK"
  }
}

Response 200 (con errores):
{
  "valido": false,
  "errores": [
    "Campo 'Producción' no puede ser negativo",
    "Falta campo 'Consumo Energía SEIN'"
  ],
  "advertencias": []
}
```

### 3.4 Reemplazar Excel

```http
PUT /api/envios/{envio_id}/archivo
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Form data:
  - archivo: [nuevo Excel]

Response 200:
{
  "id": "envio_12345",
  "estado": "BORRADOR",
  "archivo_nombre": "Plantilla_Cemento_2025_v2.xlsx",
  "fecha_carga": "2025-02-16T14:15:00Z"
}
```

### 3.5 Enviar Envío (confirmar para revisión)

```http
POST /api/envios/{envio_id}/enviar
Authorization: Bearer {access_token}

Response 200:
{
  "id": "envio_12345",
  "estado": "ENVIADO",
  "fecha_envio": "2025-02-20T09:00:00Z",
  "numero_secuencial": "EMP-999-2025-001"
}

Error 400:
{
  "error": "Validación fallida",
  "errores": ["Campo X falta"]
}
```

### 3.6 Cancelar Envío (si aún no fue revisado)

```http
POST /api/envios/{envio_id}/cancelar
Authorization: Bearer {access_token}

Response 200:
{
  "id": "envio_12345",
  "estado": "BORRADOR"
}

Error 400:
{
  "error": "No se puede cancelar",
  "mensaje": "El envío ya está bajo revisión"
}
```

### 3.7 Obtener Datos Parseados del Excel

```http
GET /api/envios/{envio_id}/datos
Authorization: Bearer {access_token}

Response 200:
{
  "envio_id": "envio_12345",
  "tipo_producto": "cemento",
  "datos": {
    "produccion": {
      "cemento_toneladas": 150000,
      "resistencia_mpa": 42.5
    },
    "energia": {
      "consumo_sein_kwh": 450000,
      "consumo_carbon_toneladas": 15000,
      "consumo_petroleo_toneladas": 2000
    },
    "materiales": {
      "clinker_toneladas": 130000,
      "aditivos_toneladas": 20000
    }
  }
}
```

---

## FASE 4: COMENTARIOS Y REVISIÓN (Coordinador)

**Timeline**: Semana 4-5
**Propósito**: Revisar envíos y dar feedback

### 4.1 Listar Envíos para Revisar

```http
GET /api/envios?ciclo_id={id}&estado=ENVIADO,VALIDANDO,RECHAZADO&pais=PE
Authorization: Bearer {access_token}

Query parameters:
  - ciclo_id: "ciclo_2025"
  - estado: "ENVIADO,VALIDANDO,RECHAZADO" (filtro múltiple)
  - pais: "PE"
  - limite: 20 (default)
  - offset: 0

Response 200:
{
  "total": 12,
  "items": [
    {
      "id": "envio_12345",
      "empresa_id": "emp_999",
      "empresa_nombre": "Cementos Perú S.A.",
      "tipo_producto": "cemento",
      "estado": "ENVIADO",
      "fecha_envio": "2025-02-20T09:00:00Z",
      "dias_pendiente": 3
    }
  ]
}
```

### 4.2 Agregar Comentario

```http
POST /api/envios/{envio_id}/comentarios
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "mensaje": "Por favor verificar que el campo de resistencia sea 42.5 MPa según especificación",
  "tipo": "SOLICITUD_INFORMACIÓN"
}

Body types:
  - SOLICITUD_INFORMACIÓN: Pregunta al responsable
  - SOLICITUD_CORRECCIÓN: Necesita corrección obligatoria
  - APROBACIÓN: El coordinador está aprobando (ver endpoint separado)
  - RECHAZO: El coordinador está rechazando (ver endpoint separado)

Response 201:
{
  "id": "coment_98765",
  "envio_id": "envio_12345",
  "autor_id": "usr_55555",
  "autor_nombre": "María García",
  "mensaje": "Por favor verificar...",
  "tipo": "SOLICITUD_INFORMACIÓN",
  "fecha": "2025-02-23T14:30:00Z"
}
```

### 4.3 Obtener Comentarios de un Envío

```http
GET /api/envios/{envio_id}/comentarios
Authorization: Bearer {access_token}

Response 200:
{
  "total": 3,
  "items": [
    {
      "id": "coment_98765",
      "autor_nombre": "María García",
      "tipo": "SOLICITUD_INFORMACIÓN",
      "mensaje": "Por favor verificar...",
      "fecha": "2025-02-23T14:30:00Z"
    }
  ]
}
```

### 4.4 Aprobar Envío

```http
POST /api/envios/{envio_id}/aprobar
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "comentario": "Datos validados correctamente. Enviando a FICEM para cálculo central." (optional)
}

Response 200:
{
  "id": "envio_12345",
  "estado": "APROBADO",
  "fecha_aprobacion": "2025-02-25T10:00:00Z",
  "aprobado_por": "usr_55555",
  "proximos_pasos": "Será procesado por FICEM en los próximos 7 días"
}
```

### 4.5 Rechazar Envío

```http
POST /api/envios/{envio_id}/rechazar
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "motivo": "Campos incompletos en sección Energía"
}

Response 200:
{
  "id": "envio_12345",
  "estado": "RECHAZADO",
  "fecha_rechazo": "2025-02-25T10:00:00Z",
  "rechazado_por": "usr_55555",
  "motivo": "Campos incompletos en sección Energía",
  "proximos_pasos": "Cargue nuevamente el Excel corregido"
}

Error 400:
{
  "error": "No se puede rechazar",
  "mensaje": "El envío ya fue aprobado o está bajo cálculo"
}
```

---

## FASE 5: RESULTADOS Y CÁLCULOS

**Timeline**: Semana 5-6
**Propósito**: Ver resultados finales y clasificación

### 5.1 Obtener Resultado (si publicado)

```http
GET /api/resultados?empresa_id={id}&ciclo_id={id}
Authorization: Bearer {access_token}

Query parameters:
  - empresa_id: "emp_999"
  - ciclo_id: "ciclo_2025"

Response 200:
{
  "id": "resultado_12345",
  "empresa_id": "emp_999",
  "ciclo_id": "ciclo_2025",
  "tipo_producto": "cemento",
  "estado": "PUBLICADO",
  "fecha_publicacion": "2025-05-31T00:00:00Z",

  "emision_total_kg_co2e": 97500,
  "emision_unitaria_kg_co2e_tcem": 650,

  "desglose_alcances": {
    "alcance_1_directo": {
      "valor_kg_co2e": 65000,
      "porcentaje": 66.7
    },
    "alcance_2_electricidad": {
      "valor_kg_co2e": 22500,
      "porcentaje": 23.1
    },
    "alcance_3_transporte": {
      "valor_kg_co2e": 10000,
      "porcentaje": 10.3
    }
  },

  "clasificacion_gcca": {
    "banda": "B",
    "descripcion": "Banda B (mejor 25% del país)",
    "limite_inferior_kg_co2e_tcem": 600,
    "limite_superior_kg_co2e_tcem": 700
  },

  "comparativas": {
    "vs_promedio_pais": {
      "promedio_pais_kg_co2e_tcem": 580,
      "diferencia_kg_co2e_tcem": 70,
      "porcentaje_diferencia": 12.1,
      "interpretacion": "12.1% PEOR que promedio"
    },
    "vs_percentil_25": {
      "valor_kg_co2e_tcem": 520,
      "diferencia": 130,
      "interpretacion": "Necesita mejorar 130 kg para estar en top 25%"
    }
  }
}

Error 404:
{
  "error": "Resultado no publicado",
  "estado_actual": "CALCULANDO",
  "mensaje": "Los resultados estarán disponibles el 2025-05-31"
}
```

### 5.2 Obtener Resultados Históricos

```http
GET /api/resultados/historico?empresa_id={id}
Authorization: Bearer {access_token}

Response 200:
{
  "total": 5,
  "items": [
    {
      "ciclo_id": "ciclo_2025",
      "año": 2025,
      "huella_unitaria_kg_co2e_tcem": 650,
      "banda_gcca": "B",
      "fecha_publicacion": "2025-05-31T00:00:00Z"
    },
    {
      "ciclo_id": "ciclo_2024",
      "año": 2024,
      "huella_unitaria_kg_co2e_tcem": 670,
      "banda_gcca": "C",
      "fecha_publicacion": "2024-06-15T00:00:00Z"
    }
  ]
}
```

### 5.3 Obtener Benchmarking Perú

```http
GET /api/benchmarking/PE?tipo_producto=cemento&ciclo_id={id}
Authorization: Bearer {access_token}

Query parameters:
  - tipo_producto: "cemento" | "clinker" | "concreto"
  - ciclo_id: "ciclo_2025"

Response 200:
{
  "ciclo_id": "ciclo_2025",
  "pais": "PE",
  "tipo_producto": "cemento",
  "tu_empresa": {
    "empresa_id": "emp_999",
    "empresa_nombre": "Cementos Perú S.A.",
    "huella_kg_co2e_tcem": 650,
    "banda": "B",
    "posicion": 12,
    "total_empresas": 45,
    "percentil": 73
  },
  "distribucion": {
    "minimo": 480,
    "q1": 550,
    "mediana": 580,
    "q3": 620,
    "maximo": 750
  },
  "bandas": {
    "A": {"count": 5, "rango": "≤500"},
    "B": {"count": 12, "rango": "501-600"},
    "C": {"count": 15, "rango": "601-650"},
    "D": {"count": 10, "rango": "651-750"},
    "E": {"count": 3, "rango": ">750"}
  }
}
```

---

## FASE 6: DATOS PARA COORDINADOR (Hoja de Ruta)

**Timeline**: Semana 6-7
**Propósito**: Ver métricas país y progreso Hoja de Ruta

### 6.1 Obtener Hoja de Ruta Perú

```http
GET /api/hoja-ruta/PE?ciclo_id={id}
Authorization: Bearer {access_token}

Query parameters:
  - ciclo_id: "ciclo_2025" (optional, default actual)

Response 200:
{
  "pais": "PE",
  "ciclo_id": "ciclo_2025",
  "año": 2025,

  "emision_promedio_actual_kg_co2e_tcem": 580,
  "emision_promedio_anterior_kg_co2e_tcem": 590,
  "reduccion_anual_kg_co2e_tcem": 10,
  "velocidad_reduccion_porcentaje": 1.7,

  "targets": {
    "target_2030": {
      "año": 2030,
      "valor_kg_co2e_tcem": 520,
      "gap_actual_kg_co2e_tcem": 60,
      "gap_porcentaje": 10.3,
      "años_restantes": 5,
      "velocidad_requerida_kg_anual": 12
    },
    "target_2050": {
      "año": 2050,
      "valor_kg_co2e_tcem": 350,
      "gap_actual_kg_co2e_tcem": 230,
      "gap_porcentaje": 39.7
    }
  },

  "proyecciones": {
    "si_continua_tendencia": {
      "año_2030": 530,
      "alcanza_target_2030": false
    }
  },

  "recomendaciones": [
    "Necesita acelerar reducción de Alcance 1 (combustibles)",
    "Implementar energías renovables para Alcance 2"
  ]
}
```

### 6.2 Obtener Métricas Ciclo (para Coordinador)

```http
GET /api/metricas/ciclo?pais=PE&ciclo_id={id}
Authorization: Bearer {access_token}

Response 200:
{
  "ciclo_id": "ciclo_2025",
  "pais": "PE",
  "año": 2025,

  "participacion": {
    "total_empresas": 45,
    "empresas_enviadas": 38,
    "tasa_respuesta_porcentaje": 84.4,
    "empresas_aprobadas": 36,
    "empresas_publicadas": 35
  },

  "emision_promedio": {
    "cemento_kg_co2e_tcem": 580,
    "clinker_kg_co2e_tcem": 650,
    "concreto_kg_co2e_tm3": 380
  },

  "distribucion_bandas": {
    "A": 5,
    "B": 12,
    "C": 15,
    "D": 10,
    "E": 3
  },

  "desglose_alcances": {
    "alcance_1_porcentaje": 67.2,
    "alcance_2_porcentaje": 22.1,
    "alcance_3_porcentaje": 10.7
  }
}
```

---

## FASE 7: REPORTES Y EXPORTACIÓN

**Timeline**: Semana 7+
**Propósito**: Generar reportes y exportar datos

### 7.1 Generar Reporte Empresa

```http
GET /api/reportes/empresa?empresa_id={id}&ciclo_id={id}&formato=pdf
Authorization: Bearer {access_token}

Query parameters:
  - empresa_id: "emp_999"
  - ciclo_id: "ciclo_2025"
  - formato: "pdf" | "excel" | "json"

Response 200:
  Content-Type: application/pdf
  Content-Disposition: attachment; filename="Reporte_CementosPerú_2025.pdf"

  [PDF binario]
```

### 7.2 Generar Reporte Ciclo (Coordinador)

```http
GET /api/reportes/ciclo?pais=PE&ciclo_id={id}&formato=pdf
Authorization: Bearer {access_token}

Response 200:
  Content-Type: application/pdf
  Content-Disposition: attachment; filename="Reporte_Ciclo_2025_Perú.pdf"

  [PDF binario con resumen nacional]
```

### 7.3 Exportar Datos para FICEM

```http
POST /api/exportar/ficem
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "pais": "PE",
  "ciclo_id": "ciclo_2025",
  "incluir": [
    "empresas",
    "envios_aprobados",
    "resultados_publicados",
    "benchmarking_anonimo"
  ],
  "formato": "excel"
}

Response 200:
  Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  Content-Disposition: attachment; filename="Exportación_FICEM_PE_2025.xlsx"

  [Excel binario]
```

---

## MATRIZ DE PRIORIDAD

| Fase | Endpoint | Prioridad | Semana |
|------|----------|-----------|--------|
| 1 | `POST /api/auth/login` | 🔴 Crítica | 1 |
| 1 | `GET /api/auth/me` | 🔴 Crítica | 1 |
| 1 | `GET /api/empresas/mi-empresa` | 🔴 Crítica | 1 |
| 2 | `GET /api/ciclos/actual` | 🔴 Crítica | 2 |
| 2 | `GET /api/plantillas/{tipo}` | 🔴 Crítica | 2 |
| 3 | `POST /api/envios` | 🔴 Crítica | 3 |
| 3 | `GET /api/envios/{id}` | 🔴 Crítica | 3 |
| 3 | `POST /api/envios/{id}/validar` | 🔴 Crítica | 3 |
| 3 | `POST /api/envios/{id}/enviar` | 🔴 Crítica | 3 |
| 4 | `GET /api/envios?estado=ENVIADO` | 🟡 Alta | 4 |
| 4 | `POST /api/envios/{id}/comentarios` | 🟡 Alta | 4 |
| 4 | `GET /api/envios/{id}/comentarios` | 🟡 Alta | 4 |
| 4 | `POST /api/envios/{id}/aprobar` | 🟡 Alta | 4 |
| 4 | `POST /api/envios/{id}/rechazar` | 🟡 Alta | 4 |
| 5 | `GET /api/resultados` | 🟡 Alta | 5 |
| 5 | `GET /api/benchmarking/PE` | 🟡 Alta | 5 |
| 6 | `GET /api/hoja-ruta/PE` | 🟡 Alta | 6 |
| 6 | `GET /api/metricas/ciclo` | 🟡 Alta | 6 |
| 7 | `GET /api/reportes/*` | 🟢 Media | 7+ |
| 7 | `POST /api/exportar/ficem` | 🟢 Media | 7+ |

---

## DATOS DUMMY PARA INICIO

Para poder trabajar en paralelo, puedes poblar ficem-core con estos datos dummy:

### Empresas Dummy (PE)

```json
[
  {
    "id": "emp_001",
    "nombre": "Cementos Perú S.A.",
    "ruc": "20123456789",
    "ubicacion": "Lima",
    "tipos_producto": ["cemento", "concreto"]
  },
  {
    "id": "emp_002",
    "nombre": "Cementos Andinos",
    "ruc": "20987654321",
    "ubicacion": "Arequipa",
    "tipos_producto": ["clinker", "cemento"]
  }
]
```

### Ciclo Dummy

```json
{
  "id": "ciclo_2025",
  "año": 2025,
  "pais": "PE",
  "estado": "ABIERTO",
  "fecha_inicio": "2025-01-01",
  "deadline_envio": "2025-03-31",
  "deadline_validacion": "2025-04-30",
  "fecha_publicacion": "2025-05-31"
}
```

### Usuario Dummy

```json
{
  "id": "usr_001",
  "email": "admin@cementos.com",
  "nombre": "Juan Pérez",
  "rol": "editor",
  "grupo": "empresa",
  "empresa_id": "emp_001",
  "pais_code": "PE",
  "password": "demo123"  // solo para testing
}
```

---

**Documento completado**: 2025-12-07
**Estado**: Listo para implementación
**Próximo paso**: Comenzar Fase 1 (Autenticación) en ficem-core
