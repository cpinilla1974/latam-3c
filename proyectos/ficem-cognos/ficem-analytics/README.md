# FICEM Analytics - Reportabilidad Inteligente

## Objetivo

Sistema de agentes IA especializados para:
- Validación automática de calidad de datos MRV (emisiones CO2)
- Detección de anomalías en reportes de sostenibilidad
- Monitoreo de cumplimiento normativo (BID, IFC, CAF, ONU)
- Generación automática de reportes ejecutivos

## Casos de Uso Día a Día

### 1. Validación de Envíos MRV
**Escenario**: Planta Yura envía Excel con datos MRV 2025 (producción clínker, consumo eléctrico, combustibles)
**Agente**: Validation Agent
**Output**:
- **Validaciones estructurales**: "Falta dato consumo eléctrico Q3" o "Factor de emisión carbón (100 kg CO2/GJ) != protocolo Perú (96.3 kg CO2/GJ)"
- **Validaciones de coherencia**: "Producción clínker 2025 = 0 pero consumo combustibles > 0"
- **Validaciones temporales**: "Factor clínker 2025 (0.95) está 25% sobre histórico 2021-2024 (0.75-0.78). ¿Es correcto?"
- Dashboard con semáforo: ✅ OK | ⚠️ Advertencias | ❌ Errores críticos

### 2. Detección de Anomalías en Series Temporales
**Escenario**: Planta reporta consumo eléctrico 2025 = 120 KWh/ton cemento cuando histórico 2021-2024 fue 95-100 KWh/ton
**Agente**: Anomaly Detection Agent
**Output**:
- Alerta: "Consumo eléctrico subió 20-25% vs histórico"
- Análisis: "Posibles causas: (1) Expansión de planta, (2) Cambio de proceso, (3) Error de dato"
- Comparación: "Promedio Perú: 98 KWh/ton | Tu valor: 120 (+22%)"
- Acción sugerida: "Solicitar verificación a empresa antes de aprobar"

### 3. Benchmarking de Bandas GCCA
**Escenario**: "¿Cómo está Pacasmayo vs otras empresas Perú en factor clínker?"
**Agente**: Benchmarking Agent
**Output**:
- **Producto-nivel**:
  - Pacasmayo CPC30: Factor clínker 0.76 → Banda GCCA B (cemento)
  - Pacasmayo Concreto 25 MPa: 215 kg CO2/m³ → Banda GCCA B (concreto)
- **Comparación nacional**:
  - Promedio Perú cemento: 0.78
  - Mejor Perú: 0.72 (Planta X anónima)
  - Percentil Pacasmayo: 65 (mejor que 65% del país)
- **Curva de Perry**: Scatter plot resistencia vs huella CO2 con Pacasmayo marcado

### 4. Tracking Hoja de Ruta 2050
**Escenario**: "¿Estamos on-track para cumplir target 2030 de 520 kg CO2e/tcem en Perú?"
**Agente**: Roadmap Monitor Agent
**Output**:
- **Situación actual (2025)**: 580 kg CO2e/tcem
- **Target 2030**: 520 kg CO2e/tcem
- **Gap**: 60 kg (10.3% reducción requerida)
- **Velocidad actual**: Reduciendo 8 kg/año (histórico 2021-2025)
- **Velocidad requerida**: 12 kg/año para llegar a meta
- **Alerta**: ⚠️ "Ritmo insuficiente, necesitas acelerar 50%"
- **Acciones sugeridas**: Aumentar coprocesamiento, reducir factor clínker, mejorar eficiencia energética

### 5. Consolidación Automática de Reportes País
**Escenario**: Coordinador ASOCEM necesita generar "Reporte Indicadores-Año 2025" para PRODUCE
**Agente**: Report Generation Agent
**Output**:
- **PDF ejecutivo con 3 secciones**:
  - Sección I: Producción consolidada (Σ de 6 plantas: clínker, cemento, concreto)
  - Sección II: Indicadores técnicos (factor clínker promedio ponderado: 0.76, consumo térmico: 3,450 MJ/ton, coprocesamiento: 12%)
  - Sección III: Emisiones CO2 por alcance (Alcance 1: 520 kg, Alcance 2: 45 kg, Alcance 3: 15 kg)
- **Gráficos**: Evolución 2021-2025, comparación vs target 2030, distribución de bandas GCCA
- **Formato**: PDF para ministerio + Excel con datos raw para análisis

### 6. Detección de Inconsistencias entre Fuentes
**Escenario**: FICEM recibe datos de Perú vía 4C-Peru (sistema digital) y vía Excel manual (Hoja de Ruta). Hay discrepancias.
**Agente**: Data Quality Agent
**Output**:
- Comparación automática: "Producción clínker Yura 2024: 4C-Peru = 450,000 ton | Excel manual = 455,000 ton (delta: +1.1%)"
- Identificación de fuente correcta: "4C-Peru tiene trazabilidad mensual, Excel manual es estimado anual"
- Sugerencia: "Usar dato 4C-Peru como oficial, marcar Excel manual como obsoleto"
- Audit trail: Log de qué dato se usó y por qué

## Inputs

### Datos MRV Estructurados (Excel + SQLite)
- **Archivos Excel MRV por país**:
  - Plantillas estandarizadas según Protocolo MRV Perú 2025 (CSI Protocol 3.1 + IPCC 2006)
  - Datos por planta: Producción (clínker, cemento, concreto), Consumo energético (SEIN, combustibles), Factores de emisión
  - Período histórico: 2010-2024 + proyección 2025-2030
  - Ejemplos: `/storage/00.- Hoja de Ruta FICEM/6 Perú/Planta A.xls`

- **Calculadoras 3C** (5 bases de datos SQLite):
  - Pacasmayo (Perú): 9 productos cemento, 3 plantas, 103 registros (2014-2024)
  - Yura (Perú): 3 productos cemento, 177 registros (2020-2024)
  - Melón (Chile): 5 productos cemento, 4 plantas, 119 registros (2023)
  - Moctezuma (México): 2 productos cemento (CPC30, CPC40), 3 plantas, 488 registros (2020-2025)
  - Loma Negra (Argentina): 3 productos cemento, 2 plantas, 75 registros (2020-2024)

- **Datos de productos individuales**:
  - 962 registros consolidados de productos comerciales reales
  - 22 productos únicos (CPO, CPC30, CPC40, Tipo I, Tipo IP, etc.)
  - Factor clínker por producto (rango: 0.377 - 0.965)
  - Base de datos: `productos_cemento.db` con tablas producto/planta/país

### Protocolos y Normativas
- **Protocolos MRV**:
  - CSI Protocol 3.1 (WBCSD Cement Sustainability Initiative)
  - IPCC 2006 Guidelines (Vol. 2 Energy, Vol. 3 Industrial Processes)
  - GHG Protocol Corporate Standard
- **Factores de emisión específicos**:
  - Perú: Factores SEIN (electricidad), factores combustibles (carbón, fueloil, gas natural)
  - Tabla C.2.1: Combustibles tradicionales (96.3 kg CO2/GJ carbón, 77.4 fuel oil, 56.1 gas natural)
  - Combustibles alternativos por empresa

### Benchmarks y Referencias
- **Bandas GCCA**: Clasificación productos por CO2
  - Cemento: Bandas A-G según kg CO2/ton cemento
  - Concreto: Bandas AA-AF según kg CO2/m³ y resistencia (MPa)
  - Clínker: Bandas según kg CO2/ton clínker
- **GNR (Getting the Numbers Right)**: Datos consolidados por país
- **Hoja de Ruta 2050**: Targets de reducción (ej: Perú 2030 = 520 kg CO2e/tcem)
- **HojaRuta_2.accdb**: Base Access con datos pseudonimizados de 52 plantas, 7 países LATAM

## Arquitectura de Agentes

```
┌──────────────────────────────────────────────────────────┐
│   1. Data Ingestion Agent                                │
│   ├─ Parser Excel MRV (CSI Protocol 3.1 format)         │
│   ├─ Extractor SQLite (calculadoras 3C)                 │
│   └─ Loader Access (HojaRuta_2.accdb)                   │
├──────────────────────────────────────────────────────────┤
│   2. Validation Agent                                     │
│   ├─ Validador Estructural (campos faltantes, tipos)    │
│   ├─ Validador de Protocolo (vs CSI/IPCC/SEIN)          │
│   ├─ Validador de Coherencia (balances de masa)         │
│   └─ Validador Temporal (vs histórico planta)           │
├──────────────────────────────────────────────────────────┤
│   3. Anomaly Detection Agent                             │
│   ├─ Detector de Outliers (Isolation Forest)            │
│   ├─ Detector de Drift (cambios estructurales)          │
│   └─ Comparador Multi-fuente (4C vs Excel manual)       │
├──────────────────────────────────────────────────────────┤
│   4. Compliance Monitor Agent                            │
│   ├─ Verificador CSI Protocol 3.1                       │
│   ├─ Verificador IPCC 2006                              │
│   └─ Monitor de actualizaciones normativas              │
├──────────────────────────────────────────────────────────┤
│   5. Benchmarking Agent                                  │
│   ├─ Clasificador Bandas GCCA (cemento/concreto/clínker)│
│   ├─ Generador Curvas de Perry (resistencia vs CO2)    │
│   ├─ Comparador Producto/Planta/País                    │
│   └─ Posicionador Percentil                             │
├──────────────────────────────────────────────────────────┤
│   6. Roadmap Monitor Agent                               │
│   ├─ Tracker Hoja de Ruta 2050                          │
│   ├─ Calculador de Gaps (actual vs target)              │
│   ├─ Proyector de Tendencias (Prophet/regresión)        │
│   └─ Sugeridor de Acciones (reducción CO2)              │
├──────────────────────────────────────────────────────────┤
│   7. Report Generation Agent                             │
│   ├─ Generador Reporte Indicadores-Año (Sección I-III)  │
│   ├─ Consolidador País (Σ plantas)                      │
│   ├─ Exportador Multi-formato (PDF/Excel/PPT)           │
│   └─ Versionador de Reportes (audit trail)              │
└──────────────────────────────────────────────────────────┘
```

## Outputs

### Automáticos (diario/semanal)
- **Dashboard de calidad de datos**: Anomalías detectadas, prioridad, status
- **Alertas de compliance**: Cambios normativos, gaps identificados
- **Resumen ejecutivo semanal**: Top 5 hallazgos críticos

### Bajo Demanda (minutos)
- **Reportes ejecutivos**: PDF/Excel con análisis específico
- **Benchmarking comparativo**: Gráficos empresa vs sector
- **Audit trail**: Trazabilidad completa de validaciones

## Tecnología

| Componente | Stack | Justificación |
|------------|-------|---------------|
| **Multi-Agent** | LangGraph | Orquestación de workflows complejos |
| **Agentes** | CrewAI / AutoGen | Framework especializado colaboración |
| **Data Quality** | Great Expectations | Validación declarativa audit-ready |
| **Anomaly Detection** | Isolation Forest / LSTM | Unsupervised ML para time-series |
| **LLM** | Claude 3.5 Sonnet | Generación reportes + análisis complejo |
| **Base de Datos** | PostgreSQL + TimescaleDB | Time-series (emisiones CO2) |
| **Vector DB** | ChromaDB | Búsqueda semántica en PDFs |
| **Dashboards** | Plotly Dash | Visualizaciones interactivas |

## Riesgos Identificados

### Alto Impacto
1. **GIGO (Garbage In, Garbage Out)**: Datos de entrada incorrectos → análisis erróneo
   - Mitigación: Validación multi-nivel + human review de inputs críticos

2. **False Negatives en Anomaly Detection**: No detectar problema real
   - Mitigación: Tuning conservador + audit random sample

3. **Regulatory Lag**: Normativa cambia pero sistema desactualizado
   - Mitigación: Regulatory Monitor Agent + versioning de reglas

### Medio Impacto
4. **Data Drift**: Cambios legítimos marcados como anomalías
5. **Integration Complexity**: Múltiples fuentes heterogéneas

### Bajo Impacto
6. **Curva de aprendizaje**: Staff debe aprender a usar agentes

## Mayor Desafío: Heterogeneidad de Fuentes de Datos

**El desafío NO es tecnológico (agentes IA maduros), ES integrar fuentes heterogéneas**:

### Problema 1: Múltiples Formatos por País
- **Excel MRV**: Cada país tiene plantilla propia (Perú, Chile, México, Argentina)
- **Calculadoras 3C**: 5 esquemas SQLite diferentes con estructura no estandarizada
  - Indicador "11" en Yura = Clínker consumido
  - Indicador "92a" en Melón/Moctezuma/Loma = Factor clínker directo
  - Suma de clínkeres por dataset (un producto puede usar múltiples tipos)
- **Access Hoja de Ruta**: HojaRuta_2.accdb con 52 plantas pseudonimizadas
- **Formatos legacy**: Excel manual con "Inconsistencias IFC", "por verificar", múltiples versiones

### Problema 2: Tres Niveles de Agregación
- **Nivel Producto**: 962 productos comerciales (CPO, CPC30, Tipo I, etc.) - lo más granular
- **Nivel Planta**: 52 plantas pseudonimizadas ("Planta A", "Planta B") - datos GNR
- **Nivel País**: Consolidados nacionales (promedios ponderados) - lo más agregado

**Riesgo crítico**: Mezclar niveles de agregación lleva a análisis incorrectos
- Ejemplo: Comparar factor clínker país (0.76 promedio) con factor producto individual (0.377-0.965 rango)

### Problema 3: Versionado y Trazabilidad
- Múltiples versiones de mismo reporte ("Reporte Perú preliminar.pdf", "por verificar pdf.pdf")
- Cambios de codificación entre años ("Nueva codificación 2016.zip")
- Datos de 4C-Peru digital vs Excel manual: ¿cuál es oficial?
- Carpetas "Inconsistencias IFC" sin documentar qué se corrigió

### Solución: Pre-fase de Data Engineering (6-8 semanas)

**Fase 1: Auditoría de Fuentes (2 semanas)**
1. Inventario completo de fuentes de datos por país
2. Mapeo de esquemas (Excel → SQLite → Access)
3. Identificación de inconsistencias entre fuentes
4. Definición de "fuente oficial" por tipo de dato

**Fase 2: Estandarización de Esquema (3 semanas)**
1. Diseño de esquema unificado para 3 niveles (producto/planta/país)
2. Scripts de ETL por fuente:
   - Parser Excel MRV → esquema unificado
   - Extractor SQLite 3C → normalización de indicadores
   - Loader Access → pseudonimización consistente
3. Implementación de suma de clínkeres por dataset
4. Validación de balances de masa (producción = consumo + stock)

**Fase 3: Versionado y Governance (1-2 semanas)**
1. Sistema de versionado de reportes (git-like para datos)
2. Audit trail: qué dato se usó de qué fuente en qué análisis
3. Políticas de conflicto: si 4C-Peru != Excel manual, ¿qué hacer?
4. Documentación de metadata (fecha, fuente, nivel de confianza)

**Fase 4: Integración con 4C-Peru (1 semana)**
1. APIs de ficem-core para envío de datos validados
2. Sincronización bidireccional 4C-Peru ↔ FICEM Analytics
3. Dashboard de salud de datos (% completitud, % validados, anomalías pendientes)

**Costo estimado**: $15-25K (consultoría especializada + desarrollo)
**Pre-requisito crítico**: Sin esto, cualquier agente IA dará resultados incorrectos

## Integración

- **FICEM Core**: Consumo de APIs de datos MRV
- **4C-Peru**: Validación de datos antes de publicación en dashboards

## Estado

Fase: **Conceptualización**
Usuarios objetivo: **Equipo técnico FICEM + Empresas socias**

## Documentación Adicional

- [Análisis de Mercado y Buenas Prácticas](analisis-mercado-buenas-practicas.md) - Benchmarking con sistemas similares, arquitectura de agentes