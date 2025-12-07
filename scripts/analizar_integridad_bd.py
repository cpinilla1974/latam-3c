#!/usr/bin/env python3
"""
Script para analizar la integridad y completitud de la base de datos PostgreSQL
del proyecto latam-3c
"""

import sys
import os
from pathlib import Path

# Agregar el directorio v1 al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / 'v1'))

from database.models import get_engine
import pandas as pd
from sqlalchemy import inspect, text
from datetime import datetime


def format_number(num):
    """Formatear números con separadores de miles"""
    return f"{num:,}".replace(",", ".")


def analyze_table_structure(engine, table_name):
    """Analizar la estructura de una tabla"""
    inspector = inspect(engine)

    if table_name not in inspector.get_table_names():
        return None

    columns = inspector.get_columns(table_name)

    print(f"\n{'='*80}")
    print(f"TABLA: {table_name}")
    print(f"{'='*80}")
    print(f"\nESTRUCTURA ({len(columns)} columnas):")
    print(f"{'-'*80}")

    for col in columns:
        col_type = str(col['type'])
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        print(f"  {col['name']:<30} {col_type:<20} {nullable}")

    return columns


def analyze_table_data(engine, table_name, columns):
    """Analizar datos de una tabla"""

    # Obtener total de registros
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) as total FROM {table_name}"))
        total_records = result.fetchone()[0]

    print(f"\n{'='*80}")
    print(f"DATOS DE LA TABLA: {table_name}")
    print(f"{'='*80}")
    print(f"Total de registros: {format_number(total_records)}")

    if total_records == 0:
        print("⚠️  La tabla está vacía")
        return

    # Analizar completitud por columna
    print(f"\n{'COMPLETITUD POR COLUMNA':^80}")
    print(f"{'-'*80}")
    print(f"{'Columna':<30} {'Registros':<15} {'NULLs':<15} {'% Completo':<15}")
    print(f"{'-'*80}")

    null_stats = []

    with engine.connect() as conn:
        for col in columns:
            col_name = col['name']

            # Escapar nombre de columna con comillas dobles para casos sensibles
            col_name_quoted = f'"{col_name}"'

            # Contar valores no nulos
            query = text(f"""
                SELECT
                    COUNT(*) - COUNT({col_name_quoted}) as nulls,
                    COUNT({col_name_quoted}) as non_nulls
                FROM {table_name}
            """)
            result = conn.execute(query)
            row = result.fetchone()
            nulls = row[0]
            non_nulls = row[1]

            pct_complete = (non_nulls / total_records * 100) if total_records > 0 else 0

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

    # Ordenar por % completo ascendente para resaltar problemas
    null_stats.sort(key=lambda x: x['pct_complete'])

    # Resumen de columnas problemáticas
    problematic = [stat for stat in null_stats if stat['pct_complete'] < 90]
    if problematic:
        print(f"\n{'COLUMNAS CON BAJA COMPLETITUD (<90%):':^80}")
        print(f"{'-'*80}")
        for stat in problematic:
            print(f"  • {stat['columna']:<30} {stat['pct_complete']:>6.2f}% completo")

    return null_stats


def analyze_numeric_ranges(engine, table_name, columns):
    """Analizar rangos de valores numéricos"""
    numeric_cols = [col for col in columns if 'FLOAT' in str(col['type']) or 'INTEGER' in str(col['type'])]

    if not numeric_cols:
        return

    print(f"\n{'RANGOS DE VALORES NUMÉRICOS':^80}")
    print(f"{'-'*80}")
    print(f"{'Columna':<30} {'Min':<15} {'Max':<15} {'Promedio':<15}")
    print(f"{'-'*80}")

    with engine.connect() as conn:
        for col in numeric_cols:
            col_name = col['name']
            col_name_quoted = f'"{col_name}"'

            try:
                query = text(f"""
                    SELECT
                        MIN({col_name_quoted}) as min_val,
                        MAX({col_name_quoted}) as max_val,
                        AVG({col_name_quoted}) as avg_val
                    FROM {table_name}
                    WHERE {col_name_quoted} IS NOT NULL
                """)
                result = conn.execute(query)
                row = result.fetchone()

                if row and row[0] is not None:
                    min_val = row[0]
                    max_val = row[1]
                    avg_val = row[2]

                    print(f"{col_name:<30} {min_val:<15.2f} {max_val:<15.2f} {avg_val:<15.2f}")
            except Exception as e:
                print(f"{col_name:<30} Error: {str(e)[:40]}")


def analyze_categorical_distribution(engine, table_name, column_name, limit=20):
    """Analizar distribución de valores categóricos"""

    print(f"\n{'DISTRIBUCIÓN: ' + column_name:^80}")
    print(f"{'-'*80}")

    with engine.connect() as conn:
        query = text(f"""
            SELECT
                {column_name},
                COUNT(*) as count,
                ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
            FROM {table_name}
            WHERE {column_name} IS NOT NULL
            GROUP BY {column_name}
            ORDER BY count DESC
            LIMIT {limit}
        """)
        result = conn.execute(query)

        print(f"{'Valor':<40} {'Registros':<15} {'%':<10}")
        print(f"{'-'*80}")

        for row in result:
            value = str(row[0])[:40]
            count = row[1]
            pct = row[2]
            print(f"{value:<40} {format_number(count):<15} {pct:>6.2f}%")


def main():
    """Función principal"""

    print("\n")
    print("="*80)
    print("ANÁLISIS DE INTEGRIDAD - BASE DE DATOS LATAM-3C")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Conectar a la base de datos
    try:
        engine = get_engine()
        print(f"\n✓ Conexión exitosa a la base de datos")
        print(f"  Database: {engine.url.database}")
    except Exception as e:
        print(f"\n✗ Error conectando a la base de datos: {e}")
        return 1

    # Obtener lista de tablas
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print(f"\nTablas encontradas: {len(tables)}")
    for table in tables:
        print(f"  • {table}")

    # Analizar tabla principal: huella_concretos
    if 'huella_concretos' in tables:
        print("\n" + "="*80)
        print("ANÁLISIS DETALLADO: huella_concretos")
        print("="*80)

        columns = analyze_table_structure(engine, 'huella_concretos')
        if columns:
            null_stats = analyze_table_data(engine, 'huella_concretos', columns)
            analyze_numeric_ranges(engine, 'huella_concretos', columns)

            # Distribuciones clave
            analyze_categorical_distribution(engine, 'huella_concretos', 'origen', limit=10)
            analyze_categorical_distribution(engine, 'huella_concretos', 'año', limit=10)

            # Verificar si existe columna 'planta'
            if any(col['name'] == 'planta' for col in columns):
                analyze_categorical_distribution(engine, 'huella_concretos', 'planta', limit=15)

    # Analizar tabla de cementos
    if 'cementos' in tables:
        print("\n" + "="*80)
        print("ANÁLISIS DETALLADO: cementos")
        print("="*80)

        columns = analyze_table_structure(engine, 'cementos')
        if columns:
            analyze_table_data(engine, 'cementos', columns)
            analyze_numeric_ranges(engine, 'cementos', columns)

    # Analizar tabla de plantas
    if 'plantas_latam' in tables:
        print("\n" + "="*80)
        print("ANÁLISIS DETALLADO: plantas_latam")
        print("="*80)

        columns = analyze_table_structure(engine, 'plantas_latam')
        if columns:
            analyze_table_data(engine, 'plantas_latam', columns)

    # Analizar cualquier otra tabla
    other_tables = [t for t in tables if t not in ['huella_concretos', 'cementos', 'plantas_latam']]
    for table in other_tables:
        print("\n" + "="*80)
        print(f"ANÁLISIS DETALLADO: {table}")
        print("="*80)

        columns = analyze_table_structure(engine, table)
        if columns:
            analyze_table_data(engine, table, columns)

    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN Y RECOMENDACIONES")
    print("="*80)

    with engine.connect() as conn:
        # Total de registros en huella_concretos
        if 'huella_concretos' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM huella_concretos"))
            total = result.fetchone()[0]
            print(f"\n✓ Total de remitos en huella_concretos: {format_number(total)}")

            # Empresas distintas
            result = conn.execute(text("SELECT COUNT(DISTINCT origen) FROM huella_concretos"))
            empresas = result.fetchone()[0]
            print(f"✓ Empresas/Orígenes distintos: {empresas}")

            # Años distintos
            result = conn.execute(text("SELECT COUNT(DISTINCT año) FROM huella_concretos WHERE año IS NOT NULL"))
            anios = result.fetchone()[0]
            print(f"✓ Años con datos: {anios}")

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80 + "\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
