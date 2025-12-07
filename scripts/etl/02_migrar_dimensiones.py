#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script 02: Migración de Dimensiones
Carga las tablas de dimensiones desde las bases SQLite origen a PostgreSQL

Ejecutar después de: 01_crear_esquema.sql
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Importar configuración centralizada
from config import (
    SQLITE_DATABASES,
    PG_CONFIG,
    ETL_OUTPUT_DIR,
    TIPOS_PLANTA,
    TIPOS_PRODUCTO
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

# ============================================================
# MIGRACIÓN DE DIMENSIONES
# ============================================================

def migrar_dim_paises(pg_conn) -> Dict[str, int]:
    """
    Migra países desde plantas_latam de ficem_bd.
    Retorna mapeo iso3 -> id_pais.
    """
    log_progress("Migrando dim_paises...")

    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    # Obtener países únicos de plantas_latam
    cursor_sqlite.execute("""
        SELECT DISTINCT pais, iso3 FROM plantas_latam
        WHERE pais IS NOT NULL AND iso3 IS NOT NULL
        ORDER BY pais
    """)

    paises = cursor_sqlite.fetchall()
    mapeo_paises = {}

    for row in paises:
        pais, iso3 = row['pais'], row['iso3']

        # Determinar región
        if iso3 in ('MEX', 'USA'):
            region = 'Norteamérica'
        elif iso3 in ('PAN', 'CRI', 'GTM', 'HND', 'NIC', 'SLV'):
            region = 'Centroamérica'
        elif iso3 in ('DOM', 'CUB', 'JAM', 'TTO'):
            region = 'Caribe'
        else:
            region = 'Sudamérica'

        # Insertar o actualizar
        cursor_pg.execute("""
            INSERT INTO dim_paises (codigo_iso3, nombre, region, activo)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (codigo_iso3) DO UPDATE SET nombre = EXCLUDED.nombre
            RETURNING id_pais
        """, (iso3, pais, region))

        id_pais = cursor_pg.fetchone()[0]
        mapeo_paises[iso3] = id_pais

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {len(mapeo_paises)} países migrados")
    return mapeo_paises


def migrar_dim_empresas(pg_conn, mapeo_paises: Dict[str, int]) -> Dict[str, int]:
    """
    Migra empresas extraídas de plantas_latam.
    Retorna mapeo (bd_origen, nombre_empresa) -> id_empresa.
    """
    log_progress("Migrando dim_empresas...")

    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    # Obtener empresas únicas
    cursor_sqlite.execute("""
        SELECT DISTINCT compania, grupo, iso3
        FROM plantas_latam
        WHERE compania IS NOT NULL
        ORDER BY compania
    """)

    empresas = cursor_sqlite.fetchall()
    mapeo_empresas = {}

    for row in empresas:
        compania = row['compania']
        grupo = row['grupo'] or compania
        iso3 = row['iso3']

        id_pais = mapeo_paises.get(iso3)

        cursor_pg.execute("""
            INSERT INTO dim_empresas (nombre, grupo_empresarial, id_pais, bd_origen, activo)
            VALUES (%s, %s, %s, %s, TRUE)
            ON CONFLICT DO NOTHING
            RETURNING id_empresa
        """, (compania, grupo, id_pais, 'ficem'))

        result = cursor_pg.fetchone()
        if result:
            mapeo_empresas[('ficem', compania)] = result[0]

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {len(mapeo_empresas)} empresas migradas")
    return mapeo_empresas


def migrar_dim_plantas(pg_conn, mapeo_paises: Dict[str, int], mapeo_empresas: Dict[str, int]) -> Dict[Tuple[str, int], int]:
    """
    Migra plantas de todas las bases de datos.
    Retorna mapeo (bd_origen, id_original) -> id_planta.
    """
    log_progress("Migrando dim_plantas...")

    cursor_pg = pg_conn.cursor()
    mapeo_plantas = {}
    total_plantas = 0

    # 1. Migrar plantas de ficem (plantas_latam - referencia)
    log_progress("  -> Procesando plantas_latam (ficem)...")
    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()

    cursor_sqlite.execute("""
        SELECT planta, codigo_planta, id_tipo_planta, ciudad, lat, lon,
               compania, pais, iso3, capacidad_instalada, tipo_planta_cemento
        FROM plantas_latam
    """)

    plantas_ficem = cursor_sqlite.fetchall()

    for row in plantas_ficem:
        tipo_planta = 'cemento' if row['id_tipo_planta'] == 1 else 'concreto'
        id_pais = mapeo_paises.get(row['iso3'])

        # Buscar empresa
        cursor_pg.execute("SELECT id_empresa FROM dim_empresas WHERE nombre = %s LIMIT 1",
                         (row['compania'],))
        empresa_result = cursor_pg.fetchone()
        id_empresa = empresa_result[0] if empresa_result else None

        cursor_pg.execute("""
            INSERT INTO dim_plantas (
                codigo_origen, bd_origen, nombre, tipo_planta,
                id_empresa, id_pais, latitud, longitud,
                capacidad_instalada, tipo_operacion, activo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            ON CONFLICT (bd_origen, codigo_origen) DO UPDATE
                SET nombre = EXCLUDED.nombre
            RETURNING id_planta
        """, (
            row['codigo_planta'], 'ficem', row['planta'], tipo_planta,
            id_empresa, id_pais, row['lat'], row['lon'],
            row['capacidad_instalada'], row['tipo_planta_cemento']
        ))

        id_planta = cursor_pg.fetchone()[0]
        mapeo_plantas[('ficem', row['codigo_planta'])] = id_planta
        total_plantas += 1

    sqlite_conn.close()

    # 2. Migrar plantas de cada BD operativa
    for bd_key in ['pacas', 'mzma', 'melon', 'yura']:
        log_progress(f"  -> Procesando tb_planta ({bd_key})...")

        try:
            sqlite_conn = get_sqlite_conn(bd_key)
            cursor_sqlite = sqlite_conn.cursor()

            # La estructura varía entre BDs
            if bd_key == 'mzma':
                cursor_sqlite.execute("""
                    SELECT id_planta, planta, ubicacion, capacidad, activa
                    FROM tb_planta
                """)
            else:
                cursor_sqlite.execute("""
                    SELECT id_planta, planta, codigo_planta, id_tipo_planta,
                           ciudad, lat, lon, pais, iso3
                    FROM tb_planta
                """)

            plantas = cursor_sqlite.fetchall()

            for row in plantas:
                id_original = row['id_planta']
                nombre = row['planta']

                if bd_key == 'mzma':
                    # MZMA tiene estructura simplificada
                    codigo = str(id_original)
                    tipo_planta = 'concreto'
                    lat, lon = None, None
                    iso3 = 'MEX'
                else:
                    codigo = row['codigo_planta'] or str(id_original)
                    tipo_planta = 'cemento' if row.get('id_tipo_planta') == 1 else 'concreto'
                    lat = row.get('lat')
                    lon = row.get('lon')
                    iso3 = row.get('iso3', 'MEX')

                id_pais = mapeo_paises.get(iso3)

                cursor_pg.execute("""
                    INSERT INTO dim_plantas (
                        codigo_origen, bd_origen, nombre, tipo_planta,
                        id_pais, latitud, longitud, activo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
                    ON CONFLICT (bd_origen, codigo_origen) DO UPDATE
                        SET nombre = EXCLUDED.nombre
                    RETURNING id_planta
                """, (codigo, bd_key, nombre, tipo_planta, id_pais, lat, lon))

                id_planta = cursor_pg.fetchone()[0]
                mapeo_plantas[(bd_key, id_original)] = id_planta
                total_plantas += 1

            sqlite_conn.close()

        except Exception as e:
            log_progress(f"  ! Error procesando {bd_key}: {e}")

    pg_conn.commit()
    log_progress(f"  -> {total_plantas} plantas migradas en total")
    return mapeo_plantas


def migrar_dim_indicadores(pg_conn) -> Dict[str, int]:
    """
    Migra indicadores desde la base común.
    Retorna mapeo codigo_indicador -> id_indicador.
    """
    log_progress("Migrando dim_indicadores...")

    sqlite_conn = get_sqlite_conn('indicadores')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    cursor_sqlite.execute("""
        SELECT supergrupo, grupo, subgrupo, codigo_indicador,
               nombre_indicador, unidad, objeto, tipo_objeto
        FROM indicadores
    """)

    indicadores = cursor_sqlite.fetchall()
    mapeo_indicadores = {}

    for row in indicadores:
        codigo = row['codigo_indicador']

        # Determinar si es indicador GCCA (códigos numéricos < 1000)
        try:
            es_gcca = int(codigo) < 1000
        except ValueError:
            es_gcca = False

        cursor_pg.execute("""
            INSERT INTO dim_indicadores (
                codigo_indicador, nombre, supergrupo, grupo, subgrupo,
                unidad, objeto, tipo_objeto, es_gcca, activo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            ON CONFLICT (codigo_indicador) DO UPDATE
                SET nombre = EXCLUDED.nombre
            RETURNING id_indicador
        """, (
            codigo, row['nombre_indicador'], row['supergrupo'], row['grupo'],
            row['subgrupo'], row['unidad'], row['objeto'], row['tipo_objeto'],
            es_gcca
        ))

        id_indicador = cursor_pg.fetchone()[0]
        mapeo_indicadores[codigo] = id_indicador

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {len(mapeo_indicadores)} indicadores migrados")
    return mapeo_indicadores


def migrar_dim_combustibles(pg_conn) -> Dict[str, int]:
    """
    Migra catálogo de combustibles desde ficem_bd.
    Retorna mapeo codigo_combustible -> id_combustible.
    """
    log_progress("Migrando dim_combustibles...")

    sqlite_conn = get_sqlite_conn('ficem')
    cursor_sqlite = sqlite_conn.cursor()
    cursor_pg = pg_conn.cursor()

    cursor_sqlite.execute("""
        SELECT codigo_consumo_combustible, combustible, tipo_combustible,
               poder_calorifico_defecto, factor_emision_defecto,
               contenido_biomasa, uso
        FROM combustibles
    """)

    combustibles = cursor_sqlite.fetchall()
    mapeo_combustibles = {}

    for row in combustibles:
        codigo = row['codigo_consumo_combustible']

        # Categorizar combustible
        tipo = row['tipo_combustible']
        if 'biomasa' in (tipo or '').lower():
            categoria = 'biomasa'
        elif 'alternativo' in (tipo or '').lower():
            categoria = 'alternativo'
        else:
            categoria = 'convencional'

        cursor_pg.execute("""
            INSERT INTO dim_combustibles (
                codigo, nombre, categoria, tipo,
                poder_calorifico, factor_emision, pct_biomasa, activo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
            ON CONFLICT (codigo) DO UPDATE
                SET nombre = EXCLUDED.nombre
            RETURNING id_combustible
        """, (
            codigo, row['combustible'], categoria, tipo,
            row['poder_calorifico_defecto'], row['factor_emision_defecto'],
            row['contenido_biomasa']
        ))

        id_combustible = cursor_pg.fetchone()[0]
        mapeo_combustibles[codigo] = id_combustible

    pg_conn.commit()
    sqlite_conn.close()

    log_progress(f"  -> {len(mapeo_combustibles)} combustibles migrados")
    return mapeo_combustibles


def migrar_dim_productos(pg_conn, mapeo_plantas: Dict[Tuple[str, int], int]) -> Dict[Tuple[str, int], int]:
    """
    Migra productos (clinker, cementos) de las bases operativas.
    Retorna mapeo (bd_origen, id_original) -> id_producto.
    """
    log_progress("Migrando dim_productos...")

    cursor_pg = pg_conn.cursor()
    mapeo_productos = {}
    total_productos = 0

    for bd_key in ['pacas', 'melon', 'yura']:
        log_progress(f"  -> Procesando tb_producto ({bd_key})...")

        try:
            sqlite_conn = get_sqlite_conn(bd_key)
            cursor_sqlite = sqlite_conn.cursor()

            # Verificar si existe la tabla
            cursor_sqlite.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='tb_producto'
            """)

            if not cursor_sqlite.fetchone():
                log_progress(f"    ! Tabla tb_producto no existe en {bd_key}")
                sqlite_conn.close()
                continue

            cursor_sqlite.execute("""
                SELECT id_producto, id_planta, id_tipo_producto, producto, codigo_producto
                FROM tb_producto
            """)

            productos = cursor_sqlite.fetchall()

            for row in productos:
                id_original = row['id_producto']
                id_planta_origen = row['id_planta']

                # Buscar id_planta en PostgreSQL
                id_planta_pg = mapeo_plantas.get((bd_key, id_planta_origen))

                # Determinar tipo de producto
                id_tipo = row.get('id_tipo_producto', 1)
                if id_tipo == 1:
                    tipo_producto = 'clinker'
                elif id_tipo == 2:
                    tipo_producto = 'cemento'
                else:
                    tipo_producto = 'otro'

                codigo = row['codigo_producto'] or str(id_original)

                cursor_pg.execute("""
                    INSERT INTO dim_productos (
                        codigo_origen, bd_origen, nombre, tipo_producto,
                        id_planta, activo
                    ) VALUES (%s, %s, %s, %s, %s, TRUE)
                    ON CONFLICT (bd_origen, codigo_origen) DO UPDATE
                        SET nombre = EXCLUDED.nombre
                    RETURNING id_producto
                """, (codigo, bd_key, row['producto'], tipo_producto, id_planta_pg))

                id_producto = cursor_pg.fetchone()[0]
                mapeo_productos[(bd_key, id_original)] = id_producto
                total_productos += 1

            sqlite_conn.close()

        except Exception as e:
            log_progress(f"  ! Error procesando {bd_key}: {e}")

    pg_conn.commit()
    log_progress(f"  -> {total_productos} productos migrados en total")
    return mapeo_productos


def guardar_mapeos(mapeos: dict, filepath: str):
    """Guarda los mapeos en archivo para uso posterior."""
    import json

    # Convertir tuplas a strings para JSON
    mapeos_serializables = {}
    for key, value in mapeos.items():
        if isinstance(value, dict):
            mapeos_serializables[key] = {}
            for k, v in value.items():
                if isinstance(k, tuple):
                    mapeos_serializables[key][str(k)] = v
                else:
                    mapeos_serializables[key][k] = v
        else:
            mapeos_serializables[key] = value

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(mapeos_serializables, f, ensure_ascii=False, indent=2)

    log_progress(f"Mapeos guardados en: {filepath}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta la migración completa de dimensiones."""
    log_progress("=" * 60)
    log_progress("INICIO: Migración de Dimensiones")
    log_progress("=" * 60)

    try:
        # Conectar a PostgreSQL
        pg_conn = get_pg_conn()
        log_progress("Conexión PostgreSQL establecida")

        # Ejecutar migraciones en orden de dependencias
        mapeo_paises = migrar_dim_paises(pg_conn)
        mapeo_empresas = migrar_dim_empresas(pg_conn, mapeo_paises)
        mapeo_plantas = migrar_dim_plantas(pg_conn, mapeo_paises, mapeo_empresas)
        mapeo_indicadores = migrar_dim_indicadores(pg_conn)
        mapeo_combustibles = migrar_dim_combustibles(pg_conn)
        mapeo_productos = migrar_dim_productos(pg_conn, mapeo_plantas)

        # Guardar mapeos para scripts posteriores
        mapeos = {
            'paises': mapeo_paises,
            'empresas': mapeo_empresas,
            'plantas': mapeo_plantas,
            'indicadores': mapeo_indicadores,
            'combustibles': mapeo_combustibles,
            'productos': mapeo_productos
        }

        mapeos_path = os.path.join(ETL_OUTPUT_DIR, 'mapeos_dimension.json')
        guardar_mapeos(mapeos, mapeos_path)

        pg_conn.close()

        log_progress("=" * 60)
        log_progress("COMPLETADO: Migración de Dimensiones")
        log_progress("=" * 60)

        return mapeos

    except Exception as e:
        log_progress(f"ERROR FATAL: {e}")
        raise


if __name__ == '__main__':
    main()
