# Detalle de Tareas ETAPA 1 - LATAM-3C

## FASE 1: FORMULARIOS Y VALIDACIÓN (160 HH)

### Semana 1: App formularios básica (15 HH)

**SQLite para sesiones temporales (2h):**
- **Diseñar** esquema tabla sessions (id, token, empresa_data, timestamp): 0.5h
- **Crear** archivo database.py con SQLAlchemy: 0.5h
- **Implementar** funciones create_session(), get_session(), delete_session(): 1h

**Sistema tokens con hashlib/uuid (3h):**
- **Generar** tokens únicos con secrets.token_urlsafe(): 1h
- **Implementar** validación token válido/expirado: 1h
- **Crear** middleware verificación en cada página: 1h

**Setup proyecto Streamlit (2h):**
- **Crear** estructura carpetas form_app/, core/, models/: 0.5h
- **Configurar** requirements.txt y dependencies: 0.5h
- **Escribir** app.py principal con routing básico: 1h

**Formulario básico (3h):**
- **Diseñar** página cuestionario con st.radio(): 1h
- **Implementar** lógica condicional (if cemento then...): 1h
- **Guardar** respuestas en sesión SQLite: 1h

**Deploy inicial Railway (2h):**
- **Configurar** railway.json y variables entorno: 0.5h
- **Subir** código a GitHub: 0.5h
- **Conectar** Railway a repo y deployar: 0.5h
- **Probar** app funcionando en URL: 0.5h

**Testing básico (3h):**
- **Escribir** tests unitarios para tokens: 1h
- **Probar** flujo completo manual: 1h
- **Documentar** bugs encontrados y corregir: 1h

### Semana 2-3: Generador Excel (30 HH)

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

### Semana 4-5: Prueba con 3 empresas (30 HH)

**Coordinar con empresas (5h):**
- **Redactar** emails explicando prueba: 1h
- **Llamar** 5-8 empresas para comprometer 3: 2h
- **Programar** sesiones de prueba: 1h
- **Enviar** instrucciones detalladas: 1h

**Generar links únicos (2h):**
- **Crear** función send_unique_link() por empresa: 1h
- **Probar** generación y envío automático: 1h

**Soporte durante pruebas (8h):**
- **Monitorear** logs y errores en tiempo real: 3h
- **Responder** consultas por email/teléfono: 3h
- **Corregir** bugs críticos on-the-fly: 2h

**Recopilar feedback (6h):**
- **Realizar** 3 reuniones post-prueba (2h c/u): 6h

**Documentar problemas encontrados (4h):**
- **Listar** errores encontrados por empresa: 2h
- **Categorizar** por severidad (crítico/medio/bajo): 1h
- **Priorizar** correcciones para siguiente semana: 1h

**Ajustes urgentes on-the-fly (5h):**
- **Corregir** errores que bloquean pruebas: 3h
- **Desplegar** fixes rápidos: 1h
- **Validar** correcciones con empresas: 1h

### Semana 6-7: Ajustar según feedback (35 HH)

**Cambiar estructura hojas según feedback (10h):**
- **Agregar** columnas faltantes identificadas: 3h
- **Remover** campos irrelevantes: 2h
- **Reordenar** secuencia de hojas: 2h
- **Modificar** nombres de campos: 3h

**Agregar/quitar campos (8h):**
- **Implementar** nuevos campos requeridos: 4h
- **Eliminar** campos confusos: 2h
- **Ajustar** tipos de datos (texto→número): 2h

**Mejorar validaciones (7h):**
- **Agregar** validaciones entre hojas: 3h
- **Corregir** rangos numéricos: 2h
- **Mejorar** mensajes de error: 2h

**Ajustar textos/instrucciones (5h):**
- **Reescribir** instrucciones confusas: 3h
- **Traducir** términos técnicos: 1h
- **Agregar** ejemplos en comentarios: 1h

**Re-testing completo (5h):**
- **Probar** todos los perfiles actualizados: 2h
- **Validar** todas las correcciones: 2h
- **Generar** Excel de prueba final: 1h

### Semana 8: Recopilar datos reales (25 HH)

**Coordinar 5+ empresas (5h):**
- **Contactar** empresas adicionales: 2h
- **Programar** generación datos reales: 2h
- **Enviar** instrucciones finales: 1h

**Soporte generación Excel (10h):**
- **Monitorear** proceso generación: 3h
- **Resolver** dudas técnicas: 4h
- **Asistir** llenado de datos: 3h

**Validar consistencia entre empresas (5h):**
- **Comparar** estructuras generadas: 2h
- **Identificar** discrepancias: 2h
- **Documentar** variaciones aceptables: 1h

**Guardar ejemplos válidos (2h):**
- **Seleccionar** mejores ejemplos por tipo: 1h
- **Organizar** archivos para testing: 1h

**Documentar casos edge (3h):**
- **Listar** casos especiales encontrados: 2h
- **Definir** como manejarlos en Fase 2: 1h

### Semana 9-10: Sistema carga básico (25 HH)

**Parser Excel con pandas (8h):**
- **Crear** función read_excel_structure(): 3h
- **Implementar** detección automática de hojas: 2h
- **Manejar** errores de lectura: 3h

**Validaciones estructura (7h):**
- **Validar** hojas requeridas presentes: 2h
- **Verificar** columnas esperadas: 2h
- **Comprobar** tipos de datos: 3h

**Generación reporte errores (5h):**
- **Crear** clase ValidationReport: 2h
- **Generar** mensajes específicos por error: 2h
- **Exportar** reporte a Excel: 1h

**UI básica Streamlit (3h):**
- **Crear** página upload archivo: 1h
- **Mostrar** resultados validación: 1h
- **Descargar** reporte errores: 1h

**Testing (2h):**
- **Probar** con archivos reales obtenidos: 1h
- **Validar** detección de errores: 1h

## FASE 2: SISTEMA PRINCIPAL Y CÁLCULOS (200 HH)

### Semana 11-12: Base de datos y modelos (40 HH)

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

### Semana 13-14: Cálculos cemento y clinker (35 HH)

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

### Semana 15-16: Cálculos concreto (35 HH)

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

### Semana 17-18: Clasificación GCCA (30 HH)

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

### Semana 19-20: Interfaz operador FICEM (30 HH)

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

### Semana 21: Testing con datos reales (30 HH)

**Cargar datos empresas reales (10h):**
- **Procesar** 5+ archivos reales: 5h
- **Identificar** problemas de datos: 3h
- **Corregir** inconsistencias: 2h

**Validar cálculos manualmente (15h):**
- **Verificar** cálculos cemento con calculadora: 8h
- **Validar** cálculos concreto: 7h

**Ajustes finales (5h):**
- **Corregir** bugs encontrados: 3h
- **Optimizar** queries lentas: 2h

## FASE 3: REPORTES Y REFINAMIENTO (180 HH)

### Semana 22-23: Generación reportes (40 HH)

**Reporte empresa PDF (20h):**
- **Crear** template con reportlab: 8h
- **Agregar** gráficos matplotlib: 6h
- **Incluir** tablas de datos: 4h
- **Formatear** para impresión: 2h

**Reporte comparativo país (15h):**
- **Agregar** datos todas las empresas: 5h
- **Crear** gráficos comparativos: 5h
- **Calcular** estadísticas nacionales: 3h
- **Generar** ranking empresas: 2h

**Exportación Excel (5h):**
- **Crear** hojas múltiples: 2h
- **Agregar** gráficos embebidos: 2h
- **Formatear** tablas: 1h

### Semana 24-25: Dashboard indicadores (40 HH)

**Vista CO2/Resistencia (20h):**
- **Crear** gráfico scatter por país: 8h
- **Agregar** líneas tendencia: 4h
- **Implementar** filtros interactivos: 4h
- **Optimizar** rendimiento: 4h

**Vista Factor clínker (15h):**
- **Crear** histograma distribución: 6h
- **Agregar** benchmarks internacionales: 5h
- **Implementar** alertas valores atípicos: 4h

**Filtros país/empresa (5h):**
- **Crear** sidebar con selectores: 3h
- **Implementar** filtrado dinámico: 2h

### Semana 26-27: Pruebas con empresas finales (40 HH)

**Coordinar 5+ empresas (8h):**
- **Contactar** empresas para pruebas finales: 3h
- **Programar** sesiones demostración: 3h
- **Preparar** datos de prueba: 2h

**Sesiones demostración (20h):**
- **Realizar** 5 demos (4h c/u): 20h

**Feedback sobre reportes (8h):**
- **Recopilar** comentarios sobre reportes: 4h
- **Documentar** mejoras solicitadas: 2h
- **Priorizar** cambios críticos: 2h

**Validación cálculos con empresas (4h):**
- **Verificar** resultados con datos conocidos: 2h
- **Ajustar** fórmulas según feedback: 2h

### Semana 28-29: Ajustes finales (40 HH)

**Correcciones según feedback (25h):**
- **Implementar** cambios críticos reportes: 10h
- **Ajustar** cálculos según validación: 8h
- **Mejorar** textos y mensajes: 4h
- **Corregir** bugs menores: 3h

**Optimización rendimiento (10h):**
- **Optimizar** queries lentas: 5h
- **Agregar** cache para cálculos: 3h
- **Mejorar** tiempo carga páginas: 2h

**Documentación usuario (5h):**
- **Crear** manual operador FICEM: 3h
- **Documentar** casos comunes de error: 2h

### Semana 30-31: Deploy y capacitación (20 HH)

**Deploy final Railway (8h):**
- **Configurar** variables producción: 2h
- **Migrar** base de datos: 3h
- **Probar** funcionamiento completo: 3h

**Capacitación operador FICEM (8h):**
- **Preparar** materiales capacitación: 3h
- **Realizar** sesión capacitación: 3h
- **Crear** videos tutoriales: 2h

**Entrega y cierre (4h):**
- **Entregar** credenciales y documentación: 1h
- **Realizar** handover completo: 2h
- **Documentar** lecciones aprendidas: 1h

## RESUMEN POR CATEGORÍAS

**Desarrollo puro**: 320 HH (60%)
**Coordinación empresas**: 80 HH (15%)
**Testing y validación**: 70 HH (13%)
**Documentación**: 40 HH (7%)
**Deploy y cierre**: 30 HH (5%)

**TOTAL**: 540 HH