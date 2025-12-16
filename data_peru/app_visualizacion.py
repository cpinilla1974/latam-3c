#!/usr/bin/env python3
"""
Aplicación Streamlit para visualizar datos del Reporte de Seguimiento Perú 2010-2023
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Configuración de página
st.set_page_config(
    page_title="Análisis Sector Cemento Perú",
    page_icon="🏭",
    layout="wide"
)

# Rutas
DB_PATH = Path(__file__).parent / "peru_consolidado.db"
GRAFICOS_PATH = Path(__file__).parent / "graficos"
REPORTES_HR_PATH = Path(__file__).parent / "reportes_hr"

# Metadatos de indicadores
INDICADORES_INFO = {
    '8': {'nombre': 'Producción Clínker', 'unidad': 't', 'grupo': 'Producción'},
    '11': {'nombre': 'Consumo Clínker', 'unidad': 't', 'grupo': 'Producción'},
    '20': {'nombre': 'Producción Cemento', 'unidad': 't', 'grupo': 'Producción'},
    '21a': {'nombre': 'Producción Cementitious', 'unidad': 't', 'grupo': 'Producción'},
    '92a': {'nombre': 'Factor Clínker', 'unidad': 'decimal', 'grupo': 'Contenido Clínker'},
    '12': {'nombre': 'Puzolana', 'unidad': 'decimal', 'grupo': 'Contenido Clínker'},
    '13': {'nombre': 'Escoria', 'unidad': 'decimal', 'grupo': 'Contenido Clínker'},
    '14': {'nombre': 'Ceniza volante', 'unidad': 'decimal', 'grupo': 'Contenido Clínker'},
    '16': {'nombre': 'Caliza', 'unidad': 'decimal', 'grupo': 'Contenido Clínker'},
    '60': {'nombre': 'Emisiones CO₂ Proceso', 'unidad': 't CO₂', 'grupo': 'Emisiones'},
    '60a': {'nombre': 'Emisiones CO₂ Clínker', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '60b': {'nombre': 'Emisiones CO₂ Combustibles', 'unidad': 't CO₂', 'grupo': 'Emisiones'},
    '62': {'nombre': 'Emisiones Netas CO₂ Cementitious', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '62a': {'nombre': 'Emisiones CO₂ Cementitious', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '63': {'nombre': 'Emisión Bruta Cemento Eq.', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '73': {'nombre': 'Emisiones Indirectas', 'unidad': 't CO₂', 'grupo': 'Emisiones'},
    '74': {'nombre': 'Emisión Específica Neta', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '75': {'nombre': 'Emisión Neta Cemento Eq.', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '93': {'nombre': 'Eficiencia Térmica', 'unidad': 'MJ/t clínker', 'grupo': 'Eficiencia'},
    '97': {'nombre': 'Consumo Eléctrico Específico', 'unidad': 'kWh/t', 'grupo': 'Eléctricos'},
    '1151': {'nombre': 'Energía Fósil', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
    '1152': {'nombre': 'Energía Biomasa', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
    '1155': {'nombre': 'Energía Residuos', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
}

# Metas Hoja de Ruta 2030
METAS_HR_2030 = {
    '62': {
        'meta_2030': 520,
        'unidad': 'kgCO₂/t cementitious',
        'nombre': 'Emisiones Netas CO₂ Cementitious',
        'tipo': 'max',
        'baseline_2019': 588,
        'reduccion_hr_pct': 11.6,
    },
    '92a': {
        'meta_2030': 0.70,
        'unidad': 'ratio',
        'nombre': 'Factor Clínker',
        'tipo': 'max',
        'baseline_2019': 0.7595,
        'meta_2050': 0.63,
    },
    '93': {
        'meta_2030': 3301,
        'unidad': 'MJ/t clínker',
        'nombre': 'Eficiencia Térmica',
        'tipo': 'max',
        'baseline_2019': 3397.68,
        'meta_2050': 3260,
    },
    '60a': {
        'meta_2030': 479.2,
        'unidad': 'kgCO₂/t clínker',
        'nombre': 'Emisiones Netas CO₂ Clínker',
        'tipo': 'max',
        'baseline_2019': 504.4,
        'reduccion_estimada_pct': 5.0,
    },
    '97': {
        'meta_2030': 102.6,
        'unidad': 'kWh/t cementitious',
        'nombre': 'Consumo Eléctrico Específico',
        'tipo': 'max',
        'reduccion_estimada_pct': 10.0,
    },
    '63': {
        'meta_2030': 578.4,
        'unidad': 'kgCO₂/t cemento eq',
        'nombre': 'Emisión Bruta Cemento Equivalente',
        'tipo': 'max',
        'reduccion_estimada_pct': 10.0,
    },
    '74': {
        'meta_2030': 586.5,
        'unidad': 'kgCO₂/t cementitious',
        'nombre': 'Emisión Específica Neta (Cementitious)',
        'tipo': 'max',
        'reduccion_estimada_pct': 10.0,
    },
    '75': {
        'meta_2030': 578.4,
        'unidad': 'kgCO₂/t cemento eq',
        'nombre': 'Emisión Neta Cemento Equivalente',
        'tipo': 'max',
        'reduccion_estimada_pct': 10.0,
    },
    '60': {
        'meta_2030': 2664.4,
        'unidad': 't CO₂/año',
        'nombre': 'Emisiones Netas Combustibles',
        'tipo': 'max',
        'reduccion_estimada_pct': 5.0,
        'baseline_año': 2017,
    },
    '73': {
        'meta_2030': 2524.2,
        'unidad': 't CO₂/año',
        'nombre': 'Emisiones Indirectas Alcance 2',
        'tipo': 'max',
        'reduccion_estimada_pct': 10.0,
        'baseline_año': 2017,
    },
}

def cargar_agregados_nacionales():
    """Carga agregados nacionales desde la base de datos."""
    conn = sqlite3.connect(DB_PATH)
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
    return df

def cargar_datos_empresas():
    """Carga datos por empresa (nivel 2: suma de plantas)."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT
            e.codigo_empresa,
            de.codigo_indicador,
            de.año,
            de.valor
        FROM datos_empresas de
        JOIN empresas e ON de.id_empresa = e.id_empresa
        WHERE de.mes IS NULL
        ORDER BY de.año, e.codigo_empresa, de.codigo_indicador
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def cargar_datos_pdf():
    """Carga datos extraídos del PDF de referencia."""
    conn = sqlite3.connect(DB_PATH)
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
    return df

def crear_grafico_trayectoria_hr(df_agregados, codigo_indicador, meta_info):
    """Crea gráfico interactivo de trayectoria hacia meta 2030 con Plotly."""
    df_ind = df_agregados[df_agregados['codigo_indicador'] == codigo_indicador].copy()

    if len(df_ind) == 0:
        return None

    df_ind = df_ind.sort_values('año')

    fig = go.Figure()

    # Datos históricos
    fig.add_trace(go.Scatter(
        x=df_ind['año'],
        y=df_ind['valor_nacional'],
        mode='lines+markers',
        name='Valor observado',
        line=dict(width=3, color='#3498db'),
        marker=dict(size=10, color='#3498db'),
        hovertemplate='Año: %{x}<br>Valor: %{y:.2f}<extra></extra>'
    ))

    # Meta 2030 y Trayectoria
    meta = meta_info.get('meta_2030')
    año_base = meta_info.get('baseline_año', 2019)

    if año_base in df_ind['año'].values:
        valor_base = df_ind[df_ind['año'] == año_base]['valor_nacional'].values[0]
    elif 'baseline_2019' in meta_info:
        valor_base = meta_info['baseline_2019']
    else:
        valor_base = df_ind['valor_nacional'].iloc[0]
        año_base = df_ind['año'].iloc[0]

    if meta:
        # Línea horizontal de meta (como trace para que aparezca en leyenda)
        x_min = df_ind['año'].min() - 1
        x_max = 2031
        fig.add_trace(go.Scatter(
            x=[x_min, x_max],
            y=[meta, meta],
            mode='lines',
            name=f'Meta 2030 ({meta:.1f})',
            line=dict(width=3, color='#27ae60', dash='dash'),
            hovertemplate=f'Meta 2030: {meta:.2f}<extra></extra>'
        ))

        # Trayectoria requerida (desde año base a 2030)
        fig.add_trace(go.Scatter(
            x=[año_base, 2030],
            y=[valor_base, meta],
            mode='lines',
            name=f'Trayectoria requerida',
            line=dict(width=2, color='#e74c3c', dash='dot'),
            hovertemplate='Año: %{x}<br>Valor: %{y:.2f}<extra></extra>'
        ))

    # Layout
    nombre = meta_info.get('nombre', codigo_indicador)
    unidad = meta_info.get('unidad', '')

    fig.update_layout(
        title=dict(
            text=f"<b>Trayectoria: {nombre}</b><br><span style='font-size:12px'>[{codigo_indicador}]</span>",
            font=dict(size=14)
        ),
        xaxis_title="Año",
        yaxis_title=f"{nombre} ({unidad})",
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            font=dict(size=9)
        ),
        xaxis=dict(
            range=[df_ind['año'].min() - 0.5, 2031],
            dtick=2
        ),
        yaxis=dict(autorange=True),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

    return fig


def crear_grafico_progreso_metas(df_agregados):
    """Crea gráfico interactivo de barras con progreso hacia metas 2030."""
    resultados = []

    for codigo, meta_info in METAS_HR_2030.items():
        df_ind = df_agregados[df_agregados['codigo_indicador'] == codigo].copy()

        if len(df_ind) == 0:
            continue

        df_ind = df_ind.sort_values('año')
        valor_actual = df_ind['valor_nacional'].iloc[-1]
        año_actual = df_ind['año'].iloc[-1]

        # Valor baseline
        if 2019 in df_ind['año'].values:
            valor_2019 = df_ind[df_ind['año'] == 2019]['valor_nacional'].values[0]
        else:
            valor_2019 = meta_info.get('baseline_2019', df_ind['valor_nacional'].iloc[0])

        meta_2030 = meta_info.get('meta_2030')

        if meta_2030 and valor_2019:
            reduccion_necesaria = valor_2019 - meta_2030
            reduccion_lograda = valor_2019 - valor_actual

            if reduccion_necesaria != 0:
                progreso_pct = (reduccion_lograda / reduccion_necesaria) * 100
            else:
                progreso_pct = 100 if valor_actual <= meta_2030 else 0

            resultados.append({
                'codigo': codigo,
                'nombre': meta_info['nombre'],
                'progreso': progreso_pct,
                'valor_actual': valor_actual,
                'meta': meta_2030,
                'año': año_actual
            })

    if not resultados:
        return None

    df_prog = pd.DataFrame(resultados)
    df_prog = df_prog.sort_values('progreso', ascending=True)

    # Colores según progreso
    colores = []
    for p in df_prog['progreso']:
        if p >= 100:
            colores.append('#27ae60')  # Verde
        elif p >= 50:
            colores.append('#f39c12')  # Naranja
        elif p >= 0:
            colores.append('#e74c3c')  # Rojo
        else:
            colores.append('#8e44ad')  # Morado (retroceso)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_prog['nombre'],
        x=df_prog['progreso'],
        orientation='h',
        marker_color=colores,
        text=[f"{p:.1f}%" for p in df_prog['progreso']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Progreso: %{x:.1f}%<extra></extra>'
    ))

    # Línea de meta (100%)
    fig.add_vline(x=100, line_dash="dash", line_color="#2c3e50", line_width=2)

    fig.update_layout(
        title="<b>Seguimiento HR Perú: Progreso hacia Metas 2030</b>",
        xaxis_title="Progreso hacia Meta 2030 (%)",
        yaxis_title="",
        height=500,
        xaxis=dict(range=[-20, 150]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

    return fig


def crear_grafico_serie_temporal(df_agregados, df_empresas, indicador, mostrar_empresas=True, df_pdf=None,
                                mostrar_pdf=True, mostrar_calculado=True,
                                mostrar_pacas=True, mostrar_yura=True, mostrar_unacem=True):
    """Crea gráfico de serie temporal para un indicador con datos por empresa, agregado y PDF."""
    df_ind = df_agregados[df_agregados['codigo_indicador'] == indicador].copy()

    if len(df_ind) == 0:
        return None

    info = INDICADORES_INFO.get(indicador, {})
    nombre = info.get('nombre', indicador)
    unidad = info.get('unidad', '')

    fig = go.Figure()

    # Si se solicita, agregar datos por empresa con control individual
    if mostrar_empresas:
        df_empresas_ind = df_empresas[df_empresas['codigo_indicador'] == indicador].copy()

        empresas_config = {
            'PACAS': {'mostrar': mostrar_pacas, 'color': '#E63946'},
            'YURA': {'mostrar': mostrar_yura, 'color': '#F77F00'},
            'UNACEM': {'mostrar': mostrar_unacem, 'color': '#06A77D'}
        }

        for empresa in sorted(df_empresas_ind['codigo_empresa'].unique()):
            config = empresas_config.get(empresa, {'mostrar': True, 'color': None})
            if config['mostrar']:
                df_emp = df_empresas_ind[df_empresas_ind['codigo_empresa'] == empresa]
                fig.add_trace(go.Scatter(
                    x=df_emp['año'],
                    y=df_emp['valor'],
                    mode='lines+markers',
                    name=empresa,
                    line=dict(width=2, dash='dot', color=config['color']),
                    marker=dict(size=6, color=config['color']),
                    opacity=0.6
                ))

    # Agregar línea del PDF si está disponible y activado
    if mostrar_pdf and df_pdf is not None:
        df_pdf_ind = df_pdf[df_pdf['codigo_indicador'] == indicador].copy()
        if len(df_pdf_ind) > 0:
            unidad_pdf = df_pdf_ind.iloc[0]['unidad']

            # Convertir valores del PDF a las mismas unidades que el gráfico
            if unidad_pdf == 'Mt' and indicador in ['8', '11', '20', '21a']:
                df_pdf_ind['valor_grafico'] = df_pdf_ind['valor'] * 1_000_000  # Mt a toneladas
            elif unidad_pdf == 'fracción' and indicador == '92a':
                df_pdf_ind['valor_grafico'] = df_pdf_ind['valor']  # Mantener en fracción
            else:
                df_pdf_ind['valor_grafico'] = df_pdf_ind['valor']

            fig.add_trace(go.Scatter(
                x=df_pdf_ind['año'],
                y=df_pdf_ind['valor_grafico'],
                mode='lines+markers',
                name='PDF (Referencia)',
                line=dict(width=3, color='#2E86AB'),
                marker=dict(size=10, symbol='circle', color='#2E86AB'),
                opacity=1.0
            ))

    # Agregar línea del agregado nacional si está activado
    if mostrar_calculado:
        fig.add_trace(go.Scatter(
            x=df_ind['año'],
            y=df_ind['valor_nacional'],
            mode='lines+markers',
            name='Calculado',
            line=dict(width=4, color='#A23B72', dash='dash'),
            marker=dict(size=10, color='#A23B72'),
            opacity=1.0
        ))

    fig.update_layout(
        title=f"{nombre}",
        xaxis_title="Año",
        yaxis_title=unidad if unidad else "Valor",
        yaxis=dict(rangemode='tozero'),  # Forzar que el eje Y comience desde 0
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    return fig

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

st.title("🏭 Análisis Sector Cemento Perú 2010-2023")
st.markdown("**Reporte de Seguimiento - Sistema de Medición y Reporte**")

# Sidebar
with st.sidebar:
    st.header("Navegación")
    pagina = st.radio(
        "Selecciona una sección:",
        ["📊 Dashboard General", "🎯 Metas HR 2030", "📈 Indicadores FICEM", "🗄️ Explorador BD"]
    )

    st.markdown("---")
    st.markdown("### Sobre este análisis")
    st.markdown("""
    Análisis de datos del sector cemento de Perú (2010-2023) según TDR Ítem 2.

    **Empresas:**
    - Pacasmayo
    - Yura
    - UNACEM
    """)

# Cargar datos
df_agregados = cargar_agregados_nacionales()
df_empresas = cargar_datos_empresas()
df_pdf = cargar_datos_pdf()

# ============================================================================
# PÁGINA 1: DASHBOARD GENERAL
# ============================================================================

if pagina == "📊 Dashboard General":
    st.header("Dashboard General")

    # KPIs principales
    años_disponibles = sorted(df_agregados['año'].unique())
    año_actual = max(años_disponibles)
    año_base = min(años_disponibles)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        prod_clinker = df_agregados[
            (df_agregados['codigo_indicador'] == '8') &
            (df_agregados['año'] == año_actual)
        ]['valor_nacional'].values[0] if len(df_agregados[
            (df_agregados['codigo_indicador'] == '8') &
            (df_agregados['año'] == año_actual)
        ]) > 0 else 0
        st.metric(
            "Producción Clínker",
            f"{prod_clinker/1_000_000:.2f} Mt",
            f"Año {año_actual}"
        )

    with col2:
        prod_cemento = df_agregados[
            (df_agregados['codigo_indicador'] == '20') &
            (df_agregados['año'] == año_actual)
        ]['valor_nacional'].values[0] if len(df_agregados[
            (df_agregados['codigo_indicador'] == '20') &
            (df_agregados['año'] == año_actual)
        ]) > 0 else 0
        st.metric(
            "Producción Cemento",
            f"{prod_cemento/1_000_000:.2f} Mt",
            f"Año {año_actual}"
        )

    with col3:
        factor_clinker = df_agregados[
            (df_agregados['codigo_indicador'] == '92a') &
            (df_agregados['año'] == año_actual)
        ]['valor_nacional'].values[0] if len(df_agregados[
            (df_agregados['codigo_indicador'] == '92a') &
            (df_agregados['año'] == año_actual)
        ]) > 0 else 0
        st.metric(
            "Factor Clínker",
            f"{factor_clinker*100:.1f}%",
            f"Año {año_actual}"
        )

    with col4:
        emisiones = df_agregados[
            (df_agregados['codigo_indicador'] == '62a') &
            (df_agregados['año'] == año_actual)
        ]['valor_nacional'].values[0] if len(df_agregados[
            (df_agregados['codigo_indicador'] == '62a') &
            (df_agregados['año'] == año_actual)
        ]) > 0 else 0
        st.metric(
            "Emisiones CO₂ Cementitious",
            f"{emisiones:.0f} kg/t",
            f"Año {año_actual}"
        )

    st.markdown("---")

    # Controles para mostrar/ocultar líneas
    st.subheader("Controles de Visualización")

    col_ctrl1, col_ctrl2 = st.columns(2)

    with col_ctrl1:
        st.markdown("**Agregados:**")
        mostrar_pdf = st.checkbox("PDF (Referencia)", value=True, key="mostrar_pdf")
        mostrar_calculado = st.checkbox("Calculado", value=True, key="mostrar_calculado")

    with col_ctrl2:
        st.markdown("**Empresas:**")
        mostrar_empresas = st.checkbox("Mostrar empresas", value=True, key="dashboard_empresas")
        if mostrar_empresas:
            mostrar_pacas = st.checkbox("PACAS", value=True, key="mostrar_pacas")
            mostrar_yura = st.checkbox("YURA", value=True, key="mostrar_yura")
            mostrar_unacem = st.checkbox("UNACEM", value=True, key="mostrar_unacem")
        else:
            mostrar_pacas = False
            mostrar_yura = False
            mostrar_unacem = False

    # GRUPO 1: PRODUCCIÓN
    st.header("📊 Grupo 1: Producción")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Producción de Clínker")
        fig1 = crear_grafico_serie_temporal(df_agregados, df_empresas, '8', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Producción de Cemento")
        fig2 = crear_grafico_serie_temporal(df_agregados, df_empresas, '20', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    # GRUPO 2: CONTENIDO DE CLÍNKER
    st.header("🔬 Grupo 2: Contenido de Clínker")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Factor Clínker")
        fig3 = crear_grafico_serie_temporal(df_agregados, df_empresas, '92a', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Consumo de Clínker")
        fig4 = crear_grafico_serie_temporal(df_agregados, df_empresas, '11', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    # GRUPO 3: EMISIONES
    st.header("🌍 Grupo 3: Emisiones CO₂")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Emisiones CO₂ Clínker")
        fig5 = crear_grafico_serie_temporal(df_agregados, df_empresas, '60a', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.subheader("Emisiones CO₂ Cementitious")
        fig6 = crear_grafico_serie_temporal(df_agregados, df_empresas, '62a', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig6:
            st.plotly_chart(fig6, use_container_width=True)

    # GRUPO 4: EFICIENCIA ENERGÉTICA
    st.header("⚡ Grupo 4: Eficiencia Energética")
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Eficiencia Térmica")
        fig7 = crear_grafico_serie_temporal(df_agregados, df_empresas, '93', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig7:
            st.plotly_chart(fig7, use_container_width=True)

    with col8:
        st.subheader("Consumo Eléctrico Específico")
        fig8 = crear_grafico_serie_temporal(df_agregados, df_empresas, '97', mostrar_empresas, df_pdf, mostrar_pdf, mostrar_calculado, mostrar_pacas, mostrar_yura, mostrar_unacem)
        if fig8:
            st.plotly_chart(fig8, use_container_width=True)

# ============================================================================
# PÁGINA 2: EXPLORADOR DE BASE DE DATOS
# ============================================================================

elif pagina == "🗄️ Explorador BD":
    st.header("Explorador de Base de Datos")
    st.markdown("Visualiza el contenido completo de cualquier tabla de la base de datos.")

    # Obtener lista de tablas
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Selector de tabla
    tabla_seleccionada = st.selectbox(
        "Selecciona una tabla:",
        options=tablas,
        help="Elige la tabla que deseas visualizar"
    )

    # Checkbox para limitar registros
    ver_primeros_50 = st.checkbox("Ver primeros 50 elementos", value=True, help="Activa para limitar la visualización a los primeros 50 registros")

    if tabla_seleccionada:
        # Cargar datos de la tabla seleccionada
        conn = sqlite3.connect(DB_PATH)

        if ver_primeros_50:
            query = f"SELECT * FROM {tabla_seleccionada} LIMIT 50"
        else:
            query = f"SELECT * FROM {tabla_seleccionada}"

        df_tabla = pd.read_sql_query(query, conn)

        # Obtener información adicional sobre la tabla
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tabla_seleccionada}")
        total_registros = cursor.fetchone()[0]
        conn.close()

        # Mostrar información
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de registros", f"{total_registros:,}")
        with col2:
            st.metric("Registros mostrados", f"{len(df_tabla):,}")
        with col3:
            st.metric("Columnas", len(df_tabla.columns))

        # Mostrar datos
        st.subheader(f"Contenido de la tabla: {tabla_seleccionada}")
        st.dataframe(df_tabla, use_container_width=True, hide_index=False, height=600)

        # Botón de descarga
        csv_tabla = df_tabla.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv_tabla,
            file_name=f"{tabla_seleccionada}.csv",
            mime="text/csv"
        )

        # Mostrar esquema de la tabla
        with st.expander("Ver esquema de la tabla"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({tabla_seleccionada})")
            esquema = cursor.fetchall()
            conn.close()

            df_esquema = pd.DataFrame(esquema, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
            st.dataframe(df_esquema, use_container_width=True, hide_index=True)

# ============================================================================
# PÁGINA 3: METAS HR 2030
# ============================================================================

elif pagina == "🎯 Metas HR 2030":
    st.header("Metas Hoja de Ruta Perú 2030")
    st.markdown("""
    Esta sección muestra las metas definidas en la **Hoja de Ruta de Descarbonización del Sector Cemento de Perú**
    para el año 2030, junto con los gráficos de trayectoria que comparan el progreso actual con la trayectoria requerida.
    """)

    # Tabla de metas
    st.subheader("📋 Tabla de Metas 2030")

    # Preparar datos para la tabla
    tabla_metas = []
    for codigo, info in METAS_HR_2030.items():
        fila = {
            'Código': codigo,
            'Indicador': info['nombre'],
            'Meta 2030': f"{info['meta_2030']:.2f}" if isinstance(info['meta_2030'], float) else str(info['meta_2030']),
            'Unidad': info['unidad'],
            'Tipo': 'Reducir' if info['tipo'] == 'max' else 'Aumentar',
        }

        # Agregar información adicional si existe
        if 'baseline_2019' in info:
            fila['Baseline 2019'] = f"{info['baseline_2019']:.2f}"
        elif 'baseline_año' in info:
            fila['Baseline'] = f"{info['baseline_año']}"

        if 'reduccion_hr_pct' in info:
            fila['Reducción (%)'] = f"{info['reduccion_hr_pct']:.1f}%"
        elif 'reduccion_estimada_pct' in info:
            fila['Reducción Est. (%)'] = f"{info['reduccion_estimada_pct']:.1f}%"

        tabla_metas.append(fila)

    df_metas = pd.DataFrame(tabla_metas)
    st.dataframe(df_metas, use_container_width=True, hide_index=True)

    # Botón de descarga
    csv_metas = df_metas.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Tabla de Metas (CSV)",
        data=csv_metas,
        file_name="metas_hr_2030.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # Gráficos de trayectoria interactivos
    st.subheader("📈 Gráficos de Trayectoria")

    # Organizar indicadores en grupos
    indicadores_principales = ['62', '92a', '93']
    indicadores_secundarios = ['60a', '97']
    indicadores_emisiones = ['63', '74', '75', '60', '73']

    # Mostrar indicadores principales
    st.markdown("### 🎯 Indicadores Principales (Metas Oficiales HR)")
    cols = st.columns(2)
    for idx, codigo in enumerate(indicadores_principales):
        meta_info = METAS_HR_2030.get(codigo)
        if meta_info:
            with cols[idx % 2]:
                fig = crear_grafico_trayectoria_hr(df_agregados, codigo, meta_info)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key=f"tray_princ_{codigo}")
                else:
                    st.warning(f"No hay datos para el indicador {codigo}")

    # Mostrar indicadores secundarios
    st.markdown("### 📊 Indicadores Secundarios (Metas Estimadas)")
    cols = st.columns(2)
    for idx, codigo in enumerate(indicadores_secundarios):
        meta_info = METAS_HR_2030.get(codigo)
        if meta_info:
            with cols[idx % 2]:
                fig = crear_grafico_trayectoria_hr(df_agregados, codigo, meta_info)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key=f"tray_sec_{codigo}")
                else:
                    st.warning(f"No hay datos para el indicador {codigo}")

    # Mostrar indicadores de emisiones adicionales
    st.markdown("### 🌍 Indicadores de Emisiones Adicionales")
    cols = st.columns(2)
    for idx, codigo in enumerate(indicadores_emisiones):
        meta_info = METAS_HR_2030.get(codigo)
        if meta_info:
            with cols[idx % 2]:
                fig = crear_grafico_trayectoria_hr(df_agregados, codigo, meta_info)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key=f"tray_emi_{codigo}")
                else:
                    st.warning(f"No hay datos para el indicador {codigo}")

    st.markdown("---")

    # Gráfico de progreso general interactivo
    st.markdown("### 📊 Progreso General hacia Metas 2030")
    fig_progreso = crear_grafico_progreso_metas(df_agregados)
    if fig_progreso:
        st.plotly_chart(fig_progreso, use_container_width=True, key="progreso_metas")

        # Leyenda de colores
        st.markdown("""
        **Leyenda de colores:**
        - 🟢 **Verde**: Meta alcanzada (≥100%)
        - 🟠 **Naranja**: Buen avance (50-99%)
        - 🔴 **Rojo**: Poco avance (0-49%)
        - 🟣 **Morado**: Retroceso (<0%)
        """)
    else:
        st.warning("No se pudieron calcular los datos de progreso")

# ============================================================================
# PÁGINA 4: INDICADORES FICEM
# ============================================================================

elif pagina == "📈 Indicadores FICEM":
    st.header("Indicadores Calculados - Protocolo FICEM")
    st.markdown("""
    Indicadores nacionales calculados según las fórmulas oficiales del **Anexo V1.4 FICEM**.
    Fuente: `FORMULAS_AGREGACION.md`
    """)

    # Metadatos de indicadores FICEM
    INDICADORES_FICEM = {
        # Eficiencia y Sustitución
        '33d': {'nombre': 'Factor emisión red eléctrica', 'unidad': 'kgCO₂/MWh', 'grupo': 'Eficiencia'},
        '92a': {'nombre': 'Factor clínker', 'unidad': 'ratio', 'grupo': 'Eficiencia'},
        '93': {'nombre': 'Consumo térmico específico', 'unidad': 'MJ/t clínker', 'grupo': 'Eficiencia'},
        '95': {'nombre': 'Fósiles alternativos', 'unidad': '%', 'grupo': 'Sustitución'},
        '96': {'nombre': 'Biomasa', 'unidad': '%', 'grupo': 'Sustitución'},
        '96a': {'nombre': 'Factor emisión combustibles', 'unidad': 'kgCO₂/GJ', 'grupo': 'Eficiencia'},
        '97': {'nombre': 'Consumo eléctrico específico', 'unidad': 'kWh/t cem', 'grupo': 'Eficiencia'},
        'coprocesamiento': {'nombre': 'Tasa coprocesamiento', 'unidad': 'ratio', 'grupo': 'Sustitución'},
        # Emisiones Clínker
        '60a': {'nombre': 'Descarbonatación (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1008': {'nombre': 'Fósiles convencionales (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1009': {'nombre': 'Fósiles alternativos (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1010': {'nombre': 'Fuera de horno (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1011': {'nombre': 'Biomasa (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1012': {'nombre': 'Electricidad externa (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '1088': {'nombre': 'Generación on-site (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '60': {'nombre': 'Específica bruta (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        '73': {'nombre': 'Específica neta (clínker)', 'unidad': 'kgCO₂/t clínker', 'grupo': 'Emisiones Clínker'},
        # Emisiones Cementitious
        '62a': {'nombre': 'Descarbonatación (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '82a': {'nombre': 'Electricidad externa (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '1020': {'nombre': 'Generación on-site (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '1021': {'nombre': 'Fuera de horno (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '1022': {'nombre': 'Fósiles convencionales (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '1023': {'nombre': 'Fósiles alternativos (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '1024': {'nombre': 'Biomasa (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '62': {'nombre': 'Específica bruta (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        '74': {'nombre': 'Específica neta (cementitious)', 'unidad': 'kgCO₂/t cementitious', 'grupo': 'Emisiones Cementitious'},
        # Emisiones Cemento
        '1001': {'nombre': 'Descarbonatación (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1002': {'nombre': 'Fuera de horno (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1003': {'nombre': 'Fósiles convencionales (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1004': {'nombre': 'Fósiles alternativos (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1005': {'nombre': 'Electricidad externa (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1006': {'nombre': 'Clínker externo (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1025': {'nombre': 'Generación on-site (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1043': {'nombre': 'Biomasa (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1044': {'nombre': 'Intensidad bruta (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        '1045': {'nombre': 'Intensidad neta (cemento)', 'unidad': 'kgCO₂/t cem', 'grupo': 'Emisiones Cemento'},
        # Emisiones Cemento Equivalente (códigos según BD común)
        '21b': {'nombre': 'Cemento equivalente', 'unidad': 't', 'grupo': 'Emisiones Cem. Equivalente'},
        '63a': {'nombre': 'Descarbonatación (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '82c': {'nombre': 'Electricidad externa (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '1410': {'nombre': 'Fósiles convencionales (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '1411': {'nombre': 'Fósiles alternativos (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '1412': {'nombre': 'Biomasa (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '1416': {'nombre': 'Fuera de horno (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '1417': {'nombre': 'Generación on-site (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '63': {'nombre': 'Específica bruta (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
        '75': {'nombre': 'Específica neta (cem. eq.)', 'unidad': 'kgCO₂/t cem eq', 'grupo': 'Emisiones Cem. Equivalente'},
    }

    # Filtrar solo indicadores calculados (no sumables)
    df_calculados = df_agregados[df_agregados['tipo_agregacion'] != 'suma'].copy()

    # Agregar metadatos
    df_calculados['nombre'] = df_calculados['codigo_indicador'].map(
        lambda x: INDICADORES_FICEM.get(x, {}).get('nombre', x)
    )
    df_calculados['unidad'] = df_calculados['codigo_indicador'].map(
        lambda x: INDICADORES_FICEM.get(x, {}).get('unidad', '')
    )
    df_calculados['grupo'] = df_calculados['codigo_indicador'].map(
        lambda x: INDICADORES_FICEM.get(x, {}).get('grupo', 'Otro')
    )

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Indicadores calculados", df_calculados['codigo_indicador'].nunique())
    with col2:
        st.metric("Años con datos", df_calculados['año'].nunique())
    with col3:
        st.metric("Total registros", len(df_calculados))

    st.markdown("---")

    # Selector de grupo
    grupos_disponibles = sorted(df_calculados['grupo'].unique())
    grupo_seleccionado = st.selectbox(
        "Selecciona un grupo de indicadores:",
        options=['Todos'] + grupos_disponibles
    )

    # Filtrar por grupo
    if grupo_seleccionado != 'Todos':
        df_filtrado = df_calculados[df_calculados['grupo'] == grupo_seleccionado]
    else:
        df_filtrado = df_calculados

    # Selector de año para vista detallada
    años_disponibles = sorted(df_filtrado['año'].unique(), reverse=True)
    año_seleccionado = st.selectbox("Año:", options=años_disponibles, index=0)

    # Tabla de indicadores para el año seleccionado
    st.subheader(f"Indicadores {grupo_seleccionado} - Año {año_seleccionado}")

    df_año = df_filtrado[df_filtrado['año'] == año_seleccionado].copy()
    df_año = df_año.sort_values('codigo_indicador')

    # Formatear tabla
    df_tabla = df_año[['codigo_indicador', 'nombre', 'valor_nacional', 'unidad', 'tipo_agregacion']].copy()
    df_tabla.columns = ['Código', 'Indicador', 'Valor', 'Unidad', 'Tipo Cálculo']
    df_tabla['Valor'] = df_tabla['Valor'].apply(lambda x: f"{x:,.4f}" if x < 10 else f"{x:,.2f}")

    st.dataframe(df_tabla, use_container_width=True, hide_index=True, height=400)

    # Descargar
    csv_data = df_tabla.to_csv(index=False)
    st.download_button(
        label="📥 Descargar tabla (CSV)",
        data=csv_data,
        file_name=f"indicadores_ficem_{año_seleccionado}.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # Gráficos de evolución temporal
    st.subheader("Evolución Temporal")

    indicadores_grupo = df_filtrado['codigo_indicador'].unique()

    if len(indicadores_grupo) > 0:
        indicador_grafico = st.selectbox(
            "Selecciona un indicador para graficar:",
            options=indicadores_grupo,
            format_func=lambda x: f"{x} - {INDICADORES_FICEM.get(x, {}).get('nombre', x)}"
        )

        df_ind = df_filtrado[df_filtrado['codigo_indicador'] == indicador_grafico].sort_values('año')

        if len(df_ind) > 0:
            info = INDICADORES_FICEM.get(indicador_grafico, {})
            nombre = info.get('nombre', indicador_grafico)
            unidad = info.get('unidad', '')

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_ind['año'],
                y=df_ind['valor_nacional'],
                mode='lines+markers',
                name=nombre,
                line=dict(width=3, color='#3498db'),
                marker=dict(size=10),
                hovertemplate='Año: %{x}<br>Valor: %{y:.4f}<extra></extra>'
            ))

            fig.update_layout(
                title=f"<b>{nombre}</b><br><span style='font-size:12px'>[{indicador_grafico}]</span>",
                xaxis_title="Año",
                yaxis_title=unidad,
                height=450,
                hovermode='x unified',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

            # Tabla de datos del indicador
            with st.expander("Ver datos completos"):
                df_detalle = df_ind[['año', 'valor_nacional', 'tipo_agregacion', 'num_empresas']].copy()
                df_detalle.columns = ['Año', 'Valor', 'Tipo Cálculo', 'Empresas']
                st.dataframe(df_detalle, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Resumen por tipo de agregación
    st.subheader("Resumen por Tipo de Agregación")
    resumen_tipo = df_calculados.groupby('tipo_agregacion').agg({
        'codigo_indicador': 'nunique',
        'año': 'nunique'
    }).reset_index()
    resumen_tipo.columns = ['Tipo', 'Indicadores', 'Años']
    st.dataframe(resumen_tipo, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Análisis de Datos - Sector Cemento Perú 2010-2023</p>
    <p>TDR Ítem 2 - Sistema de Medición y Reporte</p>
</div>
""", unsafe_allow_html=True)
