-- ============================================================
-- VISTAS MATERIALIZADAS PARA ANÁLISIS IA - LATAM 3C
-- Base de datos: latam4c_db (PostgreSQL)
-- Fecha: 2025-12-03
-- ============================================================

-- Eliminar vistas existentes si es necesario
DROP MATERIALIZED VIEW IF EXISTS mv_benchmark_comparativo CASCADE;
DROP MATERIALIZED VIEW IF EXISTS mv_tendencias_co2 CASCADE;
DROP MATERIALIZED VIEW IF EXISTS mv_kpi_plantas_anual CASCADE;
DROP MATERIALIZED VIEW IF EXISTS mv_resumen_por_pais CASCADE;
DROP MATERIALIZED VIEW IF EXISTS mv_eficiencia_energetica CASCADE;

-- ============================================================
-- VISTA 1: KPIs por Planta Anual
-- Consolida indicadores clave por planta y año
-- ============================================================

CREATE MATERIALIZED VIEW mv_kpi_plantas_anual AS
SELECT
    p.id_planta,
    p.nombre as planta,
    p.tipo_planta,
    p.bd_origen,
    e.nombre as empresa,
    pa.nombre as pais,
    pa.codigo_iso3 as iso3,
    pa.region,
    EXTRACT(YEAR FROM f.fecha)::INTEGER as año,

    -- Producción
    MAX(CASE WHEN i.codigo_indicador = '8' THEN f.valor END) as clinker_producido_t,
    MAX(CASE WHEN i.codigo_indicador = '20' THEN f.valor END) as cemento_producido_t,

    -- Factor clinker (%)
    MAX(CASE WHEN i.codigo_indicador = '92a' THEN f.valor END) as factor_clinker,

    -- Consumo Energético
    MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) as consumo_termico_mj_t,
    MAX(CASE WHEN i.codigo_indicador = '33' THEN f.valor END) as consumo_electrico_mwh,
    MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) as consumo_electrico_clinker_kwh_t,
    MAX(CASE WHEN i.codigo_indicador = '33b' THEN f.valor END) as consumo_electrico_cemento_kwh_t,

    -- Emisiones CO2
    MAX(CASE WHEN i.codigo_indicador = '60' THEN f.valor END) as co2_bruto_clinker_t,
    MAX(CASE WHEN i.codigo_indicador = '63' THEN f.valor END) as co2_neto_clinker_t,
    MAX(CASE WHEN i.codigo_indicador = '73' THEN f.valor END) as co2_especifico_clinker_kg_t,
    MAX(CASE WHEN i.codigo_indicador = '82' THEN f.valor END) as co2_bruto_cemento_t,
    MAX(CASE WHEN i.codigo_indicador = '85' THEN f.valor END) as co2_neto_cemento_t,

    -- Combustibles alternativos (%)
    MAX(CASE WHEN i.codigo_indicador = '90' THEN f.valor END) as pct_sustitucion_termica,
    MAX(CASE WHEN i.codigo_indicador = '90a' THEN f.valor END) as pct_biomasa,

    -- Conteos para control de calidad
    COUNT(DISTINCT i.codigo_indicador) as indicadores_disponibles,
    COUNT(*) as total_registros

FROM fact_indicadores_planta f
INNER JOIN dim_plantas p ON f.id_planta = p.id_planta
LEFT JOIN dim_empresas e ON p.id_empresa = e.id_empresa
LEFT JOIN dim_paises pa ON p.id_pais = pa.id_pais
INNER JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
WHERE p.tipo_planta = 'cemento'
    AND f.valor IS NOT NULL
GROUP BY
    p.id_planta, p.nombre, p.tipo_planta, p.bd_origen,
    e.nombre, pa.nombre, pa.codigo_iso3, pa.region,
    EXTRACT(YEAR FROM f.fecha);

CREATE INDEX idx_mv_kpi_año ON mv_kpi_plantas_anual(año);
CREATE INDEX idx_mv_kpi_pais ON mv_kpi_plantas_anual(pais);
CREATE INDEX idx_mv_kpi_planta ON mv_kpi_plantas_anual(id_planta);

COMMENT ON MATERIALIZED VIEW mv_kpi_plantas_anual IS 'KPIs consolidados por planta y año para análisis de desempeño';

-- ============================================================
-- VISTA 2: Benchmark Comparativo
-- Compara plantas contra benchmarks GNR/GCCA
-- ============================================================

CREATE MATERIALIZED VIEW mv_benchmark_comparativo AS
WITH plantas_anual AS (
    SELECT
        id_planta,
        planta,
        pais,
        iso3,
        region,
        año,
        factor_clinker,
        consumo_termico_mj_t,
        co2_especifico_clinker_kg_t,
        cemento_producido_t,
        pct_sustitucion_termica
    FROM mv_kpi_plantas_anual
    WHERE año >= 2020
),
gnr_latam AS (
    SELECT
        año,
        indicador,
        codigo_indicador,
        AVG(valor) as valor_promedio,
        PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY valor) as p10,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY valor) as p25,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY valor) as p50,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY valor) as p75,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY valor) as p90
    FROM ref_gnr_data
    WHERE region ILIKE '%latin%' OR region ILIKE '%america%'
    GROUP BY año, indicador, codigo_indicador
)
SELECT
    p.id_planta,
    p.planta,
    p.pais,
    p.iso3,
    p.año,
    p.factor_clinker,
    p.consumo_termico_mj_t,
    p.co2_especifico_clinker_kg_t,
    p.cemento_producido_t,
    p.pct_sustitucion_termica,

    -- Clasificación por emisiones específicas
    CASE
        WHEN p.co2_especifico_clinker_kg_t IS NULL THEN 'Sin datos'
        WHEN p.co2_especifico_clinker_kg_t <= 800 THEN 'A - Excelente (<800)'
        WHEN p.co2_especifico_clinker_kg_t <= 850 THEN 'B - Bueno (800-850)'
        WHEN p.co2_especifico_clinker_kg_t <= 900 THEN 'C - Regular (850-900)'
        ELSE 'D - Por mejorar (>900)'
    END as clasificacion_emision,

    -- Clasificación por factor clinker
    CASE
        WHEN p.factor_clinker IS NULL THEN 'Sin datos'
        WHEN p.factor_clinker <= 0.70 THEN 'A - Excelente (<70%)'
        WHEN p.factor_clinker <= 0.75 THEN 'B - Bueno (70-75%)'
        WHEN p.factor_clinker <= 0.80 THEN 'C - Regular (75-80%)'
        ELSE 'D - Por mejorar (>80%)'
    END as clasificacion_factor_clinker,

    -- Clasificación por sustitución térmica
    CASE
        WHEN p.pct_sustitucion_termica IS NULL THEN 'Sin datos'
        WHEN p.pct_sustitucion_termica >= 30 THEN 'A - Excelente (>30%)'
        WHEN p.pct_sustitucion_termica >= 20 THEN 'B - Bueno (20-30%)'
        WHEN p.pct_sustitucion_termica >= 10 THEN 'C - Regular (10-20%)'
        ELSE 'D - Por mejorar (<10%)'
    END as clasificacion_sustitucion

FROM plantas_anual p;

CREATE INDEX idx_mv_bench_año ON mv_benchmark_comparativo(año);
CREATE INDEX idx_mv_bench_pais ON mv_benchmark_comparativo(pais);

COMMENT ON MATERIALIZED VIEW mv_benchmark_comparativo IS 'Comparación de plantas contra benchmarks de la industria';

-- ============================================================
-- VISTA 3: Tendencias CO2
-- Análisis temporal de emisiones
-- ============================================================

CREATE MATERIALIZED VIEW mv_tendencias_co2 AS
SELECT
    p.id_planta,
    p.nombre as planta,
    pa.nombre as pais,
    pa.region,
    EXTRACT(YEAR FROM f.fecha)::INTEGER as año,
    f.temporalidad,

    -- Emisiones totales
    SUM(CASE WHEN i.codigo_indicador = '60' THEN f.valor ELSE 0 END) as co2_bruto_total,
    SUM(CASE WHEN i.codigo_indicador = '63' THEN f.valor ELSE 0 END) as co2_neto_total,

    -- Promedios específicos
    AVG(CASE WHEN i.codigo_indicador = '73' THEN f.valor END) as co2_especifico_clinker_avg,
    AVG(CASE WHEN i.codigo_indicador = '76' THEN f.valor END) as co2_especifico_cemento_avg,

    -- Variación año a año (calculado en aplicación)
    NULL::DECIMAL as variacion_yoy

FROM fact_indicadores_planta f
INNER JOIN dim_plantas p ON f.id_planta = p.id_planta
LEFT JOIN dim_paises pa ON p.id_pais = pa.id_pais
INNER JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
WHERE i.supergrupo = 'Clinker'
    AND i.grupo ILIKE '%emisi%'
GROUP BY
    p.id_planta, p.nombre, pa.nombre, pa.region,
    EXTRACT(YEAR FROM f.fecha), f.temporalidad;

CREATE INDEX idx_mv_tend_año ON mv_tendencias_co2(año);
CREATE INDEX idx_mv_tend_planta ON mv_tendencias_co2(id_planta);

COMMENT ON MATERIALIZED VIEW mv_tendencias_co2 IS 'Tendencias temporales de emisiones CO2 por planta';

-- ============================================================
-- VISTA 4: Resumen por País
-- Agregación a nivel país para dashboard ejecutivo
-- ============================================================

CREATE MATERIALIZED VIEW mv_resumen_por_pais AS
SELECT
    pa.id_pais,
    pa.nombre as pais,
    pa.codigo_iso3 as iso3,
    pa.region,
    k.año,

    -- Conteos
    COUNT(DISTINCT k.id_planta) as num_plantas,
    COUNT(DISTINCT k.empresa) as num_empresas,

    -- Producción total
    SUM(k.clinker_producido_t) as clinker_total_t,
    SUM(k.cemento_producido_t) as cemento_total_t,

    -- Promedios ponderados
    AVG(k.factor_clinker) as factor_clinker_promedio,
    AVG(k.consumo_termico_mj_t) as consumo_termico_promedio,
    AVG(k.co2_especifico_clinker_kg_t) as co2_especifico_promedio,
    AVG(k.pct_sustitucion_termica) as sustitucion_termica_promedio,

    -- Emisiones totales
    SUM(k.co2_bruto_clinker_t) as co2_bruto_total_t,
    SUM(k.co2_neto_clinker_t) as co2_neto_total_t,

    -- Min/Max para rangos
    MIN(k.co2_especifico_clinker_kg_t) as co2_especifico_min,
    MAX(k.co2_especifico_clinker_kg_t) as co2_especifico_max

FROM mv_kpi_plantas_anual k
INNER JOIN dim_paises pa ON k.iso3 = pa.codigo_iso3
GROUP BY
    pa.id_pais, pa.nombre, pa.codigo_iso3, pa.region, k.año;

CREATE INDEX idx_mv_pais_año ON mv_resumen_por_pais(año);
CREATE INDEX idx_mv_pais_iso3 ON mv_resumen_por_pais(iso3);

COMMENT ON MATERIALIZED VIEW mv_resumen_por_pais IS 'Resumen de indicadores agregados por país';

-- ============================================================
-- VISTA 5: Eficiencia Energética
-- Análisis detallado de consumo energético
-- ============================================================

CREATE MATERIALIZED VIEW mv_eficiencia_energetica AS
SELECT
    p.id_planta,
    p.nombre as planta,
    p.bd_origen,
    e.nombre as empresa,
    pa.nombre as pais,
    EXTRACT(YEAR FROM f.fecha)::INTEGER as año,

    -- Consumo térmico
    MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) as consumo_termico_especifico_mj_t,
    MAX(CASE WHEN i.codigo_indicador = '30' THEN f.valor END) as energia_termica_total_tj,
    MAX(CASE WHEN i.codigo_indicador = '32' THEN f.valor END) as energia_termica_clinker_tj,

    -- Consumo eléctrico
    MAX(CASE WHEN i.codigo_indicador = '33' THEN f.valor END) as consumo_electrico_total_mwh,
    MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) as consumo_electrico_clinker_kwh_t,
    MAX(CASE WHEN i.codigo_indicador = '33b' THEN f.valor END) as consumo_electrico_cemento_kwh_t,
    MAX(CASE WHEN i.codigo_indicador = '33c' THEN f.valor END) as consumo_electrico_molienda_kwh_t,

    -- Combustibles alternativos
    MAX(CASE WHEN i.codigo_indicador = '90' THEN f.valor END) as tasa_sustitucion_termica_pct,
    MAX(CASE WHEN i.codigo_indicador = '90a' THEN f.valor END) as tasa_biomasa_pct,

    -- Clasificación de eficiencia
    CASE
        WHEN MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) IS NULL THEN 'Sin datos'
        WHEN MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) <= 3200 THEN 'Excelente'
        WHEN MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) <= 3500 THEN 'Bueno'
        WHEN MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) <= 3800 THEN 'Regular'
        ELSE 'Por mejorar'
    END as clasificacion_termica,

    CASE
        WHEN MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) IS NULL THEN 'Sin datos'
        WHEN MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) <= 70 THEN 'Excelente'
        WHEN MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) <= 85 THEN 'Bueno'
        WHEN MAX(CASE WHEN i.codigo_indicador = '33a' THEN f.valor END) <= 100 THEN 'Regular'
        ELSE 'Por mejorar'
    END as clasificacion_electrica

FROM fact_indicadores_planta f
INNER JOIN dim_plantas p ON f.id_planta = p.id_planta
LEFT JOIN dim_empresas e ON p.id_empresa = e.id_empresa
LEFT JOIN dim_paises pa ON p.id_pais = pa.id_pais
INNER JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
WHERE (i.supergrupo IN ('Clinker', 'Cemento') AND i.grupo ILIKE '%energ%')
    OR i.codigo_indicador IN ('30', '32', '33', '33a', '33b', '33c', '90', '90a', '93')
GROUP BY
    p.id_planta, p.nombre, p.bd_origen,
    e.nombre, pa.nombre,
    EXTRACT(YEAR FROM f.fecha);

CREATE INDEX idx_mv_efic_año ON mv_eficiencia_energetica(año);
CREATE INDEX idx_mv_efic_planta ON mv_eficiencia_energetica(id_planta);

COMMENT ON MATERIALIZED VIEW mv_eficiencia_energetica IS 'Análisis de eficiencia energética por planta';

-- ============================================================
-- FUNCIONES DE ACTUALIZACIÓN
-- ============================================================

-- Función para refrescar todas las vistas materializadas
CREATE OR REPLACE FUNCTION refrescar_vistas_materializadas()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_kpi_plantas_anual;
    REFRESH MATERIALIZED VIEW mv_benchmark_comparativo;
    REFRESH MATERIALIZED VIEW mv_tendencias_co2;
    REFRESH MATERIALIZED VIEW mv_resumen_por_pais;
    REFRESH MATERIALIZED VIEW mv_eficiencia_energetica;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION refrescar_vistas_materializadas IS 'Actualiza todas las vistas materializadas de análisis';

-- ============================================================
-- RESUMEN DE VISTAS CREADAS
-- ============================================================
/*
VISTAS MATERIALIZADAS:

1. mv_kpi_plantas_anual
   - KPIs consolidados: producción, emisiones, energía, combustibles
   - Uso: Dashboard principal, análisis por planta

2. mv_benchmark_comparativo
   - Clasificación de plantas vs benchmarks
   - Uso: Identificar plantas destacadas y áreas de mejora

3. mv_tendencias_co2
   - Evolución temporal de emisiones
   - Uso: Análisis de tendencias, proyecciones

4. mv_resumen_por_pais
   - Agregación a nivel país
   - Uso: Dashboard ejecutivo, comparativas regionales

5. mv_eficiencia_energetica
   - Detalle de consumos térmicos y eléctricos
   - Uso: Análisis de eficiencia, oportunidades de ahorro

ACTUALIZACIÓN:
   SELECT refrescar_vistas_materializadas();
*/
