#!/usr/bin/env python3
"""
Extrae TODOS los datos históricos de Yura y los carga en peru_consolidado.db

Extrae todos los años disponibles (no solo 2010-2023) para tener series largas.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Rutas
DB_YURA = Path("/home/cpinilla/databases/yura-2c/data/main.db")
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

# Indicadores a extraer (mismos que Pacasmayo)
INDICADORES_CLAVE = [
    # Grupo 1: Producción
    '8',     # Producción Clínker
    '11',    # Consumo Clínker
    '20',    # Producción Cemento
    '21a',   # Producción Cementitious

    # Grupo 2: Contenido Clínker
    '92a',   # Factor Clínker
    '12',    # Puzolana
    '13',    # Escoria
    '14',    # Ceniza volante
    '16',    # Caliza

    # Grupo 3: Emisiones
    '60',    # Emisiones proceso
    '60a',   # Descarbonatación clínker
    '60b',   # Emisiones combustibles
    '62a',   # Emisiones cementitious
    '73',    # Emisiones indirectas

    # Grupo 4: Eficiencia
    '93',    # Eficiencia térmica
    '1151',  # Energía fósil
    '1152',  # Energía biomasa
    '1155',  # Energía residuos

    # Grupo 5: Eléctricos
    '97',    # Consumo eléctrico específico
]

def obtener_id_empresa(conn, codigo_empresa='YURA'):
    """Obtiene el ID de la empresa en la base consolidada."""
    cursor = conn.cursor()
    cursor.execute("SELECT id_empresa FROM empresas WHERE codigo_empresa = ?", (codigo_empresa,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"Empresa {codigo_empresa} no encontrada en base consolidada")

def extraer_indicadores_yura(indicadores_codigos):
    """
    Extrae indicadores de Yura usando modelo Dataset-Data.
    Yura tiene una sola planta.
    Retorna DataFrame con: codigo_indicador, año, mes, valor, id_planta, nombre_planta
    """
    print(f"\n📊 Extrayendo datos de Yura...")
    print(f"   Indicadores a extraer: {len(indicadores_codigos)}")

    conn_yura = sqlite3.connect(DB_YURA)

    # Query para extraer datos (Yura tiene una sola planta)
    placeholders = ','.join(['?' for _ in indicadores_codigos])
    query = f"""
        SELECT
            d.codigo_indicador,
            strftime('%Y', ds.fecha) as año,
            NULL as mes,
            d.valor_indicador as valor,
            ds.id_dataset as id_dataset_origen,
            ds.codigo_dataset as fuente,
            1 as id_planta,
            'Yura' as nombre_planta
        FROM tb_data d
        JOIN tb_dataset ds ON d.id_dataset = ds.id_dataset
        WHERE d.codigo_indicador IN ({placeholders})
          AND ds.id_tipo_origen = 1  -- Solo datos de plantas
          AND ds.id_rep_temp = 1  -- Solo datos anuales
          AND d.origen_dato IN (1, 2)  -- Datos importados (1) y calculados (2)
          AND CAST(strftime('%Y', ds.fecha) AS INTEGER) <= 2024  -- Solo hasta 2024
        ORDER BY año, codigo_indicador
    """

    df = pd.read_sql_query(query, conn_yura, params=indicadores_codigos)
    conn_yura.close()

    print(f"   ✅ {len(df):,} registros extraídos")
    if len(df) > 0:
        print(f"   📅 Rango: {df['año'].min()} - {df['año'].max()}")
        print(f"   🏭 Planta: {df['nombre_planta'].unique().tolist()}")

        # Mostrar resumen por indicador
        print(f"\n   Registros por indicador:")
        resumen = df.groupby('codigo_indicador').size().sort_values(ascending=False)
        for ind, count in resumen.items():
            print(f"     {ind}: {count:,} registros")
    else:
        print(f"   ⚠️  No se encontraron registros")

    return df

def registrar_plantas(df, id_empresa, conn):
    """Registra las plantas en tb_plantas y retorna mapeo id_planta_origen -> id_planta."""
    cursor = conn.cursor()
    mapeo_plantas = {}

    # Obtener plantas únicas del dataframe
    plantas_df = df[['id_planta', 'nombre_planta']].drop_duplicates()

    for _, planta in plantas_df.iterrows():
        id_planta_origen = planta['id_planta']
        nombre_planta = planta['nombre_planta']

        # Verificar si ya existe la planta
        cursor.execute("""
            SELECT id_planta FROM tb_plantas
            WHERE id_empresa = ? AND nombre_planta = ?
        """, (id_empresa, nombre_planta))

        result = cursor.fetchone()
        if result:
            mapeo_plantas[id_planta_origen] = result[0]
        else:
            # Insertar nueva planta
            cursor.execute("""
                INSERT INTO tb_plantas (id_empresa, nombre_planta, codigo_planta)
                VALUES (?, ?, ?)
            """, (id_empresa, nombre_planta, str(id_planta_origen)))
            mapeo_plantas[id_planta_origen] = cursor.lastrowid

    conn.commit()
    return mapeo_plantas

def cargar_datos_consolidada(df, id_empresa, codigo_empresa):
    """Carga datos en la base consolidada (nueva estructura con plantas)."""
    print(f"\n💾 Cargando datos en base consolidada...")

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    # 1. Registrar plantas y obtener mapeo de IDs
    print(f"   Registrando plantas...")
    mapeo_plantas = registrar_plantas(df, id_empresa, conn)
    print(f"   ✅ {len(mapeo_plantas)} plantas registradas")

    # 2. Insertar datos por planta
    registros_insertados = 0
    registros_actualizados = 0

    for _, row in df.iterrows():
        id_planta = mapeo_plantas[row['id_planta']]

        try:
            # Intentar insertar en datos_plantas
            cursor.execute("""
                INSERT INTO datos_plantas
                (id_planta, codigo_indicador, año, mes, valor, fuente, id_dataset_origen)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                id_planta,
                row['codigo_indicador'],
                int(row['año']),
                int(row['mes']) if pd.notna(row['mes']) else None,
                float(row['valor']),
                row['fuente'],
                int(row['id_dataset_origen'])
            ))
            registros_insertados += 1
        except sqlite3.IntegrityError:
            # Si ya existe, actualizar
            cursor.execute("""
                UPDATE datos_plantas
                SET valor = ?, fuente = ?, id_dataset_origen = ?, fecha_carga = CURRENT_TIMESTAMP
                WHERE id_planta = ?
                  AND codigo_indicador = ?
                  AND año = ?
                  AND (mes = ? OR (mes IS NULL AND ? IS NULL))
            """, (
                float(row['valor']),
                row['fuente'],
                int(row['id_dataset_origen']),
                id_planta,
                row['codigo_indicador'],
                int(row['año']),
                int(row['mes']) if pd.notna(row['mes']) else None,
                int(row['mes']) if pd.notna(row['mes']) else None
            ))
            registros_actualizados += 1

    # Registrar en log de carga
    cursor.execute("""
        INSERT INTO log_carga
        (id_empresa, registros_cargados, años_inicio, años_fin, script_utilizado, estado, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        id_empresa,
        registros_insertados + registros_actualizados,
        int(df['año'].min()) if len(df) > 0 else None,
        int(df['año'].max()) if len(df) > 0 else None,
        '04_extraer_yura.py',
        'exitoso',
        f"{registros_insertados} nuevos, {registros_actualizados} actualizados - {len(mapeo_plantas)} plantas"
    ))

    conn.commit()
    conn.close()

    print(f"   ✅ {registros_insertados:,} registros nuevos insertados")
    print(f"   🔄 {registros_actualizados:,} registros actualizados")

    return registros_insertados, registros_actualizados

def generar_reporte_extraccion(df, codigo_empresa):
    """Genera reporte de la extracción."""
    print(f"\n{'='*80}")
    print(f"📈 REPORTE DE EXTRACCIÓN - {codigo_empresa}")
    print(f"{'='*80}\n")

    if len(df) == 0:
        print("⚠️  No se encontraron datos para extraer")
        return

    print(f"📊 Resumen General:")
    print(f"   Total registros: {len(df):,}")
    print(f"   Indicadores únicos: {df['codigo_indicador'].nunique()}")
    print(f"   Años únicos: {df['año'].nunique()}")
    print(f"   Rango temporal: {df['año'].min()} - {df['año'].max()}")

    print(f"\n📅 Registros por año:")
    por_año = df.groupby('año').size().sort_index()
    for año, count in por_año.items():
        print(f"   {año}: {count:,} registros")

    print(f"\n📌 Indicadores más completos (top 10):")
    top_indicadores = df.groupby('codigo_indicador').agg({
        'año': ['min', 'max', 'count']
    }).sort_values(('año', 'count'), ascending=False).head(10)

    for ind in top_indicadores.index:
        año_min = int(top_indicadores.loc[ind, ('año', 'min')])
        año_max = int(top_indicadores.loc[ind, ('año', 'max')])
        count = int(top_indicadores.loc[ind, ('año', 'count')])
        print(f"   {ind}: {count:,} registros ({año_min}-{año_max})")

def main():
    """Función principal."""
    print("\n" + "🔄 EXTRACCIÓN DE DATOS YURA ".center(80, "="))

    # Verificar que existan las bases de datos
    if not DB_YURA.exists():
        print(f"❌ Error: Base de datos Yura no encontrada: {DB_YURA}")
        return

    if not DB_CONSOLIDADA.exists():
        print(f"❌ Error: Base de datos consolidada no encontrada: {DB_CONSOLIDADA}")
        print("   Ejecuta primero: python 02_crear_base_consolidada.py")
        return

    try:
        # Obtener ID de empresa
        conn_consolidada = sqlite3.connect(DB_CONSOLIDADA)
        id_empresa = obtener_id_empresa(conn_consolidada, 'YURA')
        conn_consolidada.close()
        print(f"✅ Empresa YURA encontrada (ID: {id_empresa})")

        # Extraer datos
        df = extraer_indicadores_yura(INDICADORES_CLAVE)

        if len(df) == 0:
            print(f"\n⚠️  No se encontraron datos. Verifica:")
            print(f"    - Indicadores solicitados")
            print(f"    - Estructura de la base de datos")
            return

        # Generar reporte
        generar_reporte_extraccion(df, 'YURA')

        # Cargar en base consolidada
        insertados, actualizados = cargar_datos_consolidada(df, id_empresa, 'YURA')

        print(f"\n{'='*80}")
        print("✅ EXTRACCIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}\n")

        print(f"📊 Resumen:")
        print(f"   - Registros procesados: {len(df):,}")
        print(f"   - Registros nuevos: {insertados:,}")
        print(f"   - Registros actualizados: {actualizados:,}")
        print(f"   - Rango temporal: {df['año'].min()} - {df['año'].max()}")

    except Exception as e:
        print(f"\n❌ Error durante la extracción: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
