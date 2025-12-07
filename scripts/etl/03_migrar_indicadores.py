#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script 03: Migración de Indicadores (Facts)
Carga fact_indicadores_planta y fact_indicadores_producto desde SQLite a PostgreSQL

Ejecutar después de: 02_migrar_dimensiones.py
Requiere: output/mapeos_dimension.json
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
import os
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

from config import (
    SQLITE_DATABASES,
    PG_CONFIG,
    ETL_OUTPUT_DIR,
    TEMPORALIDADES
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
        raise FileNotFoundError(
            f"Archivo de mapeos no encontrado: {mapeos_path}\n"
            "Ejecute primero 02_migrar_dimensiones.py"
        )

    with open(mapeos_path, 'r', encoding='utf-8') as f:
        mapeos = json.load(f)

    return mapeos

def parse_tuple_key(key_str: str) -> Tuple[str, int]:
    """Convierte string '(bd, id)' a tupla."""
    # Formato: "('pacas', 1)"
    key_str = key_str.strip("()")
    parts = key_str.split(", ")
    bd = parts[0].strip("'\"")
    id_val = int(parts[1])
    return (bd, id_val)

# ============================================================
# MIGRACIÓN DE INDICADORES POR PLANTA
# ============================================================

def migrar_fact_indicadores_planta(pg_conn, mapeos: dict) -> int:
    """
    Migra datos de tb_dataset + tb_data donde id_tipo_origen = 1 (Planta).
    Retorna cantidad de registros migrados.
    """
    log_progress("Migrando fact_indicadores_planta...")

    cursor_pg = pg_conn.cursor()
    total_registros = 0

    # Reconstruir mapeo de plantas (string -> int)
    mapeo_plantas = {}
    for key_str, id_planta in mapeos.get('plantas', {}).items():
        try:
            key_tuple = parse_tuple_key(key_str)
            mapeo_plantas[key_tuple] = id_planta
        except:
            pass

    # Reconstruir mapeo de indicadores
    mapeo_indicadores = mapeos.get('indicadores', {})

    for bd_key in ['pacas', 'mzma', 'melon', 'yura']:
        log_progress(f"  -> Procesando {bd_key}...")

        try:
            sqlite_conn = get_sqlite_conn(bd_key)
            cursor_sqlite = sqlite_conn.cursor()

            # Verificar tablas necesarias
            cursor_sqlite.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name IN ('tb_dataset', 'tb_data')
            """)
            tablas = [r[0] for r in cursor_sqlite.fetchall()]

            if 'tb_dataset' not in tablas or 'tb_data' not in tablas:
                log_progress(f"    ! Tablas tb_dataset/tb_data no existen en {bd_key}")
                sqlite_conn.close()
                continue

            # Obtener datos donde id_tipo_origen = 1 (Planta)
            cursor_sqlite.execute("""
                SELECT
                    ds.id_dataset,
                    ds.fecha,
                    ds.id_origen as id_planta_origen,
                    ds.id_rep_temp,
                    ds.id_escenario,
                    d.codigo_indicador,
                    d.valor_indicador
                FROM tb_dataset ds
                INNER JOIN tb_data d ON ds.id_dataset = d.id_dataset
                WHERE ds.id_tipo_origen = 1
                    AND d.valor_indicador IS NOT NULL
            """)

            datos = cursor_sqlite.fetchall()
            log_progress(f"    Encontrados {len(datos)} registros de planta")

            # Preparar batch para inserción
            batch_data = []

            for row in datos:
                id_planta_origen = row['id_planta_origen']
                codigo_indicador = row['codigo_indicador']

                # Buscar mapeos
                id_planta_pg = mapeo_plantas.get((bd_key, id_planta_origen))
                id_indicador_pg = mapeo_indicadores.get(str(codigo_indicador))

                if not id_planta_pg or not id_indicador_pg:
                    continue

                # Parsear fecha
                fecha_str = row['fecha']
                try:
                    if fecha_str and len(fecha_str) >= 10:
                        fecha = fecha_str[:10]  # YYYY-MM-DD
                    else:
                        fecha = '2024-01-01'  # Default
                except:
                    fecha = '2024-01-01'

                # Temporalidad
                id_rep_temp = row['id_rep_temp'] or 1
                temporalidad = TEMPORALIDADES.get(id_rep_temp, 'anual')

                batch_data.append((
                    id_planta_pg,
                    id_indicador_pg,
                    fecha,
                    row['valor_indicador'],
                    temporalidad,
                    row['id_escenario'] or 1,
                    bd_key,
                    row['id_dataset']
                ))

            # Insertar en lotes
            if batch_data:
                insert_sql = """
                    INSERT INTO fact_indicadores_planta (
                        id_planta, id_indicador, fecha, valor,
                        temporalidad, escenario, bd_origen, id_dataset_origen
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id_planta, id_indicador, fecha, escenario)
                    DO UPDATE SET valor = EXCLUDED.valor
                """
                execute_batch(cursor_pg, insert_sql, batch_data, page_size=1000)
                pg_conn.commit()

                total_registros += len(batch_data)
                log_progress(f"    Insertados {len(batch_data)} registros")

            sqlite_conn.close()

        except Exception as e:
            log_progress(f"    ! Error procesando {bd_key}: {e}")

    log_progress(f"  -> Total fact_indicadores_planta: {total_registros}")
    return total_registros


def migrar_fact_indicadores_producto(pg_conn, mapeos: dict) -> int:
    """
    Migra datos de tb_dataset + tb_data donde id_tipo_origen = 2 (Producto).
    Retorna cantidad de registros migrados.
    """
    log_progress("Migrando fact_indicadores_producto...")

    cursor_pg = pg_conn.cursor()
    total_registros = 0

    # Reconstruir mapeos
    mapeo_plantas = {}
    for key_str, id_planta in mapeos.get('plantas', {}).items():
        try:
            key_tuple = parse_tuple_key(key_str)
            mapeo_plantas[key_tuple] = id_planta
        except:
            pass

    mapeo_productos = {}
    for key_str, id_producto in mapeos.get('productos', {}).items():
        try:
            key_tuple = parse_tuple_key(key_str)
            mapeo_productos[key_tuple] = id_producto
        except:
            pass

    mapeo_indicadores = mapeos.get('indicadores', {})

    for bd_key in ['pacas', 'melon', 'yura']:  # mzma no tiene productos
        log_progress(f"  -> Procesando {bd_key}...")

        try:
            sqlite_conn = get_sqlite_conn(bd_key)
            cursor_sqlite = sqlite_conn.cursor()

            # Verificar tablas
            cursor_sqlite.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name IN ('tb_dataset', 'tb_data', 'tb_producto')
            """)
            tablas = [r[0] for r in cursor_sqlite.fetchall()]

            if len(tablas) < 3:
                log_progress(f"    ! Tablas necesarias no existen en {bd_key}")
                sqlite_conn.close()
                continue

            # Obtener datos donde id_tipo_origen = 2 (Producto)
            cursor_sqlite.execute("""
                SELECT
                    ds.id_dataset,
                    ds.fecha,
                    ds.id_origen as id_producto_origen,
                    ds.id_rep_temp,
                    ds.id_escenario,
                    d.codigo_indicador,
                    d.valor_indicador,
                    p.id_planta
                FROM tb_dataset ds
                INNER JOIN tb_data d ON ds.id_dataset = d.id_dataset
                LEFT JOIN tb_producto p ON ds.id_origen = p.id_producto
                WHERE ds.id_tipo_origen = 2
                    AND d.valor_indicador IS NOT NULL
            """)

            datos = cursor_sqlite.fetchall()
            log_progress(f"    Encontrados {len(datos)} registros de producto")

            batch_data = []

            for row in datos:
                id_producto_origen = row['id_producto_origen']
                id_planta_origen = row['id_planta']
                codigo_indicador = row['codigo_indicador']

                # Buscar mapeos
                id_producto_pg = mapeo_productos.get((bd_key, id_producto_origen))
                id_planta_pg = mapeo_plantas.get((bd_key, id_planta_origen)) if id_planta_origen else None
                id_indicador_pg = mapeo_indicadores.get(str(codigo_indicador))

                if not id_producto_pg or not id_indicador_pg:
                    continue

                # Parsear fecha
                fecha_str = row['fecha']
                try:
                    if fecha_str and len(fecha_str) >= 10:
                        fecha = fecha_str[:10]
                    else:
                        fecha = '2024-01-01'
                except:
                    fecha = '2024-01-01'

                id_rep_temp = row['id_rep_temp'] or 1
                temporalidad = TEMPORALIDADES.get(id_rep_temp, 'anual')

                batch_data.append((
                    id_planta_pg,
                    id_producto_pg,
                    id_indicador_pg,
                    fecha,
                    row['valor_indicador'],
                    temporalidad,
                    row['id_escenario'] or 1,
                    bd_key,
                    row['id_dataset']
                ))

            if batch_data:
                insert_sql = """
                    INSERT INTO fact_indicadores_producto (
                        id_planta, id_producto, id_indicador, fecha, valor,
                        temporalidad, escenario, bd_origen, id_dataset_origen
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """
                execute_batch(cursor_pg, insert_sql, batch_data, page_size=1000)
                pg_conn.commit()

                total_registros += len(batch_data)
                log_progress(f"    Insertados {len(batch_data)} registros")

            sqlite_conn.close()

        except Exception as e:
            log_progress(f"    ! Error procesando {bd_key}: {e}")

    log_progress(f"  -> Total fact_indicadores_producto: {total_registros}")
    return total_registros


def migrar_ref_gnr_data(pg_conn) -> int:
    """
    Migra datos de gnr_data desde ficem_bd.
    """
    log_progress("Migrando ref_gnr_data...")

    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    # Verificar estructura
    cursor_sqlite.execute("PRAGMA table_info(gnr_data)")
    columnas = [r[1] for r in cursor_sqlite.fetchall()]
    log_progress(f"  Columnas gnr_data: {columnas[:10]}...")

    # Obtener datos
    cursor_sqlite.execute("SELECT * FROM gnr_data")
    datos = cursor_sqlite.fetchall()

    total = 0
    for row in datos:
        try:
            cursor_pg.execute("""
                INSERT INTO ref_gnr_data (
                    año, region, pais, indicador, codigo_indicador,
                    valor, unidad, fuente
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                row['year'] if 'year' in columnas else row.get('año'),
                row.get('region'),
                row.get('country') if 'country' in columnas else row.get('pais'),
                row.get('indicator') if 'indicator' in columnas else row.get('indicador'),
                row.get('indicator_code') if 'indicator_code' in columnas else row.get('codigo'),
                row.get('value') if 'value' in columnas else row.get('valor'),
                row.get('unit') if 'unit' in columnas else row.get('unidad'),
                'GNR-GCCA'
            ))
            total += 1
        except Exception as e:
            pass

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {total} registros migrados a ref_gnr_data")
    return total


def migrar_ref_data_global(pg_conn) -> int:
    """
    Migra datos de data_global desde ficem_bd.
    """
    log_progress("Migrando ref_data_global...")

    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    cursor_sqlite.execute("SELECT COUNT(*) FROM data_global")
    count = cursor_sqlite.fetchone()[0]
    log_progress(f"  Registros en data_global: {count}")

    cursor_sqlite.execute("PRAGMA table_info(data_global)")
    columnas = [r[1] for r in cursor_sqlite.fetchall()]
    log_progress(f"  Columnas: {columnas}")

    cursor_sqlite.execute("SELECT * FROM data_global")
    datos = cursor_sqlite.fetchall()

    total = 0
    batch_data = []

    for row in datos:
        try:
            batch_data.append((
                row.get('año') or row.get('year'),
                row.get('pais') or row.get('country'),
                row.get('region'),
                row.get('indicador') or row.get('indicator'),
                row.get('codigo_indicador') or row.get('indicator_code'),
                row.get('valor') or row.get('value'),
                row.get('unidad') or row.get('unit'),
                row.get('fuente') or row.get('source') or 'data_global'
            ))
            total += 1
        except:
            pass

    if batch_data:
        insert_sql = """
            INSERT INTO ref_data_global (
                año, pais, region, indicador, codigo_indicador,
                valor, unidad, fuente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        execute_batch(cursor_pg, insert_sql, batch_data, page_size=1000)

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {total} registros migrados a ref_data_global")
    return total


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta la migración de indicadores."""
    log_progress("=" * 60)
    log_progress("INICIO: Migración de Indicadores (Facts)")
    log_progress("=" * 60)

    try:
        # Cargar mapeos de dimensiones
        mapeos = cargar_mapeos()
        log_progress("Mapeos de dimensiones cargados")

        # Conectar a PostgreSQL
        pg_conn = get_pg_conn()
        log_progress("Conexión PostgreSQL establecida")

        # Ejecutar migraciones
        total_planta = migrar_fact_indicadores_planta(pg_conn, mapeos)
        total_producto = migrar_fact_indicadores_producto(pg_conn, mapeos)
        total_gnr = migrar_ref_gnr_data(pg_conn)
        total_global = migrar_ref_data_global(pg_conn)

        pg_conn.close()

        log_progress("=" * 60)
        log_progress("RESUMEN:")
        log_progress(f"  - fact_indicadores_planta: {total_planta}")
        log_progress(f"  - fact_indicadores_producto: {total_producto}")
        log_progress(f"  - ref_gnr_data: {total_gnr}")
        log_progress(f"  - ref_data_global: {total_global}")
        log_progress("=" * 60)
        log_progress("COMPLETADO: Migración de Indicadores")
        log_progress("=" * 60)

    except Exception as e:
        log_progress(f"ERROR FATAL: {e}")
        raise


if __name__ == '__main__':
    main()
