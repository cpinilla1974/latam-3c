#!/usr/bin/env python3
"""
ETL: Actualizar factor clinker y coprocesamiento
Extrae datos de corp_cemento_concreto y actualiza tabla remitos
"""

import sqlite3
import psycopg2
import pandas as pd
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

SQLITE_DATABASES = {
    'pacas': '/home/cpinilla/pacas-3c/data/main.db',
    'mzma': '/home/cpinilla/databases/mzma-3c/data/main.db',
    'melon': '/home/cpinilla/databases/melon-3c/data/old/main - copia.db',
    'lomax': '/home/cpinilla/projects/lomax-3c/streamlit/data/main.db'
}

PG_DATABASE = 'latam4c_db'

# ============================================================
# EXTRACCIÓN
# ============================================================

def extraer_datos_cemento(origen, db_path):
    """Extrae factor clinker y coprocesamiento por remito"""
    print(f"\n📥 Extrayendo datos de {origen.upper()}...")

    conn = sqlite3.connect(db_path)

    # Agregar por remito (promedio ponderado por cantidad de cemento)
    query = """
    SELECT
        codigo_dataset,
        SUM(cantidad_cemento_kg) as contenido_cemento,
        SUM(fk_cemento * cantidad_cemento_kg) / SUM(cantidad_cemento_kg) as factor_clinker,
        SUM(porc_alternativos * cantidad_cemento_kg) / SUM(cantidad_cemento_kg) as coprocesamiento
    FROM corp_cemento_concreto
    WHERE tipo_dato = 'CONCRETO'
        AND cantidad_cemento_kg > 0
    GROUP BY codigo_dataset
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convertir coprocesamiento a fracción (está en porcentaje)
    df['coprocesamiento'] = df['coprocesamiento'] / 100.0

    print(f"  📊 {len(df):,} remitos con datos de cemento")
    print(f"  ✅ Factor clinker promedio: {df['factor_clinker'].mean():.3f}")
    print(f"  ✅ Coprocesamiento promedio: {df['coprocesamiento'].mean()*100:.1f}%")
    print(f"  ✅ Contenido cemento promedio: {df['contenido_cemento'].mean():.1f} kg/m³")

    return df

# ============================================================
# CARGA
# ============================================================

def actualizar_remitos(pg_conn, origen, df_cemento):
    """Actualiza campos de factor clinker y coprocesamiento"""
    cursor = pg_conn.cursor()

    print(f"\n🔄 Actualizando remitos de {origen.upper()}...")

    actualizados = 0

    for _, row in df_cemento.iterrows():
        cursor.execute("""
            UPDATE remitos
            SET
                contenido_cemento = %s,
                factor_clinker = %s,
                coprocesamiento = %s
            WHERE origen = %s
                AND id_remito = %s
        """, (
            float(row['contenido_cemento']),
            float(row['factor_clinker']),
            float(row['coprocesamiento']),
            origen,
            row['codigo_dataset']
        ))

        actualizados += cursor.rowcount

    pg_conn.commit()

    print(f"  ✅ {actualizados:,} remitos actualizados")

    return actualizados

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("ETL: Actualizar Factor Clinker y Coprocesamiento")
    print("=" * 80)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Conectar a PostgreSQL
    print("\n🔌 Conectando a PostgreSQL...")
    pg_conn = psycopg2.connect(dbname=PG_DATABASE)

    # Procesar cada origen
    total_actualizados = 0

    for origen, db_path in SQLITE_DATABASES.items():
        try:
            df_cemento = extraer_datos_cemento(origen, db_path)
            actualizados = actualizar_remitos(pg_conn, origen, df_cemento)
            total_actualizados += actualizados
        except Exception as e:
            print(f"  ❌ Error procesando {origen}: {e}")
            continue

    # Estadísticas finales
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE ACTUALIZACIÓN")
    print("=" * 80)

    cursor = pg_conn.cursor()

    # Estadísticas por origen
    cursor.execute("""
        SELECT
            origen,
            COUNT(*) as total,
            COUNT(factor_clinker) as con_fk,
            AVG(factor_clinker) as fk_prom,
            AVG(coprocesamiento) as copro_prom,
            AVG(contenido_cemento) as cem_prom
        FROM remitos
        GROUP BY origen
        ORDER BY total DESC;
    """)

    print(f"\n{'Origen':<10} {'Total':>10} {'Con FK':>10} {'FK Prom':>10} {'Copro %':>10} {'Cem kg/m³':>12}")
    print("-" * 80)

    for row in cursor.fetchall():
        origen = row[0]
        total = row[1]
        con_fk = row[2] or 0
        fk_prom = row[3] or 0
        copro_prom = (row[4] or 0) * 100
        cem_prom = row[5] or 0

        print(f"{origen:<10} {total:>10,} {con_fk:>10,} {fk_prom:>10.3f} {copro_prom:>9.1f}% {cem_prom:>11.1f}")

    print("-" * 80)
    print(f"{'TOTAL':<10} {total_actualizados:>10,}")

    # Cerrar conexión
    pg_conn.close()

    print(f"\n✅ Actualización completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total remitos actualizados: {total_actualizados:,}")

if __name__ == '__main__':
    main()
