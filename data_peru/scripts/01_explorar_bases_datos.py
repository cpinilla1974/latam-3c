#!/usr/bin/env python3
"""
Script para explorar la estructura de las bases de datos de las 3 empresas
y mapear los indicadores disponibles.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Rutas a las bases de datos
DB_PACASMAYO = Path("/home/cpinilla/pacas-3c/data/main.db")
DB_YURA = Path("/home/cpinilla/databases/yura-2c/data/main.db")
DB_UNACEM = Path("/home/cpinilla/storage/access/UNACEM.accdb")
DB_INDICADORES = Path("/home/cpinilla/databases/comun/indicadores.db")

def explorar_estructura_sqlite(db_path, nombre_empresa):
    """Explora la estructura de una base de datos SQLite."""
    print(f"\n{'='*80}")
    print(f"EXPLORANDO: {nombre_empresa}")
    print(f"Base de datos: {db_path}")
    print(f"{'='*80}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Listar tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print(f"📋 TABLAS ENCONTRADAS ({len(tablas)}):")
    for tabla in tablas:
        print(f"  - {tabla[0]}")

    # 2. Verificar si existe modelo Dataset-Data
    tablas_nombres = [t[0] for t in tablas]
    tiene_dataset_data = 'tb_dataset' in tablas_nombres and 'tb_data' in tablas_nombres

    if tiene_dataset_data:
        print(f"\n✅ Modelo Dataset-Data detectado")

        # Explorar tb_dataset
        print("\n📊 ESTRUCTURA tb_dataset:")
        cursor.execute("PRAGMA table_info(tb_dataset)")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")

        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM tb_dataset")
        count = cursor.fetchone()[0]
        print(f"\n  Total registros: {count:,}")

        # Rango de fechas
        cursor.execute("SELECT MIN(fecha), MAX(fecha) FROM tb_dataset")
        fecha_min, fecha_max = cursor.fetchone()
        print(f"  Rango fechas: {fecha_min} a {fecha_max}")

        # Explorar tb_data
        print("\n📊 ESTRUCTURA tb_data:")
        cursor.execute("PRAGMA table_info(tb_data)")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")

        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM tb_data")
        count = cursor.fetchone()[0]
        print(f"\n  Total registros: {count:,}")

        # Indicadores únicos disponibles
        cursor.execute("""
            SELECT DISTINCT codigo_indicador, COUNT(*) as count
            FROM tb_data
            GROUP BY codigo_indicador
            ORDER BY count DESC
            LIMIT 20
        """)
        indicadores = cursor.fetchall()
        print(f"\n  Top 20 indicadores más usados:")
        for ind, cnt in indicadores:
            print(f"    {ind}: {cnt:,} registros")

    else:
        print(f"\n⚠️  Modelo Dataset-Data NO detectado")
        print("     Se requiere análisis manual de la estructura")

    conn.close()
    return tiene_dataset_data

def mapear_indicadores_clave(db_path, nombre_empresa):
    """Busca indicadores clave del reporte en la base de datos."""
    # Indicadores del reporte TDR
    indicadores_reporte = [
        '8',     # Producción Clínker
        '11',    # Consumo Clínker
        '20',    # Producción Cemento
        '21a',   # Producción Cementitious
        '92a',   # Factor Clínker
        '60a',   # Emisiones CO2 Clínker
        '62a',   # Emisiones CO2 Cementitious
        '93',    # Eficiencia Térmica
        '97',    # Consumo Eléctrico Específico
        '1042',  # Consumo Eléctrico Total
    ]

    print(f"\n🔍 BÚSQUEDA DE INDICADORES CLAVE - {nombre_empresa}")
    print(f"{'='*80}\n")

    conn = sqlite3.connect(db_path)

    for cod_ind in indicadores_reporte:
        query = f"""
            SELECT
                COUNT(*) as total_registros,
                MIN(strftime('%Y', ds.fecha)) as año_min,
                MAX(strftime('%Y', ds.fecha)) as año_max
            FROM tb_data d
            JOIN tb_dataset ds ON d.id_dataset = ds.id_dataset
            WHERE d.codigo_indicador = '{cod_ind}'
        """
        try:
            df = pd.read_sql_query(query, conn)
            if df['total_registros'][0] > 0:
                print(f"✅ [{cod_ind}] Encontrado - {df['total_registros'][0]:,} registros ({df['año_min'][0]} a {df['año_max'][0]})")
            else:
                print(f"❌ [{cod_ind}] NO encontrado")
        except Exception as e:
            print(f"⚠️  [{cod_ind}] Error: {e}")

    conn.close()

def main():
    """Función principal."""
    print("\n" + "🔬 ANÁLISIS DE BASES DE DATOS - SECTOR CEMENTO PERÚ ".center(80, "="))

    # 1. Explorar Pacasmayo
    if DB_PACASMAYO.exists():
        tiene_modelo = explorar_estructura_sqlite(DB_PACASMAYO, "PACASMAYO")
        if tiene_modelo:
            mapear_indicadores_clave(DB_PACASMAYO, "PACASMAYO")
    else:
        print(f"\n❌ Base de datos Pacasmayo no encontrada: {DB_PACASMAYO}")

    # 2. Explorar Yura
    if DB_YURA.exists():
        tiene_modelo = explorar_estructura_sqlite(DB_YURA, "YURA")
        if tiene_modelo:
            mapear_indicadores_clave(DB_YURA, "YURA")
    else:
        print(f"\n❌ Base de datos Yura no encontrada: {DB_YURA}")

    # 3. Info sobre UNACEM
    print(f"\n{'='*80}")
    print(f"UNACEM (Access)")
    print(f"Base de datos: {DB_UNACEM}")
    print(f"{'='*80}\n")
    if DB_UNACEM.exists():
        print(f"✅ Archivo encontrado ({DB_UNACEM.stat().st_size / 1024 / 1024:.1f} MB)")
        print("⏳ Requiere conversión desde Access - se procesará en siguiente paso")
    else:
        print(f"❌ Base de datos UNACEM no encontrada")

    print(f"\n{'='*80}")
    print("✅ EXPLORACIÓN COMPLETADA")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
