#!/usr/bin/env python3
"""
Reestructura la base de datos para tener 3 niveles de agregación:
1. datos_plantas (nivel más bajo)
2. datos_empresas (suma de plantas)
3. agregados_nacionales (suma/promedio ponderado de empresas)
"""

import sqlite3
from pathlib import Path

DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

def crear_nuevas_tablas():
    """Crea las nuevas tablas para los 3 niveles de agregación."""
    print("\n📊 Creando nuevas tablas...")

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    # Tabla 1: Plantas (agregación de las empresas con ID único de planta)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_plantas (
            id_planta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empresa INTEGER NOT NULL,
            nombre_planta TEXT NOT NULL,
            codigo_planta TEXT,
            ubicacion TEXT,
            activo BOOLEAN DEFAULT 1,

            FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa),
            UNIQUE(id_empresa, nombre_planta)
        )
    """)
    print("   ✅ Tabla tb_plantas creada")

    # Tabla 2: Datos por planta (nivel 1)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datos_plantas (
            id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            id_planta INTEGER NOT NULL,
            codigo_indicador TEXT NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER,
            valor REAL NOT NULL,
            fuente TEXT,
            id_dataset_origen INTEGER,
            fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_planta) REFERENCES tb_plantas(id_planta),
            UNIQUE(id_planta, codigo_indicador, año, mes)
        )
    """)
    print("   ✅ Tabla datos_plantas creada")

    # Tabla 3: Datos por empresa (nivel 2 - suma de plantas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datos_empresas (
            id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empresa INTEGER NOT NULL,
            codigo_indicador TEXT NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER,
            valor REAL NOT NULL,
            fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa),
            UNIQUE(id_empresa, codigo_indicador, año, mes)
        )
    """)
    print("   ✅ Tabla datos_empresas creada")

    # Crear índices
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_plantas_planta ON datos_plantas(id_planta)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_plantas_indicador ON datos_plantas(codigo_indicador)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_plantas_año ON datos_plantas(año)")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_empresas_empresa ON datos_empresas(id_empresa)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_empresas_indicador ON datos_empresas(codigo_indicador)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datos_empresas_año ON datos_empresas(año)")

    conn.commit()
    conn.close()
    print("   ✅ Índices creados")

def renombrar_tabla_antigua():
    """Renombra la tabla antigua para no perder datos."""
    print("\n📦 Renombrando tabla antigua...")

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    # Verificar si ya existe la tabla backup
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='indicadores_hist_backup'")
    if cursor.fetchone():
        print("   ⚠️  Tabla backup ya existe, eliminándola...")
        cursor.execute("DROP TABLE indicadores_hist_backup")

    # Renombrar tabla antigua
    cursor.execute("ALTER TABLE indicadores_hist RENAME TO indicadores_hist_backup")

    conn.commit()
    conn.close()
    print("   ✅ Tabla indicadores_hist renombrada a indicadores_hist_backup")

def main():
    """Función principal."""
    print("\n" + "🔄 REESTRUCTURACIÓN DE BASE DE DATOS ".center(80, "="))

    try:
        # 1. Crear nuevas tablas
        crear_nuevas_tablas()

        # 2. Renombrar tabla antigua
        renombrar_tabla_antigua()

        print(f"\n{'='*80}")
        print("✅ REESTRUCTURACIÓN COMPLETADA")
        print(f"{'='*80}\n")

        print("📋 Próximos pasos:")
        print("   1. Ejecutar scripts de extracción (03, 04, 05) para cargar datos en datos_plantas")
        print("   2. Ejecutar script 06 para calcular datos_empresas y agregados_nacionales")

    except Exception as e:
        print(f"\n❌ Error durante la reestructuración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
