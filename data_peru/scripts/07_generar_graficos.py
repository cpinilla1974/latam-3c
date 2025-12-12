#!/usr/bin/env python3
"""
Genera gráficos del Reporte de Seguimiento 2010-2023 del Sector Cemento Perú.

Recrea los gráficos principales del reporte usando los agregados nacionales calculados.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
import seaborn as sns

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Rutas
DB_CONSOLIDADA = Path(__file__).parent.parent / "peru_consolidado.db"
DIR_GRAFICOS = Path(__file__).parent.parent / "graficos"

# Años del reporte oficial (se actualizará con años disponibles)
AÑOS_REPORTE = [2010, 2014, 2019, 2020, 2021]

def cargar_agregados():
    """Carga todos los agregados nacionales."""
    print(f"\n📊 Cargando agregados nacionales...")

    conn = sqlite3.connect(DB_CONSOLIDADA)

    query = """
        SELECT
            codigo_indicador,
            año,
            valor_nacional,
            tipo_agregacion,
            num_empresas
        FROM agregados_nacionales
        ORDER BY codigo_indicador, año
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"   ✅ {len(df):,} agregados cargados")
    print(f"   📅 Rango: {df['año'].min()} - {df['año'].max()}")

    return df

def crear_directorio_graficos():
    """Crea estructura de directorios para los gráficos."""
    directorios = [
        DIR_GRAFICOS / "grupo1_produccion",
        DIR_GRAFICOS / "grupo2_contenido_clinker",
        DIR_GRAFICOS / "grupo3_emisiones",
        DIR_GRAFICOS / "grupo4_eficiencia",
        DIR_GRAFICOS / "grupo5_electricos",
    ]

    for directorio in directorios:
        directorio.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Directorios de gráficos creados en: {DIR_GRAFICOS}")

def grafico_produccion_clinker(df):
    """Gráfico 1.1: Producción de Clínker 2010-2023"""
    print(f"\n📈 Generando: Producción de Clínker...")

    datos = df[df['codigo_indicador'] == '8'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    # Convertir a millones de toneladas
    datos['valor_Mt'] = datos['valor_nacional'] / 1_000_000

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(datos['año'], datos['valor_Mt'], color='steelblue', alpha=0.7, width=1.5)
    ax.plot(datos['año'], datos['valor_Mt'], marker='o', color='darkblue', linewidth=2)

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_Mt'] + 1, f"{row['valor_Mt']:.2f}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Millones de toneladas (Mt)', fontweight='bold')
    ax.set_title('Producción de Clínker - Perú\n2010-2023', fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo1_produccion" / "01_produccion_clinker.png", dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo1_produccion/01_produccion_clinker.png")

def grafico_produccion_cemento(df):
    """Gráfico 1.2: Producción de Cemento y Cementitious"""
    print(f"\n📈 Generando: Producción de Cemento y Cementitious...")

    datos_cemento = df[df['codigo_indicador'] == '20'].copy()
    datos_cementitious = df[df['codigo_indicador'] == '21a'].copy()

    datos_cemento = datos_cemento[datos_cemento['año'].isin(AÑOS_REPORTE)]
    datos_cementitious = datos_cementitious[datos_cementitious['año'].isin(AÑOS_REPORTE)]

    if len(datos_cemento) == 0 or len(datos_cementitious) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    # Convertir a millones de toneladas
    datos_cemento['valor_Mt'] = datos_cemento['valor_nacional'] / 1_000_000
    datos_cementitious['valor_Mt'] = datos_cementitious['valor_nacional'] / 1_000_000

    fig, ax = plt.subplots(figsize=(10, 6))

    width = 0.35
    x = range(len(AÑOS_REPORTE))

    ax.bar([i - width/2 for i in x], datos_cemento['valor_Mt'], width,
           label='Producción Cemento', color='coral', alpha=0.8)
    ax.bar([i + width/2 for i in x], datos_cementitious['valor_Mt'], width,
           label='Producción Cementitious', color='steelblue', alpha=0.8)

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Millones de toneladas (Mt)', fontweight='bold')
    ax.set_title('Producción de Cemento y Cementitious - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(AÑOS_REPORTE)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo1_produccion" / "02_produccion_cemento_cementitious.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo1_produccion/02_produccion_cemento_cementitious.png")

def grafico_factor_clinker(df):
    """Gráfico 2.1: Factor Clínker (Contenido de clínker en cemento)"""
    print(f"\n📈 Generando: Factor Clínker...")

    datos = df[df['codigo_indicador'] == '92a'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    # Convertir a porcentaje
    datos['valor_pct'] = datos['valor_nacional'] * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(datos['año'], datos['valor_pct'], marker='o', color='darkgreen',
            linewidth=2.5, markersize=8)
    ax.fill_between(datos['año'], datos['valor_pct'], alpha=0.3, color='lightgreen')

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_pct'] + 0.5, f"{row['valor_pct']:.1f}%",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Porcentaje (%)', fontweight='bold')
    ax.set_title('Factor Clínker (Contenido de clínker en cemento) - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.set_ylim(75, 90)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo2_contenido_clinker" / "01_factor_clinker.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo2_contenido_clinker/01_factor_clinker.png")

def grafico_emisiones_clinker(df):
    """Gráfico 3.1: Emisiones CO₂ Clínker"""
    print(f"\n📈 Generando: Emisiones CO₂ Clínker...")

    datos = df[df['codigo_indicador'] == '60a'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(datos['año'], datos['valor_nacional'], color='crimson', alpha=0.7, width=1.5)
    ax.plot(datos['año'], datos['valor_nacional'], marker='s', color='darkred',
            linewidth=2, markersize=7)

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_nacional'] + 5, f"{row['valor_nacional']:.1f}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('kg CO₂/t clínker', fontweight='bold')
    ax.set_title('Emisiones Netas CO₂ del Clínker - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo3_emisiones" / "01_emisiones_clinker.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo3_emisiones/01_emisiones_clinker.png")

def grafico_emisiones_cementitious(df):
    """Gráfico 3.2: Emisiones CO₂ Cementitious"""
    print(f"\n📈 Generando: Emisiones CO₂ Cementitious...")

    datos = df[df['codigo_indicador'] == '62a'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(datos['año'], datos['valor_nacional'], color='orangered', alpha=0.7, width=1.5)
    ax.plot(datos['año'], datos['valor_nacional'], marker='D', color='darkred',
            linewidth=2, markersize=7)

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_nacional'] + 5, f"{row['valor_nacional']:.1f}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('kg CO₂/t cementitious', fontweight='bold')
    ax.set_title('Emisiones Netas CO₂ del Cementitious - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo3_emisiones" / "02_emisiones_cementitious.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo3_emisiones/02_emisiones_cementitious.png")

def grafico_eficiencia_termica(df):
    """Gráfico 4.1: Eficiencia Térmica"""
    print(f"\n📈 Generando: Eficiencia Térmica...")

    datos = df[df['codigo_indicador'] == '93'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(datos['año'], datos['valor_nacional'], marker='o', color='purple',
            linewidth=2.5, markersize=8)
    ax.fill_between(datos['año'], datos['valor_nacional'], alpha=0.2, color='purple')

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_nacional'] + 20, f"{row['valor_nacional']:.1f}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('MJ/t clínker', fontweight='bold')
    ax.set_title('Eficiencia Térmica (Consumo Térmico Específico) - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo4_eficiencia" / "01_eficiencia_termica.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo4_eficiencia/01_eficiencia_termica.png")

def grafico_consumo_electrico(df):
    """Gráfico 5.1: Consumo Eléctrico Específico"""
    print(f"\n📈 Generando: Consumo Eléctrico Específico...")

    datos = df[df['codigo_indicador'] == '97'].copy()
    datos = datos[datos['año'].isin(AÑOS_REPORTE)]

    if len(datos) == 0:
        print("   ⚠️  No hay datos disponibles")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(datos['año'], datos['valor_nacional'], color='teal', alpha=0.7, width=1.5)
    ax.plot(datos['año'], datos['valor_nacional'], marker='o', color='darkcyan',
            linewidth=2, markersize=7)

    # Etiquetas de valores
    for _, row in datos.iterrows():
        ax.text(row['año'], row['valor_nacional'] + 2, f"{row['valor_nacional']:.1f}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('kWh/t cementitious', fontweight='bold')
    ax.set_title('Consumo Eléctrico Específico - Perú\n2010-2023',
                 fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "grupo5_electricos" / "01_consumo_electrico_especifico.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: grupo5_electricos/01_consumo_electrico_especifico.png")

def grafico_resumen_evolucion(df):
    """Gráfico resumen: Evolución de indicadores clave normalizados"""
    print(f"\n📈 Generando: Gráfico resumen de evolución...")

    # Indicadores clave para comparar
    indicadores = {
        '8': 'Producción Clínker',
        '92a': 'Factor Clínker',
        '60a': 'Emisiones CO₂ Clínker',
        '93': 'Eficiencia Térmica',
        '97': 'Consumo Eléctrico'
    }

    fig, ax = plt.subplots(figsize=(12, 7))

    for codigo, nombre in indicadores.items():
        datos = df[df['codigo_indicador'] == codigo].copy()
        datos = datos[datos['año'].isin(AÑOS_REPORTE)]

        if len(datos) == 0:
            continue

        # Normalizar al valor de 2010 (índice base 100)
        valor_base = datos[datos['año'] == 2010]['valor_nacional'].iloc[0]
        datos['indice'] = (datos['valor_nacional'] / valor_base) * 100

        ax.plot(datos['año'], datos['indice'], marker='o', linewidth=2, label=nombre)

    ax.axhline(y=100, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Base 2010')
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Índice (2010 = 100)', fontweight='bold')
    ax.set_title('Evolución de Indicadores Clave - Perú\n(Índice base 2010 = 100)',
                 fontweight='bold', fontsize=13)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(DIR_GRAFICOS / "resumen_evolucion_indicadores.png",
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   ✅ Guardado: resumen_evolucion_indicadores.png")

def generar_reporte_html(df):
    """Genera un reporte HTML con todos los gráficos."""
    print(f"\n📄 Generando reporte HTML...")

    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Seguimiento 2010-2023 - Sector Cemento Perú</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 40px;
            border-left: 5px solid #3498db;
            padding-left: 10px;
        }
        .grafico {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        .info {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #7f8c8d;
            border-top: 1px solid #bdc3c7;
        }
    </style>
</head>
<body>
    <h1>Reporte de Seguimiento 2010-2023<br>Sector Cemento Perú</h1>

    <div class="info">
        <p><strong>Datos consolidados de 3 empresas:</strong> Pacasmayo, Yura, UNACEM</p>
        <p><strong>Años del reporte:</strong> 2010, 2014, 2019, 2021, 2023</p>
        <p><strong>Total agregados nacionales:</strong> 269 indicadores calculados (2010-2030)</p>
    </div>

    <h2>Grupo 1: Producción de Clínker y Cemento</h2>
    <div class="grafico">
        <img src="grupo1_produccion/01_produccion_clinker.png" alt="Producción Clínker">
    </div>
    <div class="grafico">
        <img src="grupo1_produccion/02_produccion_cemento_cementitious.png" alt="Producción Cemento">
    </div>

    <h2>Grupo 2: Contenido de Clínker</h2>
    <div class="grafico">
        <img src="grupo2_contenido_clinker/01_factor_clinker.png" alt="Factor Clínker">
    </div>

    <h2>Grupo 3: Emisiones CO₂</h2>
    <div class="grafico">
        <img src="grupo3_emisiones/01_emisiones_clinker.png" alt="Emisiones Clínker">
    </div>
    <div class="grafico">
        <img src="grupo3_emisiones/02_emisiones_cementitious.png" alt="Emisiones Cementitious">
    </div>

    <h2>Grupo 4: Eficiencia Energética</h2>
    <div class="grafico">
        <img src="grupo4_eficiencia/01_eficiencia_termica.png" alt="Eficiencia Térmica">
    </div>

    <h2>Grupo 5: Indicadores Eléctricos</h2>
    <div class="grafico">
        <img src="grupo5_electricos/01_consumo_electrico_especifico.png" alt="Consumo Eléctrico">
    </div>

    <h2>Resumen</h2>
    <div class="grafico">
        <img src="resumen_evolucion_indicadores.png" alt="Evolución Indicadores">
    </div>

    <div class="footer">
        <p>Generado automáticamente desde peru_consolidado.db</p>
        <p>Datos extraídos de las bases de datos de Pacasmayo, Yura y UNACEM</p>
    </div>
</body>
</html>
"""

    output_path = DIR_GRAFICOS / "reporte_completo.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"   ✅ Reporte HTML guardado: {output_path}")

def main():
    """Función principal."""
    print("\n" + "🎨 GENERACIÓN DE GRÁFICOS DEL REPORTE ".center(80, "="))

    # Verificar que existe la base de datos
    if not DB_CONSOLIDADA.exists():
        print(f"❌ Error: Base de datos consolidada no encontrada: {DB_CONSOLIDADA}")
        return

    try:
        # Crear directorios
        crear_directorio_graficos()

        # Cargar agregados
        df = cargar_agregados()

        if len(df) == 0:
            print(f"\n⚠️  No hay agregados para graficar")
            return

        # Generar gráficos por grupo
        print(f"\n{'='*80}")
        print("GENERANDO GRÁFICOS POR GRUPO")
        print(f"{'='*80}")

        grafico_produccion_clinker(df)
        grafico_produccion_cemento(df)
        grafico_factor_clinker(df)
        grafico_emisiones_clinker(df)
        grafico_emisiones_cementitious(df)
        grafico_eficiencia_termica(df)
        grafico_consumo_electrico(df)
        grafico_resumen_evolucion(df)

        # Generar reporte HTML
        generar_reporte_html(df)

        print(f"\n{'='*80}")
        print("✅ GENERACIÓN DE GRÁFICOS COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}\n")

        print(f"📊 Resumen:")
        print(f"   - Gráficos generados: 8")
        print(f"   - Ubicación: {DIR_GRAFICOS}")
        print(f"   - Reporte HTML: {DIR_GRAFICOS / 'reporte_completo.html'}")
        print(f"\n💡 Abre el reporte HTML en tu navegador para ver todos los gráficos")

    except Exception as e:
        print(f"\n❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
