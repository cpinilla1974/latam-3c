#!/usr/bin/env python3
"""
Analiza qué campos de la tabla remitos están vacíos o con valores NULL
"""

import psycopg2
import pandas as pd

PG_DATABASE = 'latam4c_db'

def analizar_campos_vacios():
    print("=" * 80)
    print("ANÁLISIS DE CAMPOS VACÍOS EN TABLA REMITOS")
    print("=" * 80)

    conn = psycopg2.connect(dbname=PG_DATABASE)
    cursor = conn.cursor()

    # Obtener estructura de la tabla
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'remitos'
            AND table_schema = 'public'
        ORDER BY ordinal_position;
    """)

    columnas = cursor.fetchall()

    print("\n📊 ANÁLISIS POR COLUMNA")
    print("-" * 80)
    print(f"{'Campo':<25} {'Tipo':<15} {'Total':>10} {'Nulls':>10} {'% Null':>8} {'Status'}")
    print("-" * 80)

    # Analizar cada columna
    cursor.execute("SELECT COUNT(*) FROM remitos")
    total_registros = cursor.fetchone()[0]

    campos_vacios = []
    campos_parciales = []
    campos_completos = []

    for col_name, data_type, is_nullable in columnas:
        # Contar NULLs
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM remitos
            WHERE {col_name} IS NULL
        """)
        num_nulls = cursor.fetchone()[0]
        pct_null = (num_nulls / total_registros * 100) if total_registros > 0 else 0

        # Clasificar
        if num_nulls == total_registros:
            status = "❌ VACÍO"
            campos_vacios.append(col_name)
        elif num_nulls > total_registros * 0.5:
            status = "⚠️  MAYORMENTE VACÍO"
            campos_parciales.append(col_name)
        elif num_nulls > 0:
            status = "⚡ PARCIAL"
            campos_parciales.append(col_name)
        else:
            status = "✅ COMPLETO"
            campos_completos.append(col_name)

        print(f"{col_name:<25} {data_type:<15} {total_registros:>10,} {num_nulls:>10,} {pct_null:>7.1f}% {status}")

    # Resumen
    print("\n" + "=" * 80)
    print("📋 RESUMEN")
    print("=" * 80)

    print(f"\n✅ Campos completamente llenos ({len(campos_completos)}):")
    for campo in campos_completos:
        print(f"   - {campo}")

    print(f"\n⚡ Campos parcialmente llenos ({len(campos_parciales)}):")
    for campo in campos_parciales:
        cursor.execute(f"SELECT COUNT(*) FROM remitos WHERE {campo} IS NOT NULL")
        llenos = cursor.fetchone()[0]
        pct_lleno = (llenos / total_registros * 100) if total_registros > 0 else 0
        print(f"   - {campo}: {llenos:,} registros ({pct_lleno:.1f}%)")

    print(f"\n❌ Campos completamente vacíos ({len(campos_vacios)}):")
    for campo in campos_vacios:
        print(f"   - {campo}")

    # Análisis por origen
    print("\n" + "=" * 80)
    print("📊 COMPLETITUD POR ORIGEN")
    print("=" * 80)

    cursor.execute("""
        SELECT
            origen,
            COUNT(*) as total,
            COUNT(resistencia_mpa) as con_resistencia,
            COUNT(co2_kg_m3) as con_co2,
            COUNT(planta) as con_planta,
            COUNT(producto) as con_producto,
            COUNT(formulacion) as con_formulacion,
            COUNT(slump) as con_slump,
            COUNT(tipo_cemento) as con_tipo_cemento,
            COUNT(contenido_cemento) as con_contenido_cemento,
            COUNT(proyecto) as con_proyecto,
            COUNT(cliente) as con_cliente
        FROM remitos
        GROUP BY origen
        ORDER BY total DESC;
    """)

    print(f"\n{'Origen':<10} {'Total':>10} {'REST':>8} {'CO2':>8} {'Planta':>8} {'Prod':>8} {'Form':>8} {'Slump':>8}")
    print("-" * 80)

    for row in cursor.fetchall():
        origen = row[0]
        total = row[1]
        print(f"{origen:<10} {total:>10,} {row[2]/total*100:>7.1f}% {row[3]/total*100:>7.1f}% "
              f"{row[4]/total*100:>7.1f}% {row[5]/total*100:>7.1f}% {row[6]/total*100:>7.1f}% {row[7]/total*100:>7.1f}%")

    conn.close()

    print("\n✅ Análisis completado\n")

if __name__ == '__main__':
    analizar_campos_vacios()
