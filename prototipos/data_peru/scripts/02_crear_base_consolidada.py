#!/usr/bin/env python3
"""
Crea la base de datos consolidada peru_consolidado.db con todos los datos
históricos de las 3 empresas (Pacasmayo, Yura, UNACEM).

Estructura:
- empresas: Información de las 3 empresas
- indicadores_hist: Serie temporal larga de todos los indicadores disponibles
- agregados_nacionales: Totales nacionales calculados por año e indicador
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_CONSOLIDADA = Path("../data_peru/peru_consolidado.db")

def crear_esquema_base_datos():
    """Crea el esquema de la base de datos consolidada."""

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    print("🔨 Creando esquema de base de datos consolidada...")

    # Tabla 1: Empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_empresa TEXT UNIQUE NOT NULL,  -- PACAS, YURA, UNACEM
            nombre_completo TEXT NOT NULL,
            ubicacion TEXT,
            tipo TEXT,  -- Productor, Moledor, etc.
            activo BOOLEAN DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla 2: Indicadores históricos por empresa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicadores_hist (
            id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empresa INTEGER NOT NULL,
            codigo_indicador TEXT NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER,  -- NULL para datos anuales
            valor REAL NOT NULL,
            unidad TEXT,
            fuente TEXT,  -- 'dataset_original', 'calculado', 'estimado'
            id_dataset_origen INTEGER,  -- Referencia al dataset original si aplica
            fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observaciones TEXT,

            FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa),
            UNIQUE(id_empresa, codigo_indicador, año, mes)
        )
    """)

    # Tabla 3: Agregados nacionales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agregados_nacionales (
            id_agregado INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_indicador TEXT NOT NULL,
            año INTEGER NOT NULL,
            valor_nacional REAL NOT NULL,
            tipo_agregacion TEXT NOT NULL,  -- 'suma', 'promedio_ponderado'
            ponderador TEXT,  -- Indicador usado como ponderador si aplica
            num_empresas INTEGER,  -- Cantidad de empresas que aportaron datos
            fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(codigo_indicador, año)
        )
    """)

    # Tabla 4: Metadata de indicadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata_indicadores (
            codigo_indicador TEXT PRIMARY KEY,
            nombre_indicador TEXT NOT NULL,
            unidad TEXT,
            grupo TEXT,  -- Grupo 1-6 del reporte
            tipo_agregacion TEXT,  -- 'suma', 'promedio_ponderado'
            ponderador TEXT,  -- Código del indicador ponderador
            descripcion TEXT
        )
    """)

    # Tabla 5: Log de carga de datos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_carga (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empresa INTEGER,
            fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            registros_cargados INTEGER,
            años_inicio INTEGER,
            años_fin INTEGER,
            script_utilizado TEXT,
            estado TEXT,  -- 'exitoso', 'parcial', 'error'
            observaciones TEXT,

            FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa)
        )
    """)

    # Índices para optimizar consultas
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicadores_hist_empresa ON indicadores_hist(id_empresa)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicadores_hist_codigo ON indicadores_hist(codigo_indicador)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicadores_hist_año ON indicadores_hist(año)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_agregados_año ON agregados_nacionales(año)")

    conn.commit()
    print("✅ Esquema creado exitosamente")

    return conn

def insertar_empresas(conn):
    """Inserta información de las 3 empresas."""
    cursor = conn.cursor()

    empresas = [
        ('PACAS', 'Cementos Pacasmayo S.A.A.', 'Pacasmayo, La Libertad', 'Productor Integrado'),
        ('YURA', 'Yura S.A.', 'Arequipa', 'Productor Integrado'),
        ('UNACEM', 'Unión Andina de Cementos S.A.A.', 'Lima/Junín', 'Productor Integrado'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO empresas (codigo_empresa, nombre_completo, ubicacion, tipo)
        VALUES (?, ?, ?, ?)
    """, empresas)

    conn.commit()
    print(f"✅ {cursor.rowcount} empresas insertadas")

def insertar_metadata_indicadores(conn):
    """Inserta metadata de los indicadores clave del reporte."""
    cursor = conn.cursor()

    # Metadata basada en el análisis del reporte TDR
    indicadores = [
        # Grupo 1: Producción
        ('8', 'Producción de Clínker', 't/año', 'Grupo 1', 'suma', None, 'Producción anual de clínker'),
        ('11', 'Consumo de Clínker', 't/año', 'Grupo 1', 'suma', None, 'Consumo anual de clínker'),
        ('20', 'Producción de Cemento', 't/año', 'Grupo 1', 'suma', None, 'Producción anual de cemento'),
        ('21a', 'Producción de Cementitious', 't/año', 'Grupo 1', 'suma', None, 'Producción anual de cementitious'),

        # Grupo 2: Contenido Clínker
        ('92a', 'Factor Clínker', '%', 'Grupo 2', 'promedio_ponderado', '20', 'Contenido de clínker en cemento'),
        ('12', 'Puzolana en Cemento', '%', 'Grupo 2', 'promedio_ponderado', '20', 'Contenido de puzolana'),
        ('16', 'Caliza en Cemento', '%', 'Grupo 2', 'promedio_ponderado', '20', 'Contenido de caliza'),

        # Grupo 3: Emisiones CO₂
        ('60a', 'Emisiones CO₂ Clínker', 'kg CO₂/t', 'Grupo 3', 'promedio_ponderado', '8', 'Emisiones específicas clínker'),
        ('62a', 'Emisiones CO₂ Cementitious', 'kg CO₂/t', 'Grupo 3', 'promedio_ponderado', '21a', 'Emisiones específicas cementitious'),
        ('59c', 'Emisiones Consolidadas IPCC', 'Mt CO₂', 'Grupo 3', 'suma', None, 'Emisiones totales IPCC'),

        # Grupo 4: Eficiencia Energética
        ('93', 'Eficiencia Térmica', 'MJ/t clínker', 'Grupo 4', 'promedio_ponderado', '8', 'Consumo térmico específico'),
        ('95', 'Coprocesamiento', '%', 'Grupo 4', 'promedio_ponderado', '161', 'Porcentaje coprocesamiento'),

        # Grupo 5: Indicadores Eléctricos
        ('1042', 'Consumo Eléctrico Total', 'TWh/año', 'Grupo 5', 'suma', None, 'Consumo eléctrico anual total'),
        ('97', 'Consumo Eléctrico Específico', 'kWh/t', 'Grupo 5', 'promedio_ponderado', '21a', 'Consumo eléctrico específico'),
        ('33d', 'Factor Emisión Eléctrica', 'kg CO₂/MWh', 'Grupo 5', 'promedio_ponderado', '1042', 'Factor emisión matriz eléctrica'),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO metadata_indicadores
        (codigo_indicador, nombre_indicador, unidad, grupo, tipo_agregacion, ponderador, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, indicadores)

    conn.commit()
    print(f"✅ {cursor.rowcount} indicadores insertados en metadata")

def main():
    """Función principal."""
    print("\n" + "🗄️  CREACIÓN DE BASE DE DATOS CONSOLIDADA ".center(80, "="))
    print(f"\nRuta: {DB_CONSOLIDADA.absolute()}\n")

    # Crear directorio si no existe
    DB_CONSOLIDADA.parent.mkdir(parents=True, exist_ok=True)

    # Crear esquema
    conn = crear_esquema_base_datos()

    # Insertar datos maestros
    insertar_empresas(conn)
    insertar_metadata_indicadores(conn)

    # Cerrar conexión
    conn.close()

    print(f"\n{'='*80}")
    print("✅ BASE DE DATOS CONSOLIDADA CREADA EXITOSAMENTE")
    print(f"{'='*80}\n")

    print("Siguiente paso: ejecutar script de extracción de datos históricos")

if __name__ == "__main__":
    main()
