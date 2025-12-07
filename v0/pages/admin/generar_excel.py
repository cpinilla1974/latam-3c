import streamlit as st
import json
from pathlib import Path
import sys
import os

# Agregar el directorio modules al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))

from excel_generator_v2 import ExcelGenerator

def get_json_files():
    """Obtiene todos los archivos JSON disponibles en la carpeta data"""
    data_path = Path("../data")
    json_files = []
    
    if data_path.exists():
        json_files = list(data_path.glob("*.json"))
    
    # Categorizar archivos por nuevo esquema
    planta_files = [f for f in json_files if ("_P0" in f.name or "clinker_cemento" in f.name) and "concreto" not in f.name]
    concreto_files = [f for f in json_files if "concreto" in f.name]
    
    return planta_files, concreto_files

def extract_company_name(json_filename):
    """Extrae el nombre de empresa del archivo JSON"""
    try:
        generator = ExcelGenerator()
        # Si json_filename es un Path, convertir a string
        if hasattr(json_filename, 'name'):
            json_data = generator.load_json(json_filename)
        else:
            json_data = generator.load_json(json_filename)
        return json_data.get("hoja_empresa", {}).get("nombre_empresa", "Empresa")
    except Exception as e:
        print(f"Error extracting company name from {json_filename}: {e}")
        return "Empresa"

def show_generar_excel():
    """Página para generar archivos Excel de ejemplo"""
    
    st.subheader("📄 Generador de Excel")
    
    # Obtener archivos disponibles
    planta_files, concreto_files = get_json_files()
    
    if not planta_files and not concreto_files:
        st.warning("⚠️ No se encontraron archivos JSON en la carpeta data/")
        return
    
    
    tipo_archivo = st.selectbox(
        "Seleccionar tipo de archivo:",
        ["Planta de Cemento", "Concreto"],
        key="generar_tipo_archivo"
    )
    
    # Selector dinámico de archivo según el tipo
    if tipo_archivo == "Planta de Cemento":
        if not planta_files:
            st.warning("No hay archivos de plantas disponibles")
            return
        archivo_seleccionado = st.selectbox(
            "Seleccionar archivo JSON:",
            planta_files,
            format_func=lambda x: f"{extract_company_name(x.name)} ({x.name})",
            key="generar_archivo_planta"
        )
    else:
        if not concreto_files:
            st.warning("No hay archivos de Concreto disponibles")
            return
        archivo_seleccionado = st.selectbox(
            "Seleccionar archivo JSON:",
            concreto_files,
            format_func=lambda x: f"{extract_company_name(x.name)} ({x.name})",
            key="generar_archivo_concreto"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Generar Excel", type="primary"):
            generate_excel_file(tipo_archivo, archivo_seleccionado)
    
    with col2:
        visualizar_clicked = st.button("👁️ Visualizar Datos")
    
    # Mostrar visualización fuera de las columnas para usar todo el ancho
    if visualizar_clicked:
        from pages.admin.visualizar_datos import show_data_preview
        st.markdown("---")
        show_data_preview(archivo_seleccionado, tipo_archivo)

def generate_excel_file(tipo_archivo, archivo_json):
    """Genera el archivo Excel según el tipo y archivo seleccionado"""
    
    try:
        generator = ExcelGenerator()
        
        # Cargar JSON seleccionado
        json_data = generator.load_json(archivo_json)
        
        # Extraer información para el nombre del archivo
        empresa = json_data.get("hoja_empresa", {}).get("nombre_empresa", "Empresa")
        periodo = json_data.get("periodo", "2024")
        pais = json_data.get("hoja_empresa", {}).get("pais", "")
        
        if tipo_archivo == "Planta de Cemento":
            # Generar Excel
            excel_data = generator.generate_clinker_cemento_excel(json_data)
            
            # Nombre de archivo dinámico - incluir ID de planta
            id_planta = json_data.get("hoja_planta", {}).get("id_planta", "")
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_{id_planta}.xlsx"
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Excel Planta",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success(f"✅ Excel de Planta {id_planta} generado para {empresa}!")
            
        elif tipo_archivo == "Concreto":
            # Generar Excel
            excel_data = generator.generate_concreto_excel(json_data)
            
            # Nombre de archivo dinámico
            filename = f"{empresa.replace(' ', '_')}_{pais}_{periodo}_Concreto.xlsx"
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Excel Concreto",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success(f"✅ Excel de Concreto generado para {empresa}!")
            
    except Exception as e:
        st.error(f"❌ Error generando Excel: {str(e)}")

def show_json_preview(archivo_json):
    """Muestra una vista previa del JSON seleccionado"""
    
    try:
        generator = ExcelGenerator()
        json_data = generator.load_json(archivo_json)
        
        st.markdown(f"### 📋 Vista Previa - {archivo_json}")
        
        # Mostrar estructura básica
        st.json({
            "archivo": archivo_json,
            "periodo": json_data.get("periodo", "N/A"),
            "empresa": json_data.get("hoja_empresa", {}).get("nombre_empresa", "N/A"),
            "pais": json_data.get("hoja_empresa", {}).get("pais", "N/A"),
            "numero_hojas": len([k for k in json_data.keys() if k.startswith("hoja")])
        })
        
        # Expandir para ver JSON completo
        with st.expander("🔍 Ver JSON completo"):
            st.json(json_data)
            
    except Exception as e:
        st.error(f"❌ Error cargando JSON: {str(e)}")

def check_json_files():
    """Verifica que haya archivos JSON disponibles"""
    clinker_files, concreto_files = get_json_files()
    
    if not clinker_files and not concreto_files:
        st.warning("⚠️ No se encontraron archivos JSON en la carpeta ../data/")
        st.info("Agrega archivos JSON con los nombres que contengan 'clinker_cemento' o 'concreto'")
        return False
    
    return True

# Verificar archivos al cargar el módulo
if not check_json_files():
    st.stop()