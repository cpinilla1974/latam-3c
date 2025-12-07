-- ============================================
-- QUERIES ÚTILES PARA ANÁLISIS DE COMPLETITUD
-- Base de Datos: ficem_bd.db (SQLite)
-- ============================================

-- 1. RESUMEN GENERAL DE COMPLETITUD POR COLUMNA
-- ----------------------------------------------
SELECT
    'id_remito' as columna,
    COUNT(*) as total,
    COUNT(id_remito) as completos,
    COUNT(*) - COUNT(id_remito) as nulls,
    ROUND(100.0 * COUNT(id_remito) / COUNT(*), 2) as pct_completo
FROM remitos_concretos
UNION ALL
SELECT 'compania', COUNT(*), COUNT(compania), COUNT(*) - COUNT(compania),
       ROUND(100.0 * COUNT(compania) / COUNT(*), 2) FROM remitos_concretos
UNION ALL
SELECT 'tipo_cemento', COUNT(*), COUNT(tipo_cemento), COUNT(*) - COUNT(tipo_cemento),
       ROUND(100.0 * COUNT(tipo_cemento) / COUNT(*), 2) FROM remitos_concretos
UNION ALL
SELECT 'contenido_cemento', COUNT(*), COUNT(contenido_cemento), COUNT(*) - COUNT(contenido_cemento),
       ROUND(100.0 * COUNT(contenido_cemento) / COUNT(*), 2) FROM remitos_concretos
UNION ALL
SELECT 'a4_total', COUNT(*), COUNT(a4_total), COUNT(*) - COUNT(a4_total),
       ROUND(100.0 * COUNT(a4_total) / COUNT(*), 2) FROM remitos_concretos
UNION ALL
SELECT 'a5_total', COUNT(*), COUNT(a5_total), COUNT(*) - COUNT(a5_total),
       ROUND(100.0 * COUNT(a5_total) / COUNT(*), 2) FROM remitos_concretos
ORDER BY pct_completo ASC;


-- 2. DISTRIBUCIÓN DE COMPLETITUD POR FUENTE DE DATOS
-- ---------------------------------------------------
SELECT
    archivo_origen,
    COUNT(*) as total_remitos,
    COUNT(a4_total) as con_a4,
    COUNT(contenido_cemento) as con_contenido,
    COUNT(proyecto) as con_proyecto,
    COUNT(tipo_cemento) as con_tipo_cemento,
    ROUND(100.0 * COUNT(a4_total) / COUNT(*), 2) as pct_a4,
    ROUND(100.0 * COUNT(contenido_cemento) / COUNT(*), 2) as pct_contenido,
    ROUND(100.0 * COUNT(proyecto) / COUNT(*), 2) as pct_proyecto
FROM remitos_concretos
GROUP BY archivo_origen
ORDER BY total_remitos DESC;


-- 3. COMPLETITUD POR PLANTA
-- --------------------------
SELECT
    planta,
    COUNT(*) as total_remitos,
    COUNT(a4_total) as con_a4,
    COUNT(contenido_cemento) as con_contenido,
    ROUND(100.0 * COUNT(a4_total) / COUNT(*), 2) as pct_a4,
    ROUND(100.0 * COUNT(contenido_cemento) / COUNT(*), 2) as pct_contenido
FROM remitos_concretos
GROUP BY planta
ORDER BY total_remitos DESC
LIMIT 20;


-- 4. COMPLETITUD POR AÑO
-- ----------------------
SELECT
    año,
    COUNT(*) as total_remitos,
    COUNT(a4_total) as con_a4,
    COUNT(contenido_cemento) as con_contenido,
    COUNT(proyecto) as con_proyecto,
    ROUND(100.0 * COUNT(a4_total) / COUNT(*), 2) as pct_a4,
    ROUND(100.0 * COUNT(contenido_cemento) / COUNT(*), 2) as pct_contenido,
    ROUND(100.0 * COUNT(proyecto) / COUNT(*), 2) as pct_proyecto
FROM remitos_concretos
GROUP BY año
ORDER BY año DESC;


-- 5. IDENTIFICAR OUTLIERS EN HUELLA DE CARBONO
-- ---------------------------------------------
SELECT
    id_remito,
    planta,
    fecha,
    resistencia,
    volumen,
    huella_co2,
    contenido_cemento,
    archivo_origen
FROM remitos_concretos
WHERE huella_co2 > 600  -- Valores muy altos
   OR huella_co2 < 50   -- Valores muy bajos
ORDER BY huella_co2 DESC
LIMIT 100;


-- 6. IDENTIFICAR OUTLIERS EN CONTENIDO DE CEMENTO
-- ------------------------------------------------
SELECT
    id_remito,
    planta,
    fecha,
    resistencia,
    contenido_cemento,
    volumen,
    archivo_origen
FROM remitos_concretos
WHERE contenido_cemento > 600  -- Valores muy altos (típico: 250-450)
   OR contenido_cemento < 100  -- Valores muy bajos
ORDER BY contenido_cemento DESC
LIMIT 100;


-- 7. REMITOS SIN DATOS DE TRANSPORTE (A4)
-- ----------------------------------------
SELECT
    COUNT(*) as total_sin_a4,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM remitos_concretos) as pct_sin_a4
FROM remitos_concretos
WHERE a4_total IS NULL;

-- Ver distribución por planta de remitos sin A4
SELECT
    planta,
    COUNT(*) as sin_a4,
    (SELECT COUNT(*) FROM remitos_concretos rc2 WHERE rc2.planta = rc.planta) as total_planta,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM remitos_concretos rc2 WHERE rc2.planta = rc.planta), 2) as pct_sin_a4
FROM remitos_concretos rc
WHERE a4_total IS NULL
GROUP BY planta
ORDER BY sin_a4 DESC;


-- 8. ESTADÍSTICAS DESCRIPTIVAS POR PLANTA
-- ----------------------------------------
SELECT
    planta,
    COUNT(*) as total_remitos,
    ROUND(AVG(huella_co2), 2) as huella_promedio,
    ROUND(MIN(huella_co2), 2) as huella_min,
    ROUND(MAX(huella_co2), 2) as huella_max,
    ROUND(AVG(resistencia), 2) as resistencia_promedio,
    ROUND(AVG(volumen), 2) as volumen_promedio,
    ROUND(AVG(contenido_cemento), 2) as cemento_promedio
FROM remitos_concretos
GROUP BY planta
ORDER BY total_remitos DESC;


-- 9. EVOLUCIÓN TEMPORAL DE COMPLETITUD
-- -------------------------------------
SELECT
    año,
    COUNT(*) as total_remitos,
    ROUND(AVG(CASE WHEN a4_total IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100, 2) as pct_con_a4,
    ROUND(AVG(CASE WHEN contenido_cemento IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100, 2) as pct_con_contenido,
    ROUND(AVG(CASE WHEN proyecto IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100, 2) as pct_con_proyecto,
    ROUND(AVG(CASE WHEN tipo_cemento IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100, 2) as pct_con_tipo_cemento
FROM remitos_concretos
GROUP BY año
ORDER BY año;


-- 10. ANÁLISIS DE CORRELACIÓN: RESISTENCIA vs HUELLA
-- ---------------------------------------------------
SELECT
    CASE
        WHEN resistencia < 15 THEN '< 15 MPa'
        WHEN resistencia < 25 THEN '15-25 MPa'
        WHEN resistencia < 35 THEN '25-35 MPa'
        WHEN resistencia < 45 THEN '35-45 MPa'
        ELSE '> 45 MPa'
    END as rango_resistencia,
    COUNT(*) as total_remitos,
    ROUND(AVG(huella_co2), 2) as huella_promedio,
    ROUND(AVG(contenido_cemento), 2) as cemento_promedio,
    ROUND(MIN(huella_co2), 2) as huella_min,
    ROUND(MAX(huella_co2), 2) as huella_max
FROM remitos_concretos
GROUP BY rango_resistencia
ORDER BY rango_resistencia;


-- 11. TOP 10 PLANTAS CON MENOR HUELLA DE CARBONO
-- -----------------------------------------------
SELECT
    planta,
    COUNT(*) as total_remitos,
    ROUND(AVG(huella_co2), 2) as huella_promedio,
    ROUND(AVG(resistencia), 2) as resistencia_promedio
FROM remitos_concretos
GROUP BY planta
HAVING COUNT(*) > 1000  -- Solo plantas con volumen significativo
ORDER BY huella_promedio ASC
LIMIT 10;


-- 12. REMITOS CON DATOS MÁS COMPLETOS (SCORE DE CALIDAD)
-- -------------------------------------------------------
SELECT
    id_remito,
    planta,
    fecha,
    resistencia,
    volumen,
    huella_co2,
    (
        CAST(tipo_cemento IS NOT NULL AS INTEGER) +
        CAST(contenido_cemento IS NOT NULL AS INTEGER) +
        CAST(a4_total IS NOT NULL AS INTEGER) +
        CAST(proyecto IS NOT NULL AS INTEGER) +
        CAST(cliente IS NOT NULL AS INTEGER) +
        CAST(slump IS NOT NULL AS INTEGER)
    ) as score_completitud
FROM remitos_concretos
ORDER BY score_completitud DESC, fecha DESC
LIMIT 100;


-- 13. PLANTAS CON MEJOR CALIDAD DE DATOS
-- ---------------------------------------
SELECT
    planta,
    COUNT(*) as total_remitos,
    ROUND(AVG(
        CAST(tipo_cemento IS NOT NULL AS FLOAT) +
        CAST(contenido_cemento IS NOT NULL AS FLOAT) +
        CAST(a4_total IS NOT NULL AS FLOAT) +
        CAST(proyecto IS NOT NULL AS FLOAT)
    ) / 4 * 100, 2) as pct_calidad_promedio
FROM remitos_concretos
GROUP BY planta
ORDER BY pct_calidad_promedio DESC;


-- 14. ANÁLISIS DE EMISIONES POR FASE (A1, A2, A3, A4)
-- ----------------------------------------------------
SELECT
    planta,
    COUNT(*) as total_remitos,
    ROUND(AVG(a1_total), 2) as promedio_a1,
    ROUND(AVG(a2_total), 2) as promedio_a2,
    ROUND(AVG(a3_total), 2) as promedio_a3,
    ROUND(AVG(a4_total), 2) as promedio_a4,
    ROUND(AVG(a1_total + a2_total + a3_total), 2) as promedio_a1_a3,
    COUNT(a4_total) as remitos_con_a4
FROM remitos_concretos
GROUP BY planta
ORDER BY promedio_a1_a3 DESC;


-- 15. BÚSQUEDA DE DUPLICADOS POTENCIALES
-- ---------------------------------------
SELECT
    planta,
    fecha,
    formulacion,
    resistencia,
    volumen,
    COUNT(*) as num_duplicados
FROM remitos_concretos
GROUP BY planta, fecha, formulacion, resistencia, volumen
HAVING COUNT(*) > 1
ORDER BY num_duplicados DESC
LIMIT 50;


-- ============================================
-- QUERIES PARA POSTGRESQL (latam4c_db)
-- ============================================

-- 16. COMPLETITUD EN TABLA CEMENTOS (PostgreSQL)
-- -----------------------------------------------
-- Ejecutar en PostgreSQL:
/*
SELECT
    'factor_clinker' as campo,
    COUNT(*) as total,
    COUNT(factor_clinker) as completos,
    COUNT(*) - COUNT(factor_clinker) as nulls,
    ROUND(100.0 * COUNT(factor_clinker) / COUNT(*), 2) as pct_completo
FROM cementos;

-- Ver qué cementos no tienen factor de clinker
SELECT
    origen,
    planta,
    cemento,
    año,
    huella_co2_bruta,
    factor_clinker
FROM cementos
WHERE factor_clinker IS NULL
ORDER BY origen, planta, año DESC;
*/


-- 17. VERIFICAR CONSISTENCIA ENTRE BASES DE DATOS
-- ------------------------------------------------
-- Comparar agregaciones en PostgreSQL vs datos originales en SQLite
/*
-- En PostgreSQL:
SELECT
    origen,
    año,
    num_remitos,
    volumen,
    huella_co2
FROM huella_concretos
ORDER BY origen, año;

-- Comparar con SQLite (ejecutar en ficem_bd.db):
SELECT
    CASE
        WHEN planta LIKE '%Espejo%' OR planta LIKE 'Concon%' OR planta LIKE 'Maipu%'
             OR planta LIKE 'Puerto Montt%' THEN 'melon'
        WHEN planta IN ('72', '45', '4', '30') THEN 'mzma'
        WHEN planta IN ('12', '27') THEN 'pacas'
        ELSE 'lomax'
    END as origen,
    año,
    COUNT(*) as num_remitos,
    ROUND(SUM(volumen), 2) as volumen_total,
    ROUND(SUM(huella_co2 * volumen) / SUM(volumen), 2) as huella_promedio
FROM remitos_concretos
GROUP BY origen, año
ORDER BY origen, año;
*/
