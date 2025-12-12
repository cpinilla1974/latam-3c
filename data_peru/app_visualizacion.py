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
    '62a': {'nombre': 'Emisiones CO₂ Cementitious', 'unidad': 'kg CO₂/t', 'grupo': 'Emisiones'},
    '73': {'nombre': 'Emisiones Indirectas', 'unidad': 't CO₂', 'grupo': 'Emisiones'},
    '93': {'nombre': 'Eficiencia Térmica', 'unidad': 'MJ/t clínker', 'grupo': 'Eficiencia'},
    '97': {'nombre': 'Consumo Eléctrico Específico', 'unidad': 'kWh/t', 'grupo': 'Eléctricos'},
    '1151': {'nombre': 'Energía Fósil', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
    '1152': {'nombre': 'Energía Biomasa', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
    '1155': {'nombre': 'Energía Residuos', 'unidad': 'GJ', 'grupo': 'Eficiencia'},
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

def cargar_validacion():
    """Carga resultados de validación."""
    csv_path = Path(__file__).parent / "datos_procesados" / "validacion_vs_reporte.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None

def formato_numero(valor, unidad):
    """Formatea números según su unidad."""
    if unidad == 't':
        return f"{valor/1_000_000:.2f} Mt"
    elif unidad == 't CO₂':
        return f"{valor/1_000_000:.2f} Mt CO₂"
    elif unidad == 'decimal':
        return f"{valor*100:.1f}%"
    elif unidad in ['kg CO₂/t', 'kWh/t', 'MJ/t clínker']:
        return f"{valor:.1f} {unidad}"
    elif unidad == 'GJ':
        return f"{valor/1_000:.1f} TJ"
    else:
        return f"{valor:,.0f}"

def crear_grafico_serie_temporal(df_agregados, df_empresas, indicador, mostrar_empresas=True):
    """Crea gráfico de serie temporal para un indicador con datos por empresa y agregado."""
    df_ind = df_agregados[df_agregados['codigo_indicador'] == indicador].copy()

    if len(df_ind) == 0:
        return None

    info = INDICADORES_INFO.get(indicador, {})
    nombre = info.get('nombre', indicador)
    unidad = info.get('unidad', '')

    fig = go.Figure()

    # Si se solicita, agregar datos por empresa
    if mostrar_empresas:
        df_empresas_ind = df_empresas[df_empresas['codigo_indicador'] == indicador].copy()

        for empresa in sorted(df_empresas_ind['codigo_empresa'].unique()):
            df_emp = df_empresas_ind[df_empresas_ind['codigo_empresa'] == empresa]
            fig.add_trace(go.Scatter(
                x=df_emp['año'],
                y=df_emp['valor'],
                mode='lines+markers',
                name=empresa,
                line=dict(width=2, dash='dot'),
                marker=dict(size=6),
                opacity=0.6
            ))

    # Agregar línea del agregado nacional (más prominente)
    fig.add_trace(go.Scatter(
        x=df_ind['año'],
        y=df_ind['valor_nacional'],
        mode='lines+markers',
        name='NACIONAL',
        line=dict(width=4, color='black'),
        marker=dict(size=10, color='black'),
        opacity=1.0
    ))

    fig.update_layout(
        title=f"{nombre}",
        xaxis_title="Año",
        yaxis_title=unidad if unidad else "Valor",
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

def crear_grafico_comparacion_empresas(df, indicador, año_sel):
    """Crea gráfico de comparación entre empresas."""
    df_comp = df[
        (df['codigo_indicador'] == indicador) &
        (df['año'] == año_sel)
    ].copy()

    if len(df_comp) == 0:
        return None

    info = INDICADORES_INFO.get(indicador, {})
    nombre = info.get('nombre', indicador)

    fig = px.bar(
        df_comp,
        x='codigo_empresa',
        y='valor',
        title=f"{nombre} - {año_sel}",
        labels={'codigo_empresa': 'Empresa', 'valor': 'Valor'},
        color='codigo_empresa',
        text_auto=True
    )

    fig.update_layout(height=400)

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
        ["📊 Dashboard General", "📈 Análisis por Indicador", "🏢 Análisis por Empresa", "✅ Validación", "📁 Datos Crudos"]
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

    # Toggle para mostrar/ocultar datos por empresa
    mostrar_empresas = st.checkbox("Mostrar datos por empresa", value=True, key="dashboard_empresas")

    # GRUPO 1: PRODUCCIÓN
    st.header("📊 Grupo 1: Producción")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Producción de Clínker")
        fig1 = crear_grafico_serie_temporal(df_agregados, df_empresas, '8', mostrar_empresas)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Producción de Cemento")
        fig2 = crear_grafico_serie_temporal(df_agregados, df_empresas, '20', mostrar_empresas)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    # GRUPO 2: CONTENIDO DE CLÍNKER
    st.header("🔬 Grupo 2: Contenido de Clínker")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Factor Clínker")
        fig3 = crear_grafico_serie_temporal(df_agregados, df_empresas, '92a', mostrar_empresas)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Consumo de Clínker")
        fig4 = crear_grafico_serie_temporal(df_agregados, df_empresas, '11', mostrar_empresas)
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    # GRUPO 3: EMISIONES
    st.header("🌍 Grupo 3: Emisiones CO₂")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Emisiones CO₂ Clínker")
        fig5 = crear_grafico_serie_temporal(df_agregados, df_empresas, '60a', mostrar_empresas)
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.subheader("Emisiones CO₂ Cementitious")
        fig6 = crear_grafico_serie_temporal(df_agregados, df_empresas, '62a', mostrar_empresas)
        if fig6:
            st.plotly_chart(fig6, use_container_width=True)

    # GRUPO 4: EFICIENCIA ENERGÉTICA
    st.header("⚡ Grupo 4: Eficiencia Energética")
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Eficiencia Térmica")
        fig7 = crear_grafico_serie_temporal(df_agregados, df_empresas, '93', mostrar_empresas)
        if fig7:
            st.plotly_chart(fig7, use_container_width=True)

    with col8:
        st.subheader("Consumo Eléctrico Específico")
        fig8 = crear_grafico_serie_temporal(df_agregados, df_empresas, '97', mostrar_empresas)
        if fig8:
            st.plotly_chart(fig8, use_container_width=True)

# ============================================================================
# PÁGINA 2: ANÁLISIS POR INDICADOR
# ============================================================================

elif pagina == "📈 Análisis por Indicador":
    st.header("Análisis por Indicador")

    # Selector de grupo e indicador
    grupos = sorted(set([info['grupo'] for info in INDICADORES_INFO.values()]))
    grupo_sel = st.selectbox("Selecciona grupo:", grupos)

    indicadores_grupo = {
        cod: info for cod, info in INDICADORES_INFO.items()
        if info['grupo'] == grupo_sel
    }

    indicador_sel = st.selectbox(
        "Selecciona indicador:",
        options=list(indicadores_grupo.keys()),
        format_func=lambda x: f"[{x}] {indicadores_grupo[x]['nombre']}"
    )

    # Información del indicador
    info = INDICADORES_INFO[indicador_sel]
    st.markdown(f"### [{indicador_sel}] {info['nombre']}")
    st.markdown(f"**Unidad:** {info['unidad']} | **Grupo:** {info['grupo']}")

    # Datos del indicador
    df_ind = df_agregados[df_agregados['codigo_indicador'] == indicador_sel].copy()

    if len(df_ind) > 0:
        # Toggle para mostrar/ocultar datos por empresa
        mostrar_empresas_ind = st.checkbox("Mostrar datos por empresa", value=True, key="indicador_empresas")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Serie Temporal")
            fig = crear_grafico_serie_temporal(df_agregados, df_empresas, indicador_sel, mostrar_empresas_ind)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Estadísticas")
            st.metric("Años disponibles", f"{df_ind['año'].min()} - {df_ind['año'].max()}")
            st.metric("Total registros", len(df_ind))

            if info['unidad'] in ['t', 't CO₂']:
                valor_max = df_ind['valor_nacional'].max()
                año_max = df_ind[df_ind['valor_nacional'] == valor_max]['año'].values[0]
                st.metric("Máximo", f"{valor_max/1_000_000:.2f} Mt", f"en {año_max}")
            else:
                valor_max = df_ind['valor_nacional'].max()
                año_max = df_ind[df_ind['valor_nacional'] == valor_max]['año'].values[0]
                st.metric("Máximo", f"{valor_max:.2f}", f"en {año_max}")

        # Tabla de datos con desglose por empresa
        st.subheader("Datos Detallados")

        # Crear tabla pivotada con empresas como columnas
        df_empresas_ind = df_empresas[df_empresas['codigo_indicador'] == indicador_sel].copy()

        if len(df_empresas_ind) > 0:
            # Pivotar datos por empresa
            df_pivot = df_empresas_ind.pivot(index='año', columns='codigo_empresa', values='valor')

            # Agregar columna del agregado nacional
            df_nacional = df_ind.set_index('año')['valor_nacional']
            df_pivot['NACIONAL'] = df_nacional

            # Resetear índice
            df_pivot = df_pivot.reset_index()

            # Formatear valores según unidad
            cols_valor = [col for col in df_pivot.columns if col != 'año']
            for col in cols_valor:
                df_pivot[f'{col}_formatted'] = df_pivot[col].apply(
                    lambda x: formato_numero(x, info['unidad']) if pd.notna(x) else '-'
                )

            # Crear DataFrame para mostrar
            cols_display = ['año'] + [f'{col}_formatted' for col in cols_valor]
            df_display = df_pivot[cols_display].copy()

            # Renombrar columnas
            nuevas_columnas = ['Año'] + cols_valor
            df_display.columns = nuevas_columnas

            st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
        else:
            # Si no hay datos por empresa, mostrar solo agregado
            df_display = df_ind[['año', 'valor_nacional']].copy()
            df_display['valor_formateado'] = df_display['valor_nacional'].apply(
                lambda x: formato_numero(x, info['unidad'])
            )
            df_display = df_display[['año', 'valor_formateado']]
            df_display.columns = ['Año', 'NACIONAL']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No hay datos disponibles para el indicador {indicador_sel}")

# ============================================================================
# PÁGINA 3: ANÁLISIS POR EMPRESA
# ============================================================================

elif pagina == "🏢 Análisis por Empresa":
    st.header("Análisis por Empresa")

    empresas = sorted(df_empresas['codigo_empresa'].unique())
    empresa_sel = st.selectbox("Selecciona empresa:", empresas)

    df_empresa = df_empresas[df_empresas['codigo_empresa'] == empresa_sel].copy()

    # Estadísticas de la empresa
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Indicadores reportados", df_empresa['codigo_indicador'].nunique())

    with col2:
        st.metric("Años de datos", f"{df_empresa['año'].min()} - {df_empresa['año'].max()}")

    with col3:
        st.metric("Total registros", len(df_empresa))

    st.markdown("---")

    # Selector de indicador
    indicadores_disponibles = sorted(df_empresa['codigo_indicador'].unique())
    indicador_sel = st.selectbox(
        "Selecciona indicador para visualizar:",
        options=indicadores_disponibles,
        format_func=lambda x: f"[{x}] {INDICADORES_INFO.get(x, {}).get('nombre', x)}"
    )

    # Gráfico comparativo con otras empresas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Evolución - {empresa_sel}")
        df_ind_empresa = df_empresa[df_empresa['codigo_indicador'] == indicador_sel].copy()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_ind_empresa['año'],
            y=df_ind_empresa['valor'],
            mode='lines+markers',
            name=empresa_sel
        ))

        info = INDICADORES_INFO.get(indicador_sel, {})
        fig.update_layout(
            title=info.get('nombre', indicador_sel),
            xaxis_title="Año",
            yaxis_title=info.get('unidad', 'Valor'),
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Comparación con otras empresas")

        años_disponibles = sorted(df_empresas['año'].unique())
        año_comp = st.select_slider("Selecciona año:", options=años_disponibles)

        fig_comp = crear_grafico_comparacion_empresas(df_empresas, indicador_sel, año_comp)
        if fig_comp:
            st.plotly_chart(fig_comp, use_container_width=True)

    # Tabla de datos
    st.subheader("Datos de la empresa")
    df_display = df_empresa[['año', 'codigo_indicador', 'valor']].copy()
    df_display = df_display.sort_values(['año', 'codigo_indicador'])
    df_display['indicador_nombre'] = df_display['codigo_indicador'].map(
        lambda x: INDICADORES_INFO.get(x, {}).get('nombre', x)
    )
    df_display = df_display[['año', 'codigo_indicador', 'indicador_nombre', 'valor']]
    df_display.columns = ['Año', 'Código', 'Indicador', 'Valor']

    st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)

# ============================================================================
# PÁGINA 4: VALIDACIÓN
# ============================================================================

elif pagina == "✅ Validación":
    st.header("Validación contra Reporte Oficial")

    df_val = cargar_validacion()

    if df_val is not None:
        # Resumen general
        col1, col2, col3 = st.columns(3)

        with col1:
            exactos = len(df_val[df_val['error_pct'] <= 2])
            st.metric("✅ Exactos (≤2%)", f"{exactos} ({exactos/len(df_val)*100:.1f}%)")

        with col2:
            aceptables = len(df_val[(df_val['error_pct'] > 2) & (df_val['error_pct'] <= 5)])
            st.metric("⚠️ Aceptables (2-5%)", f"{aceptables} ({aceptables/len(df_val)*100:.1f}%)")

        with col3:
            revisar = len(df_val[df_val['error_pct'] > 5])
            st.metric("❌ Revisar (>5%)", f"{revisar} ({revisar/len(df_val)*100:.1f}%)")

        st.markdown("---")

        # Gráfico de errores
        st.subheader("Distribución de Errores por Indicador")

        fig = px.box(
            df_val,
            x='codigo',
            y='error_pct',
            title="Distribución de Error % por Indicador",
            labels={'codigo': 'Indicador', 'error_pct': 'Error %'}
        )
        fig.add_hline(y=2, line_dash="dash", line_color="green", annotation_text="Límite Exacto (2%)")
        fig.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Límite Aceptable (5%)")

        st.plotly_chart(fig, use_container_width=True)

        # Tabla detallada
        st.subheader("Detalle de Validación")

        df_val_display = df_val.copy()
        df_val_display['estado'] = df_val_display['error_pct'].apply(
            lambda x: '✅ OK' if x <= 2 else ('⚠️ Aceptable' if x <= 5 else '❌ Revisar')
        )

        st.dataframe(
            df_val_display[['codigo', 'año', 'oficial', 'calculado', 'diferencia', 'error_pct', 'estado']],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No se encontraron datos de validación. Ejecuta el script 08_validar_contra_reporte.py")

# ============================================================================
# PÁGINA 5: DATOS CRUDOS
# ============================================================================

elif pagina == "📁 Datos Crudos":
    st.header("Datos Crudos")

    tab1, tab2 = st.tabs(["Agregados Nacionales", "Datos por Empresa"])

    with tab1:
        st.subheader("Agregados Nacionales")

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            años_sel = st.multiselect(
                "Filtrar por años:",
                options=sorted(df_agregados['año'].unique()),
                default=None
            )

        with col2:
            indicadores_sel = st.multiselect(
                "Filtrar por indicadores:",
                options=sorted(df_agregados['codigo_indicador'].unique()),
                default=None
            )

        # Aplicar filtros
        df_filtrado = df_agregados.copy()
        if años_sel:
            df_filtrado = df_filtrado[df_filtrado['año'].isin(años_sel)]
        if indicadores_sel:
            df_filtrado = df_filtrado[df_filtrado['codigo_indicador'].isin(indicadores_sel)]

        st.dataframe(df_filtrado, use_container_width=True, hide_index=True, height=500)

        # Botón de descarga
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="agregados_nacionales.csv",
            mime="text/csv"
        )

    with tab2:
        st.subheader("Datos por Empresa")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            empresas_sel = st.multiselect(
                "Filtrar por empresas:",
                options=sorted(df_empresas['codigo_empresa'].unique()),
                default=None
            )

        with col2:
            años_sel_emp = st.multiselect(
                "Filtrar por años:",
                options=sorted(df_empresas['año'].unique()),
                default=None
            )

        with col3:
            ind_sel_emp = st.multiselect(
                "Filtrar por indicadores:",
                options=sorted(df_empresas['codigo_indicador'].unique()),
                default=None
            )

        # Aplicar filtros
        df_emp_filtrado = df_empresas.copy()
        if empresas_sel:
            df_emp_filtrado = df_emp_filtrado[df_emp_filtrado['codigo_empresa'].isin(empresas_sel)]
        if años_sel_emp:
            df_emp_filtrado = df_emp_filtrado[df_emp_filtrado['año'].isin(años_sel_emp)]
        if ind_sel_emp:
            df_emp_filtrado = df_emp_filtrado[df_emp_filtrado['codigo_indicador'].isin(ind_sel_emp)]

        st.dataframe(df_emp_filtrado, use_container_width=True, hide_index=True, height=500)

        # Botón de descarga
        csv_emp = df_emp_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv_emp,
            file_name="datos_empresas.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Análisis de Datos - Sector Cemento Perú 2010-2023</p>
    <p>TDR Ítem 2 - Sistema de Medición y Reporte</p>
</div>
""", unsafe_allow_html=True)
