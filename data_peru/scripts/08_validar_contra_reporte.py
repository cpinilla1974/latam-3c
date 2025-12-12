#!/usr/bin/env python3
"""
Valida los agregados calculados contra los valores oficiales del reporte PDF.

Compara los valores de los años clave (2010, 2014, 2019, 2021, 2023)
contra las cifras publicadas en el Reporte de Seguimiento oficial.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Rutas
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"

# Años reportados oficialmente
AÑOS_REPORTE = [2010, 2014, 2019, 2021, 2023]

# Valores oficiales del reporte PDF (extraídos manualmente de los gráficos)
VALORES_OFICIALES = {
    # Grupo 1: Producción
    '8': {  # Producción Clínker (Mt)
        2010: 6.16,
        2014: 8.80,
        2019: 9.13,
        2021: 9.94,
        2023: 9.45
    },
    '11': {  # Consumo Clínker (Mt)
        2010: 6.74,
        2014: 8.44,
        2019: 7.95,
        2021: 9.76,
        2023: 8.41
    },
    '20': {  # Producción Cemento (Mt)
        2010: 8.20,
        2014: 10.60,
        2019: 10.47,
        2021: 12.72,
        2023: 11.42
    },
    '21a': {  # Producción Cementitious (Mt)
        2010: 7.62,
        2014: 10.96,
        2019: 11.64,
        2021: 12.90,
        2023: 12.45
    },

    # Grupo 2: Contenido Clínker
    '92a': {  # Factor Clínker (%)
        2010: 82,
        2014: 80,
        2019: 76,
        2021: 77,
        2023: 74
    },

    # Grupo 3: Emisiones
    '60a': {  # Emisiones CO₂ Clínker (kg CO₂/t)
        2010: 798,
        2014: 791,
        2019: 775,
        2021: 773,
        2023: 773
    },
    '62a': {  # Emisiones CO₂ Cementitious (kg CO₂/t)
        2010: 645,
        2014: 635,
        2019: 607,
        2021: 596,
        2023: 587
    },

    # Grupo 4: Eficiencia
    '93': {  # Eficiencia Térmica (MJ/t clínker)
        2010: 3545,
        2014: 3403,
        2019: 3398,
        2021: 3386,
        2023: 3351
    },

    # Grupo 5: Eléctricos
    '97': {  # Consumo Eléctrico Específico (kWh/t)
        2010: 110,
        2014: 109,
        2019: 115,
        2021: 105,
        2023: 108
    },
}

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
        WHERE año IN (2010, 2014, 2019, 2021, 2023)
        ORDER BY codigo_indicador, año
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"   ✅ {len(df):,} agregados cargados para validación")

    return df

def convertir_unidades(codigo, valor):
    """Convierte valores a las unidades del reporte oficial."""
    # Convertir toneladas a millones de toneladas
    if codigo in ['8', '11', '20', '21a']:
        return valor / 1_000_000

    # Factor Clínker: convertir decimal a porcentaje
    if codigo == '92a':
        return valor * 100

    # Otros indicadores ya están en las unidades correctas
    return valor

def comparar_valores(df_calculados, valores_oficiales):
    """Compara valores calculados vs oficiales y genera reporte."""
    print(f"\n{'='*100}")
    print("VALIDACIÓN CONTRA REPORTE OFICIAL")
    print(f"{'='*100}\n")

    resultados = []
    errores_totales = []

    for codigo, años_oficiales in valores_oficiales.items():
        print(f"\n📌 Indicador [{codigo}]")
        print(f"{'Año':<8} {'Oficial':<15} {'Calculado':<15} {'Diferencia':<15} {'Error %':<10} {'Estado'}")
        print("-" * 100)

        for año, valor_oficial in años_oficiales.items():
            # Buscar valor calculado
            df_valor = df_calculados[
                (df_calculados['codigo_indicador'] == codigo) &
                (df_calculados['año'] == año)
            ]

            if len(df_valor) == 0:
                print(f"{año:<8} {valor_oficial:<15.2f} {'NO CALCULADO':<15} {'-':<15} {'-':<10} ❌ FALTANTE")
                continue

            valor_calculado_raw = df_valor.iloc[0]['valor_nacional']
            valor_calculado = convertir_unidades(codigo, valor_calculado_raw)

            # Calcular diferencia y error porcentual
            diferencia = valor_calculado - valor_oficial
            error_pct = abs(diferencia / valor_oficial * 100) if valor_oficial != 0 else 0

            # Determinar estado (tolerancia 2%)
            if error_pct <= 2:
                estado = "✅ OK"
            elif error_pct <= 5:
                estado = "⚠️  ACEPTABLE"
            else:
                estado = "❌ REVISAR"

            print(f"{año:<8} {valor_oficial:<15.2f} {valor_calculado:<15.2f} {diferencia:<15.2f} {error_pct:<10.2f} {estado}")

            resultados.append({
                'codigo': codigo,
                'año': año,
                'oficial': valor_oficial,
                'calculado': valor_calculado,
                'diferencia': diferencia,
                'error_pct': error_pct
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
        # Cargar agregados calculados
        df_calculados = cargar_agregados_calculados()

        # Comparar valores
        resultados, errores = comparar_valores(df_calculados, VALORES_OFICIALES)

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
