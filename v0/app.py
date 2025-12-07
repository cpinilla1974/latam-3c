import streamlit as st
import sqlite3
import os
from pathlib import Path

# Configuración de la aplicación
st.set_page_config(
    page_title="LATAM-3C v1",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_database():
    """Inicializa la base de datos SQLite si no existe"""
    db_path = Path("database/latam3c.db")
    if not db_path.exists():
        # Crear directorio si no existe
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear base de datos vacía
        conn = sqlite3.connect(str(db_path))
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_empresa (
                empresa_uuid TEXT PRIMARY KEY,
                pais TEXT NOT NULL,
                fecha_registro DATE,
                activa BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
    
    return str(db_path)

def main():
    # Inicializar base de datos
    db_path = init_database()
    
    # Título principal
    st.title("🛣️ Calculadora 3C País")
    st.markdown("### Versión 1.0 - Prototipo")
    
    # Sidebar para navegación
    st.sidebar.title("Navegación")
    
    # Inicializar session state si no existe
    if "menu_principal" not in st.session_state:
        st.session_state.menu_principal = "🏠 Inicio"
    
    # Menú principal con botones visibles
    if st.sidebar.button("🏠 Inicio", use_container_width=True, 
                        type="primary" if st.session_state.menu_principal == "🏠 Inicio" else "secondary"):
        st.session_state.menu_principal = "🏠 Inicio"
        st.rerun()
    
    st.sidebar.markdown("### Ingreso de Datos")
    
    if st.sidebar.button("📝 Ingreso Datos Empresa", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "📝 Ingreso Datos Empresa" else "secondary"):
        st.session_state.menu_principal = "📝 Ingreso Datos Empresa"
        st.rerun()
    
    st.sidebar.markdown("### Indicadores CO2")
    
    if st.sidebar.button("⚗️ CO2 Clinker", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "⚗️ CO2 Clinker" else "secondary"):
        st.session_state.menu_principal = "⚗️ CO2 Clinker"
        st.rerun()
    
    if st.sidebar.button("🏗️ CO2 Cemento", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "🏗️ CO2 Cemento" else "secondary"):
        st.session_state.menu_principal = "🏗️ CO2 Cemento"
        st.rerun()
    
    if st.sidebar.button("🪨 CO2 Concreto", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "🪨 CO2 Concreto" else "secondary"):
        st.session_state.menu_principal = "🪨 CO2 Concreto"
        st.rerun()
    
    if st.sidebar.button("💪 CO2 Resistencia Cemento", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "💪 CO2 Resistencia Cemento" else "secondary"):
        st.session_state.menu_principal = "💪 CO2 Resistencia Cemento"
        st.rerun()
    
    if st.sidebar.button("🏢 CO2 Resistencia Concreto", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "🏢 CO2 Resistencia Concreto" else "secondary"):
        st.session_state.menu_principal = "🏢 CO2 Resistencia Concreto"
        st.rerun()
    
    st.sidebar.markdown("### Otras Secciones")
    
    if st.sidebar.button("📊 Reportes", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "📊 Reportes" else "secondary"):
        st.session_state.menu_principal = "📊 Reportes"
        st.rerun()
    
    if st.sidebar.button("⚙️ Admin", use_container_width=True,
                        type="primary" if st.session_state.menu_principal == "⚙️ Admin" else "secondary"):
        st.session_state.menu_principal = "⚙️ Admin"
        st.rerun()
    
    # Contenido según selección
    menu_principal = st.session_state.menu_principal
    
    if menu_principal == "🏠 Inicio":
        show_home()
    elif menu_principal == "📝 Ingreso Datos Empresa":
        show_ingreso_datos()
    elif menu_principal == "⚗️ CO2 Clinker":
        show_co2_clinker()
    elif menu_principal == "🏗️ CO2 Cemento":
        show_co2_cemento()
    elif menu_principal == "🪨 CO2 Concreto":
        show_co2_concreto()
    elif menu_principal == "💪 CO2 Resistencia Cemento":
        show_co2_resistencia_cemento()
    elif menu_principal == "🏢 CO2 Resistencia Concreto":
        show_co2_resistencia_concreto()
    elif menu_principal == "📊 Reportes":
        show_reportes()
    elif menu_principal == "⚙️ Admin":
        show_admin()

def show_home():
    """Página de inicio"""
    st.header("Bienvenido a la Calculadora 3C País")
    st.markdown("Sistema de monitoreo de emisiones de CO2 para la industria del cemento y concreto")
    
    # Sección de accesos rápidos
    st.subheader("🚀 Accesos Rápidos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Ingreso de Datos")
        if st.button("📝 Ir a Ingreso de Datos", use_container_width=True, type="primary"):
            st.session_state.menu_principal = "📝 Ingreso Datos Empresa"
            st.rerun()
        st.caption("Visualiza formatos y descarga plantillas Excel para reportar datos")
    
    with col2:
        st.markdown("### 📊 Ver Indicadores")
        if st.button("📊 Ver Indicadores CO2", use_container_width=True, type="primary"):
            st.session_state.menu_principal = "⚗️ CO2 Clinker"
            st.rerun()
        st.caption("Consulta indicadores agregados de CO2 por país")
    
    st.markdown("---")
    
    # Indicadores disponibles
    st.subheader("📈 Indicadores Disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**⚗️ CO2 Clinker**\nEmisiones en producción de clinker")
        st.info("**🏗️ CO2 Cemento**\nEmisiones en producción de cemento")
    
    with col2:
        st.info("**🪨 CO2 Concreto**\nEmisiones en producción de concreto")
        st.info("**💪 CO2/Resistencia Cemento**\nÍndice de eficiencia del cemento")
    
    with col3:
        st.info("**🏢 CO2/Resistencia Concreto**\nÍndice de eficiencia del concreto")
        st.info("**📊 Reportes**\nReportes consolidados")
    
    st.markdown("---")
    
    # Estado del sistema
    st.subheader("💻 Estado del Sistema")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Países Reportando", "6", "+2")
    with col2:
        st.metric("Plantas Registradas", "47", "+5")
    with col3:
        st.metric("Última Actualización", "Nov 2024")
    
    st.markdown("---")
    st.caption("**Versión 1.0** - Sistema de Cálculo de Carbono para Cemento y Concreto")

def show_ingreso_datos():
    """Página de ingreso de datos de empresas"""
    st.header("📝 Ingreso de Datos de Empresa")
    
    # Pestañas para diferentes funciones
    tab1, tab2 = st.tabs(["📝 Ingresar Nuevos Datos", "👁️ Ver Datos Existentes"])
    
    with tab1:
        show_formulario_ingreso()
    
    with tab2:
        st.info("Visualiza y descarga los formatos de ejemplo en Excel")
        # Importar la funcionalidad de visualizar datos
        from pages.admin.visualizar_datos import show_visualizar_datos
        show_visualizar_datos()

def show_formulario_ingreso():
    """Formularios para ingresar nuevos datos"""
    st.subheader("📝 Formulario de Ingreso de Datos")
    
    # Selector de tipo de formulario
    tipo_formulario = st.selectbox(
        "Seleccione el tipo de datos a ingresar:",
        ["Planta de Cemento (Clinker + Cemento)", "Planta de Concreto"],
        key="tipo_formulario_ingreso"
    )
    
    if tipo_formulario == "Planta de Cemento (Clinker + Cemento)":
        show_formulario_cemento()
    else:
        show_formulario_concreto()

def show_formulario_cemento():
    """Formulario para datos de planta de cemento"""
    
    # Formulario por pestañas según estructura oficial
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏢 EMPRESA", "🏭 PLANTA", "⚗️ CLINKER", "🏗️ CEMENTO", "📊 GENERAR"])
    
    # Inicializar session state para datos del formulario
    if "cement_form_data" not in st.session_state:
        st.session_state.cement_form_data = {}
    
    with tab1:
        st.markdown("### Hoja 1: EMPRESA")
        st.info("Información general de la empresa que reporta")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.cement_form_data["nombre_empresa"] = st.text_input("Nombre Empresa*", key="cem_nombre_empresa")
            st.session_state.cement_form_data["pais"] = st.selectbox("País*", 
                ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú", "Ecuador", "Otro"], 
                key="cem_pais")
            st.session_state.cement_form_data["responsable"] = st.text_input("Responsable*", key="cem_responsable")
        
        with col2:
            st.session_state.cement_form_data["año_reporte"] = st.number_input("Año Reporte*", 
                min_value=2020, max_value=2030, value=2024, key="cem_año")
            st.session_state.cement_form_data["email"] = st.text_input("Email*", key="cem_email")
            st.session_state.cement_form_data["telefono"] = st.text_input("Teléfono", 
                placeholder="+57 1 234 5678", key="cem_telefono")

    with tab2:
        st.markdown("### Hoja 2: PLANTA")
        st.info("Información específica de esta planta de cemento")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.cement_form_data["id_planta"] = st.text_input("ID Planta*", 
                placeholder="P001", key="cem_id_planta")
            st.session_state.cement_form_data["nombre_planta"] = st.text_input("Nombre Planta*", 
                placeholder="Planta Norte", key="cem_nombre_planta")
            st.session_state.cement_form_data["ubicacion"] = st.text_input("Ubicación*", 
                placeholder="Bogotá, Cundinamarca", key="cem_ubicacion")
            st.session_state.cement_form_data["tipo_planta"] = st.selectbox("Tipo Planta*", 
                ["Integrada", "Molienda"], key="cem_tipo_planta")
        
        with col2:
            st.session_state.cement_form_data["latitud"] = st.number_input("Latitud", 
                format="%.6f", value=4.7110, key="cem_latitud")
            st.session_state.cement_form_data["longitud"] = st.number_input("Longitud", 
                format="%.6f", value=-74.0721, key="cem_longitud")
            st.session_state.cement_form_data["capacidad_clinker"] = st.number_input("Capacidad Clinker (ton/año)", 
                min_value=0, value=1200000, key="cem_cap_clinker")
            st.session_state.cement_form_data["capacidad_cemento"] = st.number_input("Capacidad Cemento (ton/año)", 
                min_value=0, value=1500000, key="cem_cap_cemento")
        
        st.session_state.cement_form_data["archivo_gcca"] = st.text_input("Archivo GCCA", 
            placeholder="GCCA_P001_2024.xlsx", key="cem_archivo_gcca")

    with tab3:
        st.markdown("### Hoja 3: CLINKER")
        
        if st.session_state.cement_form_data.get("tipo_planta") == "Integrada":
            st.info("Datos de producción de clinker (solo plantas integradas)")
            
            # Identificación
            st.markdown("#### IDENTIFICACIÓN")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.cement_form_data["produccion_clinker"] = st.number_input("Producción Clinker Anual (ton)*", 
                    min_value=0, key="cem_prod_clinker")
            with col2:
                st.session_state.cement_form_data["emisiones_proceso"] = st.number_input("Emisiones Proceso (tCO2)", 
                    min_value=0.0, help="Si disponible del archivo GCCA", key="cem_emisiones_proceso")
            
            # Sección A: Minerales
            st.markdown("#### SECCIÓN A: MINERALES")
            st.info("💡 Complete las cantidades de materias primas utilizadas")
            
            minerales_data = []
            minerales_tipos = ["Caliza", "Arcilla", "Mineral_Hierro", "Arena_Sílice", "Yeso", "Otros"]
            
            for i, mineral in enumerate(minerales_tipos):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2,1,2,1,1,1,1])
                with col1:
                    st.write(f"**{mineral}**")
                with col2:
                    cantidad = st.number_input("Cantidad (ton)", min_value=0, key=f"cem_min_{i}_cant", label_visibility="collapsed")
                with col3:
                    origen = st.text_input("Origen", key=f"cem_min_{i}_origen", label_visibility="collapsed")
                with col4:
                    dist_camion = st.number_input("Dist Camión (km)", min_value=0, key=f"cem_min_{i}_camion", label_visibility="collapsed")
                with col5:
                    dist_tren = st.number_input("Dist Tren (km)", min_value=0, key=f"cem_min_{i}_tren", label_visibility="collapsed")
                with col6:
                    dist_barco = st.number_input("Dist Barco (km)", min_value=0, key=f"cem_min_{i}_barco", label_visibility="collapsed")
                with col7:
                    dist_banda = st.number_input("Dist Banda (km)", min_value=0, key=f"cem_min_{i}_banda", label_visibility="collapsed")
                
                if cantidad > 0:
                    minerales_data.append({
                        "material": mineral,
                        "cantidad_ton": cantidad,
                        "origen": origen,
                        "dist_camion_km": dist_camion,
                        "dist_tren_km": dist_tren,
                        "dist_barco_km": dist_barco,
                        "dist_banda_km": dist_banda
                    })
            
            st.session_state.cement_form_data["minerales"] = minerales_data
            
            # Sección B: Combustibles Horno
            st.markdown("#### SECCIÓN B: COMBUSTIBLES HORNO")
            st.warning("🔗 **[Axioma A001]**: Los combustibles de horno se tomarán directamente de los archivos GCCA reportados por cada planta.")
            st.text_area("Referencia combustibles horno", 
                placeholder="Los datos se extraerán del archivo GCCA especificado en la Hoja PLANTA", 
                key="cem_combustibles_ref", disabled=True)
            
            # Sección C: Energía Eléctrica
            st.markdown("#### SECCIÓN C: ENERGÍA ELÉCTRICA")
            energia_data = []
            energia_tipos = [("Red_Nacional", "Sistema Interconectado"), ("Solar_Propia", "Paneles fotovoltaicos"), 
                           ("Eólica_PPA", "Contrato parque eólico"), ("Otra_Renovable", "Descripción")]
            
            for tipo, descripcion in energia_tipos:
                col1, col2, col3, col4 = st.columns([2,1,1,2])
                with col1:
                    st.write(f"**{tipo.replace('_', ' ')}**")
                with col2:
                    cantidad_kwh = st.number_input("kWh", min_value=0, key=f"cem_ener_{tipo}_kwh", label_visibility="collapsed")
                with col3:
                    factor_emision = st.number_input("Factor (kgCO2/kWh)", min_value=0.0, 
                                                   value=0.126 if "Red" in tipo else 0.0, 
                                                   key=f"cem_ener_{tipo}_factor", label_visibility="collapsed")
                with col4:
                    fuente = st.text_input("Fuente", value=descripcion, key=f"cem_ener_{tipo}_fuente", label_visibility="collapsed")
                
                if cantidad_kwh > 0:
                    energia_data.append({
                        "tipo_energia": tipo,
                        "cantidad_kwh": cantidad_kwh,
                        "factor_emision_kgco2_kwh": factor_emision,
                        "fuente": fuente
                    })
            
            st.session_state.cement_form_data["energia_electrica"] = energia_data
            
        else:
            st.warning("⚠️ Esta sección solo aplica para plantas integradas (que producen clinker)")
    
    with tab4:
        st.markdown("### Hojas 4+: CEMENTO_TIPO_[X]")
        st.info("Una sección por cada tipo de cemento producido en esta planta")
        
        # Permitir múltiples tipos de cemento
        num_cementos = st.number_input("Número de tipos de cemento producidos", min_value=1, max_value=5, value=1, key="cem_num_tipos")
        
        cementos_data = []
        for i in range(int(num_cementos)):
            st.markdown(f"#### CEMENTO TIPO {i+1}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**IDENTIFICACIÓN**")
                tipo_cemento = st.text_input("Tipo Cemento", placeholder="CPC 30R, CPO 40", key=f"cem_tipo_{i}")
                nombre_comercial = st.text_input("Nombre Comercial", key=f"cem_comercial_{i}")
                resistencia_28d_mpa = st.number_input("Resistencia 28d (MPa)", min_value=0.0, value=30.0, key=f"cem_resist_mpa_{i}")
                resistencia_28d_psi = st.number_input("Resistencia 28d (psi)", min_value=0.0, value=4350.0, key=f"cem_resist_psi_{i}")
                norma_tecnica = st.text_input("Norma Técnica", placeholder="NTC, ASTM, etc.", key=f"cem_norma_{i}")
                produccion_anual = st.number_input("Producción Anual (ton)", min_value=0, key=f"cem_prod_anual_{i}")
            
            with col2:
                st.markdown("**COMPOSICIÓN Y TRANSPORTE**")
                st.info("Materiales utilizados en este tipo de cemento")
                
                composicion_data = []
                materiales_cemento = [("CLK_01", "Clinker", "Producción propia"), ("CLK_02", "Clinker", "Proveedor externo"), 
                                    ("ESC_01", "Escoria", "Proveedor"), ("PUZ_01", "Puzolana/Ceniza", "Proveedor"), 
                                    ("CAL_01", "Caliza", "Cantera propia"), ("YES_01", "Yeso", "Stock/proveedor")]
                
                for id_mat, material, origen_default in materiales_cemento:
                    with st.expander(f"{material} ({id_mat})"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            proveedor = st.text_input("Proveedor/Origen", value=origen_default, key=f"cem_comp_{i}_{id_mat}_prov")
                            cantidad_ton = st.number_input("Cantidad (ton)", min_value=0, key=f"cem_comp_{i}_{id_mat}_cant")
                        with col_b:
                            dist_camion = st.number_input("Dist Camión (km)", min_value=0, key=f"cem_comp_{i}_{id_mat}_camion")
                            dist_tren = st.number_input("Dist Tren (km)", min_value=0, key=f"cem_comp_{i}_{id_mat}_tren")
                            dist_barco = st.number_input("Dist Barco (km)", min_value=0, key=f"cem_comp_{i}_{id_mat}_barco")
                            dist_banda = st.number_input("Dist Banda (km)", min_value=0, key=f"cem_comp_{i}_{id_mat}_banda")
                        
                        if cantidad_ton > 0:
                            composicion_data.append({
                                "id_material": id_mat,
                                "material": material,
                                "proveedor": proveedor,
                                "cantidad_ton": cantidad_ton,
                                "dist_camion_km": dist_camion,
                                "dist_tren_km": dist_tren,
                                "dist_barco_km": dist_barco,
                                "dist_banda_km": dist_banda
                            })
                
                st.markdown("**MOLIENDA Y COMBUSTIBLES**")
                electricidad_red_cem = st.number_input("Electricidad Red (kWh)", min_value=0, key=f"cem_elec_red_{i}")
                electricidad_renovable_cem = st.number_input("Electricidad Renovable (kWh)", min_value=0, key=f"cem_elec_ren_{i}")
                
                st.warning("🔗 **[Axioma A002]**: Los combustibles fuera de horno (molienda, secado, etc.) se tomarán directamente de los archivos GCCA de cada planta.")
            
            if tipo_cemento and produccion_anual > 0:
                cementos_data.append({
                    "tipo": tipo_cemento,
                    "identificacion": {
                        "tipo_cemento": tipo_cemento,
                        "nombre_comercial": nombre_comercial,
                        "resistencia_28d_mpa": resistencia_28d_mpa,
                        "resistencia_28d_psi": resistencia_28d_psi,
                        "norma_tecnica": norma_tecnica,
                        "produccion_anual_ton": produccion_anual
                    },
                    "composicion": composicion_data,
                    "molienda_combustibles": {
                        "electricidad_red_kwh": electricidad_red_cem,
                        "electricidad_renovable_kwh": electricidad_renovable_cem
                    }
                })
        
        st.session_state.cement_form_data["hojas_cemento"] = cementos_data

    with tab5:
        st.markdown("### 📊 Generar Archivo Excel")
        st.info("Revise la información ingresada y genere el archivo Excel para validación")
        
        # Mostrar resumen
        if st.session_state.cement_form_data:
            with st.expander("📋 Resumen de datos ingresados"):
                st.write("**Empresa:**", st.session_state.cement_form_data.get("nombre_empresa", "No especificado"))
                st.write("**País:**", st.session_state.cement_form_data.get("pais", "No especificado"))
                st.write("**Planta:**", st.session_state.cement_form_data.get("nombre_planta", "No especificado"))
                st.write("**ID Planta:**", st.session_state.cement_form_data.get("id_planta", "No especificado"))
                st.write("**Tipos de cemento configurados:**", len(st.session_state.cement_form_data.get("hojas_cemento", [])))
        
        if st.button("💾 Generar Archivo Excel para Validación", type="primary", key="cem_generar"):
            # Validar campos obligatorios
            campos_requeridos = ["nombre_empresa", "pais", "responsable", "email", "id_planta", "nombre_planta", "ubicacion"]
            campos_faltantes = [campo for campo in campos_requeridos if not st.session_state.cement_form_data.get(campo)]
            
            if campos_faltantes:
                st.error(f"⚠️ Faltan los siguientes campos obligatorios: {', '.join(campos_faltantes)}")
            else:
                # Generar estructura de datos completa
                datos_completos = st.session_state.cement_form_data
                
                # Mostrar preview y generar descarga
                with st.spinner("Generando archivo Excel..."):
                    mostrar_preview_y_descarga(datos_completos, "Cemento")
                    st.success("✅ Archivo Excel generado correctamente")
                    st.info("📁 El archivo sigue el formato oficial: [EMPRESA]_[PAIS]_[AÑO]_[ID_PLANTA].xlsx")

def show_formulario_concreto():
    """Formulario para datos consolidado de concreto según estructura oficial"""
    
    # Formulario por pestañas según las 10 hojas Excel oficiales
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🏢 EMPRESA", "🏭 PLANTAS", "📊 PRODUCCION", "🧪 MEZCLAS", 
        "🪨 AGREGADOS", "🧬 ADITIVOS", "⚡ ENERGIA", "🏭 CONSUMOS", "🚛 TRANSPORTE", "📋 GENERAR"
    ])
    
    # Inicializar session state para datos del formulario
    if "concrete_form_data" not in st.session_state:
        st.session_state.concrete_form_data = {}
    
    with tab1:
        st.markdown("### Hoja 1: EMPRESA")
        st.info("Información general de la empresa que reporta (igual que cemento)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.concrete_form_data["nombre_empresa"] = st.text_input("Nombre Empresa*", key="con_nombre_empresa")
            st.session_state.concrete_form_data["pais"] = st.selectbox("País*", 
                ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú", "Ecuador", "Otro"], 
                key="con_pais")
            st.session_state.concrete_form_data["responsable"] = st.text_input("Responsable*", key="con_responsable")
        
        with col2:
            st.session_state.concrete_form_data["año_reporte"] = st.number_input("Año Reporte*", 
                min_value=2020, max_value=2030, value=2024, key="con_año")
            st.session_state.concrete_form_data["email"] = st.text_input("Email*", key="con_email")
            st.session_state.concrete_form_data["telefono"] = st.text_input("Teléfono", key="con_telefono")

    with tab2:
        st.markdown("### Hoja 2: PLANTAS_CONCRETO")
        st.info("Listado de todas las plantas de concreto de la empresa")
        
        # Permitir múltiples plantas
        num_plantas = st.number_input("Número de plantas de concreto", min_value=1, max_value=10, value=1, key="con_num_plantas")
        
        plantas_data = []
        for i in range(int(num_plantas)):
            st.markdown(f"#### PLANTA {i+1}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                id_planta = st.text_input("ID Planta", placeholder=f"PC{str(i+1).zfill(3)}", key=f"con_planta_{i}_id")
                nombre_planta = st.text_input("Nombre Planta", placeholder="Planta Concreto Norte", key=f"con_planta_{i}_nombre")
                ubicacion = st.text_input("Ubicación", placeholder="Bogotá, Cundinamarca", key=f"con_planta_{i}_ubicacion")
            
            with col2:
                latitud = st.number_input("Latitud", format="%.6f", value=4.7110, key=f"con_planta_{i}_lat")
                longitud = st.number_input("Longitud", format="%.6f", value=-74.0721, key=f"con_planta_{i}_lon")
                tipo_planta = st.selectbox("Tipo", ["Fija", "Móvil"], key=f"con_planta_{i}_tipo")
            
            with col3:
                capacidad_m3 = st.number_input("Capacidad (m³/año)", min_value=0, value=250000, key=f"con_planta_{i}_capacidad")
            
            if id_planta and nombre_planta:
                plantas_data.append({
                    "id_planta": id_planta,
                    "nombre": nombre_planta,
                    "ubicacion": ubicacion,
                    "latitud": latitud,
                    "longitud": longitud,
                    "tipo": tipo_planta,
                    "capacidad_m3_año": capacidad_m3
                })
        
        st.session_state.concrete_form_data["plantas_concreto"] = plantas_data

    with tab3:
        st.markdown("### Hoja 3: PRODUCCION")
        st.info("Volúmenes anuales por planta y tipo de concreto")
        
        plantas_disponibles = [p["id_planta"] for p in st.session_state.concrete_form_data.get("plantas_concreto", [])]
        
        # Si no hay plantas configuradas, mostrar ejemplo para el video
        if not plantas_disponibles:
            st.warning("⚠️ Primero configure las plantas en la pestaña PLANTAS")
            st.markdown("**Vista previa de campos a configurar:**")
            plantas_disponibles = ["PC001", "PC002"]  # Plantas ejemplo para mostrar
        
        # Siempre mostrar la estructura
            st.markdown("**Configurar producción por planta:**")
            
            produccion_data = []
            categorias_disponibles = ["Estructural", "Alta_Resistencia", "Especiales"]
            tipos_disponibles = ["Convencional", "Premium", "Especializado"]
            resistencias_disponibles = ["f'c 210", "f'c 250", "f'c 280", "f'c 350", "f'c 420"]
            
            for planta_id in plantas_disponibles:
                st.markdown(f"#### Producción {planta_id}")
                
                num_productos = st.number_input(f"Productos diferentes en {planta_id}", 
                                              min_value=1, max_value=8, value=3, key=f"con_prod_{planta_id}_num")
                
                for j in range(int(num_productos)):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        categoria = st.selectbox("Categoría", categorias_disponibles, key=f"con_prod_{planta_id}_{j}_cat")
                    with col2:
                        tipo_concreto = st.selectbox("Tipo", tipos_disponibles, key=f"con_prod_{planta_id}_{j}_tipo")
                    with col3:
                        resistencia = st.selectbox("Resistencia", resistencias_disponibles, key=f"con_prod_{planta_id}_{j}_resist")
                    with col4:
                        volumen_m3 = st.number_input("Volumen (m³)", min_value=0, key=f"con_prod_{planta_id}_{j}_vol")
                    
                    if volumen_m3 > 0:
                        produccion_data.append({
                            "id_planta": planta_id,
                            "categoria": categoria,
                            "tipo_concreto": tipo_concreto,
                            "resistencia": resistencia,
                            "volumen_m3_anual": volumen_m3
                        })
            
            st.session_state.concrete_form_data["produccion"] = produccion_data

    with tab4:
        st.markdown("### Hoja 4: MEZCLAS")
        st.info("Diseños típicos utilizados")
        
        st.markdown("**Diseños de mezcla estándar:**")
        
        mezclas_data = []
        resistencias_mezcla = ["210", "250", "280", "350", "420"]
        
        for resistencia in resistencias_mezcla:
            with st.expander(f"Mezcla f'c {resistencia} MPa"):
                # Información básica
                col1, col2 = st.columns(2)
                with col1:
                    id_mezcla = st.text_input("ID Mezcla", value=f"MZ_{resistencia}", key=f"con_mezcla_{resistencia}_id")
                    tipo_cemento = st.selectbox("Tipo Cemento", ["CPC 30R", "CPO 40", "CPO 30"], key=f"con_mezcla_{resistencia}_tipo_cem")
                with col2:
                    st.markdown("**Resistencia especificada**")
                    st.write(f"f'c {resistencia} MPa")
                
                # Materiales con cantidades organizadas
                st.markdown("**Dosificación por m³:**")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("**CEMENTO**")
                    cemento_kg_m3 = st.number_input("Cantidad (kg)", min_value=0.0, value=320.0, key=f"con_mezcla_{resistencia}_cem")
                    st.text(f"Tipo: {tipo_cemento if 'tipo_cemento' in locals() else 'CPC 30R'}")
                
                with col2:
                    st.markdown("**ARENA**")
                    arena_kg_m3 = st.number_input("Cantidad (kg)", min_value=0.0, value=850.0, key=f"con_mezcla_{resistencia}_arena")
                    id_arena = st.text_input("ID Material", value="ARE_01", key=f"con_mezcla_{resistencia}_id_arena")
                
                with col3:
                    st.markdown("**GRAVA**")
                    grava_kg_m3 = st.number_input("Cantidad (kg)", min_value=0.0, value=950.0, key=f"con_mezcla_{resistencia}_grava")
                    id_grava = st.text_input("ID Material", value="GRA_01", key=f"con_mezcla_{resistencia}_id_grava")
                
                with col4:
                    st.markdown("**AGUA**")
                    agua_l_m3 = st.number_input("Cantidad (L)", min_value=0.0, value=180.0, key=f"con_mezcla_{resistencia}_agua")
                    st.text("Fuente: Red/Pozo")
                
                # Aditivos y adiciones
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**ADITIVOS**")
                    aditivo_l_m3 = st.number_input("Aditivo (L/m³)", min_value=0.0, value=2.5, key=f"con_mezcla_{resistencia}_aditivo")
                    id_aditivo = st.text_input("ID Aditivo", value="ADI_01", key=f"con_mezcla_{resistencia}_id_aditivo")
                
                with col2:
                    st.markdown("**ADICIONES**")
                    adiciones_kg_m3 = st.number_input("Adiciones (kg/m³)", min_value=0.0, key=f"con_mezcla_{resistencia}_adiciones")
                    id_adicion = st.text_input("ID Adición", placeholder="ESC_01, CEN_01, etc.", key=f"con_mezcla_{resistencia}_id_adicion")
                
                if cemento_kg_m3 > 0:
                    mezclas_data.append({
                        "id_mezcla": id_mezcla,
                        "resistencia": f"f'c {resistencia}",
                        "cemento_kg_m3": cemento_kg_m3,
                        "tipo_cemento": tipo_cemento,
                        "arena_kg_m3": arena_kg_m3,
                        "id_arena": id_arena,
                        "grava_kg_m3": grava_kg_m3,
                        "id_grava": id_grava,
                        "agua_l_m3": agua_l_m3,
                        "aditivo_l_m3": aditivo_l_m3,
                        "id_aditivo": id_aditivo,
                        "adiciones_kg_m3": adiciones_kg_m3,
                        "id_adicion": id_adicion if id_adicion != "-" else ""
                    })
        
        st.session_state.concrete_form_data["mezclas"] = mezclas_data

    with tab5:
        st.markdown("### Hoja 5: AGREGADOS Y ADICIONES")
        st.info("Materiales utilizados: arenas, gravas, adiciones")
        
        agregados_data = []
        materiales_agregados = [
            ("ARE_01", "Arena", "Río"), ("ARE_02", "Arena", "Triturada"),
            ("GRA_01", "Grava", "3/4\""), ("GRA_02", "Grava", "1/2\""),
            ("ESC_01", "Escoria", "Granulada"), ("CEN_01", "Ceniza", "Volante")
        ]
        
        for id_mat, material, tipo_default in materiales_agregados:
            with st.expander(f"{material} ({id_mat})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo = st.text_input("Tipo", value=tipo_default, key=f"con_agr_{id_mat}_tipo")
                    proveedor = st.text_input("Proveedor", placeholder="Cantera XYZ", key=f"con_agr_{id_mat}_prov")
                    cantidad_ton = st.number_input("Cantidad Anual (ton)", min_value=0, key=f"con_agr_{id_mat}_cant")
                
                with col2:
                    dist_camion = st.number_input("Distancia Camión (km)", min_value=0, key=f"con_agr_{id_mat}_camion")
                    dist_tren = st.number_input("Distancia Tren (km)", min_value=0, key=f"con_agr_{id_mat}_tren")
                    dist_barco = st.number_input("Distancia Barco (km)", min_value=0, key=f"con_agr_{id_mat}_barco")
                
                if cantidad_ton > 0:
                    agregados_data.append({
                        "id_material": id_mat,
                        "material": material,
                        "tipo": tipo,
                        "proveedor": proveedor,
                        "cantidad_ton_anual": cantidad_ton,
                        "dist_camion_km": dist_camion,
                        "dist_tren_km": dist_tren,
                        "dist_barco_km": dist_barco
                    })
        
        st.session_state.concrete_form_data["agregados_adiciones"] = agregados_data

    with tab6:
        st.markdown("### Hoja 6: ADITIVOS")
        st.info("Aditivos químicos utilizados")
        
        aditivos_data = []
        tipos_aditivos = [
            ("ADI_01", "Plastificante", "Reductor de agua"),
            ("ADI_02", "Superplastificante", "Alto rango"),
            ("ADI_03", "Retardante", "Control fraguado"),
            ("ADI_04", "Otros", "Descripción")
        ]
        
        for id_adit, tipo_default, funcion_default in tipos_aditivos:
            with st.expander(f"Aditivo {id_adit}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo_aditivo = st.text_input("Tipo", value=tipo_default, key=f"con_adit_{id_adit}_tipo")
                    funcion = st.text_input("Función", value=funcion_default, key=f"con_adit_{id_adit}_funcion")
                    marca = st.text_input("Marca", key=f"con_adit_{id_adit}_marca")
                
                with col2:
                    proveedor = st.text_input("Proveedor", key=f"con_adit_{id_adit}_prov")
                    cantidad_l = st.number_input("Cantidad Anual (L)", min_value=0, key=f"con_adit_{id_adit}_cant")
                    dist_camion = st.number_input("Distancia (km)", min_value=0, key=f"con_adit_{id_adit}_dist")
                
                if cantidad_l > 0:
                    aditivos_data.append({
                        "id_aditivo": id_adit,
                        "tipo_aditivo": tipo_aditivo,
                        "funcion": funcion,
                        "marca": marca,
                        "proveedor": proveedor,
                        "cantidad_l_anual": cantidad_l,
                        "dist_camion_km": dist_camion,
                        "dist_tren_km": 0,
                        "dist_barco_km": 0
                    })
        
        st.session_state.concrete_form_data["aditivos"] = aditivos_data

    with tab7:
        st.markdown("### Hoja 7: ENERGIA_AGUA")
        st.info("Consumos anuales consolidados de energía, combustibles y agua de todas las plantas")
        
        # Electricidad
        st.markdown("#### ⚡ ELECTRICIDAD")
        col1, col2 = st.columns(2)
        with col1:
            plantas_mezclado = st.number_input("Plantas Mezclado (kWh/año)", min_value=0, value=2500000, key="con_elec_mezclado", help="Consumo total de electricidad para mezclado en todas las plantas")
        with col2:
            plantas_bombeo = st.number_input("Plantas Bombeo (kWh/año)", min_value=0, value=800000, key="con_elec_bombeo", help="Consumo total para equipos de bombeo")
        
        st.caption("*Origen: Red nacional - Factor de emisión según país*")
        
        # Combustibles
        st.markdown("#### ⛽ COMBUSTIBLES")
        col1, col2, col3 = st.columns(3)
        with col1:
            diesel_mixers = st.number_input("Diesel Mixers (L/año)", min_value=0, value=450000, key="con_diesel_mixers", help="Consumo de diesel de todos los camiones mixer")
        with col2:
            diesel_bombas = st.number_input("Diesel Bombas (L/año)", min_value=0, value=75000, key="con_diesel_bombas", help="Consumo de diesel de equipos de bombeo")
        with col3:
            gasolina = st.number_input("Gasolina Vehículos (L/año)", min_value=0, value=25000, key="con_gasolina", help="Consumo de gasolina de vehículos auxiliares")
        
        # Agua
        st.markdown("#### 💧 AGUA")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Agua para mezcla**")
            agua_mezcla = st.number_input("Volumen total (m³/año)", min_value=0, value=180000, key="con_agua_mezcla")
            porc_red = st.slider("% de red pública", 0, 100, 80, key="con_agua_red")
            porc_pozo = st.slider("% de pozo propio", 0, 100, 20, key="con_agua_pozo")
            st.caption(f"Red: {agua_mezcla * porc_red / 100:.0f} m³/año | Pozo: {agua_mezcla * porc_pozo / 100:.0f} m³/año")
        
        with col2:
            st.markdown("**Agua para lavado**")
            agua_lavado = st.number_input("Volumen total (m³/año)", min_value=0, value=50000, key="con_agua_lavado")
            porc_reciclada = st.slider("% reciclada", 0, 100, 30, key="con_agua_reciclada")
            st.caption(f"Reciclada: {agua_lavado * porc_reciclada / 100:.0f} m³/año | Nueva: {agua_lavado * (100-porc_reciclada) / 100:.0f} m³/año")
        
        energia_agua_data = {
            "electricidad": {
                "plantas_mezclado": plantas_mezclado,
                "plantas_bombeo": plantas_bombeo
            },
            "combustibles": {
                "diesel_mixers": diesel_mixers,
                "diesel_bombas": diesel_bombas,
                "gasolina": gasolina
            },
            "agua": {
                "agua_mezcla": agua_mezcla,
                "porc_red": porc_red,
                "porc_pozo": porc_pozo,
                "agua_lavado": agua_lavado,
                "porc_reciclada": porc_reciclada
            }
        }
        
        st.session_state.concrete_form_data["energia_agua"] = energia_agua_data

    with tab8:
        st.markdown("### Hoja 8: CONSUMOS_ESPECIFICOS_PLANTA")
        st.info("Consumos específicos por m³ de concreto producido")
        
        plantas_disponibles = [p["id_planta"] for p in st.session_state.concrete_form_data.get("plantas_concreto", [])]
        
        # Si no hay plantas, mostrar ejemplo para el video
        if not plantas_disponibles:
            plantas_disponibles = ["PC001", "PC002", "PC003"]  # Plantas ejemplo
        
        st.markdown("**Consumos promedio anual por m³ de concreto producido:**")
        
        consumos_data = []
        for planta_id in plantas_disponibles:
            st.markdown(f"#### Consumos {planta_id}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                elec_kwh_m3 = st.number_input("Electricidad (kWh/m³)", min_value=0.0, value=4.5, key=f"con_consumo_{planta_id}_elec")
            with col2:
                diesel_cargador = st.number_input("Diesel Cargador (L/m³)", min_value=0.0, value=0.8, key=f"con_consumo_{planta_id}_diesel_carg")
            with col3:
                diesel_otros = st.number_input("Diesel Otros (L/m³)", min_value=0.0, value=0.2, key=f"con_consumo_{planta_id}_diesel_otros")
            with col4:
                notas = st.text_input("Notas", placeholder="Incluye iluminación", key=f"con_consumo_{planta_id}_notas")
            
            consumos_data.append({
                "id_planta": planta_id,
                "electricidad_kwh_m3": elec_kwh_m3,
                "diesel_cargador_l_m3": diesel_cargador,
                "diesel_otros_l_m3": diesel_otros,
                "notas": notas
            })
        
        st.session_state.concrete_form_data["consumos_especificos"] = consumos_data

    with tab9:
        st.markdown("### Hoja 9: TRANSPORTE_MIXER")
        st.info("Consumo de combustible de camiones mixer por planta")
        
        plantas_disponibles = [p["id_planta"] for p in st.session_state.concrete_form_data.get("plantas_concreto", [])]
        
        # Si no hay plantas, mostrar ejemplo para el video
        if not plantas_disponibles:
            plantas_disponibles = ["PC001", "PC002", "PC003"]  # Plantas ejemplo
        
        st.markdown("**Configuración de transporte por planta:**")
        st.caption("*Nota: Factor_Retorno = proporción del viaje de retorno con carga (0.7 = retorna vacío 30% del tiempo)*")
        
        transporte_data = []
        for planta_id in plantas_disponibles:
            st.markdown(f"#### Transporte {planta_id}")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                radio_promedio = st.number_input("Radio Promedio (km)", min_value=0.0, value=15.0, key=f"con_transp_{planta_id}_radio")
            with col2:
                diesel_l_m3 = st.number_input("Diesel (L/m³)", min_value=0.0, value=3.5, key=f"con_transp_{planta_id}_diesel")
            with col3:
                tipo_camion = st.selectbox("Tipo Camión", ["Mixer estándar", "Mixer pequeño"], key=f"con_transp_{planta_id}_tipo")
            with col4:
                capacidad_m3 = st.number_input("Capacidad (m³)", min_value=0, value=8, key=f"con_transp_{planta_id}_cap")
            with col5:
                factor_retorno = st.number_input("Factor Retorno", min_value=0.0, max_value=1.0, value=0.7, key=f"con_transp_{planta_id}_retorno")
            
            transporte_data.append({
                "id_planta": planta_id,
                "radio_promedio_km": radio_promedio,
                "diesel_l_m3": diesel_l_m3,
                "tipo_camion": tipo_camion,
                "capacidad_m3": capacidad_m3,
                "factor_retorno": factor_retorno
            })
        
        st.session_state.concrete_form_data["transporte_mixer"] = transporte_data

    with tab10:
        st.markdown("### 📊 Generar Archivo Excel")
        st.info("Revise la información ingresada y genere el archivo Excel consolidado")
        
        # Mostrar resumen
        if st.session_state.concrete_form_data:
            with st.expander("📋 Resumen de datos ingresados"):
                st.write("**Empresa:**", st.session_state.concrete_form_data.get("nombre_empresa", "No especificado"))
                st.write("**País:**", st.session_state.concrete_form_data.get("pais", "No especificado"))
                st.write("**Plantas configuradas:**", len(st.session_state.concrete_form_data.get("plantas_concreto", [])))
                st.write("**Productos configurados:**", len(st.session_state.concrete_form_data.get("produccion", [])))
                st.write("**Mezclas configuradas:**", len(st.session_state.concrete_form_data.get("mezclas", [])))
        
        if st.button("💾 Generar Archivo Excel Consolidado", type="primary", key="con_generar"):
            # Validar campos obligatorios
            campos_requeridos = ["nombre_empresa", "pais", "responsable", "email"]
            campos_faltantes = [campo for campo in campos_requeridos if not st.session_state.concrete_form_data.get(campo)]
            
            if campos_faltantes:
                st.error(f"⚠️ Faltan los siguientes campos obligatorios: {', '.join(campos_faltantes)}")
            elif not st.session_state.concrete_form_data.get("plantas_concreto"):
                st.error("⚠️ Debe configurar al menos una planta de concreto")
            else:
                # Generar estructura de datos completa
                datos_completos = st.session_state.concrete_form_data
                
                # Mostrar preview y generar descarga
                with st.spinner("Generando archivo Excel consolidado..."):
                    mostrar_preview_y_descarga(datos_completos, "Concreto")
                    st.success("✅ Archivo Excel generado correctamente")
                    st.info("📁 El archivo sigue el formato oficial: [EMPRESA]_[PAIS]_[AÑO]_Concreto.xlsx")

def generar_json_cemento(nombre_empresa, pais, responsable, email, telefono,
                        id_planta, nombre_planta, ubicacion, tipo_planta,
                        latitud, longitud, capacidad_clinker, capacidad_cemento,
                        produccion_clinker, emisiones_proceso, consumo_energia, factor_emision_energia,
                        tipo_cemento, nombre_comercial, resistencia_mpa, produccion_cemento,
                        contenido_clinker, norma_tecnica,
                        electricidad_red, electricidad_renovable, combustible_principal, consumo_combustible):
    """Genera estructura JSON para planta de cemento"""
    
    import datetime
    
    datos = {
        "periodo": datetime.datetime.now().year,
        "hoja_empresa": {
            "nombre_empresa": nombre_empresa,
            "pais": pais,
            "responsable": responsable,
            "email": email,
            "telefono": telefono
        },
        "hoja_planta": {
            "id_planta": id_planta,
            "nombre": nombre_planta,
            "ubicacion": ubicacion,
            "latitud": latitud,
            "longitud": longitud,
            "tipo_planta": tipo_planta,
            "capacidad_clinker_ton_año": capacidad_clinker,
            "capacidad_cemento_ton_año": capacidad_cemento,
            "archivo_gcca": ""
        }
    }
    
    # Agregar datos de clinker solo si es planta integrada
    if tipo_planta == "Integrada" and produccion_clinker > 0:
        datos["hoja_clinker"] = {
            "identificacion": {
                "produccion_clinker_anual_ton": produccion_clinker,
                "emisiones_proceso_tco2": emisiones_proceso
            },
            "minerales": [],
            "combustibles_horno_referencia": f"Combustible principal: {combustible_principal}",
            "energia_electrica": [{
                "tipo_energia": "Red eléctrica",
                "cantidad_kwh": electricidad_red,
                "factor_emision_kgco2_kwh": factor_emision_energia,
                "fuente": "Red nacional"
            }]
        }
    
    # Datos de cemento
    datos["hojas_cemento"] = [{
        "tipo": tipo_cemento,
        "identificacion": {
            "tipo_cemento": tipo_cemento,
            "nombre_comercial": nombre_comercial,
            "resistencia_28d_mpa": resistencia_mpa,
            "norma_tecnica": norma_tecnica,
            "produccion_anual_ton": produccion_cemento
        },
        "molienda_combustibles": {
            "electricidad_red_kwh": electricidad_red,
            "electricidad_renovable_kwh": electricidad_renovable,
            "combustibles_fuera_horno_referencia": f"Consumo: {consumo_combustible} GJ"
        },
        "composicion": [{
            "id_material": "CLK001",
            "material": "Clinker",
            "proveedor": "Producción propia" if tipo_planta == "Integrada" else "Externo",
            "cantidad_ton": produccion_cemento * (contenido_clinker/100),
            "dist_camion_km": 0,
            "dist_tren_km": 0,
            "dist_barco_km": 0,
            "dist_banda_km": 0
        }]
    }]
    
    return datos

def generar_json_concreto(nombre_empresa, pais, responsable, email, telefono,
                         id_planta, nombre_planta, ubicacion, latitud, longitud, capacidad_m3,
                         categoria, tipo_concreto, resistencia, volumen_anual,
                         cemento_kg_m3, tipo_cemento, arena_kg_m3, grava_kg_m3, agua_l_m3, aditivo_l_m3,
                         radio_promedio, tipo_camion, diesel_l_m3, factor_retorno):
    """Genera estructura JSON para planta de concreto"""
    
    import datetime
    
    datos = {
        "periodo": datetime.datetime.now().year,
        "hoja_empresa": {
            "nombre_empresa": nombre_empresa,
            "pais": pais,
            "responsable": responsable,
            "email": email,
            "telefono": telefono
        },
        "hoja_plantas_concreto": [{
            "id_planta": id_planta,
            "nombre": nombre_planta,
            "ubicacion": ubicacion,
            "latitud": latitud,
            "longitud": longitud,
            "tipo": categoria,
            "capacidad_m3_año": capacidad_m3
        }],
        "hoja_produccion": [{
            "id_planta": id_planta,
            "categoria": categoria,
            "tipo_concreto": tipo_concreto,
            "resistencia": resistencia,
            "volumen_m3_anual": volumen_anual
        }],
        "hoja_mezclas": [{
            "id_mezcla": f"MX_{resistencia.replace(' ', '')}",
            "resistencia": resistencia,
            "cemento_kg_m3": cemento_kg_m3,
            "tipo_cemento": tipo_cemento,
            "arena_kg_m3": arena_kg_m3,
            "id_arena": "AR001",
            "grava_kg_m3": grava_kg_m3,
            "id_grava": "GR001",
            "agua_l_m3": agua_l_m3,
            "aditivo_l_m3": aditivo_l_m3,
            "id_aditivo": "AD001",
            "adiciones_kg_m3": 0,
            "id_adicion": ""
        }],
        "hoja_agregados_adiciones": [{
            "id_material": "AR001",
            "material": "Arena",
            "tipo": "Agregado fino",
            "proveedor": "Proveedor local",
            "cantidad_ton_anual": arena_kg_m3 * volumen_anual / 1000,
            "dist_camion_km": 50,
            "dist_tren_km": 0,
            "dist_barco_km": 0
        }, {
            "id_material": "GR001",
            "material": "Grava",
            "tipo": "Agregado grueso",
            "proveedor": "Proveedor local",
            "cantidad_ton_anual": grava_kg_m3 * volumen_anual / 1000,
            "dist_camion_km": 50,
            "dist_tren_km": 0,
            "dist_barco_km": 0
        }],
        "hoja_aditivos": [{
            "id_aditivo": "AD001",
            "tipo_aditivo": "Plastificante",
            "funcion": "Reducir agua",
            "marca": "Marca comercial",
            "proveedor": "Proveedor químicos",
            "cantidad_l_anual": aditivo_l_m3 * volumen_anual,
            "dist_camion_km": 100,
            "dist_tren_km": 0,
            "dist_barco_km": 0
        }],
        "hoja_transporte_mixer": [{
            "id_planta": id_planta,
            "radio_promedio_km": radio_promedio,
            "diesel_l_m3": diesel_l_m3,
            "tipo_camion": tipo_camion,
            "capacidad_m3": int(tipo_camion.split()[1].replace('m³', '')),
            "factor_retorno": factor_retorno
        }]
    }
    
    return datos

def mostrar_preview_y_descarga(datos_json, tipo_archivo):
    """Muestra preview de los datos y permite descarga"""
    
    st.success("✅ Datos ingresados correctamente!")
    
    # Mostrar resumen
    st.markdown("### 📋 Resumen de Datos Ingresados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Empresa:** {datos_json['hoja_empresa']['nombre_empresa']}")
        st.info(f"**País:** {datos_json['hoja_empresa']['pais']}")
        st.info(f"**Tipo:** {tipo_archivo}")
    
    with col2:
        if tipo_archivo == "Planta de Cemento":
            planta = datos_json['hoja_planta']
            st.info(f"**Planta:** {planta['nombre']}")
            st.info(f"**Tipo:** {planta['tipo_planta']}")
            if 'hojas_cemento' in datos_json:
                st.info(f"**Producción Cemento:** {datos_json['hojas_cemento'][0]['identificacion']['produccion_anual_ton']:,} ton/año")
        else:
            planta = datos_json['hoja_plantas_concreto'][0]
            st.info(f"**Planta:** {planta['nombre']}")
            st.info(f"**Capacidad:** {planta['capacidad_m3_año']:,} m³/año")
            st.info(f"**Producción:** {datos_json['hoja_produccion'][0]['volumen_m3_anual']:,} m³/año")
    
    # Generar Excel y permitir descarga
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
        from excel_generator_v2 import ExcelGenerator
        
        generator = ExcelGenerator()
        
        empresa = datos_json["hoja_empresa"]["nombre_empresa"]
        periodo = datos_json["periodo"]
        pais = datos_json["hoja_empresa"]["pais"]
        
        if tipo_archivo == "Planta de Cemento":
            excel_data = generator.generate_clinker_cemento_excel(datos_json)
            id_planta = datos_json["hoja_planta"]["id_planta"]
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_{id_planta}.xlsx"
        else:
            excel_data = generator.generate_concreto_excel(datos_json)
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_Concreto.xlsx"
        
        # Botón de descarga
        st.markdown("### 📥 Descargar Archivo")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.download_button(
                label="📥 Descargar Excel Generado",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
        
        st.success("🎉 Archivo Excel generado exitosamente!")
        st.info("💡 **Próximos pasos:** El archivo Excel contiene todos los datos ingresados organizados en las pestañas correspondientes.")
        
    except Exception as e:
        st.error(f"❌ Error generando Excel: {str(e)}")
        
        # Opción alternativa: descargar JSON
        import json
        json_str = json.dumps(datos_json, indent=2, ensure_ascii=False)
        
        st.markdown("### 📄 Descarga Alternativa (JSON)")
        st.download_button(
            label="📄 Descargar JSON",
            data=json_str,
            file_name=f"{empresa.replace(' ', '_')}_{pais}_{periodo}.json",
            mime="application/json"
        )

def show_reportes():
    """Página de reportes"""
    st.header("📊 Reportes")
    st.info("Funcionalidad en desarrollo")

def show_co2_clinker():
    """Indicadores de CO2 para Clinker por país"""
    st.header("⚗️ Indicadores CO2 - Clinker")
    st.info("Resultados agregados de emisiones de CO2 en la producción de clinker por país")
    
    # Datos de ejemplo para demostración
    import pandas as pd
    
    # Tabla de indicadores por país
    st.subheader("📊 Emisiones de CO2 por País")
    
    datos_paises = pd.DataFrame({
        "País": ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú"],
        "Producción Clinker (Mt/año)": [3.2, 5.1, 38.5, 7.2, 28.4, 4.8],
        "Factor Emisión (kg CO2/ton)": [850, 840, 835, 845, 855, 848],
        "Emisiones Totales (Mt CO2/año)": [2.72, 4.28, 32.15, 6.08, 24.28, 4.07],
        "Intensidad CO2": [0.85, 0.84, 0.83, 0.84, 0.86, 0.85]
    })
    
    st.dataframe(datos_paises, use_container_width=True, hide_index=True)
    
    # Gráfico de barras
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(datos_paises.set_index("País")["Emisiones Totales (Mt CO2/año)"])
        st.caption("Emisiones totales de CO2 por país")
    
    with col2:
        st.bar_chart(datos_paises.set_index("País")["Factor Emisión (kg CO2/ton)"])
        st.caption("Factor de emisión promedio por país")
    
    # Métricas resumen
    st.subheader("📈 Métricas Regionales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Producción Total", "87.2 Mt/año", "+3.5%")
    with col2:
        st.metric("Emisiones Totales", "73.6 Mt CO2/año", "-2.1%")
    with col3:
        st.metric("Factor Promedio", "844 kg CO2/ton", "-1.2%")

def show_co2_cemento():
    """Indicadores de CO2 para Cemento por país"""
    st.header("🏗️ Indicadores CO2 - Cemento")
    st.info("Resultados agregados de emisiones de CO2 en la producción de cemento por país")
    
    import pandas as pd
    
    st.subheader("📊 Emisiones de CO2 en Producción de Cemento")
    
    datos_cemento = pd.DataFrame({
        "País": ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú"],
        "Producción Cemento (Mt/año)": [4.5, 6.8, 52.3, 9.1, 35.2, 6.2],
        "Contenido Clinker (%)": [75, 72, 68, 74, 77, 73],
        "Factor Emisión (kg CO2/ton)": [650, 625, 590, 640, 670, 635],
        "Emisiones Totales (Mt CO2/año)": [2.93, 4.25, 30.86, 5.82, 23.58, 3.94]
    })
    
    st.dataframe(datos_cemento, use_container_width=True, hide_index=True)
    
    # Gráficos comparativos
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(datos_cemento.set_index("País")["Producción Cemento (Mt/año)"])
        st.caption("Producción de cemento por país")
    
    with col2:
        st.bar_chart(datos_cemento.set_index("País")["Contenido Clinker (%)"])
        st.caption("Contenido de clinker promedio por país")
    
    # Métricas resumen
    st.subheader("📈 Métricas Regionales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Producción Total", "114.1 Mt/año", "+4.2%")
    with col2:
        st.metric("Emisiones Totales", "71.4 Mt CO2/año", "-3.1%")
    with col3:
        st.metric("Contenido Clinker Promedio", "73%", "-2%")

def show_co2_concreto():
    """Indicadores de CO2 para Concreto por país"""
    st.header("🪨 Indicadores CO2 - Concreto")
    st.info("Resultados agregados de emisiones de CO2 en la producción de concreto por país")
    
    import pandas as pd
    
    st.subheader("📊 Emisiones de CO2 en Producción de Concreto")
    
    datos_concreto = pd.DataFrame({
        "País": ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú"],
        "Producción Concreto (Mm³/año)": [12.5, 18.3, 125.6, 22.4, 85.7, 15.2],
        "Contenido Cemento (kg/m³)": [350, 340, 320, 345, 360, 355],
        "Emisiones Cemento (kg CO2/m³)": [227, 212, 189, 221, 241, 225],
        "Emisiones Transporte (kg CO2/m³)": [15, 18, 12, 16, 14, 17],
        "Emisiones Totales (Mt CO2/año)": [3.03, 4.21, 25.24, 5.31, 21.85, 3.68]
    })
    
    st.dataframe(datos_concreto, use_container_width=True, hide_index=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(datos_concreto.set_index("País")["Producción Concreto (Mm³/año)"])
        st.caption("Producción de concreto por país (millones m³)")
    
    with col2:
        st.bar_chart(datos_concreto.set_index("País")["Contenido Cemento (kg/m³)"])
        st.caption("Contenido de cemento promedio por país")
    
    # Métricas resumen
    st.subheader("📈 Métricas Regionales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Producción Total", "279.7 Mm³/año", "+5.8%")
    with col2:
        st.metric("Emisiones Totales", "63.3 Mt CO2/año", "+2.3%")
    with col3:
        st.metric("Contenido Cemento Promedio", "345 kg/m³", "-1.5%")

def show_co2_resistencia_cemento():
    """Indicadores de CO2 por Resistencia - Cemento"""
    
    import pandas as pd
    
    st.subheader("📊 Índice CO2/Resistencia de Cementos")
    
    datos_resistencia = pd.DataFrame({
        "País": ["Chile", "Argentina", "Brasil", "Colombia", "México", "Perú"],
        "Resistencia Promedio (MPa)": [42.5, 40.0, 45.0, 41.0, 38.5, 40.5],
        "Factor CO2 (kg CO2/ton)": [650, 625, 590, 640, 670, 635],
        "Índice CO2/MPa": [15.3, 15.6, 13.1, 15.6, 17.4, 15.7],
        "Tipo Cemento Predominante": ["Portland Compuesto", "Portland Normal", "Portland Puzolánico", "Portland Compuesto", "Portland Normal", "Portland Compuesto"]
    })
    
    st.dataframe(datos_resistencia, use_container_width=True, hide_index=True)
    
    # Sistema de Bandas GCCA para Cemento (según metodología oficial)
    st.subheader("🎯 Bandas GCCA - Clasificación de Cemento")
    st.info("Clasificación según fórmula oficial GCCA: X_i = (40 + 85 × CCr) × i")
    
    # Control para ajustar ratio clínker/cemento
    col1, col2 = st.columns([2, 1])
    
    with col1:
        relacion_clinker_cemento = st.slider(
            "Relación clínker/cemento (CCr)",
            min_value=0.30,
            max_value=1.0,
            value=0.706,
            step=0.001,
            format="%.3f",
            help="La relación entre clínker y cemento afecta los rangos según GCCA. Alemania usa 0.706"
        )
    
    with col2:
        st.markdown("**Fórmula utilizada:**")
        st.latex(r"X_i = (40 + 85 \\times CCr) \\times i")
        st.caption(f"CCr = {relacion_clinker_cemento}")
    
    # Función para calcular rangos según fórmula GCCA
    def calcular_rangos_gcca(CCr):
        rangos = {'AA': 0}  # Near Zero siempre es 0
        base = 40 + 85 * CCr
        
        for i in range(1, 8):
            if i == 1: rangos['A'] = int(base * i)
            elif i == 2: rangos['B'] = int(base * i)
            elif i == 3: rangos['C'] = int(base * i)
            elif i == 4: rangos['D'] = int(base * i)
            elif i == 5: rangos['E'] = int(base * i)
            elif i == 6: rangos['F'] = int(base * i)
            elif i == 7: rangos['G'] = int(base * i)
        
        return rangos
    
    # Función para clasificar cemento
    def clasificar_cemento(gwp, rangos):
        if gwp <= rangos['A']: return 'AA'
        
        clases = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for i in range(len(clases)-1):
            if rangos[clases[i]] <= gwp < rangos[clases[i+1]]:
                return clases[i]
        
        return 'G'  # Si es mayor que F
    
    # Función para obtener colores oficiales GCCA
    def obtener_color_clase(clase):
        colores = {
            'AA': '#00A651',  'A': '#39B54A',   'B': '#8DC63F',   'C': '#00AEEF',
            'D': '#0054A6',   'E': '#A7A9AC',   'F': '#6D6E71',   'G': '#231F20'
        }
        return colores.get(clase, '#CCCCCC')
    
    # Calcular rangos y clasificar países
    rangos = calcular_rangos_gcca(relacion_clinker_cemento)
    datos_resistencia['clase_gcca'] = datos_resistencia['Factor CO2 (kg CO2/ton)'].apply(
        lambda x: clasificar_cemento(x, rangos)
    )
    datos_resistencia['color_clase'] = datos_resistencia['clase_gcca'].apply(obtener_color_clase)
    
    # Mostrar tabla de rangos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Rangos de Clasificación:**")
        rangos_df = pd.DataFrame({
            "Clase": list(rangos.keys()),
            "Límite (kg CO2/t)": list(rangos.values())
        })
        
        # Agregar descripción de rangos
        rangos_df["Rango"] = ""
        for i, clase in enumerate(rangos_df["Clase"]):
            if clase == 'AA':
                rangos_df.loc[i, "Rango"] = f"0 - {rangos['A']}"
            elif clase == 'G':
                rangos_df.loc[i, "Rango"] = f">{rangos['F']}"
            else:
                clases_orden = list(rangos.keys())
                idx = clases_orden.index(clase)
                if idx < len(clases_orden) - 1:
                    siguiente = clases_orden[idx + 1]
                    rangos_df.loc[i, "Rango"] = f"{rangos[clase]} - {rangos[siguiente]}"
        
        st.dataframe(rangos_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**🎯 Clasificación de Países:**")
        for _, row in datos_resistencia.iterrows():
            st.write(f"**{row['País']}**: {row['Factor CO2 (kg CO2/ton)']} kg CO2/t → Clase **{row['clase_gcca']}**")
    
    # Visualización principal: Bandas GCCA con posición de países
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Crear bandas horizontales por clasificación
    clases_ordenadas = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
    colores_bandas = ['#00A651', '#39B54A', '#8DC63F', '#00AEEF', '#0054A6', '#A7A9AC', '#6D6E71', '#231F20']
    
    # Dibujar bandas de fondo
    x_left = 0
    max_limite = max(rangos.values()) + 50  # Un poco más para que se vea bien
    
    for i, clase in enumerate(clases_ordenadas):
        if clase in rangos:
            if clase == 'AA':
                x_right = rangos['A']
                width = x_right - x_left
            else:
                x_right = rangos[clase]
                width = x_right - x_left
            
            ax.barh([0], [width], left=x_left, height=0.6, 
                   color=colores_bandas[i], alpha=0.4, 
                   edgecolor='white', linewidth=1)
            
            # Añadir etiqueta de clase en el centro de cada banda
            center_x = x_left + width/2
            ax.text(center_x, 0, f'Clase {clase}', 
                   ha='center', va='center', fontweight='bold', 
                   fontsize=11, color='white' if i > 4 else 'black')
            
            x_left = x_right
    
    # Añadir líneas verticales para los límites
    for clase, limite in rangos.items():
        if clase != 'AA':
            ax.axvline(x=limite, color='gray', linestyle='--', alpha=0.7, linewidth=1)
            ax.text(limite, 0.4, f'{limite}', ha='center', va='bottom', 
                   fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Añadir marcadores para cada país
    for i, (_, row) in enumerate(datos_resistencia.iterrows()):
        valor = row['Factor CO2 (kg CO2/ton)']
        clase = row['clase_gcca']
        color = obtener_color_clase(clase)
        
        # Marcador principal
        ax.scatter(valor, -0.15, s=150, c=color, edgecolors='black', 
                  linewidth=2, zorder=5, marker='o')
        
        # Etiqueta del país
        ax.text(valor, -0.35, f"{row['País']}\n{valor} kg CO2/t", 
               ha='center', va='top', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7, edgecolor='black'))
    
    ax.set_xlim(0, max_limite)
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlabel('Emisiones de CO2 (kg/t)', fontsize=12, fontweight='bold')
    ax.set_title('Clasificación GCCA de Cemento - Posición de Países por Bandas', fontsize=14, fontweight='bold', pad=20)
    ax.set_yticks([])
    ax.grid(True, axis='x', alpha=0.3)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Análisis por tipo de cemento
    st.subheader("📦 Análisis por Tipo de Cemento")
    
    tipo_cemento = pd.DataFrame({
        "Tipo Cemento": ["Portland Normal", "Portland Compuesto", "Portland Puzolánico", "Alta Resistencia"],
        "Resistencia Media (MPa)": [39.3, 41.3, 45.0, 52.5],
        "Factor CO2 Medio (kg/ton)": [648, 625, 590, 680],
        "Índice CO2/MPa": [16.5, 15.1, 13.1, 13.0]
    })
    
    st.dataframe(tipo_cemento, use_container_width=True, hide_index=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mejor Índice Regional", "13.1 kg CO2/MPa", "Brasil")
    with col2:
        st.metric("Promedio Regional", "15.5 kg CO2/MPa", "-3.2%")
    with col3:
        st.metric("Cemento Más Eficiente", "Alta Resistencia", "13.0")

def show_co2_resistencia_concreto():
    """Indicadores de CO2 por Resistencia - Concreto"""
    st.header("🏢 Indicadores CO2/Resistencia - Concreto")
    st.info("Índice de eficiencia: emisiones de CO2 por unidad de resistencia del concreto por país")
    
    import pandas as pd
    import json
    import os
    
    st.subheader("📊 Índice CO2/Resistencia de Concretos")
    
    # Crear curvas completas por país para cada resistencia
    resistencias = [20, 25, 30, 35, 40, 50]
    datos_por_pais = {
        "Chile": [210, 230, 250, 280, 310, 380],
        "Argentina": [195, 215, 240, 270, 295, 360],
        "Brasil": [170, 185, 205, 230, 255, 310],
        "Colombia": [200, 220, 245, 275, 300, 370],
        "México": [220, 245, 270, 300, 330, 400],
        "Perú": [205, 225, 250, 280, 305, 375]
    }
    
    # Crear tabla resumen
    datos_resistencia_concreto = pd.DataFrame({
        "País": list(datos_por_pais.keys()),
        "Resistencia 20 MPa": [datos_por_pais[pais][0] for pais in datos_por_pais.keys()],
        "Resistencia 25 MPa": [datos_por_pais[pais][1] for pais in datos_por_pais.keys()],
        "Resistencia 30 MPa": [datos_por_pais[pais][2] for pais in datos_por_pais.keys()],
        "Resistencia 35 MPa": [datos_por_pais[pais][3] for pais in datos_por_pais.keys()],
        "Resistencia 40 MPa": [datos_por_pais[pais][4] for pais in datos_por_pais.keys()],
        "Resistencia 50 MPa": [datos_por_pais[pais][5] for pais in datos_por_pais.keys()]
    })
    
    st.dataframe(datos_resistencia_concreto, use_container_width=True, hide_index=True)
    
    # Sistema de Bandas GCCA para Concreto
    st.subheader("🎯 Bandas GCCA - Clasificación de Concreto")
    
    # Función para cargar bandas desde JSON
    def cargar_bandas_concreto():
        json_path = "/home/cpinilla/storage/files/bandas_gcca.json"
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                bandas = json.load(f)
            # Asegurar que las claves de resistencia sean enteros
            bandas = {k: {int(r): v for r, v in d.items()} for k, d in bandas.items()}
            return bandas
        except FileNotFoundError:
            st.error(f"No se pudo encontrar el archivo {json_path}")
            return {}
    
    # Cargar bandas desde JSON
    bandas = cargar_bandas_concreto()
    
    if not bandas:
        st.error("No se pudieron cargar las bandas GCCA")
        return
        
    # Crear DataFrame para visualización
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    
    # Crear DataFrame - cada fila es una banda, cada columna es una resistencia
    df_bandas = pd.DataFrame.from_dict(bandas, orient='index')
    df_bandas = df_bandas[[20, 25, 30, 35, 40, 50]]  # Asegurar orden de columnas
    df_bandas = df_bandas.sort_values(by=20)  # Ordenar por valores de resistencia 20 MPa
    
    # Definir valor máximo para banda H (fuera de límites)
    valor_maximo_banda_h = 600
    df_bandas.loc["Top of H"] = [valor_maximo_banda_h] * len(df_bandas.columns)
    
    # Colores oficiales GCCA
    bandas_ordenadas = df_bandas.index.tolist()
    colores_bandas = [
        "#2ca02c",  # AA Near Zero - Verde
        "#006400",  # A - Verde oscuro
        "#1f77b4",  # B - Azul
        "#00bfff",  # C - Azul claro
        "#007acc",  # D - Azul medio
        "#7f7f7f",  # E - Gris
        "#4d4d4d",  # F - Gris oscuro
        "#1f1f1f",  # H - Negro
    ]
    
    # Selector de tipo de visualización
    tipo_visualizacion = st.radio(
        "Seleccionar tipo de visualización:",
        ["Gráfico de Líneas con Bandas", "Clasificación por País", "Tabla Completa de Límites"],
        horizontal=True
    )
    
    # Función para clasificar en bandas
    def clasificar_en_bandas(resistencia, huella, df_bandas):
        if resistencia not in df_bandas.columns:
            # Buscar la resistencia más cercana
            resistencias = [20, 25, 30, 35, 40, 50]
            resistencia = min(resistencias, key=lambda x: abs(x - resistencia))
        
        for banda in bandas_ordenadas:
            if huella <= df_bandas.loc[banda, resistencia]:
                return banda
        return "Top of H"  # Si no cae en ninguna banda
    
    if tipo_visualizacion == "Gráfico de Líneas con Bandas":
        # Gráfico de líneas con bandas de fondo
        fig, ax = plt.subplots(figsize=(14, 8))
        resistencias_disponibles = sorted([int(col) for col in df_bandas.columns])
        
        # Dibujar bandas de fondo
        base_inferior = np.zeros(len(resistencias_disponibles))
        for i, banda in enumerate(bandas_ordenadas):
            valores_banda = [df_bandas.loc[banda, r] for r in resistencias_disponibles]
            ax.fill_between(
                resistencias_disponibles, base_inferior, valores_banda, 
                label=banda.replace("Top of ", "").replace(" -Near Zero Product", " Near Zero"), 
                color=colores_bandas[i], 
                alpha=0.7
            )
            base_inferior = valores_banda
        
        # Agregar línea con datos promedio por resistencia
        # Simular datos promedio regionales
        emisiones_promedio = [180, 210, 230, 260, 290, 350]  # Datos ejemplo
        
        ax.plot(resistencias_disponibles, emisiones_promedio, 
                marker="o", linewidth=3, markersize=8,
                label="FICEM", color="red")
        
        # Agregar curvas completas por país
        for pais, emisiones_pais in datos_por_pais.items():
            ax.plot(resistencias_disponibles, emisiones_pais, 
                   marker="s", linewidth=2, markersize=6,
                   label=pais, zorder=5)
        
        ax.set_title("Bandas GCCA para Concreto - Datos por País")
        ax.set_xlabel("Resistencia (MPa)")
        ax.set_ylabel("Huella de CO₂ (kg/m³)")
        ax.set_ylim(0, valor_maximo_banda_h)
        ax.legend(loc="upper left", fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.5)
        
        st.pyplot(fig)
        
    elif tipo_visualizacion == "Clasificación por País":
        # Clasificar cada país según sus datos
        st.subheader("📊 Clasificación de Países por Bandas GCCA")
        
        clasificaciones = []
        for pais, emisiones_por_resistencia in datos_por_pais.items():
            for i, resistencia in enumerate(resistencias):
                emisiones = emisiones_por_resistencia[i]
                banda = clasificar_en_bandas(resistencia, emisiones, df_bandas)
                
                clasificaciones.append({
                    "País": pais,
                    "Resistencia (MPa)": resistencia,
                    "Emisiones (kg CO2/m³)": emisiones,
                    "Banda GCCA": banda,
                    "Límite Banda": df_bandas.loc[banda, resistencia]
                })
        
        df_clasificaciones = pd.DataFrame(clasificaciones)
        st.dataframe(df_clasificaciones, use_container_width=True, hide_index=True)
        
        # Gráfico de distribución por bandas
        banda_counts = df_clasificaciones['Banda GCCA'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(banda_counts.index, banda_counts.values, 
                     color=[colores_bandas[bandas_ordenadas.index(b)] for b in banda_counts.index])
        
        ax.set_title("Distribución de Países por Banda GCCA")
        ax.set_xlabel("Banda GCCA")
        ax.set_ylabel("Número de Países")
        
        # Agregar etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
    else:  # Tabla Completa de Límites
        st.subheader("📋 Tabla Completa de Límites GCCA para Concreto")
        
        # Mostrar tabla completa
        tabla_limites = df_bandas.drop("Top of H").copy()  # Sin incluir banda H
        tabla_limites.index = [idx.replace("Top of ", "Banda ").replace(" -Near Zero Product", " (Near Zero)") for idx in tabla_limites.index]
        tabla_limites.columns = [f"{col} MPa" for col in tabla_limites.columns]
        
        st.dataframe(tabla_limites, use_container_width=True)
        
        # Información adicional
        st.markdown("""
        **📝 Notas:**
        - **AA (Near Zero)**: Productos con emisiones cercanas a cero
        - Los valores mostrados son los límites superiores para cada banda
        - Un concreto con emisiones ≤ límite pertenece a esa banda
        - Valores superiores a banda F se clasifican como fuera de estándar
        """)
    
    # Selector de resistencia para análisis detallado
    st.subheader("🔍 Análisis Detallado por Resistencia")
    resistencia_analisis = st.selectbox(
        "Seleccionar resistencia para análisis:",
        [20, 25, 30, 35, 40, 50],
        index=2,  # Default 30 MPa
        format_func=lambda x: f"{x} MPa"
    )
    
    # Mostrar límites para la resistencia seleccionada
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📊 Límites para {resistencia_analisis} MPa:**")
        limites_resistencia = df_bandas.drop("Top of H")[resistencia_analisis].to_frame()
        limites_resistencia.columns = ["Límite (kg CO2/m³)"]
        limites_resistencia.index = [idx.replace("Top of ", "Banda ").replace(" -Near Zero Product", " (Near Zero)") for idx in limites_resistencia.index]
        st.dataframe(limites_resistencia)
    
    with col2:
        st.markdown(f"**🎯 Clasificación por País para {resistencia_analisis} MPa:**")
        
        # Obtener índice de resistencia
        idx_resistencia = resistencias.index(resistencia_analisis)
        
        for pais, emisiones_por_resistencia in datos_por_pais.items():
            emisiones = emisiones_por_resistencia[idx_resistencia]
            banda = clasificar_en_bandas(resistencia_analisis, emisiones, df_bandas)
            banda_display = banda.replace("Top of ", "").replace(" -Near Zero Product", " (Near Zero)")
            st.write(f"**{pais}**: {emisiones} kg CO2/m³ → **Banda {banda_display}**")
    
    # Análisis por categoría de resistencia
    st.subheader("📊 Análisis por Categoría de Resistencia")
    
    categorias = pd.DataFrame({
        "Categoría": ["Concreto Normal (21-35 MPa)", "Concreto Alta Resistencia (>35 MPa)", "Concreto Especial (>50 MPa)"],
        "Contenido Cemento Promedio (kg/m³)": [340, 420, 500],
        "Emisiones Promedio (kg CO2/m³)": [220, 270, 325],
        "Índice CO2/MPa": [7.8, 6.2, 5.5]
    })
    
    st.dataframe(categorias, use_container_width=True, hide_index=True)
    
    # Métricas
    st.subheader("📈 Métricas de Eficiencia")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mejor Índice Regional", "5.40 kg CO2/MPa", "Brasil")
    with col2:
        st.metric("Promedio Regional", "7.43 kg CO2/MPa", "-4.1%")
    with col3:
        st.metric("Potencial de Mejora", "27%", "Con optimización")

def show_admin():
    """Página de administración"""
    st.header("⚙️ Administración")
    
    # Pestañas de admin
    tab1, tab2, tab3 = st.tabs(["📄 Generar Excel", "👁️ Visualizar Datos", "🔧 Configuración"])
    
    with tab1:
        # Importar y mostrar la página de generación de Excel
        from pages.admin.generar_excel import show_generar_excel
        show_generar_excel()
    
    with tab2:
        # Importar y mostrar la página de visualización
        from pages.admin.visualizar_datos import show_visualizar_datos
        show_visualizar_datos()
    
    with tab3:
        st.subheader("Configuración del Sistema")
        st.info("Configuraciones en desarrollo")

if __name__ == "__main__":
    main()