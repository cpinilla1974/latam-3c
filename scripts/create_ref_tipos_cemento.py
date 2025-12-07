#!/usr/bin/env python3
"""
Script para crear tabla de referencia de tipos de cemento
Extrae datos de la BD origen y los carga en PostgreSQL
"""

import sqlite3
import pandas as pd
import sys
import os

# Agregar path para imports
sys.path.insert(0, '/home/cpinilla/projects/latam-3c/v1')

from database.connection import get_engine
from sqlalchemy import text

print("=" * 80)
print("CREANDO TABLA DE REFERENCIA: ref_tipos_cemento")
print("=" * 80)

# 1. Conectar a SQLite (BD origen)
print("\n1️⃣  Leyendo datos de tabla 'cementos' desde SQLite...")
sqlite_path = "/home/cpinilla/databases/ficem_bd/data/ficem_bd.db"

try:
    conn_sqlite = sqlite3.connect(sqlite_path)

    query = """
    SELECT
        TRIM(cemento) as codigo_cemento,
        origen,
        planta,
        CAST(factor_clinker AS REAL) as factor_clinker,
        huella_co2_bruta,
        año
    FROM cementos
    WHERE factor_clinker IS NOT NULL
      AND factor_clinker != ''
      AND cemento IS NOT NULL
    """

    df_cementos = pd.read_sql_query(query, conn_sqlite)
    print(f"   ✅ Leído {len(df_cementos)} registros")

    print(f"\n   Tipos de cemento encontrados ({df_cementos['codigo_cemento'].nunique()}):")
    for tipo in sorted(df_cementos['codigo_cemento'].unique()):
        count = len(df_cementos[df_cementos['codigo_cemento'] == tipo])
        print(f"   - {tipo}: {count} registros")

except Exception as e:
    print(f"   ❌ Error leyendo SQLite: {e}")
    sys.exit(1)

# 2. Crear tabla de referencia agregada
print("\n2️⃣  Creando tabla de referencia agregada...")
try:
    df_ref = df_cementos.groupby(['codigo_cemento', 'origen', 'planta']).agg({
        'factor_clinker': ['mean', 'min', 'max', 'count'],
        'huella_co2_bruta': ['mean', 'min', 'max'],
        'año': ['min', 'max']
    }).reset_index()

    df_ref.columns = ['codigo_cemento', 'origen', 'planta',
                       'factor_clinker_promedio', 'factor_clinker_min', 'factor_clinker_max', 'num_registros',
                       'huella_co2_promedio', 'huella_co2_min', 'huella_co2_max',
                       'año_inicio', 'año_fin']

    # Convertir a tipos apropiados
    df_ref['num_registros'] = df_ref['num_registros'].astype(int)

    print(f"   ✅ Tabla de referencia creada con {len(df_ref)} combinaciones")

except Exception as e:
    print(f"   ❌ Error creando tabla: {e}")
    sys.exit(1)

# 3. Conectar a PostgreSQL y crear tabla
print("\n3️⃣  Conectando a PostgreSQL...")
try:
    engine = get_engine()
    print("   ✅ Conectado")
except Exception as e:
    print(f"   ❌ Error conectando a PostgreSQL: {e}")
    sys.exit(1)

print("   Creando tabla 'ref_tipos_cemento'...")
try:
    df_ref.to_sql('ref_tipos_cemento', engine, if_exists='replace', index=False)
    print("   ✅ Tabla creada")
except Exception as e:
    print(f"   ❌ Error creando tabla: {e}")
    sys.exit(1)

# Crear índices para mejor rendimiento
print("   Creando índices...")
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX idx_ref_cemento_codigo ON ref_tipos_cemento(codigo_cemento)"))
        conn.execute(text("CREATE INDEX idx_ref_cemento_origen ON ref_tipos_cemento(origen)"))
        conn.execute(text("CREATE INDEX idx_ref_cemento_planta ON ref_tipos_cemento(planta)"))
        conn.commit()
        print("   ✅ Índices creados")
except Exception as e:
    print(f"   ⚠️  Índices pueden ya existir: {e}")

# 4. Verificar datos en PostgreSQL
print("\n4️⃣  Verificando datos en PostgreSQL...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as total FROM ref_tipos_cemento"))
        total = result.scalar()
        print(f"   ✅ Total registros en ref_tipos_cemento: {total}")
except Exception as e:
    print(f"   ❌ Error verificando: {e}")
    sys.exit(1)

# 5. Mostrar top cementos
print("\n5️⃣  Top 10 tipos de cemento por cantidad de registros:")
top = df_ref.nlargest(10, 'num_registros')[['codigo_cemento', 'origen', 'planta', 'num_registros', 'factor_clinker_promedio']].copy()
for _, row in top.iterrows():
    print(f"   {row['codigo_cemento']:<40} | origen: {row['origen']:<8} | planta: {row['planta']:<10} | registros: {row['num_registros']:>3} | factor_clinker: {row['factor_clinker_promedio']:.3f}")

print("\n" + "=" * 80)
print("✅ TABLA ref_tipos_cemento CREADA EXITOSAMENTE")
print("=" * 80)
print("\n📊 Resumen:")
print(f"   - Total tipos de cemento: {df_ref['codigo_cemento'].nunique()}")
print(f"   - Total combinaciones origen-planta: {len(df_ref)}")
print(f"   - Rango de factor_clinker: {df_ref['factor_clinker_promedio'].min():.3f} - {df_ref['factor_clinker_promedio'].max():.3f}")
print(f"   - Rango de huella CO2: {df_ref['huella_co2_promedio'].min():.1f} - {df_ref['huella_co2_promedio'].max():.1f} kg CO2")

conn_sqlite.close()
engine.dispose()
