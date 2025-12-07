# Hallazgos Clave - Análisis de Integridad BD
## LATAM-3C | 2025-12-02

---

## Hallazgo Principal

**La base de datos contiene 255,328 remitos (no 500,000), con excelente calidad en datos básicos pero limitaciones críticas en metadata técnica que impiden análisis avanzados.**

---

## 5 Hallazgos Más Importantes

### 1. Campo `tipo_cemento` completamente vacío (CRÍTICO)

- **Estado:** 0% de datos (255,328 registros sin dato)
- **Impacto:** BLOQUEANTE
- **Consecuencias:**
  - No se puede clasificar por tipo de cemento (CPC, CPO, CPN, etc.)
  - No se pueden aplicar factores de emisión específicos por tipo
  - No se puede cumplir con estándares EPD internacionales
  - Análisis automático severamente limitado
- **Recomendación:** URGENTE - Agregar como campo obligatorio en captura

### 2. Fase A5 (construcción) faltante (ALTO IMPACTO)

- **Estado:** 0% de datos en A5_total, total_a1_a5, a5_intensidad
- **Impacto:** LIMITANTE
- **Consecuencias:**
  - Solo se puede calcular huella "cradle-to-gate" (A1-A3)
  - No se puede calcular ciclo de vida completo "cradle-to-grave" (A1-A5)
  - Benchmarking con estándares internacionales limitado
  - Subestimación de huella total
- **Recomendación:** Documentar alcance A1-A3 claramente O implementar cálculo A5

### 3. Datos de transporte (A4) parciales (MEDIO-ALTO IMPACTO)

- **Estado:** Solo 42.41% tiene datos (108,285 de 255,328)
- **Distribución desigual:**
  - `main.db` (nuevo): 0% tiene A4
  - `main_old.db`: 100% tiene A4
- **Impacto:** MODERADO
- **Consecuencias:**
  - 58% de remitos sin datos de transporte al sitio
  - Imposibilidad de análisis de impacto logístico completo
  - Comparaciones inconsistentes entre períodos
- **Recomendación:** Requerir distancia/modo de transporte en captura actual

### 4. Anomalías en valores extremos (CALIDAD DE DATOS)

- **Huella CO2:**
  - Máximo: 1,483.73 kg CO2/m³ (esperado: 200-450)
  - Promedio: 270.94 kg CO2/m³ (razonable)
  - Registros con valores >600: Requieren validación
- **Contenido de cemento:**
  - Máximo: 7,621 kg/m³ (FÍSICAMENTE IMPOSIBLE)
  - Esperado: 250-450 kg/m³
  - Probable error de unidades o captura
- **Recomendación:** Implementar validaciones de rango en formularios

### 5. Contenido de cemento parcial (MEDIO IMPACTO)

- **Estado:** 57.58% tiene datos (147,007 de 255,328)
- **Impacto:** MODERADO
- **Consecuencias:**
  - Dificulta análisis de optimización de mezclas
  - No se puede correlacionar huella con contenido de materiales
  - Limita cálculos de intensidad de carbono por kg de cemento
- **Recomendación:** Extraer de formulaciones técnicas cuando esté disponible

---

## Datos que SÍ funcionan bien (Fortalezas)

### Excelente calidad (100% completo)

- ✅ Identificadores únicos (id_remito)
- ✅ Datos básicos: compañía, planta, fecha, año
- ✅ Datos de producto: formulación, resistencia, volumen
- ✅ Huella A1-A3: a1_total, a2_total, a3_total, total_a1_a3
- ✅ Intensidades: a1_intensidad, a2_intensidad, a3_intensidad
- ✅ Metadata: archivo_origen, fecha_carga, version_datos

### Volumen significativo

- 255,328 remitos es una muestra MUY robusta
- 5 años de datos (2020-2024)
- 18 plantas distintas
- 4 empresas principales

---

## Distribución de Datos - Hallazgos

### Concentración temporal alta

- **2023 tiene 55% de todos los datos** (140,406 remitos)
- 2024 solo tiene 3.7% (probablemente datos parciales del año)
- Distribución desigual puede sesgar análisis temporales

### Top 3 plantas representan 41% de datos

1. Planta 72: 20.3% (51,842 remitos)
2. Planta 45: 11.3% (28,752 remitos)
3. Planta 12: 9.6% (24,379 remitos)

### Calidad desigual por fuente

- **main.db (nuevo):** 57.6% de datos, mejor calidad (22/32 campos)
- **main_old.db:** 42.4% de datos, menor calidad (18/32 campos)
  - No tiene: A4, proyecto, cliente

---

## Impacto en Análisis Automático

### Lo que SÍ se puede hacer

- ✅ Calcular huella de carbono A1-A3 (cradle-to-gate)
- ✅ Análisis de distribución por planta
- ✅ Análisis temporal de emisiones
- ✅ Estadísticas de resistencia y volumen
- ✅ Comparación de emisiones A1 vs A2 vs A3
- ✅ Cálculo de intensidades de carbono

### Lo que NO se puede hacer

- ❌ Análisis por tipo de cemento
- ❌ Clasificación de productos por categoría de cemento
- ❌ Aplicación de factores de emisión específicos
- ❌ Cálculo de ciclo de vida completo (A1-A5)
- ❌ Benchmarking con EPD internacionales (requieren A1-A5)

### Lo que se puede hacer PARCIALMENTE

- ⚠️ Análisis de impacto logístico (solo 42% de datos)
- ⚠️ Optimización de mezclas (solo 58% tiene contenido_cemento)
- ⚠️ Análisis por proyecto (solo 58% de datos)

---

## Comparación con Expectativa Inicial

### Usuario mencionó: ~500,000 remitos

**Realidad encontrada:**
- **255,328 remitos** en tabla `remitos_concretos`
- **260 registros** en tabla agregada `huella_concretos` (PostgreSQL)

**Posibles explicaciones:**
- Usuario contó registros duplicados o de múltiples tablas
- Existen otras fuentes de datos no analizadas
- Estimación aproximada vs conteo exacto

**Conclusión:** 255K remitos sigue siendo un volumen MUY significativo y suficiente para análisis robusto.

---

## Base de Datos PostgreSQL (latam4c_db)

### Hallazgo importante

**La tabla `huella_concretos` en PostgreSQL tiene solo 260 registros** porque contiene **agregaciones pre-calculadas**, no datos originales.

- No es la fuente de datos principal
- Es una tabla de resultados/agregaciones
- Los datos originales están en SQLite (ficem_bd.db)

### Problema en tabla `cementos`

- Campo `factor_clinker` solo 74% completo
- 36 de 139 registros sin factor de clinker
- Afecta cálculos de emisiones de CO2 de cemento

---

## Priorización de Acciones

### URGENTE (1 mes) - BLOQUEANTES

1. **Agregar `tipo_cemento` obligatorio**
   - Modificar formularios de captura
   - Back-fill datos históricos (consultar a plantas)
   - Impacto: ALTO | Esfuerzo: MEDIO

2. **Implementar validaciones de rango**
   - huella_co2: 50-800 kg/m³
   - contenido_cemento: 100-600 kg/m³
   - resistencia: >5 MPa
   - Impacto: MEDIO | Esfuerzo: BAJO

3. **Documentar alcance A1-A3**
   - Clarificar en reportes que es "cradle-to-gate"
   - Agregar disclaimer sobre ausencia de A4/A5
   - Impacto: MEDIO | Esfuerzo: BAJO

### IMPORTANTE (3 meses) - LIMITANTES

4. **Completar datos A4 (transporte)**
   - Requerir en captura actual
   - Calcular para datos históricos con distancias típicas
   - Impacto: ALTO | Esfuerzo: MEDIO

5. **Extraer contenido_cemento**
   - De formulaciones técnicas existentes
   - Validar con rangos esperados
   - Impacto: MEDIO | Esfuerzo: MEDIO

6. **Completar factor_clinker**
   - Solicitar a plantas
   - Usar valores por defecto documentados
   - Impacto: MEDIO | Esfuerzo: BAJO

### MEJORA (6+ meses) - OPCIONALES

7. **Implementar fase A5**
   - Definir metodología
   - Calcular para todos los remitos
   - Impacto: ALTO | Esfuerzo: ALTO

8. **Agregar slump y otros datos técnicos**
   - Si disponibles en registros
   - Útil para análisis de calidad
   - Impacto: BAJO | Esfuerzo: BAJO

---

## Conclusión Final

**La base de datos es FUNCIONAL para análisis básicos de huella A1-A3, pero requiere acciones urgentes en metadata técnica (especialmente tipo_cemento) para habilitar análisis avanzados y cumplir con estándares internacionales.**

**Score actual: 68/100**
**Score objetivo: 85/100** (con acciones de Fase 1 y 2)

---

## Recursos Generados

1. **Reporte completo (40 páginas):** `/home/cpinilla/projects/latam-3c/docs/3-sesiones/reporte_integridad_bd_2025-12-02.md`
2. **Resumen ejecutivo (3 páginas):** `/home/cpinilla/projects/latam-3c/docs/3-sesiones/resumen_ejecutivo_integridad_bd.md`
3. **Hallazgos clave (este archivo):** `/home/cpinilla/projects/latam-3c/docs/3-sesiones/hallazgos_clave_bd.md`
4. **Queries SQL útiles:** `/home/cpinilla/projects/latam-3c/scripts/queries_analisis_completitud.sql`
5. **Scripts de análisis:**
   - PostgreSQL: `/home/cpinilla/projects/latam-3c/scripts/analizar_integridad_bd.py`
   - SQLite: `/home/cpinilla/projects/latam-3c/scripts/analizar_sqlite_ficem.py`

---

**Fecha:** 2025-12-02
**Analista:** Claude AI (Análisis automatizado)
