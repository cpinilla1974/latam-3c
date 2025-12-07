# Resumen Ejecutivo - Integridad de Base de Datos
## Proyecto LATAM-3C | 2025-12-02

---

## Estado General: ⚠️ FUNCIONAL CON LIMITACIONES

**Score de Calidad:** 68/100

- ✅ **Datos Básicos:** Excelente (255,328 remitos completos)
- ✅ **Huella A1-A3:** Completa (100% de datos)
- ❌ **Metadata Técnica:** Crítica (tipo_cemento 0%)
- ⚠️ **Ciclo Completo:** Limitada (sin A5, A4 solo 42%)

---

## Datos Principales

| Métrica | Valor |
|---------|-------|
| **Total de remitos** | 255,328 |
| **Período** | 2020-2024 (5 años) |
| **Plantas** | 18 plantas |
| **Empresas** | 4 principales |
| **Año con más datos** | 2023 (55%) |

---

## 🔴 Problemas Críticos (Acción Inmediata)

### 1. Campo `tipo_cemento` - 0% datos
**Impacto:** No se puede clasificar por tipo de cemento ni cumplir estándares EPD
**Acción:** Agregar campo obligatorio en captura + back-fill histórico

### 2. Fase A5 faltante - 0% datos
**Impacto:** No se puede calcular ciclo de vida completo (A1-A5)
**Acción:** Documentar que análisis es A1-A3, o implementar cálculo A5

### 3. Anomalías en datos
- Huella CO2 máximo: 1,483 kg/m³ (esperado: <450)
- Contenido cemento máximo: 7,621 kg/m³ (esperado: 250-450)
**Acción:** Implementar validaciones de rango

---

## 🟡 Problemas Moderados (3 meses)

### 4. Transporte (A4) - 42% datos
**Impacto:** 58% de remitos sin datos de transporte al sitio
**Acción:** Requerir distancia/modo en captura

### 5. Contenido cemento - 58% datos
**Impacto:** Dificulta análisis de optimización de mezclas
**Acción:** Extraer de formulaciones técnicas

### 6. Factor clinker - 74% datos
**Impacto:** 26% de cementos sin factor (tabla PostgreSQL)
**Acción:** Solicitar a plantas o usar valores por defecto

---

## Completitud por Columna

| Columna | % Completo | Estado | Impacto |
|---------|------------|--------|---------|
| Datos básicos (id, fecha, volumen) | 100% | ✅ | - |
| Huella A1-A3 | 100% | ✅ | - |
| `tipo_cemento` | 0% | ❌ | CRÍTICO |
| `a5_total` (construcción) | 0% | ❌ | ALTO |
| `slump` | 0% | ❌ | BAJO |
| `a4_total` (transporte) | 42% | ⚠️ | ALTO |
| `contenido_cemento` | 58% | ⚠️ | MEDIO |
| `proyecto` | 58% | ⚠️ | BAJO |

---

## Impacto en Funcionalidades

| Funcionalidad | Estado | Nota |
|---------------|--------|------|
| Cálculo huella A1-A3 | ✅ Funcional | - |
| Análisis por tipo cemento | ❌ Bloqueado | Requiere tipo_cemento |
| Cálculo huella A1-A5 | ❌ Bloqueado | Requiere A5 |
| Benchmarking internacional | ⚠️ Limitado | Solo A1-A3 |
| Análisis de transporte | ⚠️ Parcial | Solo 42% |
| Optimización mezclas | ⚠️ Parcial | Solo 58% |

---

## Plan de Acción (Priorizado)

### ⏰ Inmediato (1 mes)
1. ✅ Agregar campo `tipo_cemento` obligatorio
2. ✅ Implementar validaciones de rango
3. ✅ Documentar alcance A1-A3 en reportes
4. ✅ Identificar y marcar outliers

### 📅 Corto Plazo (3 meses)
5. Back-fill `tipo_cemento` histórico
6. Completar datos A4 (transporte)
7. Extraer `contenido_cemento`
8. Completar `factor_clinker`

### 🔮 Largo Plazo (6+ meses)
9. Implementar fase A5
10. Habilitar análisis A1-A5
11. Limpiar datos históricos

---

## Distribución de Datos

### Top 5 Plantas
1. **Planta 72:** 51,842 remitos (20%)
2. **Planta 45:** 28,752 remitos (11%)
3. **Planta 12:** 24,379 remitos (10%)
4. **Lo Espejo 2:** 20,126 remitos (8%)
5. **Lo Espejo 1:** 17,541 remitos (7%)

### Por Año
- **2023:** 140,406 remitos (55%) ⚠️ Concentración alta
- **2021:** 40,974 remitos (16%)
- **2022:** 33,481 remitos (13%)
- **2020:** 31,005 remitos (12%)
- **2024:** 9,462 remitos (4%) - Datos parciales

---

## Calidad por Fuente de Datos

| Fuente | Remitos | Campos Completos | Calidad |
|--------|---------|------------------|---------|
| `main.db` (nuevo) | 147,043 (58%) | 22/32 campos | ⭐⭐⭐⭐ Buena |
| `main_old.db` | 108,285 (42%) | 18/32 campos | ⭐⭐⭐ Aceptable |

**Nota:** `main_old.db` no tiene A4, proyecto ni cliente

---

## Recomendación Principal

**Priorizar implementación de campo `tipo_cemento`**

Sin este campo:
- ❌ No se puede clasificar por tipo de cemento
- ❌ No se pueden aplicar factores de emisión específicos
- ❌ No se puede cumplir con estándares EPD internacionales
- ❌ Análisis automático queda severamente limitado

**Impacto:** CRÍTICO
**Esfuerzo:** MEDIO
**ROI:** ALTO

---

## Archivos Generados

1. **Reporte completo:** `/home/cpinilla/projects/latam-3c/docs/3-sesiones/reporte_integridad_bd_2025-12-02.md`
2. **Queries SQL útiles:** `/home/cpinilla/projects/latam-3c/scripts/queries_analisis_completitud.sql`
3. **Scripts de análisis:**
   - `/home/cpinilla/projects/latam-3c/scripts/analizar_integridad_bd.py` (PostgreSQL)
   - `/home/cpinilla/projects/latam-3c/scripts/analizar_sqlite_ficem.py` (SQLite)

---

## Próximos Pasos

1. **Revisar este reporte** con el equipo técnico
2. **Priorizar campos faltantes** según impacto en negocio
3. **Implementar validaciones** para datos nuevos
4. **Planificar back-fill** de datos históricos
5. **Definir metodología** para fase A5

---

**Contacto:** Reporte generado por análisis automatizado
**Fecha:** 2025-12-02
