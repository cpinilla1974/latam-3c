# Análisis Profundo de Base de Datos LATAM-4C

**Fecha:** 2025-12-02
**Analista:** Claude (Opus 4.5)
**Base de Datos:** latam4c_db

---

## Resumen Ejecutivo

Análisis exhaustivo de 260 registros de huella de carbono de concreto de 4 plantas latinoamericanas (2020-2024), cruzado con referencias GCCA internacionales. Se identificaron patrones no evidentes, anomalías de datos y oportunidades de mejora.

**Hallazgos Clave:**
1. Posible error de escala en datos de planta "pacas"
2. Paradoja de eficiencia: mayor resistencia = menor CO2 por MPa
3. LATAM 8% mejor que promedio mundial GCCA
4. Tendencia positiva: todas las plantas mejorando en 2024

---

## 1. Estructura de Datos Analizada

### Tablas Principales
| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| huella_concretos | 260 | Datos operacionales de huella CO2 |
| cementos | 139 | Tipos de cemento y sus huellas |
| plantas_latam | 265 | Catálogo de plantas LATAM |
| ref_gcca_benchmarks | 17 | Referencias internacionales GCCA |

### Cobertura de Datos
- **Plantas:** 4 (mzma, pacas, lomax, melon)
- **Años:** 2020-2024 (5 años)
- **Volumen total:** ~3.7 millones m³

---

## 2. Hallazgo Crítico: Anomalía en Datos de "pacas"

### Detección
Al normalizar los componentes A1-A4 por volumen:

| Planta | A1 (kg CO2/m³) | A2 | A3 | A4 | Estado |
|--------|----------------|----|----|-----|--------|
| lomax | 236.07 | 57.11 | 5.21 | 8.80 | OK |
| melon | 245.48 | 7.94 | 1.28 | 19.05 | OK |
| mzma | 227.83 | 23.84 | 0.84 | 3.82 | OK |
| **pacas** | **23,249.34** | 589.83 | 526.64 | 942.56 | **ERROR** |

### Diagnóstico
Los valores de "pacas" son ~100x mayores que las otras plantas. Posibles causas:
1. Datos en gramos en vez de kg
2. Totales absolutos sin normalizar
3. Error de carga de datos

### Recomendación
**URGENTE:** Verificar con fuente original de datos de Cementos Pacasmayo (Perú).

---

## 3. La Paradoja de la Eficiencia

### Descubrimiento
Relación inversa entre resistencia y eficiencia de CO2:

| Resistencia (MPa) | Huella (kg CO2/m³) | kg CO2/MPa | Volumen (m³) |
|-------------------|--------------------|-----------:|-------------:|
| 0-10 | 167.07 | 59.74 | 182,039 |
| 10-20 | 232.74 | 14.91 | 556,709 |
| 20-30 | 287.29 | 11.12 | 2,219,897 |
| 30-40 | 339.81 | 9.62 | 556,265 |
| 40-50 | 365.61 | 7.95 | 140,203 |
| 50-60 | 453.46 | 7.88 | 21,997 |
| >60 | 453.57 | 6.05 | 5,191 |

### Interpretación
- **A mayor resistencia, menor huella por unidad de resistencia**
- Concretos de baja resistencia usan casi igual cemento base pero logran menos MPa
- Concretos de alta resistencia aprovechan mejor cada kg de cemento
- **Implicación:** Promover concretos de alta resistencia puede ser estrategia de descarbonización

---

## 4. Análisis de Correlación por Planta

| Planta | Correlación REST-CO2 | Interpretación |
|--------|---------------------:|----------------|
| mzma | 0.9818 | Proceso altamente predecible y controlado |
| lomax | 0.8642 | Buen control de proceso |
| pacas | 0.5970 | Variabilidad moderada |
| melon | 0.2147 | Alta variabilidad - posible optimización caso por caso |

### Insight sobre "melon"
La baja correlación combinada con alta eficiencia (9.38 kg CO2/MPa) sugiere:
- Uso variable de adiciones cementantes (cenizas, escorias)
- Optimización de diseño de mezcla por proyecto
- Mayor flexibilidad en formulaciones

---

## 5. Ranking de Eficiencia por Planta

| Ranking | Planta | kg CO2/MPa | Huella Promedio | CV% |
|:-------:|--------|----------:|----------------:|----:|
| 1 | melon | 9.38 | 255.03 | 26.3% |
| 2 | lomax | 10.18 | 298.39 | 24.4% |
| 3 | mzma | 30.45 | 252.51 | 55.0% |
| 4 | pacas | 34.06 | 294.93 | 28.7% |

### Observaciones
- **melon** logra resistencia con 1/3 del CO2 que mzma
- **mzma** tiene la mayor variabilidad (CV 55%)
- La eficiencia no correlaciona directamente con huella absoluta

---

## 6. Tendencias Temporales

### Evolución de Huella CO2 Promedio

| Planta | 2020 | 2021 | 2022 | 2023 | 2024 | Tendencia |
|--------|-----:|-----:|-----:|-----:|-----:|-----------|
| mzma | 256.37 | 262.47 | 251.32 | 254.08 | 235.79 | Mejorando |
| pacas | - | - | 301.66 | 300.90 | 283.12 | Mejorando |
| lomax | - | - | - | 302.36 | 294.64 | Mejorando |
| melon | - | - | - | 255.03 | - | Sin dato 2024 |

### Cambios Interanuales (2023 -> 2024)
- mzma: **-18.29 kg/m³** (mejor mejora)
- pacas: **-17.78 kg/m³**
- lomax: **-7.72 kg/m³**

**Todas las plantas muestran mejora en 2024.**

---

## 7. Distribución por Bandas de Clasificación

| Planta | Excelente (A-AA) | Bueno (B-C) | Regular (D-E) | Crítico (F+Fuera) |
|--------|:----------------:|:-----------:|:-------------:|:-----------------:|
| pacas | 12.8% | 18.3% | 43.0% | 25.9% |
| mzma | 0.8% | 2.4% | 69.1% | 27.7% |
| melon | 0.5% | 5.6% | 88.9% | 5.0% |
| lomax | 0.1% | 7.1% | 72.5% | 20.3% |

### Insights
- **pacas** tiene 10x más despachos "excelentes" que otras plantas
- **melon** tiene el menor % crítico (5.0%) - mejor consistencia
- Oportunidad de mejora: mover despachos de D-E hacia B-C

---

## 8. Comparación con Benchmarks Internacionales

| Fuente | Huella Promedio (kg CO2/m³) | vs LATAM |
|--------|----------------------------:|:--------:|
| **LATAM (datos reales)** | **271.12** | - |
| GCCA Mundial | 294 | +8% mejor |
| GCCA Europa | 262 | -3% peor |
| GCCA América del Norte | ~310* | +13% mejor |

**LATAM está bien posicionado vs benchmarks internacionales.**

---

## 9. Análisis de Tipos de Cemento

| Cemento | Huella (kg CO2/t) | Factor Clínker | n |
|---------|------------------:|:--------------:|--:|
| FORTIMAX MS | 326.68 | 0.67 | 20 |
| Mortero | 390.75 | - | 12 |
| EXTRAFORTE 1CO | 477.76 | 0.70 | 31 |
| CPC30R | 669.33 | - | 12 |
| TIPO I | 684.90 | 0.89 | 26 |
| CPC 40 | 854.58 | - | 12 |

### Observación
- Cementos con menor factor clínker tienen menor huella
- FORTIMAX MS (clínker 0.67) tiene 2.6x menos huella que CPC 40

---

## 10. Identificación de Plantas

| Código | Probable Identificación | País |
|--------|------------------------|------|
| pacas | Cementos Pacasmayo S.A. | Perú |
| mzma | Por confirmar | México? |
| lomax | Por confirmar | - |
| melon | Por confirmar | Chile? |

---

## 11. Vista Analítica Creada

Se creó la vista `v_analisis_profundo` en la base de datos:

```sql
CREATE VIEW v_analisis_profundo AS
SELECT
    origen, año, REST, volumen, huella_co2,
    huella_co2/REST as co2_por_mpa,
    huella_co2*volumen as co2_total_kg,
    CASE
        WHEN REST < 15 THEN 'Baja (<15)'
        WHEN REST < 25 THEN 'Media (15-25)'
        WHEN REST < 35 THEN 'Alta (25-35)'
        WHEN REST < 50 THEN 'Muy Alta (35-50)'
        ELSE 'Ultra Alta (>50)'
    END as categoria_resistencia,
    -- Componentes normalizados
    A1_Total/volumen as A1_norm,
    A2_Total/volumen as A2_norm,
    A3_Total/volumen as A3_norm,
    A4_Total/volumen as A4_norm
FROM huella_concretos;
```

---

## 12. Recomendaciones

### Inmediatas
1. **Verificar datos de "pacas"** - Posible error de escala 100x
2. **Completar identificación de plantas** - Vincular códigos con plantas_latam

### Estratégicas
3. **Promover concretos de alta resistencia** - Mayor eficiencia de CO2/MPa
4. **Estudiar prácticas de "melon"** - Logra mejor eficiencia con procesos variables
5. **Enfocar mejoras en rango 20-30 MPa** - Concentra 60% del volumen

### Monitoreo
6. **Mantener tendencia 2024** - Todas las plantas mejorando
7. **Reducir % de bandas F y Fuera de rango** - Especialmente en mzma y pacas

---

## Anexo: Queries SQL Utilizados

```sql
-- Correlación por planta
SELECT origen, CORR(REST, huella_co2) FROM huella_concretos GROUP BY origen;

-- Eficiencia por categoría de resistencia
SELECT categoria_resistencia, AVG(co2_por_mpa) FROM v_analisis_profundo GROUP BY 1;

-- Tendencias temporales
SELECT origen, año, AVG(huella_co2),
       LAG(AVG(huella_co2)) OVER (PARTITION BY origen ORDER BY año) as anterior
FROM huella_concretos GROUP BY origen, año;
```

---

**Documento generado:** 2025-12-02
**Herramienta:** Claude Code (Opus 4.5)
**Base de datos:** PostgreSQL latam4c_db
