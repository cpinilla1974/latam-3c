# Reporte de Integridad y Completitud de Base de Datos
## Proyecto LATAM-3C

**Fecha:** 2025-12-02
**Analista:** Claude AI
**Base de datos analizada:** ficem_bd.db + latam4c_db (PostgreSQL)

---

## Resumen Ejecutivo

Se realizó un análisis completo de integridad de datos en el proyecto LATAM-3C. Se identificaron **dos bases de datos principales**:

1. **ficem_bd.db** (SQLite) - Base de datos operacional con **255,328 remitos**
2. **latam4c_db** (PostgreSQL) - Base de datos agregada con **260 registros** (agregaciones)

### Hallazgos Clave

- **Total de remitos individuales:** 255,328 registros
- **Cobertura temporal:** 2020-2024 (5 años)
- **Empresas/Plantas:** 18 plantas distintas
- **Columnas con problemas críticos:** 6 columnas completamente vacías
- **Campos con completitud parcial:** 5 columnas con <60% de datos

---

## 1. Base de Datos Principal: ficem_bd.db (SQLite)

### 1.1 Información General

- **Ubicación:** `/home/cpinilla/databases/ficem_bd/data/ficem_bd.db`
- **Tamaño:** 170 MB
- **Total de tablas:** 24 tablas
- **Tabla principal:** `remitos_concretos`
- **Registros totales:** 255,328 remitos

### 1.2 Estructura de la Tabla `remitos_concretos`

La tabla contiene **32 columnas** con la siguiente estructura:

#### Columnas Obligatorias (NOT NULL) - 100% Completitud

| Columna | Tipo | Descripción | Completitud |
|---------|------|-------------|-------------|
| `id_remito` | TEXT | Identificador único | 100% |
| `compania` | TEXT | Compañía emisora | 100% |
| `planta` | TEXT | Planta de origen | 100% |
| `fecha` | DATE | Fecha del remito | 100% |
| `año` | INTEGER | Año | 100% |
| `formulacion` | TEXT | Tipo de formulación | 100% |
| `resistencia` | REAL | Resistencia del concreto (MPa) | 100% |
| `volumen` | REAL | Volumen en m³ | 100% |
| `huella_co2` | REAL | Huella de carbono (kg CO2/m³) | 100% |

#### Columnas Calculadas - 100% Completitud

| Columna | Tipo | Descripción | Completitud |
|---------|------|-------------|-------------|
| `mes` | INTEGER | Mes del remito | 100% |
| `trimestre` | INTEGER | Trimestre | 100% |
| `a1_total` | REAL | Emisiones A1 totales | 100% |
| `a2_total` | REAL | Emisiones A2 totales | 100% |
| `a3_total` | REAL | Emisiones A3 totales | 100% |
| `total_a1_a3` | REAL | Total A1+A2+A3 | 100% |
| `a1_intensidad` | REAL | Intensidad A1 | 100% |
| `a2_intensidad` | REAL | Intensidad A2 | 100% |
| `a3_intensidad` | REAL | Intensidad A3 | 100% |
| `archivo_origen` | TEXT | Archivo de origen | 100% |
| `fecha_carga` | DATETIME | Fecha de carga | 100% |
| `version_datos` | TEXT | Versión de datos | 100% |

---

### 1.3 Problemas de Completitud Identificados

#### 🔴 CRÍTICO - Columnas Completamente Vacías (0% datos)

| Columna | NULLs | Impacto | Recomendación |
|---------|-------|---------|---------------|
| `tipo_cemento` | 255,328 (100%) | **ALTO** | Requerir este dato en captura. Crítico para cálculos EPD |
| `slump` | 255,328 (100%) | MEDIO | Dato técnico importante para análisis de calidad |
| `a5_total` | 255,328 (100%) | ALTO | Sin datos de fase A5 (construcción). Limita análisis ciclo de vida completo |
| `total_a1_a5` | 255,328 (100%) | ALTO | No se puede calcular huella completa A1-A5 |
| `a5_intensidad` | 255,328 (100%) | ALTO | Sin intensidad de fase construcción |
| `huella_co2_completa` | 255,328 (100%) | ALTO | Campo calculado faltante por ausencia de A5 |

#### 🟠 MODERADO - Columnas Parcialmente Llenas

| Columna | Completitud | NULLs | Impacto | Recomendación |
|---------|-------------|-------|---------|---------------|
| `a4_total` | 42.41% | 147,043 | ALTO | Solo 42% tiene datos de transporte al sitio |
| `a4_intensidad` | 42.41% | 147,043 | ALTO | Limita análisis de impacto logístico |
| `contenido_cemento` | 57.58% | 108,321 | MEDIO | Dato importante para análisis de intensidad de materiales |
| `proyecto` | 57.59% | 108,286 | BAJO | Información útil pero no crítica |
| `cliente` | 57.59% | 108,285 | BAJO | Información comercial, no crítica para análisis técnico |

---

### 1.4 Distribución de Datos

#### Por Planta (Top 15)

| Planta | Remitos | % del Total |
|--------|---------|-------------|
| 72 | 51,842 | 20.30% |
| 45 | 28,752 | 11.26% |
| 12 | 24,379 | 9.55% |
| Lo Espejo 2 | 20,126 | 7.88% |
| Lo Espejo 1 | 17,541 | 6.87% |
| 27 | 17,264 | 6.76% |
| Lo Espejo 3 | 17,228 | 6.75% |
| 4 | 15,332 | 6.00% |
| Concon | 10,779 | 4.22% |
| 30 | 9,474 | 3.71% |
| Puerto Montt | 8,976 | 3.52% |
| Maipu | 8,289 | 3.25% |
| San Martin 1 | 8,193 | 3.21% |
| La Serena 2 | 7,457 | 2.92% |
| San Martin 2 | 3,581 | 1.40% |

**Total de plantas distintas:** 18

#### Por Año

| Año | Remitos | % del Total |
|-----|---------|-------------|
| 2023 | 140,406 | 54.99% |
| 2021 | 40,974 | 16.05% |
| 2022 | 33,481 | 13.11% |
| 2020 | 31,005 | 12.14% |
| 2024 | 9,462 | 3.71% |

**Observación:** Fuerte concentración en 2023 (55% de los datos). Año 2024 con pocos datos (probablemente datos parciales).

#### Por Fuente de Datos

| Fuente | Remitos | % del Total |
|--------|---------|-------------|
| main.db (corp_concretos + corp_co2) | 147,043 | 57.59% |
| main_old.db | 108,285 | 42.41% |

**Observación:** Los datos de `main_old.db` tienen menos campos completos (no tienen A4_total, proyecto, cliente).

---

### 1.5 Rangos de Valores Numéricos

| Campo | Mínimo | Máximo | Promedio | Comentarios |
|-------|--------|--------|----------|-------------|
| `año` | 2020 | 2024 | 2022.22 | 5 años de datos |
| `resistencia` | 0.49 MPa | 79.92 MPa | 27.40 MPa | Rango amplio, incluye productos especiales |
| `volumen` | 0.50 m³ | 12.00 m³ | 6.98 m³ | Volumen promedio ~7 m³ por remito |
| `huella_co2` | 0.70 kg/m³ | 1,483.73 kg/m³ | 270.94 kg/m³ | Rango muy amplio. Máximo parece outlier |
| `contenido_cemento` | 0.01 kg/m³ | 7,621.00 kg/m³ | 2,344.27 kg/m³ | Máximo parece error de datos |
| `a1_total` | 0.00 kg CO2 | 5,592.90 kg CO2 | 1,730.07 kg CO2 | Emisiones de materiales |
| `a2_total` | 0.00 kg CO2 | 691.89 kg CO2 | 125.74 kg CO2 | Emisiones de transporte de materiales |

**⚠️ Anomalías detectadas:**
- `huella_co2` máximo de 1,483 kg/m³ parece anómalo (típico: 200-400 kg/m³)
- `contenido_cemento` máximo de 7,621 kg/m³ es físicamente imposible (típico: 250-400 kg/m³)

---

## 2. Base de Datos PostgreSQL: latam4c_db

### 2.1 Información General

- **Host:** localhost
- **Puerto:** 5432
- **Base de datos:** latam4c_db
- **Total de tablas:** 7 tablas
- **Tipo:** Base de datos de agregaciones y datos maestros

### 2.2 Tablas y Contenido

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| `huella_concretos` | 260 | Agregaciones de huella por origen/año |
| `cementos` | 139 | Datos de cementos por planta/año |
| `plantas_latam` | 265 | Catálogo de plantas en LATAM |
| `tb_cubo` | 158,232 | Cubo de indicadores por país/año |
| `indicadores` | 1,344 | Catálogo de indicadores |
| `entidades_m49` | 256 | Catálogo de países (M49) |
| `empresas` | 0 | **Tabla vacía** |

### 2.3 Tabla `huella_concretos` (Agregaciones)

**Estructura:** 20 columnas, todos los campos son NULLABLE

**Completitud:** ✅ 100% - Todos los campos tienen datos completos en los 260 registros

**Distribución:**

- **Empresas/Orígenes:** 4 (mzma, pacas, lomax, melon)
- **Años:** 5 (2020-2024)

**Observación:** Esta tabla contiene agregaciones pre-calculadas. No es la fuente de datos originales.

### 2.4 Tabla `cementos`

**Problema identificado:**
- **Columna `factor_clinker`:** Solo 74.10% completo (36 de 139 registros sin dato)
- **Impacto:** Dificulta cálculo de emisiones de CO2 de cemento con precisión

### 2.5 Tabla `plantas_latam`

**Completitud general:** ✅ Excelente (>99% en todos los campos)

- Total de plantas: 265
- Única columna con NULL: `capacidad_instalada` (1 registro faltante = 99.62% completo)

### 2.6 Otras Tablas

**`tb_cubo` (158,232 registros):**
- Problema: `fecha_migracion` solo 42.70% completo

**`indicadores` (1,344 registros):**
- Problemas críticos:
  - `id_subtipo_producto`: 17.63% completo
  - `subgrupo`: 45.31% completo
  - `tipo_objeto`: 71.28% completo

---

## 3. Análisis de Impacto y Recomendaciones

### 3.1 Campos Críticos Faltantes que Limitan el Análisis

#### 🔴 PRIORIDAD ALTA - Implementar Inmediatamente

1. **`tipo_cemento`** (0% datos)
   - **Impacto:** Sin este dato no se puede:
     - Clasificar correctamente emisiones por tipo de cemento
     - Aplicar factores de emisión específicos
     - Cumplir con estándares EPD que requieren especificar tipo de cemento
   - **Acción:** Agregar campo obligatorio en captura de datos
   - **Fuente:** Debe venir de las plantas o facturas

2. **`a5_total` y `a5_intensidad`** (0% datos)
   - **Impacto:**
     - No se puede calcular ciclo de vida completo (A1-A5)
     - Solo se tiene hasta A3 (fabricación) o A4 (transporte)
     - Limita comparaciones con benchmarks internacionales
   - **Acción:**
     - Si no se tiene el dato, documentar que análisis es A1-A3 (cradle-to-gate)
     - O calcular A5 con metodología estándar

3. **`a4_total` y `a4_intensidad`** (42% datos)
   - **Impacto:**
     - Más de la mitad de remitos no tienen datos de transporte al sitio
     - Subestimación de huella de carbono total
     - Inconsistencia en comparaciones
   - **Acción:** Requerir distancia/modo de transporte en todos los remitos

#### 🟡 PRIORIDAD MEDIA - Mejorar Calidad de Datos

4. **`contenido_cemento`** (58% datos)
   - **Impacto:**
     - Dificulta análisis de optimización de mezclas
     - No se puede correlacionar huella con contenido de cemento
   - **Acción:** Extraer de formulaciones técnicas existentes

5. **`slump`** (0% datos)
   - **Impacto:**
     - Dato técnico útil para análisis de calidad
     - No crítico para huella de carbono
   - **Acción:** Agregar si está disponible en registros de planta

6. **`factor_clinker` en tabla cementos** (74% datos)
   - **Impacto:**
     - 26% de cementos sin factor de clinker
     - Afecta precisión de cálculos de CO2
   - **Acción:** Solicitar a plantas o usar valores por defecto documentados

#### 🟢 PRIORIDAD BAJA - Información Complementaria

7. **`proyecto` y `cliente`** (58% datos)
   - **Impacto:** Bajo - información comercial
   - **Acción:** Opcional, útil para reportes por proyecto

---

### 3.2 Anomalías de Datos Detectadas

#### Valores Fuera de Rango Esperado

| Campo | Valor Anómalo | Rango Esperado | Registros Afectados | Acción |
|-------|---------------|----------------|---------------------|--------|
| `huella_co2` | Máx: 1,483 kg/m³ | 150-450 kg/m³ | Revisar outliers | Validar datos > 600 kg/m³ |
| `contenido_cemento` | Máx: 7,621 kg/m³ | 250-450 kg/m³ | Revisar outliers | Corregir errores de unidades |
| `resistencia` | Mín: 0.49 MPa | >10 MPa típico | Revisar < 5 MPa | Validar si son productos especiales |

**Recomendación:** Implementar validaciones en captura de datos:
```sql
-- Validaciones sugeridas
CHECK (huella_co2 BETWEEN 50 AND 800)
CHECK (contenido_cemento BETWEEN 100 AND 600)
CHECK (resistencia > 5.0)
CHECK (volumen BETWEEN 0.5 AND 15.0)
```

---

### 3.3 Análisis de Calidad por Fuente de Datos

| Fuente | Remitos | Campos Completos | Campos Parciales | Calidad General |
|--------|---------|------------------|------------------|-----------------|
| `main.db` (nuevo) | 147,043 (57.6%) | 22/32 | A4_total, contenido_cemento, proyecto, cliente | ⭐⭐⭐⭐ Buena |
| `main_old.db` (antiguo) | 108,285 (42.4%) | 18/32 | Sin A4, sin proyecto, sin cliente | ⭐⭐⭐ Aceptable |

**Observación:** Los datos de `main_old.db` son de menor calidad. Considerar re-procesar si es posible obtener datos faltantes.

---

## 4. Impacto en Funcionalidades del Sistema

### 4.1 Análisis Automático - Limitaciones Actuales

| Funcionalidad | Estado | Limitación | Prioridad Fix |
|---------------|--------|------------|---------------|
| Cálculo huella A1-A3 | ✅ Funcional | Ninguna | - |
| Cálculo huella A1-A5 | ❌ No funcional | Falta A5_total | 🔴 Alta |
| Análisis por tipo cemento | ❌ No funcional | Falta tipo_cemento | 🔴 Alta |
| Benchmarking internacional | ⚠️ Parcial | Solo A1-A3, no A1-A5 | 🔴 Alta |
| Análisis de transporte | ⚠️ Parcial | Solo 42% tiene A4 | 🟡 Media |
| Optimización de mezclas | ⚠️ Parcial | Solo 58% tiene contenido_cemento | 🟡 Media |
| Análisis por proyecto | ⚠️ Parcial | Solo 58% tiene proyecto | 🟢 Baja |
| Control de calidad (slump) | ❌ No funcional | Falta slump | 🟢 Baja |

### 4.2 Reportería - Capacidades Actuales

✅ **Funcional:**
- Huella promedio por planta
- Distribución de resistencias
- Volúmenes por período
- Emisiones A1, A2, A3 por separado
- Intensidad de carbono (kg CO2/m³)

❌ **No Funcional:**
- Análisis por tipo de cemento
- Huella completa A1-A5
- Benchmarking con estándares EPD (requieren A1-A5)

⚠️ **Parcial:**
- Análisis de impacto logístico (A4)
- Correlación cemento-huella

---

## 5. Recomendaciones Priorizadas

### Fase 1 - Crítico (Implementar Ya)

1. **Agregar campo `tipo_cemento` obligatorio**
   - Modificar formularios de captura
   - Back-fill datos históricos consultando a plantas
   - Validar con catálogo de cementos conocidos

2. **Documentar alcance de análisis**
   - Clarificar que análisis actual es A1-A3 (cradle-to-gate)
   - No A1-A5 (cradle-to-grave)
   - Agregar disclaimer en reportes

3. **Implementar validaciones de rango**
   - Validar huella_co2 < 800 kg/m³
   - Validar contenido_cemento < 600 kg/m³
   - Validar resistencia > 5 MPa
   - Alertar sobre valores fuera de rango

### Fase 2 - Importante (Próximos 3 meses)

4. **Completar datos de transporte (A4)**
   - Requerir distancia y modo de transporte
   - Calcular A4 para los 147,043 remitos sin dato
   - Usar valores por defecto documentados si no hay dato específico

5. **Completar `contenido_cemento`**
   - Extraer de formulaciones técnicas
   - Validar con rangos esperados
   - Usar para análisis de optimización

6. **Completar `factor_clinker` en tabla cementos**
   - Solicitar valores faltantes a plantas
   - Usar valores por defecto de literatura para tipos de cemento similares

### Fase 3 - Mejora Continua (6+ meses)

7. **Agregar fase A5 (construcción)**
   - Definir metodología de cálculo
   - Implementar en sistema
   - Permitir análisis A1-A5 completo

8. **Agregar datos de calidad (slump)**
   - Si disponible en registros de planta
   - Permite análisis más completo

9. **Limpieza de datos históricos**
   - Identificar y corregir outliers
   - Re-procesar `main_old.db` si es posible

---

## 6. Métricas de Calidad Actual

### Resumen de Completitud

| Aspecto | Métrica | Estado |
|---------|---------|--------|
| Datos básicos (id, fecha, volumen) | 100% | ✅ Excelente |
| Datos de huella A1-A3 | 100% | ✅ Excelente |
| Datos de transporte A4 | 42.41% | ⚠️ Mejorable |
| Datos de construcción A5 | 0% | ❌ Faltante |
| Metadata técnica (tipo cemento) | 0% | ❌ Faltante |
| Datos de formulación (contenido) | 57.58% | ⚠️ Mejorable |
| Datos comerciales (proyecto) | 57.59% | ⚠️ Aceptable |

### Score de Calidad General

**Score actual: 68/100**

- Datos básicos: ✅ 20/20
- Huella básica A1-A3: ✅ 20/20
- Metadata técnica: ❌ 0/20
- Ciclo de vida completo: ⚠️ 8/20 (solo A4 parcial)
- Datos de formulación: ⚠️ 12/20
- Datos comerciales: ⚠️ 8/20

---

## 7. Plan de Acción Sugerido

### Corto Plazo (1 mes)

- [ ] Agregar campo `tipo_cemento` obligatorio en captura
- [ ] Implementar validaciones de rango en formularios
- [ ] Documentar alcance A1-A3 en reportes
- [ ] Identificar y marcar outliers en datos existentes

### Mediano Plazo (3 meses)

- [ ] Back-fill `tipo_cemento` en datos históricos
- [ ] Completar datos A4 (transporte) usando distancias típicas
- [ ] Extraer `contenido_cemento` de formulaciones
- [ ] Completar `factor_clinker` en tabla cementos

### Largo Plazo (6+ meses)

- [ ] Implementar cálculo de fase A5
- [ ] Habilitar análisis A1-A5 completo
- [ ] Agregar datos de calidad (slump) si disponibles
- [ ] Limpiar y re-procesar datos históricos

---

## 8. Conclusiones

### Fortalezas

✅ **Excelente volumen de datos:** 255,328 remitos es una muestra muy significativa
✅ **Datos básicos completos:** Todos los remitos tienen datos esenciales (id, fecha, planta, volumen)
✅ **Huella A1-A3 completa:** 100% de remitos tienen cálculo de huella cradle-to-gate
✅ **Buena distribución temporal:** 5 años de datos (2020-2024)
✅ **Múltiples plantas:** 18 plantas distintas permiten análisis comparativos

### Debilidades

❌ **Falta tipo de cemento:** 0% de datos - Campo crítico faltante
❌ **Sin fase A5:** No se puede calcular ciclo de vida completo (A1-A5)
⚠️ **Transporte parcial:** Solo 42% tiene datos de transporte (A4)
⚠️ **Contenido de cemento parcial:** Solo 58% tiene este dato técnico importante
⚠️ **Anomalías en datos:** Valores fuera de rango que requieren validación

### Impacto en Análisis Automático

El sistema **puede realizar análisis básicos** de huella de carbono (A1-A3) pero tiene **limitaciones importantes** para:
- Análisis por tipo de cemento
- Benchmarking con estándares internacionales (requieren A1-A5)
- Análisis completo de impacto logístico
- Optimización de mezclas basada en contenido de materiales

---

## Anexos

### A. Scripts de Análisis Utilizados

1. `/home/cpinilla/projects/latam-3c/scripts/analizar_integridad_bd.py` - Análisis PostgreSQL
2. `/home/cpinilla/projects/latam-3c/scripts/analizar_sqlite_ficem.py` - Análisis SQLite

### B. Archivos de Salida

1. `/tmp/analisis_bd_latam3c.txt` - Salida PostgreSQL completa
2. `/tmp/analisis_ficem_bd.txt` - Salida SQLite completa

### C. Bases de Datos Analizadas

- **SQLite:** `/home/cpinilla/databases/ficem_bd/data/ficem_bd.db` (170 MB)
- **PostgreSQL:** `localhost:5432/latam4c_db`

---

**Fin del Reporte**
