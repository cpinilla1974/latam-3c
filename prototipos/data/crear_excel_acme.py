import pandas as pd
from datetime import datetime
import json

# Crear el archivo Excel ACME_Colombia_2024_Clinker_Cemento.xlsx

# Crear un writer de Excel
archivo_salida = 'ACME_Colombia_2024_Clinker_Cemento.xlsx'
writer = pd.ExcelWriter(archivo_salida, engine='xlsxwriter')

# HOJA 1: EMPRESA
empresa_data = {
    'Campo': ['Nombre_Empresa', 'País', 'Año_Reporte', 'Responsable', 'Email', 'Teléfono'],
    'Valor': ['ACME Cementos S.A.', 'Colombia', 2024, 'Ana García', 'agarcia@acme.com', '+57 1 234 5678']
}
df_empresa = pd.DataFrame(empresa_data)
df_empresa.to_excel(writer, sheet_name='EMPRESA', index=False)

# HOJA 2: PLANTAS_CEMENTO
plantas_data = {
    'ID_Planta': ['P001', 'P002'],
    'Nombre': ['Planta Norte', 'Planta Sur'],
    'Ubicación': ['Bogotá, Cundinamarca', 'Cali, Valle del Cauca'],
    'Archivo_GCCA': ['GCCA_P001_2024.xlsx', 'GCCA_P002_2024.xlsx']
}
df_plantas = pd.DataFrame(plantas_data)
df_plantas.to_excel(writer, sheet_name='PLANTAS_CEMENTO', index=False)

# HOJA 3: PRODUCCION_CLINKER
# SECCIÓN A: MINERALES
minerales_data = {
    'Material': ['Caliza', 'Arcilla', 'Mineral_Hierro', 'Arena_Sílice', 'Yeso', 'Otros'],
    'Cantidad_ton': [2700000, 320000, 28000, 0, 65000, 0],
    'Origen': ['Cantera propia', 'Cantera local', 'Proveedor Nacional', '-', 'Importado', '-'],
    'Distancia_km': [5, 25, 150, 0, 500, 0],
    'Modo_Transporte': ['Banda', 'Camión', 'Camión', '-', 'Barco', '-']
}

# SECCIÓN B: COMBUSTIBLES (Nota indicando que vienen de GCCA)
combustibles_data = {
    'Combustible': ['NOTA: Los datos de combustibles se tomarán de los archivos GCCA de cada planta'],
    'Cantidad': ['-'],
    'Unidad': ['-'],
    'Origen': ['-'],
    'Distancia_km': ['-'],
    'Modo_Transporte': ['-']
}

# SECCIÓN C: ENERGÍA ELÉCTRICA (Nota indicando que viene de GCCA)
energia_data = {
    'Tipo_Energía': ['NOTA: Los datos de energía eléctrica se tomarán de los archivos GCCA de cada planta'],
    'Cantidad_kWh': ['-'],
    'Factor_Emisión_kgCO2/kWh': ['-'],
    'Fuente': ['-']
}

# SECCIÓN D: PRODUCCIÓN
produccion_data = {
    'Concepto': ['Clinker_Producido'],
    'Cantidad_ton': [1800000]
}

# Crear DataFrame combinado con secciones
df_clinker = pd.DataFrame()

# Agregar encabezados de sección y datos
current_row = 0
with pd.ExcelWriter(archivo_salida, engine='xlsxwriter') as writer:
    # HOJA EMPRESA
    df_empresa.to_excel(writer, sheet_name='EMPRESA', index=False)
    
    # HOJA PLANTAS
    df_plantas.to_excel(writer, sheet_name='PLANTAS_CEMENTO', index=False)
    
    # HOJA PRODUCCION_CLINKER con secciones
    worksheet = writer.book.add_worksheet('PRODUCCION_CLINKER')
    bold = writer.book.add_format({'bold': True})
    
    # SECCIÓN A: MINERALES
    worksheet.write(0, 0, 'SECCIÓN A: MINERALES', bold)
    df_minerales = pd.DataFrame(minerales_data)
    for col_num, value in enumerate(df_minerales.columns.values):
        worksheet.write(1, col_num, value, bold)
    for row_num, row_data in enumerate(df_minerales.values):
        for col_num, value in enumerate(row_data):
            worksheet.write(row_num + 2, col_num, value)
    
    # SECCIÓN B: COMBUSTIBLES
    worksheet.write(10, 0, 'SECCIÓN B: COMBUSTIBLES', bold)
    worksheet.write(11, 0, '*Nota: Estos datos se tomarán de archivos GCCA de cada planta')
    
    # SECCIÓN C: ENERGÍA ELÉCTRICA  
    worksheet.write(14, 0, 'SECCIÓN C: ENERGÍA ELÉCTRICA', bold)
    worksheet.write(15, 0, '*Nota: Estos datos se tomarán de archivos GCCA de cada planta')
    
    # SECCIÓN D: PRODUCCIÓN
    worksheet.write(18, 0, 'SECCIÓN D: PRODUCCIÓN', bold)
    df_produccion = pd.DataFrame(produccion_data)
    for col_num, value in enumerate(df_produccion.columns.values):
        worksheet.write(19, col_num, value, bold)
    for row_num, row_data in enumerate(df_produccion.values):
        for col_num, value in enumerate(row_data):
            worksheet.write(row_num + 20, col_num, value)
    
    # HOJA 4: CEMENTO_TIPO_1 (CPC 30R)
    ws_cem1 = writer.book.add_worksheet('CEMENTO_TIPO_1')
    
    # IDENTIFICACIÓN
    ws_cem1.write(0, 0, 'IDENTIFICACIÓN', bold)
    ws_cem1.write(1, 0, 'Campo', bold)
    ws_cem1.write(1, 1, 'Valor', bold)
    ws_cem1.write(2, 0, 'Tipo_Cemento')
    ws_cem1.write(2, 1, 'CPC 30R')
    ws_cem1.write(3, 0, 'Nombre_Comercial')
    ws_cem1.write(3, 1, 'Cemento Estructural')
    ws_cem1.write(4, 0, 'Producción_Anual_ton')
    ws_cem1.write(4, 1, 950000)
    
    # COMPOSICIÓN Y TRANSPORTE
    ws_cem1.write(6, 0, 'COMPOSICIÓN Y TRANSPORTE', bold)
    composicion1_data = {
        'ID_Material': ['CLK_01', 'ESC_01', 'CAL_01', 'YES_01'],
        'Material': ['Clinker', 'Escoria', 'Caliza', 'Yeso'],
        'Proveedor/Origen': ['Producción propia', 'Siderúrgica Nacional', 'Cantera propia', 'Stock'],
        'Cantidad_ton': [807500, 95000, 38000, 9500],
        'Distancia_km': [0, 200, 5, 0],
        'Modo_Transporte': ['-', 'Camión', 'Banda', '-']
    }
    df_comp1 = pd.DataFrame(composicion1_data)
    for col_num, value in enumerate(df_comp1.columns.values):
        ws_cem1.write(7, col_num, value, bold)
    for row_num, row_data in enumerate(df_comp1.values):
        for col_num, value in enumerate(row_data):
            ws_cem1.write(row_num + 8, col_num, value)
    
    # MOLIENDA
    ws_cem1.write(13, 0, 'MOLIENDA', bold)
    ws_cem1.write(14, 0, 'Concepto', bold)
    ws_cem1.write(14, 1, 'Cantidad_kWh', bold)
    ws_cem1.write(15, 0, 'Electricidad_Red')
    ws_cem1.write(15, 1, 38000000)
    ws_cem1.write(16, 0, 'Electricidad_Renovable')
    ws_cem1.write(16, 1, 2000000)
    
    # HOJA 5: CEMENTO_TIPO_2 (CPO 40)
    ws_cem2 = writer.book.add_worksheet('CEMENTO_TIPO_2')
    
    # IDENTIFICACIÓN
    ws_cem2.write(0, 0, 'IDENTIFICACIÓN', bold)
    ws_cem2.write(1, 0, 'Campo', bold)
    ws_cem2.write(1, 1, 'Valor', bold)
    ws_cem2.write(2, 0, 'Tipo_Cemento')
    ws_cem2.write(2, 1, 'CPO 40')
    ws_cem2.write(3, 0, 'Nombre_Comercial')
    ws_cem2.write(3, 1, 'Cemento Alta Resistencia')
    ws_cem2.write(4, 0, 'Producción_Anual_ton')
    ws_cem2.write(4, 1, 620000)
    
    # COMPOSICIÓN Y TRANSPORTE
    ws_cem2.write(6, 0, 'COMPOSICIÓN Y TRANSPORTE', bold)
    composicion2_data = {
        'ID_Material': ['CLK_01', 'CLK_02', 'CAL_01', 'YES_01'],
        'Material': ['Clinker', 'Clinker', 'Caliza', 'Yeso'],
        'Proveedor/Origen': ['Producción propia', 'Importado Vietnam', 'Cantera propia', 'Stock'],
        'Cantidad_ton': [527000, 62000, 24800, 6200],
        'Distancia_km': [0, 15000, 5, 0],
        'Modo_Transporte': ['-', 'Barco', 'Banda', '-']
    }
    df_comp2 = pd.DataFrame(composicion2_data)
    for col_num, value in enumerate(df_comp2.columns.values):
        ws_cem2.write(7, col_num, value, bold)
    for row_num, row_data in enumerate(df_comp2.values):
        for col_num, value in enumerate(row_data):
            ws_cem2.write(row_num + 8, col_num, value)
    
    # MOLIENDA
    ws_cem2.write(13, 0, 'MOLIENDA', bold)
    ws_cem2.write(14, 0, 'Concepto', bold)
    ws_cem2.write(14, 1, 'Cantidad_kWh', bold)
    ws_cem2.write(15, 0, 'Electricidad_Red')
    ws_cem2.write(15, 1, 27900000)
    ws_cem2.write(16, 0, 'Electricidad_Renovable')
    ws_cem2.write(16, 1, 0)
    
    # HOJA 6: CEMENTO_TIPO_3 (CPO 40RS)
    ws_cem3 = writer.book.add_worksheet('CEMENTO_TIPO_3')
    
    # IDENTIFICACIÓN
    ws_cem3.write(0, 0, 'IDENTIFICACIÓN', bold)
    ws_cem3.write(1, 0, 'Campo', bold)
    ws_cem3.write(1, 1, 'Valor', bold)
    ws_cem3.write(2, 0, 'Tipo_Cemento')
    ws_cem3.write(2, 1, 'CPO 40RS')
    ws_cem3.write(3, 0, 'Nombre_Comercial')
    ws_cem3.write(3, 1, 'Cemento Resistente a Sulfatos')
    ws_cem3.write(4, 0, 'Producción_Anual_ton')
    ws_cem3.write(4, 1, 180000)
    
    # COMPOSICIÓN Y TRANSPORTE
    ws_cem3.write(6, 0, 'COMPOSICIÓN Y TRANSPORTE', bold)
    composicion3_data = {
        'ID_Material': ['CLK_01', 'CAL_01', 'YES_01'],
        'Material': ['Clinker', 'Caliza', 'Yeso'],
        'Proveedor/Origen': ['Producción propia', 'Cantera propia', 'Stock'],
        'Cantidad_ton': [162000, 14400, 3600],
        'Distancia_km': [0, 5, 0],
        'Modo_Transporte': ['-', 'Banda', '-']
    }
    df_comp3 = pd.DataFrame(composicion3_data)
    for col_num, value in enumerate(df_comp3.columns.values):
        ws_cem3.write(7, col_num, value, bold)
    for row_num, row_data in enumerate(df_comp3.values):
        for col_num, value in enumerate(row_data):
            ws_cem3.write(row_num + 8, col_num, value)
    
    # MOLIENDA
    ws_cem3.write(12, 0, 'MOLIENDA', bold)
    ws_cem3.write(13, 0, 'Concepto', bold)
    ws_cem3.write(13, 1, 'Cantidad_kWh', bold)
    ws_cem3.write(14, 0, 'Electricidad_Red')
    ws_cem3.write(14, 1, 8100000)
    ws_cem3.write(15, 0, 'Electricidad_Renovable')
    ws_cem3.write(15, 1, 0)
    
    # HOJA 7: CEMENTO_TIPO_4 (Puzolánico)
    ws_cem4 = writer.book.add_worksheet('CEMENTO_TIPO_4')
    
    # IDENTIFICACIÓN
    ws_cem4.write(0, 0, 'IDENTIFICACIÓN', bold)
    ws_cem4.write(1, 0, 'Campo', bold)
    ws_cem4.write(1, 1, 'Valor', bold)
    ws_cem4.write(2, 0, 'Tipo_Cemento')
    ws_cem4.write(2, 1, 'Cemento Puzolánico')
    ws_cem4.write(3, 0, 'Nombre_Comercial')
    ws_cem4.write(3, 1, 'EcoCem')
    ws_cem4.write(4, 0, 'Producción_Anual_ton')
    ws_cem4.write(4, 1, 250000)
    
    # COMPOSICIÓN Y TRANSPORTE
    ws_cem4.write(6, 0, 'COMPOSICIÓN Y TRANSPORTE', bold)
    composicion4_data = {
        'ID_Material': ['CLK_01', 'PUZ_01', 'PUZ_02', 'CAL_01', 'YES_01'],
        'Material': ['Clinker', 'Ceniza Volante', 'Puzolana Natural', 'Caliza', 'Yeso'],
        'Proveedor/Origen': ['Producción propia', 'Termoeléctrica Nacional', 'Cantera volcánica', 'Cantera propia', 'Stock'],
        'Cantidad_ton': [150000, 75000, 17500, 5000, 2500],
        'Distancia_km': [0, 300, 400, 5, 0],
        'Modo_Transporte': ['-', 'Tren', 'Camión', 'Banda', '-']
    }
    df_comp4 = pd.DataFrame(composicion4_data)
    for col_num, value in enumerate(df_comp4.columns.values):
        ws_cem4.write(7, col_num, value, bold)
    for row_num, row_data in enumerate(df_comp4.values):
        for col_num, value in enumerate(row_data):
            ws_cem4.write(row_num + 8, col_num, value)
    
    # MOLIENDA
    ws_cem4.write(13, 0, 'MOLIENDA', bold)
    ws_cem4.write(14, 0, 'Concepto', bold)
    ws_cem4.write(14, 1, 'Cantidad_kWh', bold)
    ws_cem4.write(15, 0, 'Electricidad_Red')
    ws_cem4.write(15, 1, 12500000)
    ws_cem4.write(16, 0, 'Electricidad_Renovable')
    ws_cem4.write(16, 1, 0)

print(f"Archivo Excel creado: {archivo_salida}")
print("\nContenido del archivo:")
print("- Hoja EMPRESA: Datos generales de la empresa")
print("- Hoja PLANTAS_CEMENTO: Listado de plantas con referencias GCCA")
print("- Hoja PRODUCCION_CLINKER: Minerales y producción (combustibles/energía desde GCCA)")
print("- Hojas CEMENTO_TIPO_1 a 4: Detalles de cada tipo de cemento")
print("\nNota: Los datos de combustibles y energía eléctrica se tomarán de los archivos GCCA")