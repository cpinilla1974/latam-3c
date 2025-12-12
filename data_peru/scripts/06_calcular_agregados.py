#!/usr/bin/env python3
"""
Calcula agregados nacionales a partir de datos de las 3 empresas.

Aplica reglas de agregación:
- SUMA: indicadores de producción/consumo (8, 11, 20, 21a, etc.)
- PROMEDIO PONDERADO: indicadores específicos (92a, 60a, 62a, 93, 97)
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Rutas
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

# Definición de reglas de agregación
INDICADORES_SUMABLES = [
    '8',     # Producción Clínker
    '11',    # Consumo Clínker
    '20',    # Producción Cemento
    '21a',   # Producción Cementitious
    '60',    # Emisiones proceso
    '60b',   # Emisiones combustibles
    '73',    # Emisiones indirectas
    '1042',  # Consumo Eléctrico Total (si existe)
    '1151',  # Energía fósil
    '1152',  # Energía biomasa
    '1155',  # Energía residuos
]

# Indicadores con promedio ponderado
# Formato: (indicador, ponderador, nombre)
INDICADORES_PONDERADOS = [
    ('92a', '20', 'Factor Clínker'),           # Ponderado por Producción Cemento
    ('60a', '8', 'Emisiones CO₂ Clínker'),     # Ponderado por Producción Clínker
    ('62a', '21a', 'Emisiones CO₂ Cementitious'), # Ponderado por Producción Cementitious
    ('93', '8', 'Eficiencia Térmica'),         # Ponderado por Producción Clínker
    ('97', '21a', 'Consumo Eléctrico Específico'), # Ponderado por Producción Cementitious
    ('12', '20', 'Puzolana'),                  # Ponderado por Producción Cemento
    ('13', '20', 'Escoria'),                   # Ponderado por Producción Cemento
    ('14', '20', 'Ceniza volante'),            # Ponderado por Producción Cemento
    ('16', '20', 'Caliza'),                    # Ponderado por Producción Cemento
]

def cargar_datos_plantas():
    """Carga todos los datos de plantas."""
    print(f"\n📊 Cargando datos de plantas...")

    conn = sqlite3.connect(DB_CONSOLIDADA)

    query = """
        SELECT
            dp.codigo_indicador,
            dp.año,
            dp.mes,
            dp.valor,
            dp.id_planta,
            p.id_empresa,
            e.codigo_empresa,
            p.nombre_planta
        FROM datos_plantas dp
        JOIN tb_plantas p ON dp.id_planta = p.id_planta
        JOIN empresas e ON p.id_empresa = e.id_empresa
        WHERE dp.mes IS NULL  -- Solo datos anuales por ahora
        ORDER BY dp.año, dp.codigo_indicador
    """

    df_plantas = pd.read_sql_query(query, conn)
    conn.close()

    print(f"   ✅ {len(df_plantas):,} registros cargados (nivel plantas)")
    print(f"   📅 Rango: {df_plantas['año'].min()} - {df_plantas['año'].max()}")
    print(f"   🏭 Plantas: {df_plantas['nombre_planta'].nunique()}")
    print(f"   🏢 Empresas: {df_plantas['codigo_empresa'].nunique()}")

    return df_plantas

def calcular_datos_empresas(df_plantas):
    """Calcula nivel 2: Agrega datos de plantas por empresa."""
    print(f"\n🏢 Calculando datos por empresa (suma de plantas)...")

    # Agrupar por empresa, año, indicador y sumar valores de plantas
    df_empresas = df_plantas.groupby(['id_empresa', 'codigo_empresa', 'año', 'codigo_indicador']).agg({
        'valor': 'sum',  # Suma de todas las plantas de cada empresa
        'id_planta': 'count'  # Contar cuántas plantas aportaron
    }).reset_index()

    df_empresas.columns = ['id_empresa', 'codigo_empresa', 'año', 'codigo_indicador', 'valor', 'num_plantas']

    print(f"   ✅ {len(df_empresas):,} registros por empresa calculados")
    print(f"   📅 Rango: {df_empresas['año'].min()} - {df_empresas['año'].max()}")
    print(f"   🏢 Empresas: {df_empresas['codigo_empresa'].unique().tolist()}")

    return df_empresas

def guardar_datos_empresas(df_empresas):
    """Guarda los datos por empresa en la tabla datos_empresas."""
    if len(df_empresas) == 0:
        print(f"\n⚠️  No hay datos de empresas para guardar")
        return 0

    print(f"\n💾 Guardando {len(df_empresas):,} registros de empresas en base de datos...")

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    # Limpiar tabla
    cursor.execute("DELETE FROM datos_empresas")
    print(f"   🗑️  Tabla datos_empresas limpiada")

    # Insertar datos de empresas
    registros_insertados = 0
    for _, row in df_empresas.iterrows():
        cursor.execute("""
            INSERT INTO datos_empresas
            (id_empresa, codigo_indicador, año, mes, valor)
            VALUES (?, ?, ?, NULL, ?)
        """, (
            int(row['id_empresa']),
            row['codigo_indicador'],
            int(row['año']),
            float(row['valor'])
        ))
        registros_insertados += 1

    conn.commit()
    conn.close()

    print(f"   ✅ {registros_insertados:,} registros de empresas guardados")
    return registros_insertados

def calcular_sumas(df, indicadores_sumables, num_empresas_requeridas=3):
    """Calcula agregados nacionales para indicadores sumables.

    Solo calcula agregados para años donde todas las empresas tienen datos.
    """
    print(f"\n➕ Calculando sumas para {len(indicadores_sumables)} indicadores...")
    print(f"   (Solo años con {num_empresas_requeridas} empresas)")

    # Filtrar solo indicadores sumables
    df_sumables = df[df['codigo_indicador'].isin(indicadores_sumables)]

    # Agrupar por año e indicador, sumando los valores
    agregados = df_sumables.groupby(['año', 'codigo_indicador']).agg({
        'valor': 'sum',
        'codigo_empresa': 'count'  # Contar cuántas empresas aportaron
    }).reset_index()

    agregados.columns = ['año', 'codigo_indicador', 'valor_nacional', 'num_empresas']

    # FILTRAR: Solo mantener años donde todas las empresas tienen datos
    agregados = agregados[agregados['num_empresas'] == num_empresas_requeridas].copy()

    agregados['tipo_agregacion'] = 'suma'
    agregados['ponderador'] = None

    print(f"   ✅ {len(agregados):,} agregados calculados")

    años_excluidos_total = set()
    # Mostrar resumen
    print(f"\n   Resumen por indicador:")
    for ind in indicadores_sumables:
        datos_ind = agregados[agregados['codigo_indicador'] == ind]
        if len(datos_ind) > 0:
            print(f"     {ind}: {len(datos_ind)} años")

            # Verificar si hay años con datos incompletos
            datos_todos = df_sumables[df_sumables['codigo_indicador'] == ind]
            años_con_datos = datos_todos.groupby('año')['codigo_empresa'].count()
            años_incompletos = años_con_datos[años_con_datos < num_empresas_requeridas]
            if len(años_incompletos) > 0:
                años_excluidos_total.update(años_incompletos.index.tolist())

    if len(años_excluidos_total) > 0:
        print(f"\n   ⚠️  Años excluidos por datos incompletos: {sorted(años_excluidos_total)}")

    return agregados

def calcular_promedios_ponderados(df, indicadores_ponderados, num_empresas_requeridas=3):
    """Calcula agregados nacionales usando promedios ponderados.

    Solo calcula agregados para años donde todas las empresas tienen datos.
    """
    print(f"\n⚖️  Calculando promedios ponderados para {len(indicadores_ponderados)} indicadores...")
    print(f"   (Solo años con {num_empresas_requeridas} empresas)")

    resultados = []

    for indicador, ponderador, nombre in indicadores_ponderados:
        print(f"\n   📌 {indicador} ({nombre}) - Ponderado por [{ponderador}]")

        # Obtener datos del indicador
        df_indicador = df[df['codigo_indicador'] == indicador].copy()

        # Obtener datos del ponderador
        df_ponderador = df[df['codigo_indicador'] == ponderador].copy()

        if len(df_indicador) == 0:
            print(f"      ⚠️  No hay datos para indicador {indicador}")
            continue

        if len(df_ponderador) == 0:
            print(f"      ⚠️  No hay datos para ponderador {ponderador}")
            continue

        # Hacer merge para tener indicador y ponderador juntos
        df_merge = df_indicador.merge(
            df_ponderador[['año', 'codigo_empresa', 'valor']],
            on=['año', 'codigo_empresa'],
            how='inner',
            suffixes=('_ind', '_pond')
        )

        if len(df_merge) == 0:
            print(f"      ⚠️  No hay datos coincidentes")
            continue

        # Contar empresas por año ANTES de calcular
        num_empresas_por_año = df_merge.groupby('año')['codigo_empresa'].nunique().reset_index()
        num_empresas_por_año.columns = ['año', 'num_empresas']

        # FILTRAR: Solo años con todas las empresas
        años_validos = num_empresas_por_año[num_empresas_por_año['num_empresas'] == num_empresas_requeridas]['año'].tolist()

        if len(años_validos) == 0:
            print(f"      ⚠️  No hay años con {num_empresas_requeridas} empresas")
            continue

        df_merge_filtrado = df_merge[df_merge['año'].isin(años_validos)].copy()

        # Calcular promedio ponderado por año
        # Formula: Σ(indicador_i × ponderador_i) / Σ(ponderador_i)
        agregado_por_año = df_merge_filtrado.groupby('año').apply(
            lambda x: (x['valor_ind'] * x['valor_pond']).sum() / x['valor_pond'].sum()
        ).reset_index()

        agregado_por_año.columns = ['año', 'valor_nacional']
        agregado_por_año['codigo_indicador'] = indicador
        agregado_por_año['tipo_agregacion'] = 'promedio_ponderado'
        agregado_por_año['ponderador'] = ponderador

        # Agregar número de empresas (siempre será num_empresas_requeridas para los años válidos)
        agregado_por_año['num_empresas'] = num_empresas_requeridas

        resultados.append(agregado_por_año)
        print(f"      ✅ {len(agregado_por_año)} años calculados")

    if len(resultados) > 0:
        df_resultado = pd.concat(resultados, ignore_index=True)
        print(f"\n   ✅ Total: {len(df_resultado):,} agregados ponderados calculados")
        return df_resultado
    else:
        print(f"\n   ⚠️  No se calcularon agregados ponderados")
        return pd.DataFrame()

def guardar_agregados(df_agregados):
    """Guarda los agregados nacionales en la base de datos."""
    if len(df_agregados) == 0:
        print(f"\n⚠️  No hay agregados para guardar")
        return 0

    print(f"\n💾 Guardando {len(df_agregados):,} agregados en base de datos...")

    conn = sqlite3.connect(DB_CONSOLIDADA)
    cursor = conn.cursor()

    # Limpiar tabla de agregados (para recalcular)
    cursor.execute("DELETE FROM agregados_nacionales")
    print(f"   🗑️  Tabla agregados_nacionales limpiada")

    # Insertar agregados
    registros_insertados = 0
    for _, row in df_agregados.iterrows():
        cursor.execute("""
            INSERT INTO agregados_nacionales
            (codigo_indicador, año, valor_nacional, tipo_agregacion, ponderador, num_empresas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['codigo_indicador'],
            int(row['año']),
            float(row['valor_nacional']),
            row['tipo_agregacion'],
            row['ponderador'] if pd.notna(row['ponderador']) else None,
            int(row['num_empresas'])
        ))
        registros_insertados += 1

    conn.commit()
    conn.close()

    print(f"   ✅ {registros_insertados:,} agregados guardados")
    return registros_insertados

def generar_reporte(df_agregados):
    """Genera reporte de los agregados calculados."""
    print(f"\n{'='*80}")
    print(f"📈 REPORTE DE AGREGADOS NACIONALES")
    print(f"{'='*80}\n")

    if len(df_agregados) == 0:
        print("⚠️  No hay agregados para reportar")
        return

    print(f"📊 Resumen General:")
    print(f"   Total agregados: {len(df_agregados):,}")
    print(f"   Indicadores únicos: {df_agregados['codigo_indicador'].nunique()}")
    print(f"   Años únicos: {df_agregados['año'].nunique()}")
    print(f"   Rango temporal: {df_agregados['año'].min()} - {df_agregados['año'].max()}")

    # Resumen por tipo de agregación
    print(f"\n📊 Por tipo de agregación:")
    por_tipo = df_agregados.groupby('tipo_agregacion').size()
    for tipo, count in por_tipo.items():
        print(f"   {tipo}: {count:,} agregados")

    # Agregados por año
    print(f"\n📅 Agregados por año:")
    por_año = df_agregados.groupby('año').size().sort_index()
    for año, count in por_año.items():
        print(f"   {año}: {count:,} indicadores")

    # Top indicadores
    print(f"\n📌 Indicadores calculados:")
    por_indicador = df_agregados.groupby('codigo_indicador').agg({
        'año': ['min', 'max', 'count'],
        'tipo_agregacion': 'first'
    }).sort_values(('año', 'count'), ascending=False)

    for ind in por_indicador.index:
        año_min = int(por_indicador.loc[ind, ('año', 'min')])
        año_max = int(por_indicador.loc[ind, ('año', 'max')])
        count = int(por_indicador.loc[ind, ('año', 'count')])
        tipo = por_indicador.loc[ind, ('tipo_agregacion', 'first')]
        print(f"   {ind}: {count} años ({año_min}-{año_max}) - {tipo}")

    # Muestra de valores para años clave del reporte
    años_reporte = [2010, 2014, 2019, 2021, 2023]
    print(f"\n📋 Muestra de valores para años del reporte:")

    for año in años_reporte:
        datos_año = df_agregados[df_agregados['año'] == año]
        if len(datos_año) > 0:
            print(f"\n   {año}:")
            # Mostrar indicadores principales
            for ind in ['8', '11', '20', '21a', '92a', '60a', '62a', '93', '97']:
                valor = datos_año[datos_año['codigo_indicador'] == ind]
                if len(valor) > 0:
                    val = valor.iloc[0]['valor_nacional']
                    tipo = valor.iloc[0]['tipo_agregacion']
                    print(f"      [{ind}] = {val:,.2f} ({tipo})")

def exportar_csv(df_agregados):
    """Exporta agregados a CSV para análisis externo."""
    if len(df_agregados) == 0:
        return

    output_path = Path(__file__).parent.parent / "datos_procesados" / "agregados_nacionales.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_agregados.to_csv(output_path, index=False)
    print(f"\n📁 Agregados exportados a: {output_path}")

def main():
    """Función principal."""
    print("\n" + "🔄 CÁLCULO DE AGREGADOS (3 NIVELES) ".center(80, "="))

    # Verificar que existe la base de datos
    if not DB_CONSOLIDADA.exists():
        print(f"❌ Error: Base de datos consolidada no encontrada: {DB_CONSOLIDADA}")
        return

    try:
        # NIVEL 1: Cargar datos de plantas
        df_plantas = cargar_datos_plantas()

        if len(df_plantas) == 0:
            print(f"\n⚠️  No hay datos de plantas para procesar")
            return

        # NIVEL 2: Calcular y guardar datos por empresa
        df_empresas = calcular_datos_empresas(df_plantas)
        guardados_empresas = guardar_datos_empresas(df_empresas)

        # NIVEL 3: Calcular agregados nacionales (desde datos de empresas)
        print(f"\n🌎 Calculando agregados nacionales (desde empresas)...")

        # Calcular sumas
        df_sumas = calcular_sumas(df_empresas, INDICADORES_SUMABLES)

        # Calcular promedios ponderados
        df_ponderados = calcular_promedios_ponderados(df_empresas, INDICADORES_PONDERADOS)

        # Combinar todos los agregados nacionales
        if len(df_ponderados) > 0:
            df_agregados = pd.concat([df_sumas, df_ponderados], ignore_index=True)
        else:
            df_agregados = df_sumas

        # Guardar agregados nacionales en base de datos
        guardados_nacionales = guardar_agregados(df_agregados)

        # Generar reporte
        generar_reporte(df_agregados)

        # Exportar a CSV
        exportar_csv(df_agregados)

        print(f"\n{'='*80}")
        print("✅ CÁLCULO DE AGREGADOS COMPLETADO EXITOSAMENTE")
        print(f"{'='*80}\n")

        print(f"📊 Resumen por nivel:")
        print(f"   Nivel 1 (Plantas): {len(df_plantas):,} registros")
        print(f"   Nivel 2 (Empresas): {guardados_empresas:,} registros guardados")
        print(f"   Nivel 3 (Nacional): {guardados_nacionales:,} agregados guardados")
        print(f"   Rango temporal: {df_agregados['año'].min()} - {df_agregados['año'].max()}")

    except Exception as e:
        print(f"\n❌ Error durante el cálculo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
