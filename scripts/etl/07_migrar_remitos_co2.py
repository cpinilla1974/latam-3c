#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL: Migrar remitos con resistencia y huella CO₂ a PostgreSQL
Extrae datos de PACAS, MZMA, Melón y Lomax, los consolida en latam4c_db
"""

import sqlite3
import psycopg2
import pandas as pd
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

SQLITE_DATABASES = {
    'pacas': {
        'path': '/home/cpinilla/pacas-3c/data/main.db',
        'empresa': 'Cementos y Concretos del Pacífico',
        'pais': 'MEX'
    },
    'mzma': {
        'path': '/home/cpinilla/databases/mzma-3c/data/main.db',
        'empresa': 'Cementos Moctezuma',
        'pais': 'MEX'
    },
    # Base activa de Melón (main - copia.db - con corrida completa)
    'melon': {
        'path': '/home/cpinilla/databases/melon-3c/data/old/main - copia.db',
        'empresa': 'Cementos Melón',
        'pais': 'CHL'
    },
    # Base legacy de Melón (Melon_2.db - pocos registros con relación)
    'melon_legacy': {
        'path': '/home/cpinilla/databases/melon-3c/data/old/Melon_2.db',
        'empresa': 'Cementos Melón',
        'pais': 'CHL'
    },
    # Lomax
    'lomax': {
        'path': '/home/cpinilla/projects/lomax-3c/streamlit/data/main.db',
        'empresa': 'Lomax',
        'pais': 'CHL'
    }
}

PG_DATABASE = 'latam4c_db'

# ============================================================
# QUERIES DE EXTRACCIÓN
# ============================================================

QUERY_PACAS = """
SELECT
    r.anio_planta_remito as id_remito,
    r.fecha,
    r.planta,
    r.formula as producto,
    a.resistencia_mpa,
    r.volumen,
    r.huella as co2_kg_m3,
    r.emision_cemento,
    r.emision_agregados,
    r.emision_aditivos,
    r.emision_total
FROM co2_remitos r
JOIN tb_atributos_concreto a ON r.formula = a.producto
WHERE a.resistencia_mpa > 0 AND r.huella > 0
"""

QUERY_MZMA = """
SELECT
    c.codigo_dataset as id_remito,
    c.fecha,
    c.planta_concretera as planta,
    c.nombre_concreto as producto,
    CAST(a.REST AS REAL) / 10.2 as resistencia_mpa,
    c.volumen,
    co2.co2_kg_m3,
    co2.co2_cem_descarbonatacion_clinker + co2.co2_cem_comb_conv_clinker +
    co2.co2_cem_comb_alter_clinker + co2.co2_cem_energia_electrica as emision_cemento,
    co2.co2_agr_alcance_1 + co2.co2_agr_alcance_2 as emision_agregados,
    co2.co2_adi_alcance_1 + co2.co2_adi_alcance_2 as emision_aditivos,
    co2.co2_total as emision_total
FROM corp_concretos c
JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
WHERE co2.co2_kg_m3 > 0 AND CAST(a.REST AS REAL) > 0
"""

# Query para base activa de Melón (main - copia.db - con corrida completa)
QUERY_MELON = """
SELECT
    r.codigo_dataset as id_remito,
    r.fecha,
    pl.planta,
    p.producto,
    CAST(a.REST AS REAL) / 10.2 as resistencia_mpa,
    r.volumen,
    co2.co2_kg_m3,
    co2.co2_cem_descarbonatacion_clinker + co2.co2_cem_comb_conv_clinker +
    co2.co2_cem_comb_alter_clinker + co2.co2_cem_energia_electrica as emision_cemento,
    co2.co2_agr_alcance_1 + co2.co2_agr_alcance_2 as emision_agregados,
    co2.co2_adi_alcance_1 + co2.co2_adi_alcance_2 as emision_aditivos,
    co2.co2_total as emision_total
FROM tb_remitos r
JOIN tb_producto p ON r.id_producto = p.id_producto
JOIN tb_planta pl ON r.id_planta = pl.id_planta
JOIN tb_atributos_concretos a ON p.producto = a.nombre_concreto
JOIN corp_co2 co2 ON r.codigo_dataset = co2.codigo_dataset
WHERE a.REST NOT LIKE '%FLUID%'
  AND CAST(a.REST AS REAL) > 0
  AND co2.co2_kg_m3 > 0
"""

# Query para base legacy de Melón (Melon_2.db - pocos registros)
QUERY_MELON_LEGACY = """
SELECT DISTINCT
    c.codigo_dataset as id_remito,
    c.fecha,
    c.planta_concretera as planta,
    c.nombre_concreto as producto,
    CAST(a.REST AS REAL) as resistencia_mpa,
    c.volumen,
    co2.co2_kg_m3,
    co2.co2_cem_descarbonatacion_clinker + co2.co2_cem_comb_conv_clinker +
    co2.co2_cem_comb_alter_clinker + co2.co2_cem_energia_electrica as emision_cemento,
    co2.co2_agr_alcance_1 + co2.co2_agr_alcance_2 as emision_agregados,
    co2.co2_adi_alcance_1 + co2.co2_adi_alcance_2 as emision_aditivos,
    co2.co2_total as emision_total
FROM corp_concretos c
JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
WHERE co2.co2_kg_m3 > 0 AND CAST(a.REST AS REAL) > 0
"""

# Query para Lomax (Chile - REST ya está en MPa, NO dividir)
QUERY_LOMAX = """
SELECT
    c.codigo_dataset as id_remito,
    c.fecha,
    c.planta_concretera as planta,
    c.nombre_concreto as producto,
    CAST(a.REST AS REAL) as resistencia_mpa,
    c.volumen,
    co2.co2_kg_m3,
    co2.co2_cem_descarbonatacion_clinker + co2.co2_cem_comb_conv_clinker +
    co2.co2_cem_comb_alter_clinker + co2.co2_cem_energia_electrica as emision_cemento,
    co2.co2_agr_alcance_1 + co2.co2_agr_alcance_2 as emision_agregados,
    co2.co2_adi_alcance_1 + co2.co2_adi_alcance_2 as emision_aditivos,
    co2.co2_total as emision_total
FROM corp_concretos c
JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
WHERE co2.co2_kg_m3 > 0 AND CAST(a.REST AS REAL) > 0
"""

# ============================================================
# FUNCIONES
# ============================================================

def crear_tabla_destino(pg_conn):
    """Crear tabla en PostgreSQL para remitos con CO₂"""
    cursor = pg_conn.cursor()

    # Eliminar tabla si existe
    cursor.execute("DROP TABLE IF EXISTS remitos_co2")

    # Crear tabla
    cursor.execute("""
        CREATE TABLE remitos_co2 (
            id SERIAL PRIMARY KEY,
            id_remito TEXT,
            origen TEXT NOT NULL,
            empresa TEXT,
            pais TEXT,
            fecha DATE,
            planta TEXT,
            producto TEXT,
            resistencia_mpa REAL,
            volumen REAL,
            co2_kg_m3 REAL,
            emision_cemento REAL,
            emision_agregados REAL,
            emision_aditivos REAL,
            emision_total REAL,
            fecha_migracion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Crear índices
    cursor.execute("CREATE INDEX idx_remitos_co2_origen ON remitos_co2(origen)")
    cursor.execute("CREATE INDEX idx_remitos_co2_resistencia ON remitos_co2(resistencia_mpa)")
    cursor.execute("CREATE INDEX idx_remitos_co2_co2 ON remitos_co2(co2_kg_m3)")

    pg_conn.commit()
    print("✅ Tabla remitos_co2 creada en PostgreSQL")


def extraer_datos(sqlite_path, query, origen, empresa, pais):
    """Extraer datos de una base SQLite"""
    try:
        conn = sqlite3.connect(sqlite_path)
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Agregar columnas de origen
        df['origen'] = origen
        df['empresa'] = empresa
        df['pais'] = pais

        print(f"  📊 {origen}: {len(df):,} registros extraídos")
        return df
    except Exception as e:
        print(f"  ❌ Error en {origen}: {e}")
        return pd.DataFrame()


def cargar_datos(pg_conn, df):
    """Cargar DataFrame en PostgreSQL"""
    if df.empty:
        return 0

    cursor = pg_conn.cursor()

    # Preparar datos
    columnas = ['id_remito', 'origen', 'empresa', 'pais', 'fecha', 'planta',
                'producto', 'resistencia_mpa', 'volumen', 'co2_kg_m3',
                'emision_cemento', 'emision_agregados', 'emision_aditivos', 'emision_total']

    # Asegurar que todas las columnas existan
    for col in columnas:
        if col not in df.columns:
            df[col] = None

    # Insertar datos
    insert_query = """
        INSERT INTO remitos_co2
        (id_remito, origen, empresa, pais, fecha, planta, producto,
         resistencia_mpa, volumen, co2_kg_m3, emision_cemento,
         emision_agregados, emision_aditivos, emision_total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    registros = 0
    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (
                row['id_remito'],
                row['origen'],
                row['empresa'],
                row['pais'],
                row['fecha'],
                row['planta'],
                row['producto'],
                row['resistencia_mpa'],
                row['volumen'],
                row['co2_kg_m3'],
                row.get('emision_cemento'),
                row.get('emision_agregados'),
                row.get('emision_aditivos'),
                row.get('emision_total')
            ))
            registros += 1
        except Exception as e:
            pass  # Ignorar errores individuales

    pg_conn.commit()
    return registros


def main():
    print("=" * 60)
    print("ETL: Migrar Remitos con Resistencia y Huella CO₂")
    print("=" * 60)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Conectar a PostgreSQL
    print("🔌 Conectando a PostgreSQL...")
    pg_conn = psycopg2.connect(dbname=PG_DATABASE)

    # Crear tabla destino
    crear_tabla_destino(pg_conn)

    # Extraer y cargar datos de cada origen
    print("\n📥 Extrayendo datos de bases SQLite...")

    total_registros = 0

    # PACAS
    df_pacas = extraer_datos(
        SQLITE_DATABASES['pacas']['path'],
        QUERY_PACAS,
        'pacas',
        SQLITE_DATABASES['pacas']['empresa'],
        SQLITE_DATABASES['pacas']['pais']
    )
    registros = cargar_datos(pg_conn, df_pacas)
    total_registros += registros
    print(f"  ✅ PACAS: {registros:,} registros cargados")

    # MZMA
    df_mzma = extraer_datos(
        SQLITE_DATABASES['mzma']['path'],
        QUERY_MZMA,
        'mzma',
        SQLITE_DATABASES['mzma']['empresa'],
        SQLITE_DATABASES['mzma']['pais']
    )
    registros = cargar_datos(pg_conn, df_mzma)
    total_registros += registros
    print(f"  ✅ MZMA: {registros:,} registros cargados")

    # Melón
    df_melon = extraer_datos(
        SQLITE_DATABASES['melon']['path'],
        QUERY_MELON,
        'melon',
        SQLITE_DATABASES['melon']['empresa'],
        SQLITE_DATABASES['melon']['pais']
    )
    registros = cargar_datos(pg_conn, df_melon)
    total_registros += registros
    print(f"  ✅ Melón: {registros:,} registros cargados")

    # Lomax
    df_lomax = extraer_datos(
        SQLITE_DATABASES['lomax']['path'],
        QUERY_LOMAX,
        'lomax',
        SQLITE_DATABASES['lomax']['empresa'],
        SQLITE_DATABASES['lomax']['pais']
    )
    registros = cargar_datos(pg_conn, df_lomax)
    total_registros += registros
    print(f"  ✅ Lomax: {registros:,} registros cargados")

    # Estadísticas finales
    cursor = pg_conn.cursor()
    cursor.execute("""
        SELECT
            origen,
            COUNT(*) as registros,
            ROUND(AVG(resistencia_mpa)::numeric, 1) as avg_resistencia,
            ROUND(AVG(co2_kg_m3)::numeric, 1) as avg_co2
        FROM remitos_co2
        GROUP BY origen
        ORDER BY registros DESC
    """)
    stats = cursor.fetchall()

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE MIGRACIÓN")
    print("=" * 60)
    print(f"\n{'Origen':<10} {'Registros':>12} {'Avg REST (MPa)':>15} {'Avg CO₂ (kg/m³)':>17}")
    print("-" * 60)
    for row in stats:
        print(f"{row[0]:<10} {row[1]:>12,} {row[2]:>15} {row[3]:>17}")
    print("-" * 60)
    print(f"{'TOTAL':<10} {total_registros:>12,}")

    # Cerrar conexión
    pg_conn.close()

    print(f"\n✅ Migración completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Datos en: PostgreSQL latam4c_db.remitos_co2")


if __name__ == '__main__':
    main()
