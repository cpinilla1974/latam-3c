#!/usr/bin/env python3
"""
Valida los agregados calculados contra los valores oficiales del reporte PDF.

Compara los valores extraídos del PDF (tabla datos_pdf_referencia)
contra los agregados calculados (tabla agregados_nacionales).
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Rutas
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

def cargar_datos_pdf():
    """Carga los valores oficiales extraídos del PDF."""
    print(f"\n📄 Cargando datos del PDF de referencia...")

    conn = sqlite3.connect(DB_CONSOLIDADA)

    query = """
        SELECT
            codigo_indicador,
            año,
            valor,
            unidad
        FROM datos_pdf_referencia
        ORDER BY codigo_indicador, año
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"   ✅ {len(df):,} valores del PDF cargados")
    print(f"   📊 Indicadores: {df['codigo_indicador'].unique().tolist()}")
    print(f"   📅 Años: {sorted(df['año'].unique())}")

    return df

def cargar_agregados_calculados():
    """Carga los agregados calculados de la base de datos."""
    print(f"\n📊 Cargando agregados calculados...")

    conn = sqlite3.connect(DB_CONSOLIDADA)

    query = """
        SELECT
            codigo_indicador,
            año,
            valor_nacional
        FROM agregados_nacionales
        ORDER BY codigo_indicador, año
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"   ✅ {len(df):,} agregados calculados cargados")

    return df

def convertir_unidades(codigo, valor, unidad_pdf):
    """Convierte valores a las mismas unidades para comparación."""
    # Si el valor del PDF está en Mt, convertir el valor calculado (en toneladas) a Mt
    if unidad_pdf == 'Mt' and codigo in ['8', '11', '20', '21a']:
        return valor / 1_000_000

    # Si el valor del PDF está en fracción (0-1), el valor calculado ya debe estar en fracción
    # Si el PDF tiene % y el calculado está en fracción, convertir calculado a %
    if codigo == '92a':
        # Valor calculado está en fracción (0-1), PDF también está en fracción
        # Para comparar, convertir ambos a porcentaje
        return valor * 100

    # Otros indicadores ya están en las unidades correctas
    return valor

def comparar_valores(df_calculados, df_pdf):
    """Compara valores calculados vs PDF y genera reporte."""
    print(f"\n{'='*100}")
    print("VALIDACIÓN CONTRA VALORES EXTRAÍDOS DEL PDF")
    print(f"{'='*100}\n")

    resultados = []
    errores_totales = []

    # Agrupar por indicador
    indicadores = df_pdf['codigo_indicador'].unique()

    for codigo in indicadores:
        df_ind_pdf = df_pdf[df_pdf['codigo_indicador'] == codigo]

        print(f"\n📌 Indicador [{codigo}]")
        print(f"{'Año':<8} {'PDF (Ref)':<15} {'Calculado':<15} {'Diferencia':<15} {'Error %':<10} {'Estado'}")
        print("-" * 100)

        for _, row_pdf in df_ind_pdf.iterrows():
            año = row_pdf['año']
            valor_pdf_raw = row_pdf['valor']
            unidad_pdf = row_pdf['unidad']

            # Convertir valor del PDF a unidades de comparación
            if unidad_pdf == 'Mt':
                valor_pdf = valor_pdf_raw  # Ya está en Mt
            elif unidad_pdf == 'fracción' and codigo == '92a':
                valor_pdf = valor_pdf_raw * 100  # Convertir fracción a porcentaje
            else:
                valor_pdf = valor_pdf_raw

            # Buscar valor calculado
            df_valor = df_calculados[
                (df_calculados['codigo_indicador'] == codigo) &
                (df_calculados['año'] == año)
            ]

            if len(df_valor) == 0:
                print(f"{año:<8} {valor_pdf:<15.2f} {'NO CALCULADO':<15} {'-':<15} {'-':<10} ❌ FALTANTE")
                resultados.append({
                    'codigo': codigo,
                    'año': año,
                    'pdf': valor_pdf,
                    'calculado': None,
                    'diferencia': None,
                    'error_pct': None,
                    'estado': 'FALTANTE'
                })
                continue

            valor_calculado_raw = df_valor.iloc[0]['valor_nacional']
            valor_calculado = convertir_unidades(codigo, valor_calculado_raw, unidad_pdf)

            # Calcular diferencia y error porcentual
            diferencia = valor_calculado - valor_pdf
            error_pct = abs(diferencia / valor_pdf * 100) if valor_pdf != 0 else 0

            # Determinar estado (tolerancia 2%)
            if error_pct <= 2:
                estado = "✅ OK"
            elif error_pct <= 5:
                estado = "⚠️  ACEPTABLE"
            else:
                estado = "❌ REVISAR"

            print(f"{año:<8} {valor_pdf:<15.2f} {valor_calculado:<15.2f} {diferencia:<15.2f} {error_pct:<10.2f} {estado}")

            resultados.append({
                'codigo': codigo,
                'año': año,
                'pdf': valor_pdf,
                'calculado': valor_calculado,
                'diferencia': diferencia,
                'error_pct': error_pct,
                'estado': estado
            })

            errores_totales.append(error_pct)

    return resultados, errores_totales

def generar_resumen(resultados, errores_totales):
    """Genera resumen estadístico de la validación."""
    print(f"\n{'='*100}")
    print("RESUMEN ESTADÍSTICO DE VALIDACIÓN")
    print(f"{'='*100}\n")

    df_resultados = pd.DataFrame(resultados)

    print(f"📊 Estadísticas Generales:")
    print(f"   Total comparaciones: {len(resultados)}")
    print(f"   Error promedio: {sum(errores_totales)/len(errores_totales):.2f}%")
    print(f"   Error máximo: {max(errores_totales):.2f}%")
    print(f"   Error mínimo: {min(errores_totales):.2f}%")

    # Contar por estado
    exactos = sum(1 for e in errores_totales if e <= 2)
    aceptables = sum(1 for e in errores_totales if 2 < e <= 5)
    revisar = sum(1 for e in errores_totales if e > 5)

    print(f"\n📈 Distribución de Resultados:")
    print(f"   ✅ Exactos (≤2%): {exactos} ({exactos/len(errores_totales)*100:.1f}%)")
    print(f"   ⚠️  Aceptables (2-5%): {aceptables} ({aceptables/len(errores_totales)*100:.1f}%)")
    print(f"   ❌ Revisar (>5%): {revisar} ({revisar/len(errores_totales)*100:.1f}%)")

    # Indicadores con mayor diferencia
    print(f"\n🔍 Indicadores con mayor diferencia:")
    top_errores = df_resultados.nlargest(5, 'error_pct')
    for _, row in top_errores.iterrows():
        print(f"   [{row['codigo']}] {row['año']}: {row['error_pct']:.2f}% de error")

    # Exportar resultados
    output_path = Path(__file__).parent.parent / "datos_procesados" / "validacion_vs_reporte.csv"
    df_resultados.to_csv(output_path, index=False)
    print(f"\n📁 Resultados exportados a: {output_path}")

    return df_resultados

def main():
    """Función principal."""
    print("\n" + "🔍 VALIDACIÓN CONTRA REPORTE OFICIAL ".center(100, "="))

    # Verificar que existe la base de datos
    if not DB_CONSOLIDADA.exists():
        print(f"❌ Error: Base de datos consolidada no encontrada: {DB_CONSOLIDADA}")
        return

    try:
        # Cargar datos del PDF
        df_pdf = cargar_datos_pdf()

        # Cargar agregados calculados
        df_calculados = cargar_agregados_calculados()

        # Comparar valores
        resultados, errores = comparar_valores(df_calculados, df_pdf)

        # Generar resumen
        df_resumen = generar_resumen(resultados, errores)

        print(f"\n{'='*100}")
        print("✅ VALIDACIÓN COMPLETADA")
        print(f"{'='*100}\n")

        # Conclusión
        error_promedio = sum(errores)/len(errores)
        if error_promedio <= 2:
            print("🎉 CONCLUSIÓN: Los valores calculados coinciden EXCELENTEMENTE con el reporte oficial")
        elif error_promedio <= 5:
            print("✅ CONCLUSIÓN: Los valores calculados son CONSISTENTES con el reporte oficial")
        else:
            print("⚠️  CONCLUSIÓN: Se requiere REVISIÓN de algunos cálculos")

        print(f"    Error promedio: {error_promedio:.2f}%")

    except Exception as e:
        print(f"\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
