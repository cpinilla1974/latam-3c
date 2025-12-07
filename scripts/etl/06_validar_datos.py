#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script 06: Validación de Datos
Verifica integridad y completitud de la migración

Ejecutar después de: 05_crear_vistas.sql
"""

import psycopg2
from datetime import datetime
import json
import os

from config import PG_CONFIG, ETL_OUTPUT_DIR

# ============================================================
# UTILIDADES
# ============================================================

def get_pg_conn():
    """Obtiene conexión PostgreSQL."""
    return psycopg2.connect(**PG_CONFIG)

def log_progress(message: str):
    """Log con timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

# ============================================================
# VALIDACIONES
# ============================================================

def validar_conteos(cursor) -> dict:
    """Valida conteos de registros en todas las tablas."""
    log_progress("Validando conteos de tablas...")

    tablas = [
        'dim_paises',
        'dim_empresas',
        'dim_plantas',
        'dim_productos',
        'dim_indicadores',
        'dim_combustibles',
        'fact_indicadores_planta',
        'fact_indicadores_producto',
        'fact_distancias',
        'fact_composicion_cemento',
        'ref_gnr_data',
        'ref_data_global'
    ]

    conteos = {}
    for tabla in tablas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            conteos[tabla] = count
            log_progress(f"  {tabla}: {count:,} registros")
        except Exception as e:
            conteos[tabla] = f"ERROR: {e}"
            log_progress(f"  {tabla}: ERROR - {e}")

    return conteos


def validar_integridad_referencial(cursor) -> list:
    """Verifica que no haya registros huérfanos."""
    log_progress("Validando integridad referencial...")

    errores = []

    # Plantas sin país
    cursor.execute("""
        SELECT COUNT(*) FROM dim_plantas
        WHERE id_pais IS NULL
    """)
    huerfanos = cursor.fetchone()[0]
    if huerfanos > 0:
        errores.append(f"Plantas sin país asignado: {huerfanos}")
        log_progress(f"  ! Plantas sin país: {huerfanos}")

    # Indicadores sin planta válida
    cursor.execute("""
        SELECT COUNT(*) FROM fact_indicadores_planta f
        WHERE NOT EXISTS (SELECT 1 FROM dim_plantas p WHERE p.id_planta = f.id_planta)
    """)
    huerfanos = cursor.fetchone()[0]
    if huerfanos > 0:
        errores.append(f"Indicadores con planta inválida: {huerfanos}")
        log_progress(f"  ! Indicadores con planta inválida: {huerfanos}")

    # Indicadores sin indicador válido
    cursor.execute("""
        SELECT COUNT(*) FROM fact_indicadores_planta f
        WHERE NOT EXISTS (SELECT 1 FROM dim_indicadores i WHERE i.id_indicador = f.id_indicador)
    """)
    huerfanos = cursor.fetchone()[0]
    if huerfanos > 0:
        errores.append(f"Datos con indicador inválido: {huerfanos}")
        log_progress(f"  ! Datos con indicador inválido: {huerfanos}")

    if not errores:
        log_progress("  ✓ Integridad referencial correcta")

    return errores


def validar_cobertura_datos(cursor) -> dict:
    """Analiza cobertura de datos por base de datos origen."""
    log_progress("Analizando cobertura de datos...")

    cobertura = {}

    # Por base de datos
    cursor.execute("""
        SELECT bd_origen, COUNT(*) as registros, COUNT(DISTINCT id_planta) as plantas
        FROM fact_indicadores_planta
        GROUP BY bd_origen
        ORDER BY registros DESC
    """)

    for row in cursor.fetchall():
        bd = row[0] or 'sin_origen'
        cobertura[bd] = {
            'registros': row[1],
            'plantas': row[2]
        }
        log_progress(f"  {bd}: {row[1]:,} registros, {row[2]} plantas")

    return cobertura


def validar_rangos_datos(cursor) -> list:
    """Verifica que los valores estén en rangos razonables."""
    log_progress("Validando rangos de datos...")

    alertas = []

    # Factor clinker debe estar entre 0 y 1
    cursor.execute("""
        SELECT COUNT(*) FROM fact_indicadores_planta f
        JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
        WHERE i.codigo_indicador = '92a'
        AND (f.valor < 0 OR f.valor > 1)
    """)
    fuera_rango = cursor.fetchone()[0]
    if fuera_rango > 0:
        alertas.append(f"Factor clinker fuera de rango [0,1]: {fuera_rango}")
        log_progress(f"  ! Factor clinker fuera de rango: {fuera_rango}")

    # Emisiones específicas deben ser positivas y razonables (< 2000 kg/t)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_indicadores_planta f
        JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
        WHERE i.codigo_indicador = '73'
        AND (f.valor < 0 OR f.valor > 2000)
    """)
    fuera_rango = cursor.fetchone()[0]
    if fuera_rango > 0:
        alertas.append(f"Emisiones específicas fuera de rango: {fuera_rango}")
        log_progress(f"  ! Emisiones fuera de rango: {fuera_rango}")

    # Consumo térmico específico (MJ/t clinker) típico: 2800-4500
    cursor.execute("""
        SELECT COUNT(*) FROM fact_indicadores_planta f
        JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
        WHERE i.codigo_indicador = '93'
        AND (f.valor < 2000 OR f.valor > 6000)
    """)
    fuera_rango = cursor.fetchone()[0]
    if fuera_rango > 0:
        alertas.append(f"Consumo térmico fuera de rango típico: {fuera_rango}")
        log_progress(f"  ! Consumo térmico fuera de rango: {fuera_rango}")

    if not alertas:
        log_progress("  ✓ Rangos de datos correctos")

    return alertas


def validar_vistas_materializadas(cursor) -> dict:
    """Verifica que las vistas materializadas tengan datos."""
    log_progress("Validando vistas materializadas...")

    vistas = [
        'mv_kpi_plantas_anual',
        'mv_benchmark_comparativo',
        'mv_tendencias_co2',
        'mv_resumen_por_pais',
        'mv_eficiencia_energetica'
    ]

    conteos = {}
    for vista in vistas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {vista}")
            count = cursor.fetchone()[0]
            conteos[vista] = count
            status = "✓" if count > 0 else "!"
            log_progress(f"  {status} {vista}: {count:,} registros")
        except Exception as e:
            conteos[vista] = f"ERROR: {e}"
            log_progress(f"  ! {vista}: ERROR - {e}")

    return conteos


def generar_estadisticas(cursor) -> dict:
    """Genera estadísticas generales del dataset."""
    log_progress("Generando estadísticas...")

    stats = {}

    # Rango de fechas
    cursor.execute("""
        SELECT MIN(fecha), MAX(fecha) FROM fact_indicadores_planta
    """)
    row = cursor.fetchone()
    stats['fecha_min'] = str(row[0]) if row[0] else None
    stats['fecha_max'] = str(row[1]) if row[1] else None
    log_progress(f"  Rango fechas: {stats['fecha_min']} a {stats['fecha_max']}")

    # Países con datos
    cursor.execute("""
        SELECT COUNT(DISTINCT pa.nombre)
        FROM fact_indicadores_planta f
        JOIN dim_plantas p ON f.id_planta = p.id_planta
        JOIN dim_paises pa ON p.id_pais = pa.id_pais
    """)
    stats['paises_con_datos'] = cursor.fetchone()[0]
    log_progress(f"  Países con datos: {stats['paises_con_datos']}")

    # Top 5 indicadores más reportados
    cursor.execute("""
        SELECT i.codigo_indicador, i.nombre, COUNT(*) as registros
        FROM fact_indicadores_planta f
        JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
        GROUP BY i.codigo_indicador, i.nombre
        ORDER BY registros DESC
        LIMIT 5
    """)
    stats['top_indicadores'] = [
        {'codigo': r[0], 'nombre': r[1], 'registros': r[2]}
        for r in cursor.fetchall()
    ]
    log_progress("  Top 5 indicadores:")
    for ind in stats['top_indicadores']:
        log_progress(f"    - {ind['codigo']}: {ind['registros']:,}")

    return stats


def ejecutar_consulta_ejemplo(cursor):
    """Ejecuta una consulta de ejemplo para verificar funcionalidad."""
    log_progress("Ejecutando consulta de ejemplo...")

    try:
        cursor.execute("""
            SELECT
                pais,
                año,
                COUNT(*) as plantas,
                ROUND(AVG(co2_especifico_clinker_kg_t)::numeric, 1) as co2_promedio,
                ROUND(AVG(factor_clinker)::numeric, 3) as factor_clinker_promedio
            FROM mv_kpi_plantas_anual
            WHERE año >= 2020
            GROUP BY pais, año
            ORDER BY pais, año
            LIMIT 10
        """)

        log_progress("  Resultado:")
        log_progress("  | País | Año | Plantas | CO2 (kg/t) | Factor Clinker |")
        log_progress("  |------|-----|---------|------------|----------------|")

        for row in cursor.fetchall():
            log_progress(f"  | {row[0][:15]:15} | {row[1]} | {row[2]:7} | {row[3] or 'N/A':>10} | {row[4] or 'N/A':>14} |")

        log_progress("  ✓ Consulta ejecutada correctamente")
        return True

    except Exception as e:
        log_progress(f"  ! Error en consulta: {e}")
        return False


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta validación completa."""
    log_progress("=" * 60)
    log_progress("INICIO: Validación de Datos")
    log_progress("=" * 60)

    resultados = {
        'timestamp': datetime.now().isoformat(),
        'conteos': {},
        'integridad': [],
        'cobertura': {},
        'rangos': [],
        'vistas': {},
        'estadisticas': {},
        'consulta_ok': False
    }

    try:
        pg_conn = get_pg_conn()
        cursor = pg_conn.cursor()
        log_progress("Conexión PostgreSQL establecida")

        # Ejecutar validaciones
        resultados['conteos'] = validar_conteos(cursor)
        resultados['integridad'] = validar_integridad_referencial(cursor)
        resultados['cobertura'] = validar_cobertura_datos(cursor)
        resultados['rangos'] = validar_rangos_datos(cursor)
        resultados['vistas'] = validar_vistas_materializadas(cursor)
        resultados['estadisticas'] = generar_estadisticas(cursor)
        resultados['consulta_ok'] = ejecutar_consulta_ejemplo(cursor)

        pg_conn.close()

        # Guardar resultados
        output_path = os.path.join(ETL_OUTPUT_DIR, 'validacion_resultado.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2, default=str)
        log_progress(f"Resultados guardados en: {output_path}")

        # Resumen final
        log_progress("=" * 60)
        log_progress("RESUMEN DE VALIDACIÓN:")
        log_progress("=" * 60)

        total_registros = sum(
            v for v in resultados['conteos'].values()
            if isinstance(v, int)
        )
        log_progress(f"  Total registros: {total_registros:,}")

        errores = len(resultados['integridad']) + len(resultados['rangos'])
        if errores > 0:
            log_progress(f"  ⚠ Alertas encontradas: {errores}")
        else:
            log_progress("  ✓ Sin errores de integridad")

        if resultados['consulta_ok']:
            log_progress("  ✓ Consultas funcionando correctamente")

        log_progress("=" * 60)
        log_progress("COMPLETADO: Validación de Datos")
        log_progress("=" * 60)

        return resultados

    except Exception as e:
        log_progress(f"ERROR FATAL: {e}")
        raise


if __name__ == '__main__':
    main()
