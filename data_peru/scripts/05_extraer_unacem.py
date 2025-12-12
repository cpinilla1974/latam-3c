#!/usr/bin/env python3
"""
Extrae TODOS los datos históricos de UNACEM desde Access y los carga en peru_consolidado.db

Usa mdb-tools para extraer datos de la base Access.
"""

import subprocess
import sqlite3
import pandas as pd
from pathlib import Path
import io

# Rutas
DB_UNACEM = Path("/home/cpinilla/storage/access/UNACEM.accdb")
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

# Indicadores a extraer (mismos que Pacasmayo y Yura)
INDICADORES_CLAVE = [
    # Grupo 1: Producción
    '8', '11', '20', '21a',
    # Grupo 2: Contenido Clínker
    '92a', '12', '13', '14', '16',
    # Grupo 3: Emisiones
    '60', '60a', '60b', '62a', '73',
    # Grupo 4: Eficiencia
    '93', '1151', '1152', '1155',
    # Grupo 5: Eléctricos
    '97',
]

def extraer_tabla_access(db_path, tabla):
    """Extrae una tabla completa de Access usando mdb-export."""
    cmd = ['mdb-export', str(db_path), tabla]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return pd.read_csv(io.StringIO(result.stdout))

def explorar_estructura():
    """Explora la estructura de la base de datos UNACEM."""
    print(f"\n{'='*80}")
    print("EXPLORANDO ESTRUCTURA DE UNACEM.accdb")
    print(f"{'='*80}\n")

    # Listar tablas
    cmd = ['mdb-tables', str(DB_UNACEM)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    tablas = result.stdout.strip().split()

    print(f"📋 TABLAS ENCONTRADAS ({len(tablas)}):")
    for tabla in tablas:
        print(f"  - {tabla}")

    # Verificar modelo Dataset-Data
    tiene_dataset = 'tbDataset' in tablas
    tiene_data = 'tbData' in tablas

    if tiene_dataset and tiene_data:
        print(f"\n✅ Modelo Dataset-Data detectado (tbDataset + tbData)")
        return True
    else:
        print(f"\n⚠️  Modelo Dataset-Data NO detectado")
        return False

def extraer_indicadores_unacem(indicadores_codigos):
    """
    Extrae indicadores de UNACEM por planta usando modelo Dataset-Data.
    Extrae datos de 2 plantas: Atocongo (ATO) y Condorcocha (COND).
    Retorna DataFrame con: codigo_indicador, año, mes, valor, id_planta
    """
    print(f"\n📊 Extrayendo datos de UNACEM...")
    print(f"   Indicadores a extraer: {len(indicadores_codigos)}")

    # IDs de plantas de UNACEM (Perú)
    PLANTAS_UNACEM = [2, 3]  # 2=ATO (Atocongo), 3=COND (Condorcocha)

    # Extraer tablas completas
    print(f"   Extrayendo tbDataset...")
    df_dataset = extraer_tabla_access(DB_UNACEM, 'tbDataset')
    print(f"   ✅ {len(df_dataset):,} datasets encontrados")

    print(f"   Extrayendo tbData...")
    df_data = extraer_tabla_access(DB_UNACEM, 'tbData')
    print(f"   ✅ {len(df_data):,} registros de datos encontrados")

    print(f"   Extrayendo tbPlanta...")
    df_planta = extraer_tabla_access(DB_UNACEM, 'tbPlanta')
    print(f"   ✅ {len(df_planta):,} plantas encontradas")

    # Filtrar por indicadores clave y origen_dato = 1 (importados)
    df_data_filtrado = df_data[
        (df_data['campoGNR'].isin(indicadores_codigos)) &
        (df_data['origenDato'] == 1)  # Solo datos importados
    ].copy()
    print(f"   📌 {len(df_data_filtrado):,} registros coinciden con indicadores clave y son importados")

    # Filtrar solo datasets anuales de plantas peruanas con escenario BAU (datos reales)
    df_dataset_anual = df_dataset[
        (df_dataset['RepTemp'] == 'Anual') &
        (df_dataset['IDPlanta'].isin(PLANTAS_UNACEM)) &
        (df_dataset['escenario'].str.contains('BAU', case=False, na=False))
    ].copy()
    print(f"   📅 {len(df_dataset_anual):,} datasets anuales BAU de plantas peruanas disponibles")

    # Hacer join con dataset para obtener años y plantas
    df_join = df_data_filtrado.merge(
        df_dataset_anual[['IdDataset', 'agno', 'RepTemp', 'CodigoDataset', 'IDPlanta']],
        left_on='IdDataset',
        right_on='IdDataset',
        how='inner'
    )

    # Agregar nombres de plantas
    df_join = df_join.merge(
        df_planta[['Idplanta', 'planta']],
        left_on='IDPlanta',
        right_on='Idplanta',
        how='left'
    )

    # Preparar DataFrame final
    df_final = pd.DataFrame({
        'codigo_indicador': df_join['campoGNR'],
        'año': df_join['agno'],
        'mes': None,  # Solo datos anuales
        'valor': df_join['valor'],
        'id_dataset_origen': df_join['IdDataset'],
        'fuente': df_join['CodigoDataset'].fillna('UNACEM'),
        'id_planta': df_join['IDPlanta'],
        'nombre_planta': df_join['planta']
    })

    # Filtrar solo datos hasta 2024
    df_final = df_final[df_final['año'] <= 2024].copy()

    print(f"\n   ✅ {len(df_final):,} registros procesados")
    if len(df_final) > 0:
        print(f"   📅 Rango: {df_final['año'].min()} - {df_final['año'].max()}")
        print(f"   🏭 Plantas: {df_final['nombre_planta'].unique().tolist()}")

        # Mostrar resumen por planta
        print(f"\n   Registros por planta:")
        por_planta = df_final.groupby('nombre_planta').size().sort_values(ascending=False)
        for planta, count in por_planta.items():
            print(f"     {planta}: {count:,} registros")

    return df_final

def obtener_id_empresa(conn, codigo_empresa='UNACEM'):
    """Obtiene el ID de la empresa en la base consolidada."""
    cursor = conn.cursor()
    cursor.execute("SELECT id_empresa FROM empresas WHERE codigo_empresa = ?", (codigo_empresa,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"Empresa {codigo_empresa} no encontrada en base consolidada")

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
    if len(df) == 0:
        print(f"\n⚠️  No hay datos para cargar")
        return 0, 0

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
                str(row['codigo_indicador']),
                int(row['año']),
                int(row['mes']) if pd.notna(row['mes']) else None,
                float(row['valor']),
                str(row['fuente']),
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
                str(row['fuente']),
                int(row['id_dataset_origen']),
                id_planta,
                str(row['codigo_indicador']),
                int(row['año']),
                int(row['mes']) if pd.notna(row['mes']) else None,
                int(row['mes']) if pd.notna(row['mes']) else None
            ))
            registros_actualizados += 1

    # Log de carga
    cursor.execute("""
        INSERT INTO log_carga
        (id_empresa, registros_cargados, años_inicio, años_fin, script_utilizado, estado, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        id_empresa,
        registros_insertados + registros_actualizados,
        int(df['año'].min()) if len(df) > 0 else None,
        int(df['año'].max()) if len(df) > 0 else None,
        '05_extraer_unacem.py',
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
    print("\n" + "🔄 EXTRACCIÓN DE DATOS UNACEM (Access) ".center(80, "="))

    # Verificar que exista la base de datos
    if not DB_UNACEM.exists():
        print(f"❌ Error: Base de datos UNACEM no encontrada: {DB_UNACEM}")
        return

    if not DB_CONSOLIDADA.exists():
        print(f"❌ Error: Base de datos consolidada no encontrada: {DB_CONSOLIDADA}")
        return

    try:
        # Explorar estructura
        tiene_modelo = explorar_estructura()

        if not tiene_modelo:
            print(f"\n❌ No se encontró el modelo Dataset-Data esperado")
            return

        # Extraer datos
        df = extraer_indicadores_unacem(INDICADORES_CLAVE)

        if len(df) == 0:
            print(f"\n⚠️  No se encontraron datos. Verifica la estructura de la base Access.")
            return

        # Generar reporte
        generar_reporte_extraccion(df, 'UNACEM')

        # Cargar en base consolidada
        conn_consolidada = sqlite3.connect(DB_CONSOLIDADA)
        id_empresa = obtener_id_empresa(conn_consolidada, 'UNACEM')
        conn_consolidada.close()

        insertados, actualizados = cargar_datos_consolidada(df, id_empresa, 'UNACEM')

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
