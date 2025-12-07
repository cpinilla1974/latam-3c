#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL: Migrar remitos con emisiones desagregadas a estructura unificada
Extrae datos de PACAS, MZMA, Melón y Lomax a tablas remitos + remitos_emisiones_componentes
"""

import sqlite3
import psycopg2
import pandas as pd
from datetime import datetime
import sys

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

# Mapeo de componentes a categorías
CATEGORIAS_COMPONENTES = {
    'Cemento': ['co2_cem_', 'co2_transporte_cemento'],
    'Agregados': ['co2_agr_', 'co2_transporte_agregado'],
    'Aditivos': ['co2_adi_', 'co2_transporte_aditivo'],
    'Agua': ['co2_agu_', 'co2_transporte_agua'],
    'Planta': ['co2_con_']
}

ALCANCES = {
    # Cemento - Producción
    'co2_cem_descarbonatacion_clinker': 'A1',
    'co2_cem_comb_conv_clinker': 'A1',
    'co2_cem_comb_alter_clinker': 'A1',
    'co2_cem_comb_biom_clinker': 'A1',
    'co2_cem_autogeneracion_clinker': 'A1',
    'co2_cem_energia_electrica_clinker': 'A1',
    'co2_cem_comb_fuera_horno': 'A1',
    'co2_cem_autogeneracion': 'A1',
    'co2_cem_energia_electrica': 'A1',

    # Escoria, ceniza, filler, arcilla
    'co2_cem_transporte_escoria': 'A1',
    'co2_cem_comb_conv_escoria': 'A1',
    'co2_cem_transporte_ceniza': 'A1',
    'co2_cem_transporte_filler': 'A1',
    'co2_cem_transporte_arcilla': 'A1',

    # Transporte clinker y cemento
    'co2_cem_transporte_clinker': 'A2',
    'co2_cem_transporte_cemento': 'A2',
    'co2_transporte_cemento': 'A2',

    # Agregados
    'co2_agr_alcance_1': 'A1',
    'co2_agr_alcance_2': 'A1',
    'co2_transporte_agregado': 'A2',

    # Aditivos
    'co2_adi_alcance_1': 'A1',
    'co2_adi_alcance_2': 'A1',
    'co2_adi_min_alcance_1': 'A1',
    'co2_adi_min_alcance_2': 'A1',
    'co2_transporte_aditivo': 'A2',
    'co2_transporte_adi_min': 'A2',

    # Agua
    'co2_agu_alcance_1': 'A1',
    'co2_agu_alcance_2': 'A1',
    'co2_transporte_agua': 'A2',

    # Planta concretera
    'co2_con_combustibles': 'A3',
    'co2_con_electricidad': 'A3',
    'co2_con_autogeneracion': 'A3',

    # Transporte concreto
    'co2_transporte_concreto': 'A4'
}

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def limpiar_tablas(pg_conn):
    """Limpia las tablas destino"""
    cursor = pg_conn.cursor()
    print("🧹 Limpiando tablas destino...")
    cursor.execute("DELETE FROM remitos_emisiones_componentes")
    cursor.execute("DELETE FROM remitos")
    pg_conn.commit()
    print("  ✅ Tablas limpiadas")


def obtener_categoria(componente):
    """Determina la categoría de un componente"""
    for categoria, prefijos in CATEGORIAS_COMPONENTES.items():
        for prefijo in prefijos:
            if prefijo in componente:
                return categoria
    return 'Otros'


def obtener_alcance(componente):
    """Determina el alcance de un componente"""
    # Buscar match exacto primero
    for comp, alcance in ALCANCES.items():
        if comp in componente:
            return alcance
    return 'A1'  # Default


# ============================================================
# EXTRACCIÓN MZMA / MELÓN / LOMAX (estructura corp_co2)
# ============================================================

def extraer_corp_co2(origen, config):
    """
    Extrae datos de bases con estructura corp_co2 (columnas anchas)
    Retorna: (df_remitos, df_componentes)
    """
    print(f"\n📥 Extrayendo {origen.upper()}...")

    conn = sqlite3.connect(config['path'])

    # Query para datos del remito
    if origen == 'mzma':
        query_remitos = """
        SELECT DISTINCT
            c.codigo_dataset as id_remito,
            c.fecha,
            CAST(strftime('%Y', c.fecha) AS INTEGER) as año,
            CAST(strftime('%m', c.fecha) AS INTEGER) as mes,
            c.planta_concretera as planta,
            c.nombre_concreto as producto,
            NULL as formulacion,
            CAST(a.REST AS REAL) / 10.2 as resistencia_mpa,
            c.volumen,
            NULL as slump,
            NULL as tipo_cemento,
            (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
             FROM corp_cemento_concreto
             WHERE codigo_dataset = c.codigo_dataset AND volumen > 0) as contenido_cemento,
            NULL as proyecto,
            NULL as cliente,
            co2.co2_total as co2_total,
            co2.co2_total / NULLIF(c.volumen, 0) as co2_kg_m3
        FROM corp_concretos c
        JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
        JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
        WHERE co2.co2_kg_m3 > 0 AND CAST(a.REST AS REAL) > 0
        """
    elif origen == 'melon':
        query_remitos = """
        SELECT DISTINCT
            r.codigo_dataset as id_remito,
            r.fecha,
            CAST(strftime('%Y', r.fecha) AS INTEGER) as año,
            CAST(strftime('%m', r.fecha) AS INTEGER) as mes,
            pl.planta,
            p.producto,
            NULL as formulacion,
            CAST(a.REST AS REAL) / 10.2 as resistencia_mpa,
            r.volumen,
            NULL as slump,
            NULL as tipo_cemento,
            (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
             FROM corp_cemento_concreto
             WHERE codigo_dataset = r.codigo_dataset AND volumen > 0) as contenido_cemento,
            NULL as proyecto,
            NULL as cliente,
            co2.co2_total as co2_total,
            co2.co2_total / NULLIF(r.volumen, 0) as co2_kg_m3
        FROM tb_remitos r
        JOIN tb_producto p ON r.id_producto = p.id_producto
        JOIN tb_planta pl ON r.id_planta = pl.id_planta
        JOIN tb_atributos_concretos a ON p.producto = a.nombre_concreto
        JOIN corp_co2 co2 ON r.codigo_dataset = co2.codigo_dataset
        WHERE a.REST NOT LIKE '%FLUID%'
          AND CAST(a.REST AS REAL) > 0
          AND co2.co2_kg_m3 > 0
        """
    else:  # lomax
        query_remitos = """
        SELECT DISTINCT
            c.codigo_dataset as id_remito,
            c.fecha,
            CAST(strftime('%Y', c.fecha) AS INTEGER) as año,
            CAST(strftime('%m', c.fecha) AS INTEGER) as mes,
            c.planta_concretera as planta,
            c.nombre_concreto as producto,
            NULL as formulacion,
            CAST(a.REST AS REAL) as resistencia_mpa,
            c.volumen,
            NULL as slump,
            NULL as tipo_cemento,
            (SELECT SUM(cantidad_cemento_kg) / MAX(volumen)
             FROM corp_cemento_concreto
             WHERE codigo_dataset = c.codigo_dataset AND volumen > 0) as contenido_cemento,
            NULL as proyecto,
            NULL as cliente,
            co2.co2_total as co2_total,
            co2.co2_total / NULLIF(c.volumen, 0) as co2_kg_m3
        FROM corp_concretos c
        JOIN corp_co2 co2 ON c.codigo_dataset = co2.codigo_dataset
        JOIN tb_atributos_concretos a ON c.codigo_concreto = a.codigo_concreto
        WHERE co2.co2_kg_m3 > 0 AND CAST(a.REST AS REAL) > 0
        """

    df_remitos = pd.read_sql_query(query_remitos, conn)
    df_remitos['origen'] = origen
    df_remitos['empresa'] = config['empresa']
    df_remitos['pais'] = config['pais']

    # Query para emisiones desagregadas (UNPIVOT)
    query_co2 = """
    SELECT codigo_dataset, * FROM corp_co2
    """
    df_co2_wide = pd.read_sql_query(query_co2, conn)

    conn.close()

    # UNPIVOT: Convertir columnas a filas manualmente
    columnas_co2 = [col for col in df_co2_wide.columns if col.startswith('co2_') and col != 'co2_total' and col != 'co2_kg_m3']

    # Crear lista de componentes
    registros = []
    for _, row in df_co2_wide.iterrows():
        codigo = row['codigo_dataset']
        for col in columnas_co2:
            valor = row[col]
            if pd.notna(valor) and valor > 0:
                registros.append({
                    'id_remito': codigo,
                    'componente': col,
                    'valor_co2': valor
                })

    df_componentes = pd.DataFrame(registros)

    # Agregar alcance y categoría
    if len(df_componentes) > 0:
        df_componentes['alcance'] = df_componentes['componente'].apply(obtener_alcance)
        df_componentes['categoria'] = df_componentes['componente'].apply(obtener_categoria)

    print(f"  📊 {len(df_remitos):,} remitos")
    print(f"  🔍 {len(df_componentes):,} componentes")

    return df_remitos, df_componentes


# ============================================================
# EXTRACCIÓN PACAS (estructura tb_resultados_co2)
# ============================================================

def extraer_pacas(origen, config):
    """
    Extrae datos de PACAS con estructura normalizada tb_resultados_co2
    Retorna: (df_remitos, df_componentes)
    """
    print(f"\n📥 Extrayendo {origen.upper()}...")

    conn = sqlite3.connect(config['path'])

    # Extraer remitos desde co2_remitos
    query_remitos = """
    SELECT
        r.anio_planta_remito as id_remito,
        r.fecha,
        CAST(strftime('%Y', r.fecha) AS INTEGER) as año,
        CAST(strftime('%m', r.fecha) AS INTEGER) as mes,
        r.planta,
        r.formula as producto,
        r.formula as formulacion,
        a.resistencia_mpa,
        r.volumen,
        NULL as slump,
        NULL as tipo_cemento,
        (SELECT ROUND(c.cantidad / r.volumen, 2)
         FROM tb_remitos_componentes c
         WHERE c.codigo_dataset = r.anio_planta_remito
           AND c.tipo_componente_remito = 'cemento'
           AND c.cantidad > 0
         LIMIT 1) as contenido_cemento,
        r.obra as proyecto,
        NULL as cliente,
        r.emision_total as co2_total,
        r.huella as co2_kg_m3
    FROM co2_remitos r
    LEFT JOIN tb_atributos_concreto a ON r.formula = a.producto
    WHERE r.volumen > 0 AND r.huella > 0
    """

    df_remitos = pd.read_sql_query(query_remitos, conn)
    df_remitos['origen'] = origen
    df_remitos['empresa'] = config['empresa']
    df_remitos['pais'] = config['pais']

    # Extraer componentes desde tb_resultados_co2
    # Esta tabla tiene estructura: objeto, alcance, categoria, subcategoria, tipo_indicador, valor
    query_componentes = """
    SELECT
        r.objeto as id_remito,
        r.subcategoria as componente,
        r.valor as valor_co2,
        r.alcance,
        r.categoria
    FROM tb_resultados_co2 r
    WHERE r.tipo_indicador = 'Emisión kg CO2'
      AND r.valor > 0
    """

    df_componentes = pd.read_sql_query(query_componentes, conn)

    conn.close()

    print(f"  📊 {len(df_remitos):,} remitos")
    print(f"  🔍 {len(df_componentes):,} componentes")

    return df_remitos, df_componentes


# ============================================================
# CARGA A POSTGRESQL
# ============================================================

def cargar_remitos(pg_conn, df_remitos):
    """Carga remitos a tabla principal usando batch insert"""
    from psycopg2.extras import execute_values
    cursor = pg_conn.cursor()

    # Preparar datos en formato de tuplas
    valores = []
    for _, row in df_remitos.iterrows():
        trimestre = ((row['mes'] - 1) // 3 + 1) if pd.notna(row['mes']) else None
        valores.append((
            row['id_remito'],
            row['origen'],
            row['empresa'],
            row['pais'],
            row['fecha'],
            row['año'],
            row['mes'],
            trimestre,
            row['planta'],
            row['producto'],
            row.get('formulacion'),
            row['resistencia_mpa'],
            row['volumen'],
            row.get('slump'),
            row.get('tipo_cemento'),
            row.get('contenido_cemento'),
            row.get('proyecto'),
            row.get('cliente'),
            row.get('co2_total'),
            row.get('co2_kg_m3')
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

    # Recuperar IDs de los remitos insertados para este origen
    origen = df_remitos['origen'].iloc[0]

    # Crear set de id_remitos que acabamos de insertar
    id_remitos_insertados = [str(v[0]) for v in valores]

    # Query parametrizada con IN usando ANY
    cursor.execute("""
        SELECT id, origen, id_remito
        FROM remitos
        WHERE origen = %s AND id_remito = ANY(%s)
    """, (origen, id_remitos_insertados))

    remito_ids = {}
    for row in cursor.fetchall():
        remito_ids[(row[1], str(row[2]))] = row[0]

    return remito_ids, len(valores)


def cargar_componentes(pg_conn, df_componentes, remito_ids, origen):
    """Carga componentes a tabla de emisiones usando batch insert"""
    cursor = pg_conn.cursor()

    insert_query = """
        INSERT INTO remitos_emisiones_componentes (
            remito_id, alcance, categoria, componente, valor_co2
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (remito_id, componente) DO NOTHING
    """

    # Preparar batch de registros
    batch = []

    for _, row in df_componentes.iterrows():
        # Asegurar conversión a scalar values
        id_remito = str(row['id_remito'])
        key = (origen, id_remito)

        if key not in remito_ids:
            continue

        remito_id = remito_ids[key]

        try:
            batch.append((
                int(remito_id),
                str(row['alcance']),
                str(row['categoria']) if pd.notna(row['categoria']) else None,
                str(row['componente']),
                float(row['valor_co2'])
            ))
        except Exception as e:
            continue

    # Ejecutar batch insert
    if batch:
        cursor.executemany(insert_query, batch)
        pg_conn.commit()

    return len(batch)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("ETL: Migrar Remitos a Estructura Unificada")
    print("=" * 80)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Conectar a PostgreSQL
    print("🔌 Conectando a PostgreSQL...")
    pg_conn = psycopg2.connect(dbname=PG_DATABASE)

    # Limpiar tablas
    limpiar_tablas(pg_conn)

    # Procesar cada origen
    total_remitos = 0
    total_componentes = 0

    # MZMA
    df_rem, df_comp = extraer_corp_co2('mzma', SQLITE_DATABASES['mzma'])
    remito_ids, n_rem = cargar_remitos(pg_conn, df_rem)
    n_comp = cargar_componentes(pg_conn, df_comp, remito_ids, 'mzma')
    print(f"  ✅ MZMA: {n_rem:,} remitos, {n_comp:,} componentes")
    total_remitos += n_rem
    total_componentes += n_comp

    # Melón
    df_rem, df_comp = extraer_corp_co2('melon', SQLITE_DATABASES['melon'])
    remito_ids, n_rem = cargar_remitos(pg_conn, df_rem)
    n_comp = cargar_componentes(pg_conn, df_comp, remito_ids, 'melon')
    print(f"  ✅ Melón: {n_rem:,} remitos, {n_comp:,} componentes")
    total_remitos += n_rem
    total_componentes += n_comp

    # Lomax
    df_rem, df_comp = extraer_corp_co2('lomax', SQLITE_DATABASES['lomax'])
    remito_ids, n_rem = cargar_remitos(pg_conn, df_rem)
    n_comp = cargar_componentes(pg_conn, df_comp, remito_ids, 'lomax')
    print(f"  ✅ Lomax: {n_rem:,} remitos, {n_comp:,} componentes")
    total_remitos += n_rem
    total_componentes += n_comp

    # PACAS
    df_rem, df_comp = extraer_pacas('pacas', SQLITE_DATABASES['pacas'])
    remito_ids, n_rem = cargar_remitos(pg_conn, df_rem)
    n_comp = cargar_componentes(pg_conn, df_comp, remito_ids, 'pacas')
    print(f"  ✅ PACAS: {n_rem:,} remitos, {n_comp:,} componentes")
    total_remitos += n_rem
    total_componentes += n_comp

    # Estadísticas finales
    cursor = pg_conn.cursor()
    cursor.execute("""
        SELECT
            origen,
            COUNT(*) as num_remitos,
            AVG(resistencia_mpa) as avg_resistencia,
            AVG(co2_kg_m3) as avg_co2
        FROM remitos
        GROUP BY origen
        ORDER BY num_remitos DESC
    """)
    stats = cursor.fetchall()

    print("\n" + "=" * 80)
    print("📊 RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"\n{'Origen':<10} {'Remitos':>12} {'Avg REST':>12} {'Avg CO₂':>12}")
    print("-" * 80)
    for row in stats:
        print(f"{row[0]:<10} {row[1]:>12,} {row[2]:>12.1f} {row[3]:>12.1f}")
    print("-" * 80)
    print(f"{'TOTAL':<10} {total_remitos:>12,}")
    print(f"\nComponentes cargados: {total_componentes:,}")

    # Cerrar conexión
    pg_conn.close()

    print(f"\n✅ Migración completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Datos en: PostgreSQL latam4c_db")
    print(f"   - Tabla: remitos")
    print(f"   - Tabla: remitos_emisiones_componentes")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
