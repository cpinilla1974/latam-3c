"""
Exportar solo la nube masiva de puntos como imagen 4K con fondo negro
Usa datos REALES de PostgreSQL (tabla remitos_co2)
"""
import psycopg2
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import asyncio
from playwright.async_api import async_playwright
import os

# Configuración de colores
COLOR_PRIMARIO = '#1E3A5F'
COLOR_ACENTO = '#FF6B35'

print("🎨 Generando nube masiva de puntos en 4K...")
print("📊 Cargando datos REALES desde PostgreSQL...")

# Conectar a PostgreSQL y cargar datos reales
conn = psycopg2.connect(dbname='latam4c_db')
query = """
SELECT
    id_remito,
    origen as planta,
    empresa,
    pais,
    fecha,
    resistencia_mpa as resistencia,
    volumen,
    co2_kg_m3 as huella_co2
FROM remitos_co2
WHERE resistencia_mpa > 0 AND co2_kg_m3 > 0
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Agregar columna de año
df['fecha'] = pd.to_datetime(df['fecha'])
df['año'] = df['fecha'].dt.year

n_remitos_plot = 150000  # Máximo de puntos a visualizar

# Crear muestra para graficar (si hay más de 150k)
if len(df) > n_remitos_plot:
    df_plot = df.sample(n=n_remitos_plot, random_state=42).reset_index(drop=True)
else:
    df_plot = df.copy()

print(f"📊 Datos REALES: {len(df):,} remitos totales, {len(df_plot):,} visualizados")

# Crear figura SOLO con nube de puntos
fig = go.Figure()

# Nube masiva
scatter = go.Scatter(
    x=df_plot['resistencia'],
    y=df_plot['huella_co2'],
    mode='markers',
    marker=dict(
        size=6,
        color=df_plot['huella_co2'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title="Huella CO₂<br>(kg/m³)",
            thickness=20,
            len=0.7,
            x=1.02,
        ),
        opacity=0.7,
        line=dict(width=0.3, color='rgba(255,255,255,0.2)')
    ),
    text=[f"Resistencia: {row['resistencia']:.1f} MPa<br>" +
          f"Huella: {row['huella_co2']:.1f} kg CO₂/m³<br>" +
          f"Volumen: {row['volumen']:.1f} m³<br>" +
          f"Planta: {row['planta']}"
          for _, row in df_plot.iterrows()],
    hovertemplate='<b>%{text}</b><extra></extra>',
    name='Remitos',
    showlegend=False
)
fig.add_trace(scatter)

# Línea de tendencia (usar datos COMPLETOS)
z = np.polyfit(df['resistencia'].dropna(), df['huella_co2'].dropna(), 2)
p = np.poly1d(z)
x_trend = np.linspace(df['resistencia'].min(), df['resistencia'].max(), 200)
y_trend = p(x_trend)

fig.add_trace(
    go.Scatter(
        x=x_trend, y=y_trend,
        mode='lines',
        name='Tendencia',
        line=dict(color=COLOR_ACENTO, width=4, dash='dash'),
        hovertemplate='Tendencia: %{y:.0f} kg CO₂/m³<extra></extra>',
        showlegend=True
    )
)

# Layout minimalista para la imagen
fig.update_layout(
    title={
        'text': f'<b>Nube Masiva de Remitos</b><br><sub>{len(df_plot):,} de {len(df):,} remitos | Resistencia vs Huella CO₂</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28, 'color': 'white'}
    },
    xaxis=dict(
        title=dict(text='<b>Resistencia (MPa)</b>', font=dict(size=22, color='white')),
        tickfont=dict(size=18, color='white'),
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor='white',
    ),
    yaxis=dict(
        title=dict(text='<b>Huella CO₂ (kg/m³)</b>', font=dict(size=22, color='white')),
        tickfont=dict(size=18, color='white'),
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor='white',
    ),
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(family='Arial, sans-serif', size=16, color='white'),
    hovermode='closest',
    showlegend=True,
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(0, 0, 0, 0.8)',
        bordercolor='white',
        borderwidth=2,
        font=dict(size=16, color='white')
    ),
    margin=dict(l=120, r=150, t=150, b=120),
    width=3840,
    height=2160,
    template='plotly_dark'
)

# Guardar HTML temporal
temp_html = '/tmp/nube_puntos_temp.html'
fig.write_html(temp_html)
print(f"✅ HTML temporal creado: {temp_html}")

# Exportar a PNG 4K con Playwright
async def exportar_4k():
    exports = [
        {
            'name': '4K Ultra HD',
            'width': 3840,
            'height': 2160,
            'output': '/home/cpinilla/projects/latam-3c/docs/analisis/nube_puntos_4k.png'
        },
        {
            'name': '8K Super Resolution',
            'width': 7680,
            'height': 4320,
            'output': '/home/cpinilla/projects/latam-3c/docs/analisis/nube_puntos_8k.png'
        }
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for export_config in exports:
            print(f"\n📸 Exportando: {export_config['name']}")
            print(f"   Resolución: {export_config['width']}x{export_config['height']}")

            page = await browser.new_page(
                viewport={'width': export_config['width'], 'height': export_config['height']}
            )

            file_url = f'file://{os.path.abspath(temp_html)}'
            await page.goto(file_url, wait_until='networkidle')
            await page.wait_for_load_state('networkidle')
            await page.evaluate('() => new Promise(resolve => setTimeout(resolve, 2000))')

            # Fondo negro (por seguridad)
            await page.add_style_tag(content="""
                body, html {
                    background-color: #000000 !important;
                }
                .plotly {
                    background-color: #000000 !important;
                }
            """)

            await page.evaluate('() => new Promise(resolve => setTimeout(resolve, 500))')

            await page.screenshot(path=export_config['output'], full_page=False)
            print(f"   ✅ Guardado: {export_config['output']}")

            if os.path.exists(export_config['output']):
                size = os.path.getsize(export_config['output']) / (1024*1024)
                print(f"   Tamaño: {size:.1f} MB")

            await page.close()

        await browser.close()

    # Resumen
    print("\n" + "="*80)
    print("✨ EXPORTACIÓN COMPLETADA")
    print("="*80)
    print("\n📊 Archivos generados:")
    for export_config in exports:
        if os.path.exists(export_config['output']):
            size = os.path.getsize(export_config['output']) / (1024*1024)
            print(f"\n  {export_config['name']}")
            print(f"    📍 {export_config['output']}")
            print(f"    📐 {export_config['width']}x{export_config['height']}")
            print(f"    💾 {size:.1f} MB")

print("\n🚀 Exportando a imágenes de máxima resolución con fondo negro...")
asyncio.run(exportar_4k())

print("\n🎉 Nube de puntos exportada exitosamente!")
