# Cronograma Etapa 1 Replanteado - LATAM-3C

## RESUMEN EJECUTIVO

**Horas totales**: 250 HH (reducción de 290 HH vs plan original)
**Duración**: 22 semanas (Oct 2025 - Feb 2026)
**Costo**: $25,000
**Modelo**: Operador centralizado FICEM + Templates Excel

## FASES REPLANTEADAS

### FASE 1: GENERADOR EXCEL Y VALIDACIÓN (60 HH)

#### Semana 1-2: Generador Excel (30 HH)

**Lógica perfiles (5h):**
- **Definir** clases PlantProfile, CementoProfile, ConcretoProfile: 2h
- **Implementar** método get_required_sheets() por perfil: 2h
- **Crear** tests unitarios para cada perfil: 1h

**Openpyxl crear workbook dinámico (5h):**
- **Instalar** y configurar openpyxl: 0.5h
- **Crear** clase ExcelGenerator con método create_workbook(): 2h
- **Implementar** método add_sheet_conditionally(): 1.5h
- **Probar** generación workbook vacío: 1h

**Generar 8-10 hojas condicionales (10h):**
- **Crear** hoja EMPRESA con campos básicos: 1h
- **Crear** hoja PLANTA con validaciones: 1h
- **Crear** hoja CLINKER (solo si integrada): 1.5h
- **Crear** hojas CEMENTO_TIPO_X dinámicas: 2h
- **Crear** hoja CONCRETO (solo si aplica): 1.5h
- **Crear** hojas MEZCLAS, AGREGADOS: 2h
- **Crear** hoja ENERGIA_AGUA: 1h

**Validaciones Excel (5h):**
- **Implementar** data validation para listas desplegables: 2h
- **Crear** validaciones numéricas (rangos): 1h
- **Agregar** formulas de verificación entre celdas: 2h

**Formato y estilos (3h):**
- **Aplicar** colores a headers: 1h
- **Configurar** ancho columnas automático: 1h
- **Agregar** instrucciones en celdas comentarios: 1h

**Testing diferentes perfiles (2h):**
- **Probar** perfil integrada genera 8 hojas: 0.5h
- **Probar** perfil molienda genera 5 hojas: 0.5h
- **Probar** perfil concreto genera 6 hojas: 0.5h
- **Documentar** diferencias por perfil: 0.5h

#### Semana 3-4: Prueba con 2 empresas (15 HH)

**Coordinar con empresas (5h):**
- **Redactar** emails explicando prueba: 1h
- **Llamar** 4-5 empresas para comprometer 2: 2h
- **Programar** sesiones de prueba: 1h
- **Enviar** instrucciones detalladas: 1h

**Soporte durante pruebas (5h):**
- **Monitorear** problemas y dudas por email/teléfono: 2h
- **Responder** consultas técnicas: 2h
- **Documentar** problemas encontrados: 1h

**Recopilar feedback (5h):**
- **Realizar** 2 reuniones post-prueba (2.5h c/u): 5h

#### Semana 5: Ajustes según feedback (15 HH)

**Cambiar estructura hojas según feedback (7h):**
- **Agregar** columnas faltantes identificadas: 3h
- **Remover** campos irrelevantes: 1h
- **Reordenar** secuencia de hojas: 1h
- **Modificar** nombres de campos: 2h

**Mejorar validaciones (5h):**
- **Agregar** validaciones entre hojas: 2h
- **Corregir** rangos numéricos: 2h
- **Mejorar** mensajes de error: 1h

**Ajustar textos/instrucciones (3h):**
- **Reescribir** instrucciones confusas: 2h
- **Agregar** ejemplos en comentarios: 1h

### FASE 2: SISTEMA PRINCIPAL Y CÁLCULOS (130 HH)

#### Semana 6-7: Base de datos y modelos (40 HH)

**Diseñar esquema SQLite completo (8h):**
- **Crear** diagrama entidad-relación: 3h
- **Definir** tablas principales (empresa, planta, material): 3h
- **Establecer** relaciones y constraints: 2h

**Crear modelos SQLAlchemy (12h):**
- **Implementar** modelo Empresa: 2h
- **Implementar** modelo Planta: 3h
- **Implementar** modelo Material: 2h
- **Implementar** modelo Produccion: 3h
- **Crear** relaciones entre modelos: 2h

**Sistema migración/creación BD (5h):**
- **Crear** script create_tables.py: 2h
- **Implementar** función drop_and_recreate(): 1h
- **Agregar** datos de ejemplo: 2h

**Mapeo Excel → Base de datos (10h):**
- **Crear** clase ExcelToDB: 3h
- **Implementar** inserción por hojas: 4h
- **Manejar** duplicados y actualizaciones: 3h

**CRUD operaciones básicas (5h):**
- **Crear** funciones get_empresa(), get_planta(): 2h
- **Implementar** update_data(), delete_data(): 2h
- **Agregar** queries de consulta: 1h

#### Semana 8-9: Cálculos cemento y clinker (35 HH)

**Factor clínker/cemento (8h):**
- **Investigar** fórmulas estándar: 2h
- **Implementar** cálculo por tipo cemento: 3h
- **Validar** rangos típicos (0.5-0.95): 2h
- **Crear** tests unitarios: 1h

**Emisiones proceso (12h):**
- **Implementar** emisiones calcinación: 4h
- **Calcular** emisiones por combustibles: 4h
- **Agregar** emisiones transporte materias primas: 4h

**Emisiones combustibles (10h):**
- **Integrar** datos archivos GCCA: 4h
- **Calcular** CO2 por tipo combustible: 3h
- **Manejar** combustibles alternativos: 3h

**Factor emisión total (5h):**
- **Sumar** todas las emisiones: 2h
- **Calcular** tCO2/ton cemento: 2h
- **Generar** reporte por planta: 1h

#### Semana 10-11: Cálculos concreto (35 HH)

**Huella por m³ (15h):**
- **Calcular** emisiones cemento usado: 5h
- **Agregar** emisiones agregados: 4h
- **Incluir** transporte y aditivos: 4h
- **Sumar** total por dosificación: 2h

**Huella por resistencia (10h):**
- **Agrupar** por resistencia (f'c 210, 250, etc): 3h
- **Calcular** promedio ponderado: 4h
- **Generar** curva resistencia vs CO2: 3h

**Agregación por planta (10h):**
- **Consolidar** datos múltiples mezclas: 4h
- **Calcular** volúmenes totales: 3h
- **Generar** indicadores planta: 3h

#### Semana 12: Clasificación GCCA (30 HH)

**Bandas A-G cemento (15h):**
- **Investigar** rangos oficiales GCCA: 3h
- **Implementar** función classify_cement(): 5h
- **Asignar** banda por valor emisión: 4h
- **Generar** distribución por país: 3h

**Bandas AA-F concreto (15h):**
- **Definir** rangos por resistencia: 4h
- **Implementar** classify_concrete(): 5h
- **Calcular** posición relativa: 3h
- **Crear** visualización bandas: 3h

#### Semana 13: Sistema carga básico (15 HH)

**Parser Excel con pandas (8h):**
- **Crear** función read_excel_structure(): 3h
- **Implementar** detección automática de hojas: 2h
- **Manejar** errores de lectura: 3h

**Validaciones estructura (4h):**
- **Validar** hojas requeridas presentes: 2h
- **Verificar** columnas esperadas: 2h

**Generación reporte errores (3h):**
- **Crear** clase ValidationReport: 2h
- **Generar** mensajes específicos por error: 1h

### FASE 3: INTERFAZ Y REPORTES (60 HH)

#### Semana 14-15: Interfaz operador FICEM (30 HH)

**Dashboard Streamlit principal (15h):**
- **Crear** página principal con métricas: 5h
- **Agregar** filtros por país/empresa/año: 5h
- **Implementar** navegación entre secciones: 5h

**Página carga archivos (8h):**
- **Crear** drag&drop interface: 3h
- **Mostrar** progreso de procesamiento: 2h
- **Manejar** errores de carga: 3h

**Vista resultados (7h):**
- **Mostrar** tabla empresas procesadas: 3h
- **Agregar** indicadores por empresa: 2h
- **Exportar** resultados a Excel: 2h

#### Semana 16: Testing con datos reales (15 HH)

**Cargar datos empresas reales (8h):**
- **Procesar** 3-4 archivos reales: 4h
- **Identificar** problemas de datos: 2h
- **Corregir** inconsistencias: 2h

**Validar cálculos manualmente (5h):**
- **Verificar** cálculos cemento (spot checks): 3h
- **Validar** cálculos concreto (casos clave): 2h

**Ajustes críticos (2h):**
- **Corregir** bugs críticos encontrados: 2h

#### Semana 17-18: Reportes y Deploy (15 HH)

**Reporte empresa Excel (8h):**
- **Crear** template básico con openpyxl: 5h
- **Incluir** tablas esenciales: 3h

**Reporte comparativo simplificado (4h):**
- **Calcular** estadísticas básicas: 2h
- **Generar** ranking simple: 2h

**Deploy y cierre (3h):**
- **Deploy final Railway**: 2h
- **Entrega documentación básica**: 1h

## COMPARACIÓN CON PLAN ORIGINAL

| Aspecto | Plan Original | Plan Ajustado | Reducción |
|---------|--------------|---------------|-----------|
| **Horas totales** | 540 HH | 250 HH | 290 HH (54%) |
| **Duración** | 31 semanas | 22 semanas | 9 semanas (29%) |
| **Entregables** | 17 | 9 | 8 entregables |
| **Costo estimado** | $54,000 | $25,000 | $29,000 (54%) |

## RECORTES APLICADOS

### Optimizaciones principales:
1. **Pruebas reducidas**: 3 empresas → 2 empresas
2. **Testing simplificado**: Validación dirigida vs exhaustiva
3. **Reportes básicos**: Templates simples, funcionalidad esencial
4. **Capacitación mínima**: Documentación integrada en desarrollo
5. **Menor iteración**: Una ronda de ajustes vs múltiples

### Elementos eliminados:
- **Testing perfiles extensivo**
- **Optimizaciones avanzadas**
- **Documentación detallada**
- **Videos tutoriales elaborados**
- **Benchmarking adicional**

## BENEFICIOS DEL AJUSTE PRESUPUESTARIO

- ✅ **Presupuesto objetivo**: Exactamente $25,000
- ✅ **Alcance core preservado**: Motor de cálculos completo
- ✅ **Calidad mantenida**: Sin reducir tarifa por hora
- ✅ **Modelo operativo intacto**: FICEM centralizado funcional
- ✅ **Mayor eficiencia**: Enfoque en entregables esenciales