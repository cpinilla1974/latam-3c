import pandas as pd
import json
from pathlib import Path
import io

class ExcelGenerator:
    """Generador de archivos Excel desde JSON - Versión actualizada para nuevo esquema"""
    
    def __init__(self):
        self.data_path = Path("../data")
    
    def load_json(self, json_file):
        """Carga un archivo JSON"""
        try:
            if isinstance(json_file, Path):
                file_path = json_file
            else:
                file_path = self.data_path / json_file
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error cargando {json_file}: {str(e)}")
    
    def generate_clinker_cemento_excel(self, json_data):
        """Genera Excel de Planta de Cemento desde JSON (nuevo esquema)"""
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Definir formatos
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
            decimal_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '0.0000'
            })
            note_format = workbook.add_format({
                'italic': True,
                'font_color': '#7C7C7C',
                'bg_color': '#F2F2F2',
                'text_wrap': True
            })
            
            # HOJA 1: EMPRESA
            ws_empresa = workbook.add_worksheet('EMPRESA')
            self._create_empresa_sheet(ws_empresa, json_data, header_format, data_format)
            
            # HOJA 2: PLANTA
            ws_planta = workbook.add_worksheet('PLANTA')
            self._create_planta_sheet(ws_planta, json_data, header_format, data_format, number_format, decimal_format)
            
            # HOJA 3: CLINKER (si existe)
            if json_data.get('hoja_clinker'):
                ws_clinker = workbook.add_worksheet('CLINKER')
                self._create_clinker_sheet(ws_clinker, json_data, header_format, section_format, 
                                         data_format, number_format, note_format, decimal_format)
            
            # HOJAS DE CEMENTO
            for i, cemento in enumerate(json_data.get('hojas_cemento', []), 1):
                sheet_name = f'CEMENTO_TIPO_{i}'
                ws_cemento = workbook.add_worksheet(sheet_name)
                self._create_cemento_sheet(ws_cemento, cemento, header_format, section_format,
                                         data_format, number_format, note_format)
        
        output.seek(0)
        return output.getvalue()
    
    def _create_empresa_sheet(self, worksheet, json_data, header_format, data_format):
        """Crea hoja de empresa"""
        worksheet.write(0, 0, 'Campo', header_format)
        worksheet.write(0, 1, 'Valor', header_format)
        
        empresa_info = [
            ('Nombre_Empresa', json_data['hoja_empresa'].get('nombre_empresa', '')),
            ('País', json_data['hoja_empresa'].get('pais', '')),
            ('Año_Reporte', json_data.get('periodo', '')),
            ('Responsable', json_data['hoja_empresa'].get('responsable', '')),
            ('Email', json_data['hoja_empresa'].get('email', '')),
            ('Teléfono', json_data['hoja_empresa'].get('telefono', ''))
        ]
        
        for row, (campo, valor) in enumerate(empresa_info, 1):
            worksheet.write(row, 0, campo, data_format)
            worksheet.write(row, 1, valor, data_format)
        
        worksheet.set_column('A:A', 18)
        worksheet.set_column('B:B', 30)
    
    def _create_planta_sheet(self, worksheet, json_data, header_format, data_format, number_format, decimal_format):
        """Crea hoja de planta"""
        worksheet.write(0, 0, 'Campo', header_format)
        worksheet.write(0, 1, 'Valor', header_format)
        
        planta_data = json_data.get('hoja_planta', {})
        planta_info = [
            ('ID_Planta', planta_data.get('id_planta', '')),
            ('Nombre', planta_data.get('nombre', '')),
            ('Ubicación', planta_data.get('ubicacion', '')),
            ('Latitud', planta_data.get('latitud', '')),
            ('Longitud', planta_data.get('longitud', '')),
            ('Tipo_Planta', planta_data.get('tipo_planta', '')),
            ('Capacidad_Clinker_ton/año', planta_data.get('capacidad_clinker_ton_año', 0)),
            ('Capacidad_Cemento_ton/año', planta_data.get('capacidad_cemento_ton_año', 0)),
            ('Archivo_GCCA', planta_data.get('archivo_gcca', ''))
        ]
        
        for row, (campo, valor) in enumerate(planta_info, 1):
            worksheet.write(row, 0, campo, data_format)
            if isinstance(valor, (int, float)) and 'Capacidad' in campo:
                worksheet.write(row, 1, valor, number_format)
            elif isinstance(valor, float):
                worksheet.write(row, 1, valor, decimal_format)
            else:
                worksheet.write(row, 1, valor, data_format)
        
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
    
    def _create_clinker_sheet(self, worksheet, json_data, header_format, section_format, data_format, number_format, note_format, decimal_format):
        """Crea hoja de clinker"""
        clinker_data = json_data['hoja_clinker']
        current_row = 0
        
        # IDENTIFICACIÓN
        worksheet.merge_range(current_row, 0, current_row, 1, 'IDENTIFICACIÓN', section_format)
        current_row += 1
        worksheet.write(current_row, 0, 'Campo', header_format)
        worksheet.write(current_row, 1, 'Valor', header_format)
        current_row += 1
        
        identificacion = clinker_data.get('identificacion', {})
        id_info = [
            ('Producción_Clinker_Anual_ton', identificacion.get('produccion_clinker_anual_ton', 0)),
            ('Emisiones_Proceso_tCO2', identificacion.get('emisiones_proceso_tco2', 0))
        ]
        
        for campo, valor in id_info:
            worksheet.write(current_row, 0, campo, data_format)
            worksheet.write(current_row, 1, valor, number_format)
            current_row += 1
        
        current_row += 1
        
        # MINERALES
        worksheet.merge_range(current_row, 0, current_row, 6, 'SECCIÓN A: MINERALES', section_format)
        current_row += 1
        
        headers = ['Material', 'Cantidad_ton', 'Origen', 'Dist_Camión_km', 'Dist_Tren_km', 'Dist_Barco_km', 'Dist_Banda_km']
        for col, header in enumerate(headers):
            worksheet.write(current_row, col, header, header_format)
        current_row += 1
        
        for mineral in clinker_data.get('minerales', []):
            worksheet.write(current_row, 0, mineral.get('material', ''), data_format)
            worksheet.write(current_row, 1, mineral.get('cantidad_ton', 0), number_format)
            worksheet.write(current_row, 2, mineral.get('origen', ''), data_format)
            worksheet.write(current_row, 3, mineral.get('dist_camion_km', 0), number_format)
            worksheet.write(current_row, 4, mineral.get('dist_tren_km', 0), number_format)
            worksheet.write(current_row, 5, mineral.get('dist_barco_km', 0), number_format)
            worksheet.write(current_row, 6, mineral.get('dist_banda_km', 0), number_format)
            current_row += 1
        
        current_row += 1
        
        # COMBUSTIBLES HORNO - REFERENCIA
        worksheet.merge_range(current_row, 0, current_row, 6, 'SECCIÓN B: COMBUSTIBLES HORNO', section_format)
        current_row += 1
        ref_text = clinker_data.get('combustibles_horno_referencia', '[Axioma A001] - Datos tomados de archivos GCCA')
        worksheet.merge_range(current_row, 0, current_row, 6, ref_text, note_format)
        current_row += 2
        
        # ENERGÍA ELÉCTRICA
        if clinker_data.get('energia_electrica'):
            worksheet.merge_range(current_row, 0, current_row, 3, 'SECCIÓN C: ENERGÍA ELÉCTRICA', section_format)
            current_row += 1
            
            energia_headers = ['Tipo_Energía', 'Cantidad_kWh', 'Factor_Emisión_kgCO2/kWh', 'Fuente']
            for col, header in enumerate(energia_headers):
                worksheet.write(current_row, col, header, header_format)
            current_row += 1
            
            for energia in clinker_data['energia_electrica']:
                worksheet.write(current_row, 0, energia.get('tipo_energia', ''), data_format)
                worksheet.write(current_row, 1, energia.get('cantidad_kwh', 0), number_format)
                worksheet.write(current_row, 2, energia.get('factor_emision_kgco2_kwh', 0), decimal_format)
                worksheet.write(current_row, 3, energia.get('fuente', ''), data_format)
                current_row += 1
        
        # Ajustar columnas
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:G', 12)
    
    def _create_cemento_sheet(self, worksheet, cemento_data, header_format, section_format, data_format, number_format, note_format):
        """Crea hoja de cemento"""
        current_row = 0
        
        # IDENTIFICACIÓN
        worksheet.merge_range(current_row, 0, current_row, 1, 'IDENTIFICACIÓN', section_format)
        current_row += 1
        worksheet.write(current_row, 0, 'Campo', header_format)
        worksheet.write(current_row, 1, 'Valor', header_format)
        current_row += 1
        
        identificacion = cemento_data.get('identificacion', {})
        id_fields = [
            ('Tipo_Cemento', identificacion.get('tipo_cemento', '')),
            ('Nombre_Comercial', identificacion.get('nombre_comercial', '')),
            ('Resistencia_28d_MPa', identificacion.get('resistencia_28d_mpa', '')),
            ('Resistencia_28d_psi', identificacion.get('resistencia_28d_psi', '')),
            ('Norma_Técnica', identificacion.get('norma_tecnica', '')),
            ('Producción_Anual_ton', identificacion.get('produccion_anual_ton', 0))
        ]
        
        for campo, valor in id_fields:
            worksheet.write(current_row, 0, campo, data_format)
            if isinstance(valor, (int, float)) and valor != 0:
                worksheet.write(current_row, 1, valor, number_format if 'Producción' in campo else data_format)
            else:
                worksheet.write(current_row, 1, valor, data_format)
            current_row += 1
        
        current_row += 1
        
        # COMPOSICIÓN Y TRANSPORTE
        worksheet.merge_range(current_row, 0, current_row, 7, 'COMPOSICIÓN Y TRANSPORTE', section_format)
        current_row += 1
        
        comp_headers = ['ID_Material', 'Material', 'Proveedor/Origen', 'Cantidad_ton', 
                       'Dist_Camión_km', 'Dist_Tren_km', 'Dist_Barco_km', 'Dist_Banda_km']
        for col, header in enumerate(comp_headers):
            worksheet.write(current_row, col, header, header_format)
        current_row += 1
        
        for comp in cemento_data.get('composicion', []):
            worksheet.write(current_row, 0, comp.get('id_material', ''), data_format)
            worksheet.write(current_row, 1, comp.get('material', ''), data_format)
            worksheet.write(current_row, 2, comp.get('proveedor', ''), data_format)
            worksheet.write(current_row, 3, comp.get('cantidad_ton', 0), number_format)
            worksheet.write(current_row, 4, comp.get('dist_camion_km', 0), number_format)
            worksheet.write(current_row, 5, comp.get('dist_tren_km', 0), number_format)
            worksheet.write(current_row, 6, comp.get('dist_barco_km', 0), number_format)
            worksheet.write(current_row, 7, comp.get('dist_banda_km', 0), number_format)
            current_row += 1
        
        current_row += 1
        
        # MOLIENDA Y COMBUSTIBLES
        worksheet.merge_range(current_row, 0, current_row, 2, 'MOLIENDA Y COMBUSTIBLES', section_format)
        current_row += 1
        
        worksheet.write(current_row, 0, 'Concepto', header_format)
        worksheet.write(current_row, 1, 'Cantidad', header_format)
        worksheet.write(current_row, 2, 'Unidad', header_format)
        current_row += 1
        
        molienda = cemento_data.get('molienda_combustibles', {})
        worksheet.write(current_row, 0, 'Electricidad_Red', data_format)
        worksheet.write(current_row, 1, molienda.get('electricidad_red_kwh', 0), number_format)
        worksheet.write(current_row, 2, 'kWh', data_format)
        current_row += 1
        
        worksheet.write(current_row, 0, 'Electricidad_Renovable', data_format)
        worksheet.write(current_row, 1, molienda.get('electricidad_renovable_kwh', 0), number_format)
        worksheet.write(current_row, 2, 'kWh', data_format)
        current_row += 1
        
        # Referencia a combustibles
        ref_text = molienda.get('combustibles_fuera_horno_referencia', '[Axioma A002] - Datos tomados de archivos GCCA')
        worksheet.merge_range(current_row, 0, current_row, 7, ref_text, note_format)
        
        # Ajustar columnas
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:H', 12)
    
    def generate_concreto_excel(self, json_data):
        """Genera Excel de Concreto desde JSON (nuevo esquema)"""
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Formatos
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
            decimal_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '0.0'
            })
            
            # HOJA 1: EMPRESA
            ws_empresa = workbook.add_worksheet('EMPRESA')
            self._create_empresa_sheet(ws_empresa, json_data, header_format, data_format)
            
            # HOJA 2: PLANTAS_CONCRETO
            ws_plantas = workbook.add_worksheet('PLANTAS_CONCRETO')
            self._create_plantas_concreto_sheet(ws_plantas, json_data, header_format, data_format, number_format, decimal_format)
            
            # HOJA 3: PRODUCCION
            ws_prod = workbook.add_worksheet('PRODUCCION')
            self._create_produccion_sheet(ws_prod, json_data, header_format, data_format, number_format)
            
            # HOJA 4: MEZCLAS
            ws_mezclas = workbook.add_worksheet('MEZCLAS')
            self._create_mezclas_sheet(ws_mezclas, json_data, header_format, data_format, number_format, decimal_format)
            
            # HOJA 5: AGREGADOS_ADICIONES
            ws_agr = workbook.add_worksheet('AGREGADOS_ADICIONES')
            self._create_agregados_sheet(ws_agr, json_data, header_format, data_format, number_format)
            
            # HOJA 6: ADITIVOS
            ws_adt = workbook.add_worksheet('ADITIVOS')
            self._create_aditivos_sheet(ws_adt, json_data, header_format, data_format, number_format)
            
            # HOJA 7: ENERGIA_AGUA
            ws_energia = workbook.add_worksheet('ENERGIA_AGUA')
            self._create_energia_agua_sheet(ws_energia, json_data, header_format, data_format, number_format)
            
            # HOJA 8: CONSUMOS_ESPECIFICOS_PLANTA
            ws_consumos = workbook.add_worksheet('CONSUMOS_ESPECIFICOS')
            self._create_consumos_sheet(ws_consumos, json_data, header_format, data_format, decimal_format)
            
            # HOJA 9: TRANSPORTE_MIXER
            ws_transporte = workbook.add_worksheet('TRANSPORTE_MIXER')
            self._create_transporte_sheet(ws_transporte, json_data, header_format, data_format, number_format, decimal_format)
            
            # HOJA 10: SITIOS_MINERALES (si existe)
            if json_data.get('hoja_sitios_minerales'):
                ws_sitios = workbook.add_worksheet('SITIOS_MINERALES')
                self._create_sitios_sheet(ws_sitios, json_data, header_format, data_format, number_format, decimal_format)
        
        output.seek(0)
        return output.getvalue()
    
    def _create_plantas_concreto_sheet(self, worksheet, json_data, header_format, data_format, number_format, decimal_format):
        """Crea hoja de plantas de concreto"""
        headers = ['ID_Planta', 'Nombre', 'Ubicación', 'Latitud', 'Longitud', 'Tipo', 'Capacidad_m3_año']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, planta in enumerate(json_data.get('hoja_plantas_concreto', []), 1):
            worksheet.write(row, 0, planta.get('id_planta', ''), data_format)
            worksheet.write(row, 1, planta.get('nombre', ''), data_format)
            worksheet.write(row, 2, planta.get('ubicacion', ''), data_format)
            worksheet.write(row, 3, planta.get('latitud', ''), decimal_format)
            worksheet.write(row, 4, planta.get('longitud', ''), decimal_format)
            worksheet.write(row, 5, planta.get('tipo', ''), data_format)
            worksheet.write(row, 6, planta.get('capacidad_m3_año', 0), number_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:E', 12)
        worksheet.set_column('F:F', 8)
        worksheet.set_column('G:G', 15)
    
    def _create_produccion_sheet(self, worksheet, json_data, header_format, data_format, number_format):
        """Crea hoja de producción"""
        headers = ['ID_Planta', 'Categoría', 'Tipo_Concreto', 'Resistencia', 'Volumen_m3_Anual']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, prod in enumerate(json_data.get('hoja_produccion', []), 1):
            worksheet.write(row, 0, prod.get('id_planta', ''), data_format)
            worksheet.write(row, 1, prod.get('categoria', ''), data_format)
            worksheet.write(row, 2, prod.get('tipo_concreto', ''), data_format)
            worksheet.write(row, 3, prod.get('resistencia', ''), data_format)
            worksheet.write(row, 4, prod.get('volumen_m3_anual', 0), number_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 18)
    
    def _create_mezclas_sheet(self, worksheet, json_data, header_format, data_format, number_format, decimal_format):
        """Crea hoja de mezclas"""
        headers = ['ID_Mezcla', 'Resistencia', 'Cemento_kg/m3', 'Tipo_Cemento', 'Arena_kg/m3', 'ID_Arena', 
                   'Grava_kg/m3', 'ID_Grava', 'Agua_L/m3', 'Aditivo_L/m3', 'ID_Aditivo', 'Adiciones_kg/m3', 'ID_Adicion']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, mezcla in enumerate(json_data.get('hoja_mezclas', []), 1):
            worksheet.write(row, 0, mezcla.get('id_mezcla', ''), data_format)
            worksheet.write(row, 1, mezcla.get('resistencia', ''), data_format)
            worksheet.write(row, 2, mezcla.get('cemento_kg_m3', 0), number_format)
            worksheet.write(row, 3, mezcla.get('tipo_cemento', ''), data_format)
            worksheet.write(row, 4, mezcla.get('arena_kg_m3', 0), number_format)
            worksheet.write(row, 5, mezcla.get('id_arena', ''), data_format)
            worksheet.write(row, 6, mezcla.get('grava_kg_m3', 0), number_format)
            worksheet.write(row, 7, mezcla.get('id_grava', ''), data_format)
            worksheet.write(row, 8, mezcla.get('agua_l_m3', 0), number_format)
            worksheet.write(row, 9, mezcla.get('aditivo_l_m3', 0), decimal_format)
            worksheet.write(row, 10, mezcla.get('id_aditivo', ''), data_format)
            worksheet.write(row, 11, mezcla.get('adiciones_kg_m3', 0), number_format)
            worksheet.write(row, 12, mezcla.get('id_adicion', ''), data_format)
        
        for col in range(13):
            worksheet.set_column(col, col, 12)
    
    def _create_agregados_sheet(self, worksheet, json_data, header_format, data_format, number_format):
        """Crea hoja de agregados y adiciones"""
        headers = ['ID_Material', 'Material', 'Tipo', 'Proveedor', 'Cantidad_ton_Anual', 
                   'Dist_Camión_km', 'Dist_Tren_km', 'Dist_Barco_km']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, agr in enumerate(json_data.get('hoja_agregados_adiciones', []), 1):
            worksheet.write(row, 0, agr.get('id_material', ''), data_format)
            worksheet.write(row, 1, agr.get('material', ''), data_format)
            worksheet.write(row, 2, agr.get('tipo', ''), data_format)
            worksheet.write(row, 3, agr.get('proveedor', ''), data_format)
            worksheet.write(row, 4, agr.get('cantidad_ton_anual', 0), number_format)
            worksheet.write(row, 5, agr.get('dist_camion_km', 0), number_format)
            worksheet.write(row, 6, agr.get('dist_tren_km', 0), number_format)
            worksheet.write(row, 7, agr.get('dist_barco_km', 0), number_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 18)
        worksheet.set_column('F:H', 12)
    
    def _create_aditivos_sheet(self, worksheet, json_data, header_format, data_format, number_format):
        """Crea hoja de aditivos"""
        headers = ['ID_Aditivo', 'Tipo_Aditivo', 'Función', 'Marca', 'Proveedor', 
                   'Cantidad_L_Anual', 'Dist_Camión_km', 'Dist_Tren_km', 'Dist_Barco_km']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, adt in enumerate(json_data.get('hoja_aditivos', []), 1):
            worksheet.write(row, 0, adt.get('id_aditivo', ''), data_format)
            worksheet.write(row, 1, adt.get('tipo_aditivo', ''), data_format)
            worksheet.write(row, 2, adt.get('funcion', ''), data_format)
            worksheet.write(row, 3, adt.get('marca', ''), data_format)
            worksheet.write(row, 4, adt.get('proveedor', ''), data_format)
            worksheet.write(row, 5, adt.get('cantidad_l_anual', 0), number_format)
            worksheet.write(row, 6, adt.get('dist_camion_km', 0), number_format)
            worksheet.write(row, 7, adt.get('dist_tren_km', 0), number_format)
            worksheet.write(row, 8, adt.get('dist_barco_km', 0), number_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 18)
        worksheet.set_column('G:I', 12)
    
    def _create_energia_agua_sheet(self, worksheet, json_data, header_format, data_format, number_format):
        """Crea hoja de energía y agua"""
        worksheet.write(0, 0, 'Concepto', header_format)
        worksheet.write(0, 1, 'Cantidad_Anual', header_format)
        worksheet.write(0, 2, 'Unidad', header_format)
        worksheet.write(0, 3, 'Origen/Uso', header_format)
        
        row = 1
        energia_agua = json_data.get('hoja_energia_agua', {})
        
        # Electricidad
        worksheet.write(row, 0, '**ELECTRICIDAD**', header_format)
        row += 1
        for elec in energia_agua.get('electricidad', []):
            worksheet.write(row, 0, elec.get('concepto', ''), data_format)
            worksheet.write(row, 1, elec.get('cantidad_anual', 0), number_format)
            worksheet.write(row, 2, elec.get('unidad', ''), data_format)
            worksheet.write(row, 3, elec.get('origen', ''), data_format)
            row += 1
        
        # Combustibles
        row += 1
        worksheet.write(row, 0, '**COMBUSTIBLES**', header_format)
        row += 1
        for comb in energia_agua.get('combustibles', []):
            worksheet.write(row, 0, comb.get('concepto', ''), data_format)
            worksheet.write(row, 1, comb.get('cantidad_anual', 0), number_format)
            worksheet.write(row, 2, comb.get('unidad', ''), data_format)
            worksheet.write(row, 3, comb.get('uso', ''), data_format)
            row += 1
        
        # Agua
        row += 1
        worksheet.write(row, 0, '**AGUA**', header_format)
        row += 1
        for agua in energia_agua.get('agua', []):
            worksheet.write(row, 0, agua.get('concepto', ''), data_format)
            worksheet.write(row, 1, agua.get('cantidad_anual', 0), number_format)
            worksheet.write(row, 2, agua.get('unidad', ''), data_format)
            worksheet.write(row, 3, agua.get('origen', ''), data_format)
            row += 1
        
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 8)
        worksheet.set_column('D:D', 25)
    
    def _create_consumos_sheet(self, worksheet, json_data, header_format, data_format, decimal_format):
        """Crea hoja de consumos específicos"""
        headers = ['ID_Planta', 'Electricidad_kWh/m3', 'Diesel_Cargador_L/m3', 'Diesel_Otros_L/m3', 'Notas']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, consumo in enumerate(json_data.get('hoja_consumos_especificos_planta', []), 1):
            worksheet.write(row, 0, consumo.get('id_planta', ''), data_format)
            worksheet.write(row, 1, consumo.get('electricidad_kwh_m3', 0), decimal_format)
            worksheet.write(row, 2, consumo.get('diesel_cargador_l_m3', 0), decimal_format)
            worksheet.write(row, 3, consumo.get('diesel_otros_l_m3', 0), decimal_format)
            worksheet.write(row, 4, consumo.get('notas', ''), data_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:D', 18)
        worksheet.set_column('E:E', 25)
    
    def _create_transporte_sheet(self, worksheet, json_data, header_format, data_format, number_format, decimal_format):
        """Crea hoja de transporte mixer"""
        headers = ['ID_Planta', 'Radio_Promedio_km', 'Diesel_L/m3', 'Tipo_Camión', 'Capacidad_m3', 'Factor_Retorno']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, transporte in enumerate(json_data.get('hoja_transporte_mixer', []), 1):
            worksheet.write(row, 0, transporte.get('id_planta', ''), data_format)
            worksheet.write(row, 1, transporte.get('radio_promedio_km', 0), number_format)
            worksheet.write(row, 2, transporte.get('diesel_l_m3', 0), decimal_format)
            worksheet.write(row, 3, transporte.get('tipo_camion', ''), data_format)
            worksheet.write(row, 4, transporte.get('capacidad_m3', 0), number_format)
            worksheet.write(row, 5, transporte.get('factor_retorno', 0), decimal_format)
        
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 15)
    
    def _create_sitios_sheet(self, worksheet, json_data, header_format, data_format, number_format, decimal_format):
        """Crea hoja de sitios minerales"""
        headers = ['ID_Sitio', 'Tipo', 'Material_Principal', 'Ubicación', 'Latitud', 'Longitud', 
                   'Capacidad_Anual_ton', 'Distancia_Planta_km']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        for row, sitio in enumerate(json_data.get('hoja_sitios_minerales', []), 1):
            worksheet.write(row, 0, sitio.get('id_sitio', ''), data_format)
            worksheet.write(row, 1, sitio.get('tipo', ''), data_format)
            worksheet.write(row, 2, sitio.get('material_principal', ''), data_format)
            worksheet.write(row, 3, sitio.get('ubicacion', ''), data_format)
            worksheet.write(row, 4, sitio.get('latitud', ''), decimal_format)
            worksheet.write(row, 5, sitio.get('longitud', ''), decimal_format)
            worksheet.write(row, 6, sitio.get('capacidad_anual_ton', 0), number_format)
            worksheet.write(row, 7, sitio.get('distancia_planta_km', 0), number_format)
        
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 8)
        worksheet.set_column('C:C', 18)
        worksheet.set_column('D:D', 25)
        worksheet.set_column('E:F', 12)
        worksheet.set_column('G:G', 18)
        worksheet.set_column('H:H', 18)