#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script 04: Migración de Distancias
Unifica distancias de transporte de todas las bases + datos hardcodeados de Yura

Ejecutar después de: 02_migrar_dimensiones.py
Requiere: output/mapeos_dimension.json
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
import os
import json
from datetime import datetime
from typing import Dict, Tuple, List

from config import (
    SQLITE_DATABASES,
    PG_CONFIG,
    ETL_OUTPUT_DIR,
    DISTANCIAS_DEFAULT_YURA,
    FACTORES_EMISION_TRANSPORTE
)

# ============================================================
# UTILIDADES
# ============================================================

def get_sqlite_conn(db_key: str) -> sqlite3.Connection:
    """Obtiene conexión SQLite para una base específica."""
    config = SQLITE_DATABASES.get(db_key)
    if not config:
        raise ValueError(f"Base de datos no configurada: {db_key}")

    path = config['path']
    if not os.path.exists(path):
        raise FileNotFoundError(f"Base de datos no encontrada: {db_key} -> {path}")

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def get_pg_conn() -> psycopg2.extensions.connection:
    """Obtiene conexión PostgreSQL."""
    return psycopg2.connect(**PG_CONFIG)

def log_progress(message: str):
    """Log con timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def cargar_mapeos() -> dict:
    """Carga mapeos de dimensiones desde JSON."""
    mapeos_path = os.path.join(ETL_OUTPUT_DIR, 'mapeos_dimension.json')

    if not os.path.exists(mapeos_path):
        raise FileNotFoundError(f"Archivo de mapeos no encontrado: {mapeos_path}")

    with open(mapeos_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_tuple_key(key_str: str) -> Tuple[str, int]:
    """Convierte string '(bd, id)' a tupla."""
    key_str = key_str.strip("()")
    parts = key_str.split(", ")
    bd = parts[0].strip("'\"")
    id_val = int(parts[1])
    return (bd, id_val)

def calcular_emision(distancia_km: float, modo: str) -> float:
    """Calcula kg CO2 por tonelada para una distancia y modo de transporte."""
    factor = FACTORES_EMISION_TRANSPORTE.get(modo, 0.062)
    return distancia_km * factor

# ============================================================
# MIGRACIÓN DE DISTANCIAS POR BASE
# ============================================================

def migrar_distancias_pacas(pg_conn, mapeo_plantas: dict) -> int:
    """
    Migra tb_distancias_plantas de PACAS.
    """
    log_progress("  -> Procesando distancias PACAS...")

    sqlite_conn = get_sqlite_conn('pacas')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    # Verificar tabla
    cursor_sqlite.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='tb_distancias_plantas'
    """)
    if not cursor_sqlite.fetchone():
        log_progress("    ! Tabla tb_distancias_plantas no existe en PACAS")
        sqlite_conn.close()
        return 0

    # Obtener estructura
    cursor_sqlite.execute("PRAGMA table_info(tb_distancias_plantas)")
    columnas = [r[1] for r in cursor_sqlite.fetchall()]
    log_progress(f"    Columnas: {columnas}")

    cursor_sqlite.execute("SELECT * FROM tb_distancias_plantas")
    datos = cursor_sqlite.fetchall()

    batch_data = []
    for row in datos:
        # Mapear planta origen si existe
        id_planta_origen = row.get('id_planta_origen') or row.get('id_planta')
        id_planta_pg = mapeo_plantas.get(('pacas', id_planta_origen)) if id_planta_origen else None

        distancia = row.get('distancia') or row.get('distancia_km') or 0
        modo = row.get('modo_transporte') or row.get('modo') or 'camion'

        batch_data.append((
            id_planta_pg,
            None,  # id_planta_destino
            row.get('nombre_origen') or row.get('origen'),
            row.get('nombre_destino') or row.get('destino'),
            row.get('tipo_ruta') or 'insumo',
            row.get('material'),
            row.get('codigo_material'),
            modo,
            distancia,
            row.get('lat_origen'),
            row.get('lon_origen'),
            row.get('lat_destino'),
            row.get('lon_destino'),
            FACTORES_EMISION_TRANSPORTE.get(modo, 0.062),
            calcular_emision(distancia, modo),
            'MEX',
            'pacas',
            'base_datos'
        ))

    if batch_data:
        insert_sql = """
            INSERT INTO fact_distancias (
                id_planta_origen, id_planta_destino,
                nombre_origen, nombre_destino,
                tipo_ruta, material, codigo_material,
                modo_transporte, distancia_km,
                lat_origen, lon_origen, lat_destino, lon_destino,
                factor_emision, kg_co2_tonelada,
                pais_origen, bd_origen, fuente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        execute_batch(cursor_pg, insert_sql, batch_data, page_size=100)
        pg_conn.commit()

    sqlite_conn.close()
    log_progress(f"    Insertados {len(batch_data)} registros de PACAS")
    return len(batch_data)


def migrar_distancias_mzma(pg_conn, mapeo_plantas: dict) -> int:
    """
    Migra tb_distancias_rutas de MZMA.
    """
    log_progress("  -> Procesando distancias MZMA...")

    sqlite_conn = get_sqlite_conn('mzma')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    cursor_sqlite.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='tb_distancias_rutas'
    """)
    if not cursor_sqlite.fetchone():
        log_progress("    ! Tabla tb_distancias_rutas no existe en MZMA")
        sqlite_conn.close()
        return 0

    cursor_sqlite.execute("SELECT * FROM tb_distancias_rutas")
    datos = cursor_sqlite.fetchall()

    batch_data = []
    for row in datos:
        id_planta_origen = row.get('id_planta_origen') or row.get('id_planta')
        id_planta_pg = mapeo_plantas.get(('mzma', id_planta_origen)) if id_planta_origen else None

        distancia = row.get('distancia') or row.get('distancia_km') or 0
        modo = row.get('modo_transporte') or row.get('modo') or 'camion'

        batch_data.append((
            id_planta_pg,
            None,
            row.get('nombre_origen') or row.get('origen'),
            row.get('nombre_destino') or row.get('destino'),
            row.get('tipo_ruta') or 'despacho',
            row.get('material'),
            row.get('codigo_material'),
            modo,
            distancia,
            row.get('lat_origen'),
            row.get('lon_origen'),
            row.get('lat_destino'),
            row.get('lon_destino'),
            FACTORES_EMISION_TRANSPORTE.get(modo, 0.062),
            calcular_emision(distancia, modo),
            'MEX',
            'mzma',
            'base_datos'
        ))

    if batch_data:
        insert_sql = """
            INSERT INTO fact_distancias (
                id_planta_origen, id_planta_destino,
                nombre_origen, nombre_destino,
                tipo_ruta, material, codigo_material,
                modo_transporte, distancia_km,
                lat_origen, lon_origen, lat_destino, lon_destino,
                factor_emision, kg_co2_tonelada,
                pais_origen, bd_origen, fuente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        execute_batch(cursor_pg, insert_sql, batch_data, page_size=100)
        pg_conn.commit()

    sqlite_conn.close()
    log_progress(f"    Insertados {len(batch_data)} registros de MZMA")
    return len(batch_data)


def migrar_distancias_melon(pg_conn, mapeo_plantas: dict) -> int:
    """
    Migra tb_distancias_rutas de Melón.
    """
    log_progress("  -> Procesando distancias Melón...")

    sqlite_conn = get_sqlite_conn('melon')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    cursor_sqlite.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='tb_distancias_rutas'
    """)
    if not cursor_sqlite.fetchone():
        log_progress("    ! Tabla tb_distancias_rutas no existe en Melón")
        sqlite_conn.close()
        return 0

    cursor_sqlite.execute("SELECT * FROM tb_distancias_rutas")
    datos = cursor_sqlite.fetchall()

    batch_data = []
    for row in datos:
        id_planta_origen = row.get('id_planta_origen') or row.get('id_planta')
        id_planta_pg = mapeo_plantas.get(('melon', id_planta_origen)) if id_planta_origen else None

        distancia = row.get('distancia') or row.get('distancia_km') or 0
        modo = row.get('modo_transporte') or row.get('modo') or 'camion'

        batch_data.append((
            id_planta_pg,
            None,
            row.get('nombre_origen') or row.get('origen'),
            row.get('nombre_destino') or row.get('destino'),
            row.get('tipo_ruta') or 'despacho',
            row.get('material'),
            row.get('codigo_material'),
            modo,
            distancia,
            row.get('lat_origen'),
            row.get('lon_origen'),
            row.get('lat_destino'),
            row.get('lon_destino'),
            FACTORES_EMISION_TRANSPORTE.get(modo, 0.062),
            calcular_emision(distancia, modo),
            'CHL',
            'melon',
            'base_datos'
        ))

    if batch_data:
        insert_sql = """
            INSERT INTO fact_distancias (
                id_planta_origen, id_planta_destino,
                nombre_origen, nombre_destino,
                tipo_ruta, material, codigo_material,
                modo_transporte, distancia_km,
                lat_origen, lon_origen, lat_destino, lon_destino,
                factor_emision, kg_co2_tonelada,
                pais_origen, bd_origen, fuente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        execute_batch(cursor_pg, insert_sql, batch_data, page_size=100)
        pg_conn.commit()

    sqlite_conn.close()
    log_progress(f"    Insertados {len(batch_data)} registros de Melón")
    return len(batch_data)


def migrar_distancias_yura_hardcoded(pg_conn) -> int:
    """
    Migra distancias hardcodeadas de Yura desde config.py.
    Estas distancias estaban en /home/cpinilla/projects/yura-2c/streamlit/services/const.py
    """
    log_progress("  -> Procesando distancias YURA (hardcodeadas)...")

    cursor_pg = pg_conn.cursor()
    batch_data = []

    for material, paises in DISTANCIAS_DEFAULT_YURA.items():
        for pais, modos in paises.items():
            for modo, distancia in modos.items():
                # Determinar tipo de ruta
                if material in ['cemento_despachado', 'clinker_importado']:
                    tipo_ruta = 'despacho'
                else:
                    tipo_ruta = 'insumo'

                # Pais origen según material
                if material == 'clinker_importado':
                    pais_origen = pais
                else:
                    pais_origen = 'PER'

                batch_data.append((
                    None,  # id_planta_origen (Yura genérico)
                    None,  # id_planta_destino
                    f'Yura - {pais}',  # nombre_origen
                    material,  # nombre_destino
                    tipo_ruta,
                    material,
                    material,  # codigo_material
                    modo,
                    distancia,
                    None, None, None, None,  # coordenadas
                    FACTORES_EMISION_TRANSPORTE.get(modo, 0.062),
                    calcular_emision(distancia, modo),
                    pais_origen,
                    'yura',
                    'hardcoded_const.py'
                ))

    if batch_data:
        insert_sql = """
            INSERT INTO fact_distancias (
                id_planta_origen, id_planta_destino,
                nombre_origen, nombre_destino,
                tipo_ruta, material, codigo_material,
                modo_transporte, distancia_km,
                lat_origen, lon_origen, lat_destino, lon_destino,
                factor_emision, kg_co2_tonelada,
                pais_origen, bd_origen, fuente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        execute_batch(cursor_pg, insert_sql, batch_data, page_size=100)
        pg_conn.commit()

    log_progress(f"    Insertados {len(batch_data)} registros de YURA (hardcoded)")
    return len(batch_data)


def migrar_composicion_cemento(pg_conn, mapeo_plantas: dict) -> int:
    """
    Migra composición de cementos desde Yura (cementos_bruto) y FICEM (cementos).
    """
    log_progress("Migrando fact_composicion_cemento...")

    cursor_pg = pg_conn.cursor()
    total = 0

    # 1. Migrar desde Yura - cementos_bruto
    log_progress("  -> Procesando cementos_bruto (Yura)...")
    try:
        sqlite_conn = get_sqlite_conn('yura')
        cursor_sqlite = sqlite_conn.cursor()

        cursor_sqlite.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='cementos_bruto'
        """)

        if cursor_sqlite.fetchone():
            cursor_sqlite.execute("PRAGMA table_info(cementos_bruto)")
            columnas = [r[1] for r in cursor_sqlite.fetchall()]
            log_progress(f"    Columnas: {columnas}")

            cursor_sqlite.execute("SELECT * FROM cementos_bruto")
            datos = cursor_sqlite.fetchall()

            for row in datos:
                try:
                    id_planta_origen = row.get('id_planta')
                    id_planta_pg = mapeo_plantas.get(('yura', id_planta_origen)) if id_planta_origen else None

                    cursor_pg.execute("""
                        INSERT INTO fact_composicion_cemento (
                            id_planta, nombre_planta, tipo_cemento, año, mes,
                            factor_clinker, pct_yeso, pct_caliza, pct_puzolana,
                            pct_escoria, pct_ceniza, pct_aditivo, factor_co2, bd_origen
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        id_planta_pg,
                        row.get('planta') or row.get('nombre_planta'),
                        row.get('tipo_cemento') or row.get('cemento'),
                        row.get('año') or row.get('year'),
                        row.get('mes') or row.get('month'),
                        row.get('factor_clinker') or row.get('pct_clinker'),
                        row.get('pct_yeso'),
                        row.get('pct_caliza'),
                        row.get('pct_puzolana'),
                        row.get('pct_escoria'),
                        row.get('pct_ceniza') or row.get('pct_ceniza_volante'),
                        row.get('pct_aditivo'),
                        row.get('factor_co2'),
                        'yura'
                    ))
                    total += 1
                except Exception as e:
                    pass

            pg_conn.commit()
            log_progress(f"    Insertados {total} registros de Yura")

        sqlite_conn.close()
    except Exception as e:
        log_progress(f"    ! Error procesando Yura: {e}")

    # 2. Migrar desde FICEM - cementos
    log_progress("  -> Procesando cementos (FICEM)...")
    try:
        sqlite_conn = get_sqlite_conn('ficem')
        cursor_sqlite = sqlite_conn.cursor()

        cursor_sqlite.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='cementos'
        """)

        if cursor_sqlite.fetchone():
            cursor_sqlite.execute("SELECT * FROM cementos")
            datos = cursor_sqlite.fetchall()
            count_ficem = 0

            for row in datos:
                try:
                    cursor_pg.execute("""
                        INSERT INTO fact_composicion_cemento (
                            nombre_planta, tipo_cemento, año,
                            factor_clinker, factor_co2, bd_origen
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        row.get('planta'),
                        row.get('tipo_cemento') or row.get('cemento'),
                        row.get('año') or row.get('year'),
                        row.get('factor_clinker'),
                        row.get('factor_co2') or row.get('co2_por_tonelada'),
                        'ficem'
                    ))
                    count_ficem += 1
                except:
                    pass

            pg_conn.commit()
            total += count_ficem
            log_progress(f"    Insertados {count_ficem} registros de FICEM")

        sqlite_conn.close()
    except Exception as e:
        log_progress(f"    ! Error procesando FICEM: {e}")

    log_progress(f"  -> Total fact_composicion_cemento: {total}")
    return total


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta la migración de distancias y composición."""
    log_progress("=" * 60)
    log_progress("INICIO: Migración de Distancias y Composición")
    log_progress("=" * 60)

    try:
        # Cargar mapeos
        mapeos = cargar_mapeos()

        # Reconstruir mapeo de plantas
        mapeo_plantas = {}
        for key_str, id_planta in mapeos.get('plantas', {}).items():
            try:
                key_tuple = parse_tuple_key(key_str)
                mapeo_plantas[key_tuple] = id_planta
            except:
                pass

        log_progress(f"Mapeos cargados: {len(mapeo_plantas)} plantas")

        # Conectar a PostgreSQL
        pg_conn = get_pg_conn()
        log_progress("Conexión PostgreSQL establecida")

        # Migrar distancias
        log_progress("Migrando fact_distancias...")
        total_distancias = 0
        total_distancias += migrar_distancias_pacas(pg_conn, mapeo_plantas)
        total_distancias += migrar_distancias_mzma(pg_conn, mapeo_plantas)
        total_distancias += migrar_distancias_melon(pg_conn, mapeo_plantas)
        total_distancias += migrar_distancias_yura_hardcoded(pg_conn)

        # Migrar composición de cementos
        total_composicion = migrar_composicion_cemento(pg_conn, mapeo_plantas)

        pg_conn.close()

        log_progress("=" * 60)
        log_progress("RESUMEN:")
        log_progress(f"  - fact_distancias: {total_distancias}")
        log_progress(f"  - fact_composicion_cemento: {total_composicion}")
        log_progress("=" * 60)
        log_progress("COMPLETADO: Migración de Distancias y Composición")
        log_progress("=" * 60)

    except Exception as e:
        log_progress(f"ERROR FATAL: {e}")
        raise


if __name__ == '__main__':
    main()
