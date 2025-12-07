#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL: Migrar remitos a estructura unificada
Extrae datos de PACAS, MZMA, Melón y Lomax a tabla remitos
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from datetime import datetime
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

SQLITE_DATABASES = {
    'pacas': {
        'path': '/home/cpinilla/pacas-3c/data/main.db',
        'empresa': 'Cementos del Pacífico',
        'pais': 'PER'
    },
    'mzma': {
        'path': '/home/cpinilla/databases/mzma-3c/data/main.db',
        'empresa': 'Cementos Moctezuma',
        'pais': 'MEX'
    },
    'melon': {
        'path': '/home/cpinilla/databases/melon-3c/data/old/main - copia.db',
        'empresa': 'Cementos Melón',
        'pais': 'CHL'
    },
    'lomax': {
        'path': '/home/cpinilla/projects/lomax-3c/streamlit/data/main.db',
        'empresa': 'Lomax',
        'pais': 'ARG'
    }
}

PG_DATABASE = 'latam4c_db'
LOG_DIR = 'scripts/etl/logs'

# ============================================================
# LOGGING
# ============================================================

class ETLLogger:
    def __init__(self, script_name):
        self.script_name = script_name
        self.start_time = datetime.now()
        self.logs = []

        # Crear directorio de logs si no existe
        os.makedirs(LOG_DIR, exist_ok=True)

        # Nombre del archivo de log
        timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
        self.log_file = f"{LOG_DIR}/{script_name}_{timestamp}.log"

        self.log("=" * 80)
        self.log(f"Script: {script_name}")
        self.log(f"Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 80)

    def log(self, message, print_console=True):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)

        if print_console:
            print(message)

        # Escribir al archivo
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

    def log_step(self, step_name, found=None, imported=None):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        msg = f"\n{'='*80}\n"
        msg += f"PASO: {step_name}\n"
        msg += f"Tiempo transcurrido: {elapsed:.1f}s\n"
        if found is not None:
            msg += f"Registros encontrados: {found:,}\n"
        if imported is not None:
            msg += f"Registros importados: {imported:,}\n"
        msg += f"{'='*80}"
        self.log(msg)

    def finalize(self, total_records=None):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        self.log("\n" + "=" * 80)
        self.log("RESUMEN FINAL")
        self.log("=" * 80)
        self.log(f"Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Fin: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Duración total: {duration:.1f}s ({duration/60:.1f} min)")
        if total_records:
            self.log(f"Total registros procesados: {total_records:,}")
        self.log(f"Archivo de log: {self.log_file}")
        self.log("=" * 80)

        return self.log_file

# ============================================================
# EXTRACCIÓN
# ============================================================

def extraer_mzma(origen, db_config):
    """Extrae remitos de MZMA"""
    conn = sqlite3.connect(db_config['path'])

    query = """
    SELECT
        c.codigo_dataset as id_remito,
        c.fecha,
        c.planta_concretera as planta,
        c.nombre_concreto as producto,
        c.volumen,
        co2.co2_kg_m3,
        co2.co2_total,
        a.REST as resistencia_raw,
        (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
         FROM corp_cemento_concreto
         WHERE codigo_dataset = c.codigo_dataset AND volumen > 0) as contenido_cemento
    FROM corp_concretos c
    JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
    LEFT JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Procesar resistencia (México: dividir por 10.2)
    df['resistencia_mpa'] = pd.to_numeric(df['resistencia_raw'], errors='coerce') / 10.2

    # Extraer año y mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    # Agregar metadata
    df['origen'] = origen
    df['empresa'] = db_config['empresa']
    df['pais'] = db_config['pais']

    # Limpiar columnas innecesarias
    df = df.drop(columns=['resistencia_raw'])

    print(f"  📊 {origen.upper()}: {len(df):,} remitos extraídos")
    return df


def extraer_melon(origen, db_config):
    """Extrae remitos de Melón"""
    conn = sqlite3.connect(db_config['path'])

    query = """
    SELECT
        r.codigo_dataset as id_remito,
        r.fecha,
        pl.planta,
        p.producto,
        r.volumen,
        co2.co2_kg_m3,
        co2.co2_total,
        a.REST as resistencia_raw,
        (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
         FROM corp_cemento_concreto
         WHERE codigo_dataset = r.codigo_dataset AND volumen > 0) as contenido_cemento
    FROM tb_remitos r
    JOIN tb_producto p ON r.id_producto = p.id_producto
    JOIN tb_planta pl ON r.id_planta = pl.id_planta
    JOIN corp_co2 co2 ON r.codigo_dataset = co2.codigo_dataset
    LEFT JOIN tb_atributos_concretos a ON p.producto = a.nombre_concreto
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Procesar resistencia (Chile: dividir por 10.2 - están en kg/cm²)
    df['resistencia_mpa'] = pd.to_numeric(df['resistencia_raw'], errors='coerce') / 10.2

    # Extraer año y mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    # Agregar metadata
    df['origen'] = origen
    df['empresa'] = db_config['empresa']
    df['pais'] = db_config['pais']

    # Limpiar columnas innecesarias
    df = df.drop(columns=['resistencia_raw'])

    print(f"  📊 {origen.upper()}: {len(df):,} remitos extraídos")
    return df


def extraer_lomax(origen, db_config):
    """Extrae remitos de Lomax"""
    conn = sqlite3.connect(db_config['path'])

    query = """
    SELECT
        c.codigo_dataset as id_remito,
        c.fecha,
        c.planta_concretera as planta,
        c.nombre_concreto as producto,
        c.volumen,
        co2.co2_kg_m3,
        co2.co2_total,
        a.REST as resistencia_raw,
        (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
         FROM corp_cemento_concreto
         WHERE codigo_dataset = c.codigo_dataset AND volumen > 0) as contenido_cemento
    FROM corp_concretos c
    JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
    LEFT JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Procesar resistencia (Argentina: directo)
    df['resistencia_mpa'] = pd.to_numeric(df['resistencia_raw'], errors='coerce')

    # Extraer año y mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    # Agregar metadata
    df['origen'] = origen
    df['empresa'] = db_config['empresa']
    df['pais'] = db_config['pais']

    # Limpiar columnas innecesarias
    df = df.drop(columns=['resistencia_raw'])

    print(f"  📊 {origen.upper()}: {len(df):,} remitos extraídos")
    return df


def extraer_pacas(origen, db_config):
    """Extrae remitos de PACAS con estructura diferente"""
    conn = sqlite3.connect(db_config['path'])

    query = """
    SELECT
        r.anio_planta_remito as id_remito,
        r.fecha,
        r.planta,
        r.formula as producto,
        r.volumen,
        r.huella as co2_kg_m3,
        r.emision_total as co2_total,
        a.resistencia_mpa
    FROM co2_remitos r
    LEFT JOIN tb_atributos_concreto a ON r.formula = a.producto
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Extraer año y mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    # Agregar metadata
    df['origen'] = origen
    df['empresa'] = db_config['empresa']
    df['pais'] = db_config['pais']

    print(f"  📊 {origen.upper()}: {len(df):,} remitos extraídos")
    return df


# ============================================================
# CARGA A POSTGRESQL
# ============================================================

def limpiar_tabla(pg_conn):
    """Limpia tabla remitos"""
    cursor = pg_conn.cursor()
    cursor.execute("TRUNCATE TABLE remitos CASCADE")
    pg_conn.commit()
    print("  ✅ Tabla remitos limpiada")


def cargar_remitos(pg_conn, df_remitos):
    """Carga remitos a tabla principal usando batch insert"""
    cursor = pg_conn.cursor()

    # Preparar datos en formato de tuplas
    valores = []
    for _, row in df_remitos.iterrows():
        trimestre = ((row['mes'] - 1) // 3 + 1) if pd.notna(row['mes']) else None

        # Función auxiliar para convertir NaN a None
        def nan_to_none(val):
            return None if pd.isna(val) else val

        valores.append((
            row['id_remito'],
            row['origen'],
            row['empresa'],
            row['pais'],
            row['fecha'],
            row['año'],
            row['mes'],
            trimestre,
            nan_to_none(row.get('planta')),
            nan_to_none(row.get('producto')),
            nan_to_none(row.get('formulacion')),
            nan_to_none(row['resistencia_mpa']),
            nan_to_none(row['volumen']),
            nan_to_none(row.get('slump')),
            nan_to_none(row.get('tipo_cemento')),
            nan_to_none(row.get('contenido_cemento')),
            nan_to_none(row.get('proyecto')),
            nan_to_none(row.get('cliente')),
            nan_to_none(row.get('co2_total')),
            nan_to_none(row.get('co2_kg_m3'))
        ))

    # Ejecutar batch insert
    insert_query = """
        INSERT INTO remitos (
            id_remito, origen, empresa, pais, fecha, año, mes, trimestre,
            planta, producto, formulacion, resistencia_mpa, volumen, slump,
            tipo_cemento, contenido_cemento, proyecto, cliente,
            co2_total, co2_kg_m3
        ) VALUES %s
        ON CONFLICT (origen, id_remito) DO NOTHING
    """

    execute_values(cursor, insert_query, valores, page_size=1000)
    pg_conn.commit()

    print(f"  ✅ {len(valores):,} remitos cargados")
    return len(valores)


# ============================================================
# MAIN
# ============================================================

def main():
    # Inicializar logger
    logger = ETLLogger('08_migrar_remitos')

    logger.log("=" * 80)
    logger.log("ETL: Migrar Remitos a Estructura Unificada")
    logger.log("=" * 80)

    # Conectar a PostgreSQL
    logger.log("\n🔌 Conectando a PostgreSQL...")
    pg_conn = psycopg2.connect(dbname=PG_DATABASE)
    logger.log("  ✅ Conexión establecida")

    # Limpiar tabla
    logger.log("\n🧹 Limpiando tabla destino...")
    limpiar_tabla(pg_conn)

    # Procesar cada origen
    logger.log("\n📥 Extrayendo y cargando datos...")
    total_remitos = 0

    # MZMA
    logger.log_step("Extracción MZMA - Iniciando")
    df = extraer_mzma('mzma', SQLITE_DATABASES['mzma'])
    found = len(df)
    imported = cargar_remitos(pg_conn, df)
    total_remitos += imported
    logger.log_step("Extracción MZMA - Completado", found=found, imported=imported)

    # Melón
    logger.log_step("Extracción Melón - Iniciando")
    df = extraer_melon('melon', SQLITE_DATABASES['melon'])
    found = len(df)
    imported = cargar_remitos(pg_conn, df)
    total_remitos += imported
    logger.log_step("Extracción Melón - Completado", found=found, imported=imported)

    # Lomax
    logger.log_step("Extracción Lomax - Iniciando")
    df = extraer_lomax('lomax', SQLITE_DATABASES['lomax'])
    found = len(df)
    imported = cargar_remitos(pg_conn, df)
    total_remitos += imported
    logger.log_step("Extracción Lomax - Completado", found=found, imported=imported)

    # PACAS
    logger.log_step("Extracción PACAS - Iniciando")
    df = extraer_pacas('pacas', SQLITE_DATABASES['pacas'])
    found = len(df)
    imported = cargar_remitos(pg_conn, df)
    total_remitos += imported
    logger.log_step("Extracción PACAS - Completado", found=found, imported=imported)

    # Estadísticas finales
    logger.log("\n" + "=" * 80)
    logger.log("📊 RESUMEN DE MIGRACIÓN")
    logger.log("=" * 80)

    cursor = pg_conn.cursor()
    cursor.execute("""
        SELECT
            origen,
            COUNT(*) as num_remitos,
            ROUND(AVG(resistencia_mpa)::numeric, 1) as avg_resistencia,
            ROUND(AVG(co2_kg_m3)::numeric, 1) as avg_co2
        FROM remitos
        GROUP BY origen
        ORDER BY num_remitos DESC
    """)

    stats = cursor.fetchall()
    logger.log(f"\n{'Origen':<10} {'Remitos':>12} {'Avg REST (MPa)':>15} {'Avg CO₂ (kg/m³)':>17}")
    logger.log("-" * 80)
    for row in stats:
        avg_rest = row[2] if row[2] else 'N/A'
        logger.log(f"{row[0]:<10} {row[1]:>12,} {str(avg_rest):>15} {row[3]:>17}")
    logger.log("-" * 80)
    logger.log(f"{'TOTAL':<10} {total_remitos:>12,}")

    # Refrescar vistas materializadas
    logger.log("\n🔄 Refrescando vistas materializadas...")
    cursor.execute("SELECT refresh_dashboard_views();")
    pg_conn.commit()
    logger.log("  ✅ Vistas materializadas actualizadas")

    # Cerrar conexión
    pg_conn.close()

    logger.log(f"\n✅ Migración completada")
    logger.log(f"📍 Datos en: PostgreSQL {PG_DATABASE}.remitos")
    logger.log(f"📊 Vistas materializadas: mv_resumen_por_origen, mv_evolucion_temporal, mv_top_plantas, mv_distribucion_resistencia")

    # Finalizar logging
    log_file = logger.finalize(total_records=total_remitos)
    print(f"\n📄 Log guardado en: {log_file}")


if __name__ == '__main__':
    main()
