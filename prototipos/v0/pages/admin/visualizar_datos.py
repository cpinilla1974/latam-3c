import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys
import os

# Agregar el directorio modules al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))

from excel_generator_v2 import ExcelGenerator

def get_json_files():
    """Obtiene todos los archivos JSON disponibles"""
    data_path = Path("../data")
    json_files = []
    
    if data_path.exists():
        json_files = [f for f in data_path.glob("*.json") if f.is_file()]
    
    # Categorizar archivos por tipo
    planta_files = [f for f in json_files if ("_P0" in f.name or "clinker_cemento" in f.name) and "concreto" not in f.name]
    concreto_files = [f for f in json_files if "concreto" in f.name]
    
    return planta_files, concreto_files

def load_json_data(file_path):
    """Carga datos JSON desde archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error cargando archivo: {str(e)}")
        return None

def show_empresa_info(data):
    """Muestra información de empresa en formato tabla"""
    empresa_data = data.get("hoja_empresa", {})
    
    df_empresa = pd.DataFrame([{
        "Campo": "Nombre Empresa",
        "Valor": empresa_data.get("nombre_empresa", "N/A")
    }, {
        "Campo": "País", 
        "Valor": empresa_data.get("pais", "N/A")
    }, {
        "Campo": "Responsable",
        "Valor": empresa_data.get("responsable", "N/A") 
    }, {
        "Campo": "Email",
        "Valor": empresa_data.get("email", "N/A")
    }, {
        "Campo": "Teléfono",
        "Valor": empresa_data.get("telefono", "N/A")
    }])
    
    st.dataframe(df_empresa, use_container_width=True, hide_index=True)

def show_planta_info(data):
    """Muestra información de planta en formato tabla"""
    planta_data = data.get("hoja_planta", {})
    
    df_planta = pd.DataFrame([{
        "Campo": "ID Planta",
        "Valor": planta_data.get("id_planta", "N/A")
    }, {
        "Campo": "Nombre",
        "Valor": planta_data.get("nombre", "N/A")
    }, {
        "Campo": "Ubicación", 
        "Valor": planta_data.get("ubicacion", "N/A")
    }, {
        "Campo": "Latitud",
        "Valor": planta_data.get("latitud", "N/A")
    }, {
        "Campo": "Longitud",
        "Valor": planta_data.get("longitud", "N/A")
    }, {
        "Campo": "Tipo Planta",
        "Valor": planta_data.get("tipo_planta", "N/A")
    }, {
        "Campo": "Capacidad Clinker (ton/año)",
        "Valor": f"{planta_data.get('capacidad_clinker_ton_año', 0):,}"
    }, {
        "Campo": "Capacidad Cemento (ton/año)", 
        "Valor": f"{planta_data.get('capacidad_cemento_ton_año', 0):,}"
    }, {
        "Campo": "Archivo GCCA",
        "Valor": planta_data.get("archivo_gcca", "N/A")
    }])
    
    st.dataframe(df_planta, use_container_width=True, hide_index=True)

def show_clinker_data(data):
    """Muestra datos de clinker"""
    clinker_data = data.get("hoja_clinker")
    
    if not clinker_data:
        st.info("Esta planta no produce clinker (solo molienda)")
        return
        
    # Identificación
    st.subheader("📊 Identificación")
    identificacion = clinker_data.get("identificacion", {})
    
    df_id = pd.DataFrame([{
        "Producción Clinker Anual (ton)": f"{identificacion.get('produccion_clinker_anual_ton', 0):,}",
        "Emisiones Proceso (tCO2)": f"{identificacion.get('emisiones_proceso_tco2', 0):,}"
    }])
    
    st.dataframe(df_id, use_container_width=True, hide_index=True)
    
    # Minerales
    st.subheader("🪨 Minerales")
    minerales = clinker_data.get("minerales", [])
    
    if minerales:
        df_minerales = pd.DataFrame([{
            "Material": m.get("material", ""),
            "Cantidad (ton)": f"{m.get('cantidad_ton', 0):,}",
            "Origen": m.get("origen", ""),
            "Dist. Camión (km)": m.get("dist_camion_km", 0),
            "Dist. Tren (km)": m.get("dist_tren_km", 0),
            "Dist. Barco (km)": m.get("dist_barco_km", 0),
            "Dist. Banda (km)": m.get("dist_banda_km", 0)
        } for m in minerales])
        
        st.dataframe(df_minerales, use_container_width=True, hide_index=True)
    
    # Referencias a combustibles
    st.subheader("🔥 Combustibles Horno")
    ref = clinker_data.get("combustibles_horno_referencia", "")
    st.info(ref)
    
    # Energía eléctrica
    st.subheader("⚡ Energía Eléctrica")
    energia = clinker_data.get("energia_electrica", [])
    
    if energia:
        df_energia = pd.DataFrame([{
            "Tipo Energía": e.get("tipo_energia", ""),
            "Cantidad (kWh)": f"{e.get('cantidad_kwh', 0):,}",
            "Factor Emisión (kgCO2/kWh)": e.get("factor_emision_kgco2_kwh", 0),
            "Fuente": e.get("fuente", "")
        } for e in energia])
        
        st.dataframe(df_energia, use_container_width=True, hide_index=True)

def show_cemento_data(data):
    """Muestra datos de cemento por tipo"""
    hojas_cemento = data.get("hojas_cemento", [])
    
    if not hojas_cemento:
        st.info("No hay datos de cemento disponibles")
        return
    
    for i, cemento in enumerate(hojas_cemento):
        tipo = cemento.get("tipo", f"Cemento {i+1}")
        
        with st.expander(f"🏭 {tipo}", expanded=i==0):
            # Identificación
            identificacion = cemento.get("identificacion", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Identificación:**")
                df_id = pd.DataFrame([{
                    "Campo": "Tipo Cemento",
                    "Valor": identificacion.get("tipo_cemento", "")
                }, {
                    "Campo": "Nombre Comercial", 
                    "Valor": identificacion.get("nombre_comercial", "")
                }, {
                    "Campo": "Resistencia 28d (MPa)",
                    "Valor": identificacion.get("resistencia_28d_mpa", "")
                }, {
                    "Campo": "Resistencia 28d (psi)",
                    "Valor": identificacion.get("resistencia_28d_psi", "")
                }, {
                    "Campo": "Norma Técnica",
                    "Valor": identificacion.get("norma_tecnica", "")
                }, {
                    "Campo": "Producción Anual (ton)",
                    "Valor": f"{identificacion.get('produccion_anual_ton', 0):,}"
                }])
                
                st.dataframe(df_id, use_container_width=True, hide_index=True)
            
            with col2:
                # Molienda y combustibles
                molienda = cemento.get("molienda_combustibles", {})
                st.markdown("**Molienda y Combustibles:**")
                
                df_molienda = pd.DataFrame([{
                    "Campo": "Electricidad Red (kWh)",
                    "Valor": f"{molienda.get('electricidad_red_kwh', 0):,}"
                }, {
                    "Campo": "Electricidad Renovable (kWh)",
                    "Valor": f"{molienda.get('electricidad_renovable_kwh', 0):,}"
                }, {
                    "Campo": "Combustibles Fuera Horno",
                    "Valor": molienda.get("combustibles_fuera_horno_referencia", "")
                }])
                
                st.dataframe(df_molienda, use_container_width=True, hide_index=True)
            
            # Composición
            st.markdown("**Composición y Transporte:**")
            composicion = cemento.get("composicion", [])
            
            if composicion:
                df_composicion = pd.DataFrame([{
                    "ID Material": c.get("id_material", ""),
                    "Material": c.get("material", ""),
                    "Proveedor": c.get("proveedor", ""),
                    "Cantidad (ton)": f"{c.get('cantidad_ton', 0):,}",
                    "Dist. Camión (km)": c.get("dist_camion_km", 0),
                    "Dist. Tren (km)": c.get("dist_tren_km", 0),
                    "Dist. Barco (km)": c.get("dist_barco_km", 0),
                    "Dist. Banda (km)": c.get("dist_banda_km", 0)
                } for c in composicion])
                
                st.dataframe(df_composicion, use_container_width=True, hide_index=True)

def show_plantas_concreto(data):
    """Muestra plantas de concreto"""
    plantas = data.get("hoja_plantas_concreto", [])
    
    if not plantas:
        st.info("No hay plantas de concreto definidas")
        return
    
    df_plantas = pd.DataFrame([{
        "ID Planta": p.get("id_planta", ""),
        "Nombre": p.get("nombre", ""),
        "Ubicación": p.get("ubicacion", ""),
        "Latitud": p.get("latitud", ""),
        "Longitud": p.get("longitud", ""),
        "Tipo": p.get("tipo", ""),
        "Capacidad (m³/año)": f"{p.get('capacidad_m3_año', 0):,}"
    } for p in plantas])
    
    st.dataframe(df_plantas, use_container_width=True, hide_index=True)

def show_produccion_concreto(data):
    """Muestra producción de concreto"""
    produccion = data.get("hoja_produccion", [])
    
    if not produccion:
        st.info("No hay datos de producción")
        return
        
    df_produccion = pd.DataFrame([{
        "ID Planta": p.get("id_planta", ""),
        "Categoría": p.get("categoria", ""),
        "Tipo Concreto": p.get("tipo_concreto", ""),
        "Resistencia": p.get("resistencia", ""),
        "Volumen m³ Anual": f"{p.get('volumen_m3_anual', 0):,}"
    } for p in produccion])
    
    st.dataframe(df_produccion, use_container_width=True, hide_index=True)

def show_mezclas(data):
    """Muestra diseños de mezcla"""
    mezclas = data.get("hoja_mezclas", [])
    
    if not mezclas:
        st.info("No hay diseños de mezcla")
        return
    
    df_mezclas = pd.DataFrame([{
        "ID Mezcla": m.get("id_mezcla", ""),
        "Resistencia": m.get("resistencia", ""),
        "Cemento (kg/m³)": m.get("cemento_kg_m3", 0),
        "Tipo Cemento": m.get("tipo_cemento", ""),
        "Arena (kg/m³)": m.get("arena_kg_m3", 0),
        "ID Arena": m.get("id_arena", ""),
        "Grava (kg/m³)": m.get("grava_kg_m3", 0),
        "ID Grava": m.get("id_grava", ""),
        "Agua (L/m³)": m.get("agua_l_m3", 0),
        "Aditivo (L/m³)": m.get("aditivo_l_m3", 0),
        "ID Aditivo": m.get("id_aditivo", ""),
        "Adiciones (kg/m³)": m.get("adiciones_kg_m3", 0),
        "ID Adición": m.get("id_adicion", "")
    } for m in mezclas])
    
    st.dataframe(df_mezclas, use_container_width=True, hide_index=True)

def show_agregados(data):
    """Muestra agregados y adiciones"""
    agregados = data.get("hoja_agregados_adiciones", [])
    
    if not agregados:
        st.info("No hay agregados definidos")
        return
        
    df_agregados = pd.DataFrame([{
        "ID Material": a.get("id_material", ""),
        "Material": a.get("material", ""),
        "Tipo": a.get("tipo", ""),
        "Proveedor": a.get("proveedor", ""),
        "Cantidad Anual (ton)": f"{a.get('cantidad_ton_anual', 0):,}",
        "Dist. Camión (km)": a.get("dist_camion_km", 0),
        "Dist. Tren (km)": a.get("dist_tren_km", 0),
        "Dist. Barco (km)": a.get("dist_barco_km", 0)
    } for a in agregados])
    
    st.dataframe(df_agregados, use_container_width=True, hide_index=True)

def show_aditivos(data):
    """Muestra aditivos"""
    aditivos = data.get("hoja_aditivos", [])
    
    if not aditivos:
        st.info("No hay aditivos definidos")
        return
    
    df_aditivos = pd.DataFrame([{
        "ID Aditivo": a.get("id_aditivo", ""),
        "Tipo": a.get("tipo_aditivo", ""),
        "Función": a.get("funcion", ""),
        "Marca": a.get("marca", ""),
        "Proveedor": a.get("proveedor", ""),
        "Cantidad Anual (L)": f"{a.get('cantidad_l_anual', 0):,}",
        "Dist. Camión (km)": a.get("dist_camion_km", 0),
        "Dist. Tren (km)": a.get("dist_tren_km", 0),
        "Dist. Barco (km)": a.get("dist_barco_km", 0)
    } for a in aditivos])
    
    st.dataframe(df_aditivos, use_container_width=True, hide_index=True)

def show_consumos_especificos(data):
    """Muestra consumos específicos por planta"""
    consumos = data.get("hoja_consumos_especificos_planta", [])
    
    if not consumos:
        st.info("No hay consumos específicos definidos")
        return
    
    df_consumos = pd.DataFrame([{
        "ID Planta": c.get("id_planta", ""),
        "Electricidad (kWh/m³)": c.get("electricidad_kwh_m3", 0),
        "Diesel Cargador (L/m³)": c.get("diesel_cargador_l_m3", 0),
        "Diesel Otros (L/m³)": c.get("diesel_otros_l_m3", 0),
        "Notas": c.get("notas", "")
    } for c in consumos])
    
    st.dataframe(df_consumos, use_container_width=True, hide_index=True)

def show_transporte_mixer(data):
    """Muestra datos de transporte mixer"""
    transporte = data.get("hoja_transporte_mixer", [])
    
    if not transporte:
        st.info("No hay datos de transporte mixer")
        return
    
    df_transporte = pd.DataFrame([{
        "ID Planta": t.get("id_planta", ""),
        "Radio Promedio (km)": t.get("radio_promedio_km", 0),
        "Diesel (L/m³)": t.get("diesel_l_m3", 0),
        "Tipo Camión": t.get("tipo_camion", ""),
        "Capacidad (m³)": t.get("capacidad_m3", 0),
        "Factor Retorno": t.get("factor_retorno", 0)
    } for t in transporte])
    
    st.dataframe(df_transporte, use_container_width=True, hide_index=True)

def show_visualizar_datos():
    """Página principal de visualización de datos"""
    
    st.subheader("👁️ Visualizar Datos por Pestañas")
    st.markdown("Examina los datos antes de descargar Excel")
    
    # Obtener archivos disponibles  
    planta_files, concreto_files = get_json_files()
    
    if not planta_files and not concreto_files:
        st.warning("⚠️ No se encontraron archivos JSON en la carpeta data/")
        return
    
    # Selector de tipo de archivo
    tipo_archivo = st.selectbox(
        "Seleccionar tipo de archivo:",
        ["Planta de Cemento", "Concreto"],
        key="visualizar_tipo_archivo"
    )
    
    # Selector de archivo específico
    if tipo_archivo == "Planta de Cemento":
        if not planta_files:
            st.warning("No hay archivos de plantas disponibles")
            return
        archivo_seleccionado = st.selectbox(
            "Seleccionar archivo:",
            planta_files,
            format_func=lambda x: x.name,
            key="visualizar_archivo_planta"
        )
    else:
        if not concreto_files:
            st.warning("No hay archivos de concreto disponibles") 
            return
        archivo_seleccionado = st.selectbox(
            "Seleccionar archivo:",
            concreto_files,
            format_func=lambda x: x.name,
            key="visualizar_archivo_concreto"
        )
    
    # Cargar datos
    data = load_json_data(archivo_seleccionado)
    if not data:
        return
    
    st.markdown("---")
    
    # Crear pestañas según el tipo de archivo
    if tipo_archivo == "Planta de Cemento":
        tabs = st.tabs(["🏢 Empresa", "🏭 Planta", "🪨 Clinker", "🏗️ Cementos"])
        
        with tabs[0]:
            st.subheader("🏢 Información de Empresa")
            show_empresa_info(data)
            
        with tabs[1]:
            st.subheader("🏭 Información de Planta")
            show_planta_info(data)
            
        with tabs[2]: 
            st.subheader("🪨 Datos de Clinker")
            show_clinker_data(data)
            
        with tabs[3]:
            st.subheader("🏗️ Datos de Cementos")
            show_cemento_data(data)
            
    else:  # Concreto
        tabs = st.tabs([
            "🏢 Empresa", 
            "🏭 Plantas", 
            "📊 Producción",
            "🧪 Mezclas",
            "🪨 Agregados",
            "🧴 Aditivos",
            "⚡ Consumos",
            "🚛 Transporte"
        ])
        
        with tabs[0]:
            st.subheader("🏢 Información de Empresa")
            show_empresa_info(data)
            
        with tabs[1]:
            st.subheader("🏭 Plantas de Concreto")
            show_plantas_concreto(data)
            
        with tabs[2]:
            st.subheader("📊 Producción")
            show_produccion_concreto(data)
            
        with tabs[3]:
            st.subheader("🧪 Diseños de Mezcla")
            show_mezclas(data)
            
        with tabs[4]:
            st.subheader("🪨 Agregados y Adiciones")
            show_agregados(data)
            
        with tabs[5]:
            st.subheader("🧴 Aditivos")
            show_aditivos(data)
            
        with tabs[6]:
            st.subheader("⚡ Consumos Específicos")
            show_consumos_especificos(data)
            
        with tabs[7]:
            st.subheader("🚛 Transporte Mixer")
            show_transporte_mixer(data)
    
    # Botón de descarga al final
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📥 Descargar Excel", type="primary", use_container_width=True):
            # Generar y descargar Excel
            try:
                generator = ExcelGenerator()
                json_data = data
                
                empresa = json_data.get("hoja_empresa", {}).get("nombre_empresa", "Empresa")
                periodo = json_data.get("periodo", "2024")
                pais = json_data.get("hoja_empresa", {}).get("pais", "")
                
                if tipo_archivo == "Planta de Cemento":
                    excel_data = generator.generate_clinker_cemento_excel(json_data)
                    id_planta = json_data.get("hoja_planta", {}).get("id_planta", "")
                    filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_{id_planta}.xlsx"
                else:
                    excel_data = generator.generate_concreto_excel(json_data)
                    filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_Concreto.xlsx"
                
                st.download_button(
                    label="📥 Confirmar Descarga",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                st.success("✅ Excel generado correctamente!")
                
            except Exception as e:
                st.error(f"❌ Error generando Excel: {str(e)}")

def show_data_preview(archivo_seleccionado, tipo_archivo):
    """Función para mostrar preview de datos desde la pestaña generar excel"""
    
    # Cargar datos
    data = load_json_data(archivo_seleccionado)
    if not data:
        st.error("No se pudo cargar el archivo seleccionado")
        return
    
    # Título más compacto
    st.markdown(f"### 📊 Vista Previa de Datos")
    st.caption(f"Archivo: {archivo_seleccionado.name}")
    
    # Crear pestañas según el tipo de archivo
    if tipo_archivo == "Planta de Cemento":
        tabs = st.tabs(["🏢 Empresa", "🏭 Planta", "🪨 Clinker", "🏗️ Cementos"])
        
        with tabs[0]:
            st.markdown("**🏢 Información de Empresa**")
            show_empresa_info(data)
            
        with tabs[1]:
            st.markdown("**🏭 Información de Planta**")
            show_planta_info(data)
            
        with tabs[2]: 
            st.markdown("**🪨 Datos de Clinker**")
            show_clinker_data(data)
            
        with tabs[3]:
            st.markdown("**🏗️ Datos de Cementos**")
            show_cemento_data(data)
            
    else:  # Concreto
        tabs = st.tabs([
            "🏢 Empresa", 
            "🏭 Plantas", 
            "📊 Producción",
            "🧪 Mezclas",
            "🪨 Agregados",
            "🧴 Aditivos",
            "⚡ Consumos",
            "🚛 Transporte"
        ])
        
        with tabs[0]:
            st.markdown("**🏢 Información de Empresa**")
            show_empresa_info(data)
            
        with tabs[1]:
            st.markdown("**🏭 Plantas de Concreto**")
            show_plantas_concreto(data)
            
        with tabs[2]:
            st.markdown("**📊 Producción**")
            show_produccion_concreto(data)
            
        with tabs[3]:
            st.markdown("**🧪 Diseños de Mezcla**")
            show_mezclas(data)
            
        with tabs[4]:
            st.markdown("**🪨 Agregados y Adiciones**")
            show_agregados(data)
            
        with tabs[5]:
            st.markdown("**🧴 Aditivos**")
            show_aditivos(data)
            
        with tabs[6]:
            st.markdown("**⚡ Consumos Específicos**")
            show_consumos_especificos(data)
            
        with tabs[7]:
            st.markdown("**🚛 Transporte Mixer**")
            show_transporte_mixer(data)
    
    # Botón de descarga
    st.markdown("---")
    
    # Generar Excel directamente sin botón adicional
    try:
        generator = ExcelGenerator()
        
        empresa = data.get("hoja_empresa", {}).get("nombre_empresa", "Empresa")
        periodo = data.get("periodo", "2024")
        pais = data.get("hoja_empresa", {}).get("pais", "")
        
        if tipo_archivo == "Planta de Cemento":
            excel_data = generator.generate_clinker_cemento_excel(data)
            id_planta = data.get("hoja_planta", {}).get("id_planta", "")
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_{id_planta}.xlsx"
        else:
            excel_data = generator.generate_concreto_excel(data)
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_Concreto.xlsx"
        
        # Centrar el botón de descarga
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="descarga_desde_preview",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"❌ Error generando Excel: {str(e)}")