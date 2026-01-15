# Estructura de Contenidos - 4C Perú

**Versión**: 1.0
**Fecha**: 2025-12-07
**Scope**: Macroestructura del frontend 4c-peru aligned con Hoja de Ruta 2050 y modelo de dual validation

---

## 1. CONTEXTO ARQUITECTÓNICO

### 1.1 Modelo de Dual Validation

El sistema implementa dos tipos de cálculos:

```
Empresa                          4c-peru (Coordinadores/ASOCEM/PRODUCE)      FICEM Central
    │                                          │                                    │
    ├─ Calcula LOCALMENTE                      │                                    │
    │  (autoevaluación)                        │                                    │
    │  • Genera archivo Excel                  │                                    │
    │  • Ve sus cálculos preliminares          │                                    │
    │  • Valida internamente                   │                                    │
    │                                          │                                    │
    └─ ENVÍA SUBMISSION ─────────────────────>│                                    │
                                               │                                    │
                                    Coordinador REVISA                             │
                                               │                                    │
                                    Aprueba o rechaza ────────────────────────────>│
                                               │                                    │
                                               │      CALCULA CENTRALMENTE          │
                                               │      (validación externa)          │
                                               │      • Verifica factores emisión   │
                                               │      • Re-calcula si es necesario  │
                                               │      • Asigna banda GCCA oficial   │
                                               │      • Publica resultado           │
                                               │<─────────────────────────────────  │
                                               │                                    │
                                   Ve resultado PUBLICADO
```

### 1.2 Estados del Flujo de Datos

```
Empresa: BORRADOR  →  ENVIADO  →  VALIDANDO  →  VALIDADO  →  PUBLICADO
                                   (Coordinador revisa)       (FICEM calcula)
```

**Estados por paso:**
- **BORRADOR**: Empresa está completando su Excel local
- **ENVIADO**: Empresa confirmó envío, está en cola de revisión
- **VALIDANDO**: Coordinador está revisando, puede pedir correcciones
- **RECHAZADO**: Coordinador rechazó, empresa necesita corregir y reenviar
- **APROBADO**: Coordinador aprobó, enviado a FICEM Central
- **CALCULANDO**: FICEM Central está ejecutando cálculos centrales
- **PUBLICADO**: Resultados finales disponibles

### 1.3 Ciclo Anual

- **Inicio**: Generalmente enero o según regulación
- **Deadline para envío**: Según TDR (típicamente 30-90 días)
- **Validación coordinador**: 15-30 días
- **Cálculo central**: 7-14 días
- **Publicación**: Anual (con opción a mensual futuro)

---

## 2. ROLES Y SUS RESPONSABILIDADES

### 2.1 Empresa (Personal de Planta Cementera)

**Niveles de acceso:**
- **Editor**: Carga/edita datos, genera Excel, envía
- **Supervisor**: Aprueba internamente antes de enviar
- **Observador**: Solo lectura

**Responsabilidades:**
1. Descargar plantilla Excel (por tipo: clinker/cemento/concreto)
2. Completar datos de producción, consumo energético, materiales
3. Validar internamente (cálculos locales)
4. Enviar cuando esté lista
5. Recibir feedback de coordinador (aprobado/rechazado)
6. Corregir si fue rechazada
7. Ver resultados finales publicados
8. Compararse en benchmarking anónimo
9. Descargar reporte individual

### 2.2 Coordinador País (ASOCEM + PRODUCE)

**Niveles de acceso:**
- **Coordinador gremio**: Revisa envíos de su gremio/sector
- **Oficial gobierno**: Revisa envíos, valida requisitos legales
- **Analista**: Genera reportes, analiza tendencias
- **Observador**: Solo lectura

**Responsabilidades:**
1. Revisar envíos de empresas (validación de formato, completitud)
2. Aprobar o rechazar con comentarios
3. Monitorear progreso del ciclo anual
4. Ver dashboard de métricas país
5. Generar reportes país para ministerio/gremio
6. Comparar contra targets de Hoja de Ruta 2050
7. Seguimiento de avance hacia 2030 (588 → 520 kg CO₂e/tcem)
8. Análisis de benchmarking nacional
9. Exportar datos consolidados para FICEM

---

## 3. ESTRUCTURA DE PÁGINAS (MACROESTRUCTURA)

### 3.1 Acceso y Autenticación

```
Login (/)
  ├─ Empresa (pertenece a empresa)
  │   └─ Dashboard Empresa
  │
└─ Coordinador (pertenece a ASOCEM/PRODUCE)
      └─ Dashboard Coordinador
```

**JWT Bearer Token** de ficem-core contiene:
- `user_id`: ID del usuario
- `rol`: "editor", "supervisor", "coordinador", "analista"
- `grupo`: "empresa" o "coordinador"
- `empresa_id`: (si grupo = empresa)
- `pais_code`: "PE"

### 3.2 Menú de Navegación

**EMPRESA:**
```
4C PERÚ
├─ Dashboard Empresa
├─ Ciclo Actual [2025]
│   ├─ Descargar Plantilla
│   ├─ Mi Envío
│   └─ Ver Comentarios
├─ Resultados
│   ├─ Mi Resultado (estado actual)
│   ├─ Histórico (años anteriores)
│   └─ Benchmarking
├─ Reportes
│   ├─ Reporte Individual
│   └─ Datos para Exportar
└─ Configuración
    ├─ Perfil
    ├─ Datos Empresa
    └─ Usuarios (si es supervisor)
```

**COORDINADOR:**
```
4C PERÚ
├─ Dashboard Coordinador
├─ Ciclo Actual [2025]
│   ├─ Envíos Pendientes
│   ├─ Por Validar
│   ├─ Validados
│   └─ Histórico
├─ Hoja de Ruta 2050
│   ├─ Dashboard Progreso
│   ├─ Comparativa 2025 vs Target 2030
│   └─ Proyección a 2050
├─ Análisis
│   ├─ Benchmarking Nacional
│   ├─ Tendencias
│   └─ Comparativa por Tipo
├─ Reportes
│   ├─ Reporte Ciclo Anual
│   ├─ Reporte para Ministerio
│   └─ Exportar Datos FICEM
└─ Configuración
    ├─ Usuarios Coordinadores
    └─ Datos País
```

---

## 4. PÁGINAS DETALLADAS POR ROL

### 4.1 EMPRESA

#### **4.1.1 Dashboard Empresa** (`/empresa/dashboard`)

**Propósito**: Resumen del estado actual y acciones rápidas

**Contenido:**
- **Tarjeta principal**: Estado del ciclo actual
  - ¿Hay ciclo abierto? Sí/No
  - Plazo de envío: DD/MM/YYYY
  - Estado de mi envío: BORRADOR | ENVIADO | VALIDANDO | VALIDADO | PUBLICADO
  - Progreso visual (barra)

- **Acciones rápidas:**
  - "Descargar Plantilla" (si en estado BORRADOR)
  - "Ver Comentarios" (si en estado VALIDANDO)
  - "Reenviar" (si rechazado)
  - "Ver Resultado" (si PUBLICADO)

- **Métricas simplificadas:**
  - Mi huella de carbono (kg CO₂e/tcem) - si publicado
  - Mi banda GCCA - si publicado
  - Comparación vs promedio Perú - si publicado

- **Histórico rápido:**
  - Tabla con envíos de años anteriores
  - Estados finales y bandas GCCA

**Rol**: Editor, Supervisor, Observador

---

#### **4.1.2 Ciclo Actual - Descargar Plantilla** (`/empresa/ciclo-actual/descargar`)

**Propósito**: Obtener el Excel personalizado para la empresa

**Contenido:**
- Selector del tipo de producto (si la empresa fabrica múltiples):
  - ☐ Clínker
  - ☐ Cemento
  - ☐ Concreto

- Información sobre qué incluye la plantilla:
  - Hojas: Datos Producción, Energía, Materiales, Cálculos Locales
  - Instrucciones integradas
  - Factores de emisión por Perú 2025

- Botón: **Descargar Excel**
  - Genera con datos de plantilla genérica o pre-poblado si existe envío previo

- Opcionales:
  - Ver guía en línea de cómo completar
  - Descargar versión PDF de instrucciones

**Rol**: Editor, Supervisor

---

#### **4.1.3 Ciclo Actual - Mi Envío** (`/empresa/ciclo-actual/mi-envio`)

**Propósito**: Gestionar el envío actual (borrador, revisión, etc.)

**Contenido:**
- **Estado actual visualizado:**
  - Timeline visual: BORRADOR → ENVIADO → VALIDANDO → VALIDADO → PUBLICADO
  - Dónde estamos: marcado con color
  - Fechas de cada transición

- **Sección BORRADOR:**
  - Si nunca cargó: botón "Cargar Excel"
  - Si ya cargó:
    - Nombre del archivo
    - Fecha de última carga
    - Botones: "Reemplazar", "Validar Localmente", "Enviar"
  - Ver resumen de datos: "Mostrar datos cargados"

- **Sección ENVIADO (después de enviar):**
  - Fecha de envío
  - "Cambiar de parecer": botón para volver a BORRADOR (si no ha sido revisado aún)

- **Sección VALIDANDO (en revisión):**
  - "Coordinador está revisando..."
  - Botón para ver comentarios si hay

- **Sección RECHAZADO (si lo rechazaron):**
  - Motivo del rechazo (comentarios del coordinador)
  - Opción para "Volver a cargar y enviar"

- **Sección VALIDADO (aprobado por coordinador):**
  - "Tu envío fue aprobado"
  - "Esperando resultados finales de FICEM..."

**Rol**: Editor, Supervisor

---

#### **4.1.4 Ciclo Actual - Ver Comentarios** (`/empresa/ciclo-actual/comentarios`)

**Propósito**: Leer feedback del coordinador

**Contenido:**
- Timeline de comentarios (más reciente arriba)
- Por cada comentario:
  - Fecha/hora
  - Autor (coordinador)
  - Mensaje
  - Tipo: INFORMACIÓN | SOLICITUD CORRECCIÓN | RECHAZO | APROBACIÓN

- Si hay SOLICITUD CORRECCIÓN:
  - Botón: "Entendido, voy a corregir" (desbloquea carga nueva)

- Si hay APROBACIÓN:
  - "Tu envío fue aprobado"

**Rol**: Editor, Supervisor, Observador

---

#### **4.1.5 Resultados - Mi Resultado** (`/empresa/resultados/actual`)

**Propósito**: Ver cálculos finales publicados

**Disponible solo cuando: Estado = PUBLICADO**

**Contenido:**
- **Resultado por producto (si fabrica múltiples):**
  - Clínker: 850 kg CO₂e/ton
  - Cemento: 650 kg CO₂e/ton
  - Concreto: 350 kg CO₂e/m³

- **Desglose de emisiones (Alcances):**
  - Alcance 1 (Directo): % del total
  - Alcance 2 (Electricidad): % del total
  - Alcance 3 (Transporte): % del total

- **Clasificación GCCA:**
  - Banda: A | B | C | D | E | F | G (para cemento)
  - Banda: AA | AB | AC | AD | AE | AF (para concreto)
  - Descripción: "Tu producto está en banda A (mejor 10%)"

- **Comparación:**
  - vs Promedio Perú: "Estás 15% por debajo del promedio"
  - vs Target 2030 (Hoja de Ruta): "Necesitas reducir X kg CO₂e/tcem más"
  - Gráfico de posición en benchmarking (anónimo, rangos)

- **Acciones:**
  - Botón: "Descargar Reporte Completo"
  - Botón: "Compartir Resultado"

**Rol**: Editor, Supervisor, Observador

---

#### **4.1.6 Resultados - Histórico** (`/empresa/resultados/historico`)

**Propósito**: Ver evolución anual de huellas

**Contenido:**
- Tabla/Gráfico con años anteriores:
  - Año | Producto | Huella (kg CO₂e) | Banda GCCA | Vs Año Anterior

- Gráfico de tendencia:
  - Eje X: Años
  - Eje Y: kg CO₂e/tcem
  - Línea de tendencia
  - Línea de target 2030 y 2050

**Rol**: Observador, Supervisor, Editor

---

#### **4.1.7 Benchmarking** (`/empresa/resultados/benchmarking`)

**Propósito**: Compararse anónimamente vs industria Perú

**Contenido:**
- Disclaimer: "Datos anónimos, no identificas a otras empresas"
- Gráfico de distribución (box plot o histograma):
  - Tu resultado marcado
  - Rango: mínimo, Q1, mediana, Q3, máximo
  - Bandas GCCA visualizadas como colores

- Tabla de percentiles:
  - "Estás en percentil 65: mejor que 65% del país"

- Desglose por tipo (si aplica):
  - Benchmarking Clínker
  - Benchmarking Cemento
  - Benchmarking Concreto

**Rol**: Observador, Supervisor, Editor

---

#### **4.1.8 Reportes - Reporte Individual** (`/empresa/reportes/individual`)

**Propósito**: Exportar reporte completo para documentación

**Contenido:**
- Opción de formato: PDF | Excel | JSON
- Incluye:
  - Resumen ejecutivo
  - Metodología de cálculo (resumen)
  - Datos de entrada (si se permite)
  - Resultados por alcance
  - Clasificación GCCA
  - Comparativas
  - Sugerencias de mejora (IA)

**Rol**: Supervisor, Observador

---

### 4.2 COORDINADOR

#### **4.2.1 Dashboard Coordinador** (`/coordinador/dashboard`)

**Propósito**: Visión ejecutiva del ciclo anual y salud de Hoja de Ruta

**Contenido:**
- **Tarjetas de estado:**
  - Total Empresas: 45
  - Enviadas: 38 (84%)
  - Por Validar: 7 (16%)
  - Rechazadas/Corrigiendo: 2
  - Aprobadas: 36
  - Con Resultados Publicados: 35

- **Indicadores Hoja de Ruta 2050:**
  - Promedio Perú 2025: 580 kg CO₂e/tcem
  - Target 2030: 520 kg CO₂e/tcem
  - Avance: "Necesitamos reducir 60 kg más (10%)"
  - Proyección si continúa tendencia: "Llegaremos a 565 en 2030 (no alcanzamos)"

- **Gráfico de timeline del ciclo:**
  - Hito actual, próximas fechas importantes

- **Botones de acceso rápido:**
  - "Revisar Envíos Pendientes"
  - "Ver Análisis Hoja de Ruta"
  - "Generar Reporte Ciclo"

**Rol**: Coordinador, Oficial Gobierno, Analista

---

#### **4.2.2 Ciclo Actual - Envíos Pendientes** (`/coordinador/ciclo-actual/pendientes`)

**Propósito**: Revisar y validar envíos de empresas

**Contenido:**
- **Tabla de envíos:**
  - Empresa | Tipo Producto | Fecha Envío | Estado | Acciones

- **Estados visibles en tabla:**
  - ENVIADO (no revisado)
  - VALIDANDO (en revisión actualmente)
  - RECHAZADO (empresa corrigiendo)
  - APROBADO (listo para FICEM)

- **Acciones por row:**
  - "Revisar" → Abre panel lateral para validación
  - "Comentarios" → Ver historial de feedback
  - "Descargar Excel" → Descarga el archivo enviado

- **Panel de revisión (lateral o modal):**
  - Vista previa del Excel cargado
  - Checklist de validación:
    - ☐ Estructura correcta
    - ☐ Todos los campos completados
    - ☐ Datos coherentes (ej: producción > 0)
    - ☐ Factores de emisión consistentes

  - Cuadro de comentarios para escribir feedback
  - Botones:
    - "Aprobar" (→ Estado APROBADO, envía a FICEM)
    - "Rechazar" (requiere comentario)
    - "Guardar Comentario" (sin cambiar estado)
    - "Solicitar Información" (mantiene en VALIDANDO)

**Rol**: Coordinador, Oficial Gobierno

---

#### **4.2.3 Ciclo Actual - Por Validar** (`/coordinador/ciclo-actual/por-validar`)

**Propósito**: Filtro rápido de envíos que necesitan revisión

**Contenido:**
- Similar a "Envíos Pendientes" pero:
  - Filtrado solo a: ENVIADO + RECHAZADO (ignora APROBADO)
  - Colores destacados para RECHAZADO (urgente)
  - Contador: "7 pendientes, 2 rechazadas"

**Rol**: Coordinador, Oficial Gobierno

---

#### **4.2.4 Ciclo Actual - Validados** (`/coordinador/ciclo-actual/validados`)

**Propósito**: Historial de lo que ya aprobó

**Contenido:**
- Tabla de envíos APROBADOS:
  - Empresa | Tipo | Fecha Aprobación | Estado en FICEM | Acciones

- Estado en FICEM:
  - ENVIADO A FICEM
  - CALCULANDO
  - PUBLICADO

- Acciones:
  - "Ver Resultado Final" (si PUBLICADO)
  - "Descargar Reporte"

**Rol**: Coordinador, Oficial Gobierno, Analista

---

#### **4.2.5 Hoja de Ruta 2050 - Dashboard Progreso** (`/coordinador/hoja-ruta/dashboard`)

**Propósito**: Visualizar avance vs targets de reducción de emisiones

**Contenido:**
- **Indicador Principal:**
  - Huella de carbono promedio Perú (kg CO₂e/tcem)
  - Gráfico tipo speedometer:
    - 2025: 580 (posición actual)
    - Target 2030: 520
    - Meta 2050: 350 (estimado)

- **Gráfico de línea temporal:**
  - Histórico: 2021 → 2025 (con datos reales)
  - Tendencia: línea de tendencia basada en últimos años
  - Targets: líneas horizontales en 2030 (520) y 2050 (350)
  - Proyección: si continúa tendencia actual, dónde estaremos en 2030

- **Desglose por alcance:**
  - Gráfico de contribución: % por Alcance 1, 2, 3
  - Comparación vs año anterior

- **Distribución de bandas GCCA:**
  - Gráfico de pastel: % de empresas en A, B, C, D, E, F, G
  - Conteo de empresas por banda

**Rol**: Coordinador, Oficial Gobierno, Analista

---

#### **4.2.6 Hoja de Ruta - Comparativa 2025 vs Target 2030** (`/coordinador/hoja-ruta/comparativa-2030`)

**Propósito**: Análisis detallado del gap hacia 2030

**Contenido:**
- **Métricas:**
  - Huella 2025: 580 kg CO₂e/tcem
  - Target 2030: 520 kg CO₂e/tcem
  - Gap: 60 kg CO₂e/tcem (10.3%)
  - Años restantes: 5

- **Velocidad de reducción requerida:**
  - Actual: X kg/año
  - Requerida: 60 kg / 5 años = 12 kg/año
  - Estado: "Reduciendo 8 kg/año, necesitamos acelerar"

- **Análisis por subsector (si aplica):**
  - Clínker: X kg (Y años para target)
  - Cemento: X kg (Y años para target)
  - Concreto: X kg (Y años para target)

- **Empresas líderes vs rezagadas:**
  - Top 5 en reducción (últimos 3 años)
  - Bottom 5 (más estancadas)

- **Recomendaciones:**
  - "Necesitas fomentar X tecnología"
  - "Y empresas están atrasadas"

**Rol**: Coordinador, Oficial Gobierno, Analista

---

#### **4.2.7 Análisis - Benchmarking Nacional** (`/coordinador/analisis/benchmarking`)

**Propósito**: Comparar posiciones de empresas Perú vs LATAM

**Contenido:**
- **Tabla de ranking (anónimo):**
  - Posición | Tipo Producto | Huella (kg CO₂e) | Banda GCCA | Empresa
    - (nota: empresa puede estar anónima para empresas pequeñas)

- **Filtros:**
  - Por tipo de producto (clínker/cemento/concreto)
  - Por tamaño de empresa (opcional)
  - Por ubicación (opcional)

- **Gráficos:**
  - Distribución de huella por producto
  - Curva de Perry para cemento/clínker (si hay datos de resistencia)

**Rol**: Analista, Coordinador

---

#### **4.2.8 Análisis - Tendencias** (`/coordinador/analisis/tendencias`)

**Propósito**: Evolución histórica 2021-2025

**Contenido:**
- **Gráfico de línea múltiple:**
  - Línea 1: Promedio Perú
  - Línea 2: Mediana
  - Línea 3: Percentil 25 (mejor 25%)
  - Línea 4: Percentil 75 (peor 25%)

- **Análisis por subsector:**
  - Clínker trend
  - Cemento trend
  - Concreto trend

- **Indicadores:**
  - Mejora anual en %
  - Volatilidad

**Rol**: Analista, Coordinador

---

#### **4.2.9 Reportes - Reporte Ciclo Anual** (`/coordinador/reportes/ciclo-anual`)

**Propósito**: Generar reporte oficial del ciclo 2025

**Contenido:**
- **Resumen ejecutivo:**
  - Empresas participantes
  - Tasa de respuesta
  - Promedio de emisiones
  - Bandas GCCA distribuidas

- **Resultados detallados:**
  - Por tipo de producto
  - Por ubicación (si aplica)
  - Por subsector

- **Análisis Hoja de Ruta:**
  - Progreso 2030
  - Proyección 2050

- **Recomendaciones:**
  - Para gremio (ASOCEM)
  - Para gobierno (PRODUCE)

- **Formatos disponibles:**
  - PDF ejecutivo (5 páginas)
  - Excel detallado (tablas)
  - PPT para presentación

**Rol**: Coordinador, Oficial Gobierno, Analista

---

#### **4.2.10 Reportes - Reporte para Ministerio** (`/coordinador/reportes/ministerio`)

**Propósito**: Documento formal para PRODUCE

**Contenido:**
- Similar a "Ciclo Anual" pero:
  - Enfoque en cumplimiento regulatorio
  - Análisis de impacto ambiental
  - Recomendaciones de política
  - Tablas de comparativa vs otros países (si se tienen datos LATAM)

**Rol**: Oficial Gobierno, Coordinador

---

#### **4.2.11 Reportes - Exportar Datos FICEM** (`/coordinador/reportes/exportar-ficem`)

**Propósito**: Enviar datos consolidados al backend FICEM para análisis regional

**Contenido:**
- Selector de datos:
  - ☐ Envíos aprobados
  - ☐ Resultados publicados
  - ☐ Información de empresas (anónima)
  - ☐ Metadata del ciclo

- Formato:
  - CSV | JSON | Excel

- Botón: "Exportar"
  - Genera archivo listo para compartir con FICEM

**Rol**: Oficial Gobierno, Coordinador

---

## 5. ENDPOINTS NECESARIOS (CONSUMIDOS DE FICEM-CORE)

### 5.1 Autenticación

```
POST /api/auth/login
  Input: { email, password }
  Output: { token, refresh_token, user }

GET /api/auth/me
  Output: { user_id, rol, grupo, empresa_id, ... }
```

### 5.2 Empresas

```
GET /api/empresas?pais=PE
  Output: [{ id, nombre, ubicacion, tipo_producto, ... }]

GET /api/empresas/{id}
  Output: { id, nombre, datos_empresa, ... }

GET /api/empresas/{id}/contactos
  Output: [{ email, rol, ... }]
```

### 5.3 Ciclos y Envíos

```
GET /api/ciclos/actual?pais=PE
  Output: { id, año, fecha_inicio, fecha_fin, estado }

POST /api/plantillas/{tipo}
  Input: { empresa_id, tipo: "clinker|cemento|concreto" }
  Output: { archivo: Excel binario }

POST /api/envios
  Input: { empresa_id, archivo: FormData, ciclo_id }
  Output: { envio_id, estado: "ENVIADO" }

GET /api/envios/{id}
  Output: { id, empresa_id, estado, comentarios, ... }

POST /api/envios/{id}/validar
  Input: { ... (validación local) }
  Output: { errores: [], advertencias: [] }

POST /api/envios/{id}/enviar
  Output: { estado: "ENVIADO", fecha_envio }

GET /api/envios?ciclo_id={id}&estado=ENVIADO
  Output: [{ id, empresa, estado, ... }]

POST /api/envios/{id}/comentarios
  Input: { mensaje, tipo: "SOLICITUD_CORRECCIÓN|APROBACIÓN|RECHAZO" }
  Output: { id, timestamp }

GET /api/envios/{id}/comentarios
  Output: [{ id, autor, mensaje, timestamp }]

POST /api/envios/{id}/aprobar
  Output: { estado: "APROBADO" }

POST /api/envios/{id}/rechazar
  Input: { motivo }
  Output: { estado: "RECHAZADO" }
```

### 5.4 Resultados

```
GET /api/resultados/{empresa_id}?ciclo_id={id}
  Output: {
    huella_kg_co2e,
    banda_gcca,
    desglose: { alcance_1, alcance_2, alcance_3 },
    estado: "PUBLICADO|CALCULANDO"
  }

GET /api/resultados/{empresa_id}/historico
  Output: [{ año, huella, banda, ... }]

GET /api/benchmarking/PE?tipo_producto=cemento
  Output: {
    tu_posicion: { valor, percentil, banda },
    distribucion: { min, q1, mediana, q3, max },
    empresas: [{ posicion, huella, banda }]
  }
```

### 5.5 Hoja de Ruta y Métricas

```
GET /api/hoja-ruta/PE
  Output: {
    año_actual: 2025,
    huella_actual: 580,
    target_2030: 520,
    target_2050: 350,
    proyeccion: { año: 2030, valor: 565 }
  }

GET /api/metricas/PE?ciclo_id={id}
  Output: {
    total_empresas: 45,
    empresas_enviadas: 38,
    empresas_aprobadas: 36,
    empresas_publicadas: 35,
    promedio_huella: 580,
    distribucion_bandas: { A: 5, B: 8, ... }
  }
```

### 5.6 Reportes

```
GET /api/reportes/ciclo-anual?pais=PE&ciclo_id={id}&formato=pdf
  Output: { archivo PDF binario }

GET /api/reportes/ministerio?pais=PE&ciclo_id={id}&formato=pdf
  Output: { archivo PDF binario }

POST /api/exportar/ficem
  Input: { empresa_ids: [], ciclo_id, incluir: [...] }
  Output: { archivo binario (CSV/JSON/Excel) }
```

---

## 6. ESTRUCTURA DE DIRECTORIOS EN 4C-PERU

```
4c-peru/
├── app/
│   ├── layout.tsx                    # Layout principal
│   ├── page.tsx                      # Redirección a login o dashboard
│   │
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx              # Login con JWT
│   │
│   ├── empresa/                      # Namespace empresas
│   │   ├── layout.tsx                # Layout con navbar empresa
│   │   ├── page.tsx                  # Redirige a /empresa/dashboard
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── ciclo-actual/
│   │   │   ├── descargar/
│   │   │   │   └── page.tsx
│   │   │   ├── mi-envio/
│   │   │   │   └── page.tsx
│   │   │   └── comentarios/
│   │   │       └── page.tsx
│   │   ├── resultados/
│   │   │   ├── actual/
│   │   │   │   └── page.tsx
│   │   │   ├── historico/
│   │   │   │   └── page.tsx
│   │   │   └── benchmarking/
│   │   │       └── page.tsx
│   │   └── reportes/
│   │       ├── individual/
│   │       │   └── page.tsx
│   │       └── descargar/
│   │           └── page.tsx
│   │
│   ├── coordinador/                 # Namespace coordinadores
│   │   ├── layout.tsx                # Layout con navbar coordinador
│   │   ├── page.tsx                  # Redirige a /coordinador/dashboard
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── ciclo-actual/
│   │   │   ├── pendientes/
│   │   │   │   └── page.tsx
│   │   │   ├── por-validar/
│   │   │   │   └── page.tsx
│   │   │   └── validados/
│   │   │       └── page.tsx
│   │   ├── hoja-ruta/
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── comparativa-2030/
│   │   │   │   └── page.tsx
│   │   │   └── proyeccion-2050/
│   │   │       └── page.tsx
│   │   ├── analisis/
│   │   │   ├── benchmarking/
│   │   │   │   └── page.tsx
│   │   │   └── tendencias/
│   │   │       └── page.tsx
│   │   └── reportes/
│   │       ├── ciclo-anual/
│   │       │   └── page.tsx
│   │       ├── ministerio/
│   │       │   └── page.tsx
│   │       └── exportar-ficem/
│   │           └── page.tsx
│   │
│   └── error.tsx                    # Error boundary global
│
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── layouts/
│   │   ├── NavbarEmpresa.tsx
│   │   ├── NavbarCoordinador.tsx
│   │   ├── Footer.tsx
│   │   └── Sidebar.tsx
│   ├── shared/
│   │   ├── ThemeToggle.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorAlert.tsx
│   │   └── SuccessAlert.tsx
│   ├── charts/
│   │   ├── HuellaChart.tsx
│   │   ├── BandaGccaChart.tsx
│   │   ├── BenchmarkingChart.tsx
│   │   └── ProgresoHojadeRutaChart.tsx
│   └── forms/
│       ├── UploadExcelForm.tsx
│       ├── ValidacionLocalForm.tsx
│       └── ComentariosForm.tsx
│
├── hooks/
│   ├── useAuth.ts                   # Hook para JWT y usuario
│   ├── useFiemCore.ts               # Hook para consumir APIs
│   └── useLocalStorage.ts
│
├── lib/
│   ├── api.ts                       # Cliente HTTP configurado
│   ├── auth.ts                      # Lógica de JWT
│   └── validators.ts                # Validaciones locales
│
├── utils/
│   ├── apiClient.ts                 # Cliente REST para ficem-core (existente)
│   ├── formatters.ts                # Formateo de datos (números, fechas)
│   └── constants.ts                 # Constantes (estados, bandas, etc.)
│
├── styles/
│   └── globals.css                  # Estilos globales + temas
│
├── public/
│   └── [assets]
│
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── next.config.js
```

---

## 7. FLUJO DE DATOS DETALLADO

### 7.1 Flujo Empresa (Carga + Envío)

```
1. Login
   └─> POST /api/auth/login
   └─> Recibe JWT, guarda en cookie httpOnly

2. Dashboard
   └─> GET /api/ciclos/actual?pais=PE
   └─> GET /api/envios/{empresa_id}?ciclo_id={id}
   └─> Muestra estado actual

3. Descargar Plantilla
   └─> POST /api/plantillas/cemento
   └─> Recibe Excel con estructura + instrucciones

4. Completar Excel (local)
   └─> Empresa abre en su computadora
   └─> Llena datos
   └─> Calcula localmente (fórmulas en Excel)

5. Cargar Excel
   └─> POST /api/envios (con FormData del archivo)
   └─> Backend parsea y valida estructura
   └─> Guarda archivo binario
   └─> Retorna envio_id + estado BORRADOR

6. Validación Local (opcional)
   └─> POST /api/envios/{id}/validar
   └─> Backend devuelve lista de errores/advertencias
   └─> Frontend muestra a empresa

7. Confirmar Envío
   └─> POST /api/envios/{id}/enviar
   └─> Estado pasa a ENVIADO
   └─> Notificación a coordinador

8. Esperar Revisión
   └─> GET /api/envios/{id}/comentarios (polling o WebSocket futuro)
   └─> Muestra feedback del coordinador

9. Ver Resultado (si PUBLICADO)
   └─> GET /api/resultados/{empresa_id}?ciclo_id={id}
   └─> Muestra huella final + banda GCCA
```

### 7.2 Flujo Coordinador (Revisión)

```
1. Login
   └─> POST /api/auth/login (con rol "coordinador")

2. Dashboard
   └─> GET /api/metricas/PE?ciclo_id={id}
   └─> GET /api/hoja-ruta/PE
   └─> Muestra resumen estado

3. Ver Envíos Pendientes
   └─> GET /api/envios?ciclo_id={id}&estado=ENVIADO
   └─> Muestra lista

4. Revisar Envío
   └─> GET /api/envios/{id}
   └─> Descarga Excel con Descargar
   └─> Valida manualmente + guarda comentarios

5. Aprobar
   └─> POST /api/envios/{id}/aprobar
   └─> POST /api/envios/{id}/comentarios (con tipo APROBACIÓN)
   └─> Estado → APROBADO
   └─> Backend envía a ficem-core para cálculos centrales

6. Ver Resultados Publicados
   └─> GET /api/resultados/{empresa_id}?ciclo_id={id}
   └─> Muestra resultados finales

7. Generar Reportes
   └─> GET /api/reportes/ciclo-anual?formato=pdf
   └─> Descarga PDF con análisis consolidado
```

---

## 8. DECISIONES CLAVE

### 8.1 Estados vs Roles

**Estados (del Envío):**
- BORRADOR (local)
- ENVIADO (en cola)
- VALIDANDO (coordinador revisando)
- RECHAZADO (necesita corrección)
- APROBADO (aprobado por coordinador)
- CALCULANDO (FICEM ejecutando)
- PUBLICADO (resultados finales)

**Roles:**
- Empresa Editor (carga Excel)
- Empresa Supervisor (aprueba envío interno)
- Empresa Observador (solo lectura)
- Coordinador (revisa + aprueba)
- Oficial Gobierno (revisa + aprueba)
- Analista (reportes + análisis)

### 8.2 Cálculos Locales vs Centrales

- **Locales**: Empresa puede validar en Excel antes de enviar (fórmulas incluidas)
- **Centrales**: FICEM re-calcula con factores oficiales, asigna banda GCCA final

### 8.3 Visibilidad de Datos

- **Empresa**: Solo ve sus propios datos + benchmarking anónimo
- **Coordinador**: Ve todos los envíos de Perú + agregados + Hoja de Ruta
- **IA/Analytics (futuro)**: Acceso a datos consolidados para análisis

### 8.4 Frecuencia de Ciclos

- **Ciclo 2025**: Anual
- **Futuro**: Posibilidad de mensual o trimestral

---

## 9. PRÓXIMAS ETAPAS

### 9.1 En Desarrollo Paralelo
- ficem-core: Implementar endpoints de API
- knowledge-api: Desarrollar módulo de insights IA

### 9.2 Integración Posterior
- Chat IA sobre datos ("¿Por qué subió mi huella?")
- Predicciones de huella futuro
- Recomendaciones automáticas de mejora

### 9.3 Expansión a Otros Países
- 4c-colombia (mismo frontend, diferente país)
- 4c-ecuador
- Reutiliza APIs de ficem-core con parámetro país

---

**Documento completado**: 2025-12-07
**Próxima revisión**: Después de implementación de páginas 1-2
**Responsable**: Desarrollador Full-Stack
