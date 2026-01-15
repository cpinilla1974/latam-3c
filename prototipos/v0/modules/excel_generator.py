import pandas as pd
import json
from pathlib import Path
import io

class ExcelGenerator:
    """Generador de archivos Excel desde JSON"""
    
    def __init__(self):
        self.data_path = Path("../data")
    
    def load_json(self, json_file):
        """Carga un archivo JSON"""
        try:
            file_path = self.data_path / json_file
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error cargando {json_file}: {str(e)}")
    
    def generate_clinker_cemento_excel(self, json_data):
        """Genera Excel de Clinker/Cemento desde JSON"""
        
        # Crear un buffer en memoria
        output = io.BytesIO()
        
        # Crear writer de Excel
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Definir formatos
            bold_format = workbook.add_format({'bold': True})
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            section_format = workbook.add_format({
                'bold': True,
                'bg_color': '#70AD47',
                'font_color': 'white',
                'border': 1,
                'font_size': 12
            })
            data_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'vcenter'
            })
            number_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '#,##0'
            })
            note_format = workbook.add_format({
                'italic': True,
                'font_color': '#7C7C7C',
                'bg_color': '#F2F2F2'
            })
            
            # HOJA 1: EMPRESA
            ws_empresa = workbook.add_worksheet('EMPRESA')
            ws_empresa.write(0, 0, 'Campo', header_format)
            ws_empresa.write(0, 1, 'Valor', header_format)
            
            empresa_info = [
                ('Nombre_Empresa', json_data['hoja_empresa']['nombre_empresa']),
                ('País', json_data['hoja_empresa']['pais']),
                ('Año_Reporte', json_data['periodo']),
                ('Responsable', json_data['hoja_empresa']['responsable']),
                ('Email', json_data['hoja_empresa']['email'])
            ]
            
            for row, (campo, valor) in enumerate(empresa_info, 1):
                ws_empresa.write(row, 0, campo, data_format)
                ws_empresa.write(row, 1, valor, data_format)
            
            # Ajustar ancho de columnas
            ws_empresa.set_column('A:A', 18)
            ws_empresa.set_column('B:B', 25)
            
            # HOJA 2: PLANTAS_CEMENTO
            ws_plantas = workbook.add_worksheet('PLANTAS_CEMENTO')
            
            # Headers
            plantas_headers = ['ID_Planta', 'Nombre', 'Ubicación', 'Archivo_GCCA']
            for col, header in enumerate(plantas_headers):
                ws_plantas.write(0, col, header, header_format)
            
            # Data
            for row, planta in enumerate(json_data['hoja_plantas'], 1):
                ws_plantas.write(row, 0, planta['id_planta'], data_format)
                ws_plantas.write(row, 1, planta['nombre'], data_format)
                ws_plantas.write(row, 2, planta['ubicacion'], data_format)
                ws_plantas.write(row, 3, planta['archivo_gcca'], data_format)
            
            # Ajustar ancho de columnas
            ws_plantas.set_column('A:A', 12)
            ws_plantas.set_column('B:B', 20)
            ws_plantas.set_column('C:C', 25)
            ws_plantas.set_column('D:D', 22)
            
            # HOJA 3: PRODUCCION_CLINKER
            ws_clinker = workbook.add_worksheet('PRODUCCION_CLINKER')
            
            # SECCIÓN A: MINERALES
            ws_clinker.merge_range(0, 0, 0, 4, 'SECCIÓN A: MINERALES', section_format)
            
            # Headers
            headers = ['Material', 'Cantidad_ton', 'Origen', 'Distancia_km', 'Modo_Transporte']
            for col, header in enumerate(headers):
                ws_clinker.write(1, col, header, header_format)
            
            # Data
            row = 2
            for mineral in json_data['hoja_produccion_clinker']['minerales']:
                ws_clinker.write(row, 0, mineral['material'], data_format)
                ws_clinker.write(row, 1, mineral['cantidad_ton'], number_format)
                ws_clinker.write(row, 2, mineral['origen'], data_format)
                ws_clinker.write(row, 3, mineral['distancia_km'], number_format)
                ws_clinker.write(row, 4, mineral['modo_transporte'], data_format)
                row += 1
            
            # SECCIÓN B: COMBUSTIBLES (Nota)
            ws_clinker.merge_range(row + 2, 0, row + 2, 4, 'SECCIÓN B: COMBUSTIBLES', section_format)
            ws_clinker.write(row + 3, 0, '*Nota: Estos datos se tomarán de archivos GCCA de cada planta', note_format)
            
            # SECCIÓN C: ENERGÍA ELÉCTRICA (Nota)
            ws_clinker.merge_range(row + 5, 0, row + 5, 4, 'SECCIÓN C: ENERGÍA ELÉCTRICA', section_format)
            ws_clinker.write(row + 6, 0, '*Nota: Estos datos se tomarán de archivos GCCA de cada planta', note_format)
            
            # SECCIÓN D: PRODUCCIÓN
            ws_clinker.merge_range(row + 8, 0, row + 8, 1, 'SECCIÓN D: PRODUCCIÓN', section_format)
            ws_clinker.write(row + 9, 0, 'Concepto', header_format)
            ws_clinker.write(row + 9, 1, 'Cantidad_ton', header_format)
            ws_clinker.write(row + 10, 0, 'Clinker_Producido', data_format)
            ws_clinker.write(row + 10, 1, json_data['hoja_produccion_clinker']['produccion']['clinker_producido_ton'], number_format)
            
            # Ajustar ancho de columnas
            ws_clinker.set_column('A:A', 18)
            ws_clinker.set_column('B:B', 15)
            ws_clinker.set_column('C:C', 20)
            ws_clinker.set_column('D:D', 12)
            ws_clinker.set_column('E:E', 18)
            
            # HOJAS DE CEMENTO
            for i, cemento in enumerate(json_data['hojas_cemento'], 1):
                sheet_name = f'CEMENTO_TIPO_{i}'
                ws_cemento = workbook.add_worksheet(sheet_name)
                
                # IDENTIFICACIÓN
                ws_cemento.merge_range(0, 0, 0, 1, 'IDENTIFICACIÓN', section_format)
                ws_cemento.write(1, 0, 'Campo', header_format)
                ws_cemento.write(1, 1, 'Valor', header_format)
                ws_cemento.write(2, 0, 'Tipo_Cemento', data_format)
                ws_cemento.write(2, 1, cemento['identificacion']['tipo_cemento'], data_format)
                ws_cemento.write(3, 0, 'Nombre_Comercial', data_format)
                ws_cemento.write(3, 1, cemento['identificacion']['nombre_comercial'], data_format)
                ws_cemento.write(4, 0, 'Producción_Anual_ton', data_format)
                ws_cemento.write(4, 1, cemento['identificacion']['produccion_anual_ton'], number_format)
                
                # COMPOSICIÓN Y TRANSPORTE
                ws_cemento.merge_range(6, 0, 6, 5, 'COMPOSICIÓN Y TRANSPORTE', section_format)
                comp_headers = ['ID_Material', 'Material', 'Proveedor/Origen', 'Cantidad_ton', 'Distancia_km', 'Modo_Transporte']
                for col, header in enumerate(comp_headers):
                    ws_cemento.write(7, col, header, header_format)
                
                for row_idx, comp in enumerate(cemento['composicion'], 8):
                    ws_cemento.write(row_idx, 0, comp['id_material'], data_format)
                    ws_cemento.write(row_idx, 1, comp['material'], data_format)
                    ws_cemento.write(row_idx, 2, comp['proveedor'], data_format)
                    ws_cemento.write(row_idx, 3, comp['cantidad_ton'], number_format)
                    ws_cemento.write(row_idx, 4, comp['distancia_km'], number_format)
                    ws_cemento.write(row_idx, 5, comp['modo_transporte'], data_format)
                
                # MOLIENDA
                molienda_row = len(cemento['composicion']) + 10
                ws_cemento.merge_range(molienda_row, 0, molienda_row, 2, 'MOLIENDA', section_format)
                ws_cemento.write(molienda_row + 1, 0, 'Concepto', header_format)
                ws_cemento.write(molienda_row + 1, 1, 'Cantidad_kWh', header_format)
                ws_cemento.write(molienda_row + 1, 2, 'Factor_Emisión_kg_CO2/kWh', header_format)
                ws_cemento.write(molienda_row + 2, 0, 'Electricidad_Red', data_format)
                ws_cemento.write(molienda_row + 2, 1, cemento['molienda']['electricidad_red_kwh'], number_format)
                ws_cemento.write(molienda_row + 2, 2, cemento['molienda'].get('factor_emision_red', 0.65), number_format)
                ws_cemento.write(molienda_row + 3, 0, 'Electricidad_Renovable', data_format)
                ws_cemento.write(molienda_row + 3, 1, cemento['molienda']['electricidad_renovable_kwh'], number_format)
                ws_cemento.write(molienda_row + 3, 2, cemento['molienda'].get('factor_emision_renovable', 0.0), number_format)
                
                # Ajustar ancho de columnas
                ws_cemento.set_column('A:A', 15)
                ws_cemento.set_column('B:B', 15)
                ws_cemento.set_column('C:C', 25)
                ws_cemento.set_column('D:D', 15)
                ws_cemento.set_column('E:E', 12)
                ws_cemento.set_column('F:F', 18)
        
        # Obtener los datos del buffer
        output.seek(0)
        return output.getvalue()
    
    def generate_concreto_excel(self, json_data):
        """Genera Excel de Concreto desde JSON"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Definir formatos (mismos que clinker/cemento)
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            data_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'vcenter'
            })
            number_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '#,##0'
            })
            
            # HOJA 1: EMPRESA
            ws_empresa = workbook.add_worksheet('EMPRESA')
            ws_empresa.write(0, 0, 'Campo', header_format)
            ws_empresa.write(0, 1, 'Valor', header_format)
            
            empresa_info = [
                ('Nombre_Empresa', json_data['hoja_empresa']['nombre_empresa']),
                ('País', json_data['hoja_empresa']['pais']),
                ('Año_Reporte', json_data['periodo']),
                ('Responsable', json_data['hoja_empresa']['responsable']),
                ('Email', json_data['hoja_empresa']['email'])
            ]
            
            for row, (campo, valor) in enumerate(empresa_info, 1):
                ws_empresa.write(row, 0, campo, data_format)
                ws_empresa.write(row, 1, valor, data_format)
            
            ws_empresa.set_column('A:A', 18)
            ws_empresa.set_column('B:B', 25)
            
            # HOJA 2: PRODUCCION
            ws_prod = workbook.add_worksheet('PRODUCCION')
            
            prod_headers = ['Categoría', 'Tipo_Concreto', 'Resistencia', 'Volumen_m3_Anual']
            for col, header in enumerate(prod_headers):
                ws_prod.write(0, col, header, header_format)
            
            for row, prod in enumerate(json_data['hoja_produccion'], 1):
                ws_prod.write(row, 0, prod['categoria'], data_format)
                ws_prod.write(row, 1, prod['tipo_concreto'], data_format)
                ws_prod.write(row, 2, prod['resistencia'], data_format)
                ws_prod.write(row, 3, prod['volumen_m3_anual'], number_format)
            
            ws_prod.set_column('A:A', 18)
            ws_prod.set_column('B:B', 15)
            ws_prod.set_column('C:C', 12)
            ws_prod.set_column('D:D', 18)
            
            # HOJA 3: MEZCLAS
            ws_mezclas = workbook.add_worksheet('MEZCLAS')
            
            mezcla_headers = ['ID_Mezcla', 'Resistencia', 'Cemento_kg/m3', 'Tipo_Cemento', 'Arena_kg/m3', 'Grava_kg/m3', 'Agua_L/m3', 'Aditivo_L/m3']
            for col, header in enumerate(mezcla_headers):
                ws_mezclas.write(0, col, header, header_format)
            
            for row, mezcla in enumerate(json_data['hoja_mezclas'], 1):
                ws_mezclas.write(row, 0, mezcla['id_mezcla'], data_format)
                ws_mezclas.write(row, 1, mezcla['resistencia'], data_format)
                ws_mezclas.write(row, 2, mezcla['cemento_kg_m3'], number_format)
                ws_mezclas.write(row, 3, mezcla['tipo_cemento'], data_format)
                ws_mezclas.write(row, 4, mezcla['arena_kg_m3'], number_format)
                ws_mezclas.write(row, 5, mezcla['grava_kg_m3'], number_format)
                ws_mezclas.write(row, 6, mezcla['agua_l_m3'], number_format)
                ws_mezclas.write(row, 7, mezcla['aditivo_principal_l_m3'], number_format)
            
            ws_mezclas.set_column('A:A', 12)
            ws_mezclas.set_column('B:B', 15)
            ws_mezclas.set_column('C:C', 15)
            ws_mezclas.set_column('D:D', 15)
            ws_mezclas.set_column('E:H', 12)
            
            # HOJA 4: AGREGADOS
            ws_agr = workbook.add_worksheet('AGREGADOS')
            
            agr_headers = ['Material', 'Tipo', 'Proveedor', 'Cantidad_ton_Anual', 'Distancia_km', 'Modo_Transporte']
            for col, header in enumerate(agr_headers):
                ws_agr.write(0, col, header, header_format)
            
            for row, agr in enumerate(json_data['hoja_agregados'], 1):
                ws_agr.write(row, 0, agr['material'], data_format)
                ws_agr.write(row, 1, agr['tipo'], data_format)
                ws_agr.write(row, 2, agr['proveedor'], data_format)
                ws_agr.write(row, 3, agr['cantidad_ton_anual'], number_format)
                ws_agr.write(row, 4, agr['distancia_km'], number_format)
                ws_agr.write(row, 5, agr['modo_transporte'], data_format)
            
            ws_agr.set_column('A:A', 10)
            ws_agr.set_column('B:B', 12)
            ws_agr.set_column('C:C', 20)
            ws_agr.set_column('D:D', 18)
            ws_agr.set_column('E:E', 12)
            ws_agr.set_column('F:F', 18)
            
            # HOJA 5: ADITIVOS
            ws_adt = workbook.add_worksheet('ADITIVOS')
            
            adt_headers = ['Tipo_Aditivo', 'Función', 'Marca', 'Proveedor', 'Cantidad_L_Anual', 'Distancia_km', 'Modo_Transporte']
            for col, header in enumerate(adt_headers):
                ws_adt.write(0, col, header, header_format)
            
            for row, adt in enumerate(json_data['hoja_aditivos'], 1):
                ws_adt.write(row, 0, adt['tipo_aditivo'], data_format)
                ws_adt.write(row, 1, adt['funcion'], data_format)
                ws_adt.write(row, 2, adt['marca'], data_format)
                ws_adt.write(row, 3, adt['proveedor'], data_format)
                ws_adt.write(row, 4, adt['cantidad_l_anual'], number_format)
                ws_adt.write(row, 5, adt['distancia_km'], number_format)
                ws_adt.write(row, 6, adt['modo_transporte'], data_format)
            
            ws_adt.set_column('A:A', 18)
            ws_adt.set_column('B:B', 15)
            ws_adt.set_column('C:C', 15)
            ws_adt.set_column('D:D', 15)
            ws_adt.set_column('E:E', 18)
            ws_adt.set_column('F:F', 12)
            ws_adt.set_column('G:G', 18)
        
        output.seek(0)
        return output.getvalue()