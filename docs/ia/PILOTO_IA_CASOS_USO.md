# Casos de Uso - Piloto IA FICEM BD

## 📖 Introducción

Este documento detalla los casos de uso principales que el sistema de IA debe resolver. Cada caso incluye:
- **Descripción**: Qué problema resuelve
- **Usuario tipo**: Quién lo usa
- **Input**: Qué información provee el usuario
- **Output esperado**: Qué debe entregar el sistema
- **Datos necesarios**: Qué tablas/indicadores se consultan
- **Criterios de éxito**: Cómo validar que funciona correctamente

---

## 🎯 Caso de Uso 1: Benchmarking Comparativo

### Descripción
Comparar el desempeño de una compañía específica contra benchmarks regionales e internacionales para identificar brechas y oportunidades de mejora.

### Usuario tipo
Analista de sostenibilidad, Gerente de planta

### Input (ejemplos de queries)
```
"Compara la huella de MZMA 2024 con el promedio regional y benchmarks GCCA"
"¿Cómo está mi desempeño de concreto vs competidores?"
"Benchmarking de productos 25 MPa vs mercado"
```

### Output esperado

#### 1. Resumen ejecutivo (texto)
```
Análisis de Benchmarking - MZMA 2024

HUELLA PROMEDIO:
- MZMA 2024: 245 kg CO₂/m³
- Promedio regional (2 compañías): 238 kg CO₂/m³
- Brecha: +7 kg CO₂/m³ (+2.9%)

POSICIÓN EN BANDAS GCCA:
- Banda A (≤210): 15% de productos
- Banda B (211-260): 60% de productos
- Banda C (261-310): 20% de productos
- Banda D-E: 5% de productos

COMPARACIÓN INTERNACIONAL (GNR):
- México (2021): 267 kg CO₂/m³ emisión específica clinker
- Chile (2021): 245 kg CO₂/m³
- Tu posición: Similar a Chile, mejor que promedio México

RECOMENDACIONES:
1. Enfocarse en productos de Banda C y D (25% de volumen)
2. Aumentar uso de SCMs en productos 25-30 MPa
3. Potencial de reducción: ~15 kg CO₂/m³ alcanzando nivel Chile
```

#### 2. Visualizaciones
- **Gráfico de distribución**: Histograma de huella MZMA vs competidores
- **Bandas GCCA**: Pie chart con % de productos por banda
- **Serie temporal**: Evolución de huella 2020-2024
- **Scatter plot**: Resistencia vs Huella con líneas de benchmark

#### 3. Tabla de datos
| Métrica | MZMA 2024 | Competidor | Benchmark GCCA | Gap |
|---------|-----------|------------|----------------|-----|
| Huella promedio (kg CO₂/m³) | 245 | 231 | 235 | +10 |
| % Banda A | 15% | 25% | 30% | -15pp |
| % Banda B | 60% | 55% | 50% | +10pp |
| Volumen Banda C+ (m³) | 50,000 | 30,000 | - | - |

### Datos necesarios
- **Tablas SQL**: `remitos_concretos`, `huella_concretos`, `GCCA_EPD_5_1`, `gnr_data`
- **Indicadores GNR**:
  - `emisión específica clinker` (kg CO₂/t clinker)
  - `emisión neta cemento eq` (kg CO₂/t cem eq)
- **Documentos RAG**: Metodología GCCA, mejores prácticas de reducción

### Criterios de éxito
- ✅ Calcula correctamente huella promedio por compañía/período
- ✅ Clasifica productos en bandas GCCA según tabla de referencia
- ✅ Recupera benchmarks GNR de países relevantes
- ✅ Identifica gaps cuantitativos (kg CO₂, %)
- ✅ Genera 2-3 recomendaciones accionables basadas en datos

---

## 🎯 Caso de Uso 2: Análisis de Portafolio

### Descripción
Identificar qué productos del portafolio de concreto deben optimizarse prioritariamente para maximizar el impacto de reducción de huella.

### Usuario tipo
Gerente de sostenibilidad, Director técnico

### Input (ejemplos de queries)
```
"¿Qué productos debo optimizar primero para reducir mi huella total?"
"Quick wins en mi portafolio de concretos"
"Productos con mayor potencial de mejora"
```

### Output esperado

#### 1. Ranking de productos
```
ANÁLISIS DE PORTAFOLIO - Priorización de Optimización

TOP 5 PRODUCTOS PRIORITARIOS:

1. Concreto 25 MPa (Formulación X)
   - Volumen anual: 45,000 m³ (18% del total)
   - Huella actual: 268 kg CO₂/m³ (Banda C)
   - Huella benchmark: 235 kg CO₂/m³ (Banda B)
   - Potencial de reducción: 33 kg CO₂/m³ × 45,000 m³ = 1,485 t CO₂/año
   - Acción: Reducir clinker 10%, aumentar SCMs
   - Impacto: ⭐⭐⭐⭐⭐ (Alto volumen + gran brecha)

2. Concreto 30 MPa (Formulación Y)
   - Volumen anual: 38,000 m³ (15% del total)
   - Huella actual: 285 kg CO₂/m³ (Banda C)
   - Huella benchmark: 255 kg CO₂/m³ (Banda B)
   - Potencial de reducción: 30 kg CO₂/m³ × 38,000 m³ = 1,140 t CO₂/año
   - Acción: Optimizar mezcla, reducir slump
   - Impacto: ⭐⭐⭐⭐ (Alto volumen + brecha moderada)

[...productos 3-5...]

RESUMEN:
- Optimizando top 5 productos: Reducción potencial de 4,200 t CO₂/año
- Representa 35% del volumen total
- Inversión estimada: Baja (cambios en formulación)
```

#### 2. Visualizaciones
- **Matriz de impacto**: Bubble chart (X: brecha vs benchmark, Y: volumen, tamaño: reducción potencial)
- **Pareto**: Contribución acumulada de productos a huella total
- **Heatmap**: Resistencia vs Año con color = huella promedio

### Datos necesarios
- **Tablas SQL**: `remitos_concretos`, `huella_integrada`, `GCCA_EPD_5_1`
- **Cálculos**:
  - Volumen por producto/formulación/resistencia
  - Huella promedio por producto
  - Gap vs benchmark (Banda GCCA correspondiente)
  - Impacto = Gap × Volumen

### Criterios de éxito
- ✅ Identifica top 5-10 productos por impacto potencial
- ✅ Cuantifica reducción potencial en t CO₂/año
- ✅ Sugiere acciones específicas por producto (basado en RAG de mejores prácticas)
- ✅ Prioriza por "quick wins" (bajo esfuerzo, alto impacto)

---

## 🎯 Caso de Uso 3: Predicción de Huella CO₂

### Descripción
Predecir la huella de carbono de un concreto antes de producirlo, dado sus parámetros técnicos.

### Usuario tipo
Ingeniero de planta, Diseñador de mezclas

### Input (ejemplos de queries)
```
"Si produzco un concreto de 25 MPa con 15% menos clinker, ¿cuál sería la huella?"
"Predice huella de concreto 30 MPa con 20% escoria"
"¿Qué huella tendría si cambio el tipo de cemento de CPC a CPP?"
```

### Output esperado

#### 1. Predicción (texto + valor)
```
PREDICCIÓN DE HUELLA CO₂

Parámetros de entrada:
- Resistencia: 25 MPa
- Tipo de cemento: CPC (Portland Compuesto)
- Contenido cemento: 320 kg/m³ (-15% vs histórico)
- SCMs: 20% escoria
- Slump: 120 mm
- Fecha estimada: 2025-Q1

PREDICCIÓN:
- Huella estimada: 215 kg CO₂/m³
- Intervalo de confianza (95%): 205 - 225 kg CO₂/m³
- Banda GCCA: B (211-260)
- Comparación vs promedio histórico 25 MPa: -18% ✅

FACTORES MÁS INFLUYENTES:
1. Contenido de cemento (-15%): -25 kg CO₂/m³
2. Uso de escoria (20%): -12 kg CO₂/m³
3. Tipo de cemento (CPC vs CPO): -5 kg CO₂/m³

VALIDACIÓN:
- Basado en 18,450 remitos similares (25±2 MPa, 2022-2024)
- Confianza del modelo: Alta (R²=0.84)
```

#### 2. Visualizaciones
- **Rango de predicción**: Gauge chart con intervalo de confianza
- **Bandas GCCA**: Indicador visual de posición
- **Comparación histórica**: Box plot de histórico vs predicción
- **Feature importance**: Bar chart de factores influyentes

### Datos necesarios
- **Tablas SQL**: `remitos_concretos` (para entrenamiento y contexto)
- **Modelo ML**: Modelo entrenado (XGBoost/Random Forest)
- **Features**:
  - Obligatorias: resistencia, contenido_cemento, año
  - Opcionales: tipo_cemento, slump, % SCMs

### Criterios de éxito
- ✅ Predicción con RMSE < 20 kg CO₂/m³
- ✅ Intervalos de confianza realistas (validados con test set)
- ✅ Explica principales factores (feature importance)
- ✅ Advierte si inputs están fuera de rango de entrenamiento
- ✅ Compara predicción con distribución histórica

---

## 🎯 Caso de Uso 4: Detección de Anomalías

### Descripción
Identificar remitos con huellas de carbono inusuales que requieren revisión (errores de carga, formulaciones atípicas, etc.)

### Usuario tipo
Analista de datos, Responsable de calidad de datos

### Input (ejemplos de queries)
```
"Identifica remitos con huellas anormales en octubre 2024"
"Anomalías en datos de MZMA último trimestre"
"¿Hay remitos sospechosos que deba revisar?"
```

### Output esperado

#### 1. Lista de anomalías
```
DETECCIÓN DE ANOMALÍAS - MZMA Octubre 2024

Se identificaron 12 remitos con valores atípicos:

ANOMALÍAS CRÍTICAS (revisar urgente):
1. Remito #MZ-2024-10-1523
   - Huella: 450 kg CO₂/m³ (Esperado: 235±20)
   - Resistencia: 25 MPa
   - Volumen: 8 m³
   - Desviación: +215 kg CO₂/m³ (+91%)
   - Causa probable: Error en carga de dato A1 (muy alto)
   - Acción: Verificar dato origen

2. Remito #MZ-2024-10-1687
   - Huella: 95 kg CO₂/m³ (Esperado: 280±25)
   - Resistencia: 35 MPa
   - Volumen: 12 m³
   - Desviación: -185 kg CO₂/m³ (-66%)
   - Causa probable: Dato incompleto (solo A1, falta A2-A5)
   - Acción: Completar etapas faltantes

ANOMALÍAS LEVES (revisar si es posible):
[...remitos 3-12 con desviaciones menores...]

RESUMEN:
- Total remitos octubre: 8,450
- Anomalías detectadas: 12 (0.14%)
- Impacto en huella promedio: +2.1 kg CO₂/m³
- Huella corregida (sin anomalías): 243 kg CO₂/m³
```

#### 2. Visualizaciones
- **Scatter plot**: Resistencia vs Huella con anomalías marcadas en rojo
- **Time series**: Huella diaria con picos anómalos destacados
- **Distribution**: Histograma con outliers sombreados

### Datos necesarios
- **Tablas SQL**: `remitos_concretos` (datos recientes + histórico para baseline)
- **Modelo**: Isolation Forest o Z-score
- **Umbral**: Definir según distribución (ej: ±3σ o percentil 99)

### Criterios de éxito
- ✅ Detecta >80% de anomalías reales (validado con expertos)
- ✅ Tasa de falsos positivos <10%
- ✅ Sugiere causa probable de anomalía
- ✅ Cuantifica impacto en métricas agregadas
- ✅ Permite marcar remitos como "revisados" o "validados"

---

## 🎯 Caso de Uso 5: Roadmap de Descarbonización

### Descripción
Evaluar la factibilidad de metas de reducción de huella y proponer acciones para alcanzarlas.

### Usuario tipo
Director de sostenibilidad, Gerente general

### Input (ejemplos de queries)
```
"¿Es realista alcanzar 200 kg CO₂/m³ promedio en 2030?"
"Roadmap para reducir 20% mi huella en 5 años"
"¿Qué necesito hacer para estar en Banda A GCCA?"
```

### Output esperado

#### 1. Análisis de factibilidad
```
ROADMAP DE DESCARBONIZACIÓN - Meta: 200 kg CO₂/m³ en 2030

SITUACIÓN ACTUAL (2024):
- Huella promedio: 245 kg CO₂/m³
- Distribución: 15% Banda A, 60% Banda B, 25% Banda C-D
- Tendencia histórica (2020-2024): -3 kg CO₂/m³ por año

META 2030:
- Huella objetivo: 200 kg CO₂/m³
- Reducción requerida: 45 kg CO₂/m³ (-18%)
- Brecha vs tendencia actual: 27 kg CO₂/m³

ANÁLISIS DE FACTIBILIDAD: ⚠️ DESAFIANTE PERO ALCANZABLE

Benchmarking:
- Chile (2021): 245 kg CO₂/m³ → Ya estás en este nivel
- Líder regional: 210 kg CO₂/m³ → Brecha de 35 kg adicionales
- Top global (Europa): 180 kg CO₂/m³ → Requiere inversión mayor

ACCIONES NECESARIAS (Prioridad):

1. CORTO PLAZO (2025-2026): -15 kg CO₂/m³
   - Optimizar top 10 productos (Caso de Uso #2)
   - Aumentar % SCMs de 25% → 35% promedio
   - Reducir clinker en productos Banda C
   - Inversión: Baja | Impacto: Medio

2. MEDIANO PLAZO (2027-2028): -20 kg CO₂/m³
   - Cambiar mix de cementos (más CPP, menos CPO)
   - Incorporar ceniza volante en productos estructurales
   - Mejorar eficiencia energética hornos
   - Inversión: Media | Impacto: Alto

3. LARGO PLAZO (2029-2030): -10 kg CO₂/m³
   - Captura de carbono (piloto)
   - Combustibles alternativos
   - Innovación en formulaciones (geopolímeros)
   - Inversión: Alta | Impacto: Transformacional

PROYECCIÓN:
- Año 2026: 230 kg CO₂/m³
- Año 2028: 215 kg CO₂/m³
- Año 2030: 205 kg CO₂/m³ (ligeramente arriba de meta)

RECOMENDACIÓN:
Ajustar meta a 205-210 kg CO₂/m³ (más realista) o acelerar acciones de mediano plazo.
```

#### 2. Visualizaciones
- **Roadmap timeline**: Gráfico de línea con proyección vs meta
- **Waterfall chart**: Contribución de cada acción a reducción total
- **Scenario analysis**: Comparación de escenarios (conservador/moderado/ambicioso)

### Datos necesarios
- **Tablas SQL**: `remitos_concretos`, `cementos`, `gnr_data`
- **Histórico**: Tendencia de huella 2020-2024
- **Benchmarks**: GNR de países con niveles objetivo
- **Modelo ML**: Proyección de tendencias (Prophet/regresión lineal)
- **RAG**: Base de conocimiento de acciones de descarbonización

### Criterios de éxito
- ✅ Proyecta tendencia histórica con datos reales
- ✅ Compara meta con benchmarks internacionales
- ✅ Propone 3-5 acciones concretas priorizadas
- ✅ Cuantifica impacto de cada acción
- ✅ Identifica gaps entre proyección y meta
- ✅ Genera escenarios alternativos (best/worst case)

---

## 🎯 Caso de Uso 6: Comparación Temporal

### Descripción
Analizar la evolución de la huella de carbono a lo largo del tiempo para identificar tendencias, estacionalidad y cambios estructurales.

### Usuario tipo
Analista de sostenibilidad, Gerente de mejora continua

### Input (ejemplos de queries)
```
"¿Cómo ha evolucionado mi huella en los últimos 3 años?"
"Comparar Q1 2024 vs Q1 2023"
"Tendencias mensuales de huella por resistencia"
```

### Output esperado

#### 1. Análisis de tendencias
```
ANÁLISIS TEMPORAL - MZMA 2020-2024

EVOLUCIÓN GENERAL:
- 2020: 265 kg CO₂/m³
- 2021: 258 kg CO₂/m³ (-7, -2.6%)
- 2022: 251 kg CO₂/m³ (-7, -2.7%)
- 2023: 247 kg CO₂/m³ (-4, -1.6%)
- 2024: 245 kg CO₂/m³ (-2, -0.8%)

Reducción total: 20 kg CO₂/m³ (-7.5% en 4 años)
Tasa promedio: -5 kg CO₂/m³ por año

CAMBIOS ESTRUCTURALES DETECTADOS:
- Jun 2022: Caída de 15 kg (implementación de nueva formulación 25 MPa)
- Ene 2024: Incremento de 8 kg (cambio de proveedor cemento)

ESTACIONALIDAD:
- Q1: Huella +3% vs promedio (mayor uso de productos alta resistencia)
- Q2-Q3: Huella -2% vs promedio
- Q4: Huella +1% vs promedio

POR RESISTENCIA:
- 20 MPa: Mayor mejora (-12 kg, -9%)
- 25 MPa: Mejora moderada (-8 kg, -6%)
- 30+ MPa: Mejora leve (-3 kg, -2%)
```

#### 2. Visualizaciones
- **Serie temporal**: Línea con huella mensual + línea de tendencia
- **Año sobre año**: Bar chart comparativo por trimestre
- **Heatmap**: Mes × Año con color = huella promedio
- **Decomposición**: Tendencia + estacionalidad + residuos

### Datos necesarios
- **Tablas SQL**: `remitos_concretos`, `huella_concretos`
- **Agregaciones**: Por año, trimestre, mes, resistencia
- **Modelo**: Prophet o descomposición estacional

### Criterios de éxito
- ✅ Calcula correctamente tasas de cambio (%, kg CO₂/m³ por período)
- ✅ Detecta cambios estructurales (puntos de quiebre)
- ✅ Identifica patrones estacionales
- ✅ Desagrega por variables relevantes (resistencia, planta, producto)
- ✅ Explica causas probables de cambios (requiere RAG o input usuario)

---

## 📋 Resumen de Priorización

| Caso de Uso | Prioridad | Complejidad | Dependencias |
|-------------|-----------|-------------|--------------|
| 1. Benchmarking Comparativo | ⭐⭐⭐⭐⭐ Alta | Media | RAG + SQL |
| 2. Análisis de Portafolio | ⭐⭐⭐⭐⭐ Alta | Media | SQL + RAG |
| 3. Predicción de Huella | ⭐⭐⭐⭐ Alta | Alta | ML + SQL |
| 4. Detección de Anomalías | ⭐⭐⭐ Media | Media | ML + SQL |
| 5. Roadmap de Descarbonización | ⭐⭐⭐⭐ Alta | Alta | RAG + ML + SQL |
| 6. Comparación Temporal | ⭐⭐⭐ Media | Baja | SQL + ML (opcional) |

### Recomendación para MVP:
1. **Fase 1 (MVP)**: Casos de uso #1, #2, #3
2. **Fase 2 (Extensión)**: Casos de uso #4, #6
3. **Fase 3 (Avanzado)**: Caso de uso #5

---

**Última actualización**: 2025-11-29
**Versión**: 1.0
