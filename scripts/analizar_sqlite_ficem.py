#!/usr/bin/env python3
"""
Script para analizar la base de datos SQLite ficem_bd.db
"""

import sqlite3
import sys
from datetime import datetime


def format_number(num):
    """Formatear números con separadores de miles"""
    return f"{num:,}".replace(",", ".")


def analyze_sqlite_database(db_path):
    """Analizar base de datos SQLite"""

    print("\n" + "="*80)
    print("ANÁLISIS DE INTEGRIDAD - BASE DE DATOS FICEM_BD (SQLite)")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Archivo: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"\n✓ Conexión exitosa a la base de datos SQLite")
    except Exception as e:
        print(f"\n✗ Error conectando: {e}")
        return 1

    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\n{'='*80}")
    print(f"TABLAS ENCONTRADAS: {len(tables)}")
    print(f"{'='*80}")

    # Primero mostrar conteos de todas las tablas
    table_counts = {}
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        table_counts[table] = count
        print(f"  • {table:<40} {format_number(count):>15} registros")

    # Buscar tabla de remitos (probablemente la más grande)
    remitos_table = None
    max_count = 0
    for table, count in table_counts.items():
        if count > max_count and 'remit' in table.lower():
            remitos_table = table
            max_count = count

    # Si no hay tabla con "remit", usar la más grande
    if not remitos_table:
        remitos_table = max(table_counts.items(), key=lambda x: x[1])[0]

    print(f"\n{'='*80}")
    print(f"TABLA PRINCIPAL IDENTIFICADA: {remitos_table}")
    print(f"Total de registros: {format_number(table_counts[remitos_table])}")
    print(f"{'='*80}")

    # Analizar estructura de la tabla principal
    cursor.execute(f"PRAGMA table_info({remitos_table})")
    columns = cursor.fetchall()

    print(f"\nESTRUCTURA ({len(columns)} columnas):")
    print(f"{'-'*80}")
    print(f"{'Columna':<30} {'Tipo':<20} {'Not Null':<10}")
    print(f"{'-'*80}")

    for col in columns:
        col_name = col[1]
        col_type = col[2]
        not_null = "NOT NULL" if col[3] else "NULL"
        print(f"{col_name:<30} {col_type:<20} {not_null}")

    # Analizar completitud
    print(f"\n{'='*80}")
    print(f"COMPLETITUD POR COLUMNA")
    print(f"{'='*80}")
    print(f"{'Columna':<30} {'Registros':<15} {'NULLs':<15} {'% Completo':<15}")
    print(f"{'-'*80}")

    total_records = table_counts[remitos_table]
    null_stats = []

    for col in columns:
        col_name = col[1]

        # Contar valores no nulos
        cursor.execute(f"""
            SELECT
                COUNT(*) as total,
                COUNT({col_name}) as non_nulls
            FROM {remitos_table}
        """)
        result = cursor.fetchone()
        total = result[0]
        non_nulls = result[1]
        nulls = total - non_nulls

        pct_complete = (non_nulls / total * 100) if total > 0 else 0

        null_stats.append({
            'columna': col_name,
            'non_nulls': non_nulls,
            'nulls': nulls,
            'pct_complete': pct_complete
        })

        # Marcar columnas con problemas
        flag = ""
        if pct_complete < 50:
            flag = " ⚠️  CRÍTICO"
        elif pct_complete < 90:
            flag = " ⚠️  BAJO"

        print(f"{col_name:<30} {format_number(non_nulls):<15} {format_number(nulls):<15} {pct_complete:>6.2f}%{flag}")

    # Resumen de columnas problemáticas
    null_stats.sort(key=lambda x: x['pct_complete'])
    problematic = [stat for stat in null_stats if stat['pct_complete'] < 90]

    if problematic:
        print(f"\n{'='*80}")
        print(f"COLUMNAS CON BAJA COMPLETITUD (<90%):")
        print(f"{'='*80}")
        for stat in problematic:
            print(f"  • {stat['columna']:<30} {stat['pct_complete']:>6.2f}% completo ({format_number(stat['nulls'])} NULLs)")

    # Analizar valores categóricos clave
    print(f"\n{'='*80}")
    print(f"DISTRIBUCIONES DE VALORES CLAVE")
    print(f"{'='*80}")

    # Identificar columnas categóricas comunes
    categorical_columns = []
    for col in columns:
        col_name = col[1].lower()
        if any(keyword in col_name for keyword in ['origen', 'company', 'empresa', 'planta', 'plant', 'año', 'year', 'pais', 'country']):
            categorical_columns.append(col[1])

    for cat_col in categorical_columns[:5]:  # Limitar a 5 primeras
        print(f"\n{'DISTRIBUCIÓN: ' + cat_col:^80}")
        print(f"{'-'*80}")

        cursor.execute(f"""
            SELECT
                {cat_col},
                COUNT(*) as count,
                ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM {remitos_table}), 2) as percentage
            FROM {remitos_table}
            WHERE {cat_col} IS NOT NULL
            GROUP BY {cat_col}
            ORDER BY count DESC
            LIMIT 15
        """)

        results = cursor.fetchall()
        print(f"{'Valor':<40} {'Registros':<15} {'%':<10}")
        print(f"{'-'*80}")

        for row in results:
            value = str(row[0])[:40] if row[0] else "(vacío)"
            count = row[1]
            pct = row[2]
            print(f"{value:<40} {format_number(count):<15} {pct:>6.2f}%")

    # Analizar rangos numéricos
    print(f"\n{'='*80}")
    print(f"RANGOS DE VALORES NUMÉRICOS")
    print(f"{'='*80}")

    numeric_columns = []
    for col in columns:
        col_type = col[2].upper()
        if any(t in col_type for t in ['INT', 'REAL', 'NUMERIC', 'FLOAT', 'DOUBLE']):
            numeric_columns.append(col[1])

    if numeric_columns:
        print(f"{'Columna':<30} {'Min':<15} {'Max':<15} {'Promedio':<15}")
        print(f"{'-'*80}")

        for num_col in numeric_columns[:10]:  # Limitar a 10
            try:
                cursor.execute(f"""
                    SELECT
                        MIN({num_col}) as min_val,
                        MAX({num_col}) as max_val,
                        AVG({num_col}) as avg_val
                    FROM {remitos_table}
                    WHERE {num_col} IS NOT NULL
                """)
                result = cursor.fetchone()

                if result and result[0] is not None:
                    min_val = result[0]
                    max_val = result[1]
                    avg_val = result[2]
                    print(f"{num_col:<30} {min_val:<15.2f} {max_val:<15.2f} {avg_val:<15.2f}")
            except Exception as e:
                print(f"{num_col:<30} Error: {str(e)[:40]}")

    # Resumen final
    print(f"\n{'='*80}")
    print(f"RESUMEN GENERAL")
    print(f"{'='*80}")

    print(f"\n✓ Total de tablas en la base de datos: {len(tables)}")
    print(f"✓ Tabla principal: {remitos_table}")
    print(f"✓ Total de registros en tabla principal: {format_number(total_records)}")
    print(f"✓ Total de columnas: {len(columns)}")
    print(f"✓ Columnas con baja completitud (<90%): {len(problematic)}")

    # Distribuciones clave
    for cat_col in ['origen', 'company', 'empresa', 'planta']:
        for col in columns:
            if col[1].lower() == cat_col.lower():
                cursor.execute(f"SELECT COUNT(DISTINCT {col[1]}) FROM {remitos_table} WHERE {col[1]} IS NOT NULL")
                distinct_count = cursor.fetchone()[0]
                print(f"✓ Valores distintos en '{col[1]}': {distinct_count}")
                break

    print(f"\n{'='*80}")
    print("ANÁLISIS COMPLETADO")
    print(f"{'='*80}\n")

    conn.close()
    return 0


if __name__ == '__main__':
    db_path = '/home/cpinilla/databases/ficem_bd/data/ficem_bd.db'
    sys.exit(analyze_sqlite_database(db_path))
