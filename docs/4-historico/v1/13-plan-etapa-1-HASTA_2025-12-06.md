# Plan Detallado ETAPA 1 - LATAM-3C (REVISADO)
**Período**: Octubre 2024 - Marzo 2025
**Desarrollador**: 1 persona
**Dedicación**: 30 horas/semana
**CRÍTICO**: Validar con empresas Oct-Nov antes de vacaciones

## FASE 1: FORMULARIOS Y VALIDACIÓN CON EMPRESAS (Oct-Nov)
**Total**: 160 HH / $16,000

### Entregable 1: Aplicación Formularios Base (Semana 1 - 15 HH)
Se desarrolla una aplicación web simple en Streamlit que funciona como generador inicial de formularios dinámicos. Incluye sistema de tokens únicos para acceso sin autenticación, almacenamiento temporal en SQLite para guardar sesiones de usuario, y un cuestionario básico que determina el tipo de planta (integrada, molienda, concreto). Al finalizar se obtiene una aplicación funcional desplegada en Railway que puede recibir empresas vía links únicos y capturar sus respuestas sobre configuración operativa.

### Entregable 2: Motor Generación Excel Personalizado (Semana 2-3 - 30 HH)
Se construye el núcleo del sistema que convierte las respuestas del cuestionario en archivos Excel personalizados usando openpyxl. La lógica implementa perfiles operativos que determinan qué hojas incluir (ej: plantas integradas tienen hoja CLINKER, plantas molienda no), genera dinámicamente entre 5-10 hojas según el perfil, incorpora validaciones de datos y listas desplegables contextuales. El resultado es un generador que produce Excel con solo campos relevantes para cada tipo de empresa, eliminando confusión por campos irrelevantes.

### Entregable 3: Validación con Empresas Piloto (Semana 4-5 - 30 HH)
Se ejecuta la primera validación real del sistema con 3 empresas comprometidas previamente. Se coordina el proceso completo: envío de links únicos, soporte durante generación de Excel, recopilación estructurada de feedback mediante reuniones, y documentación detallada de problemas encontrados. Al completar se obtiene validación del mercado sobre la utilidad del sistema, identificación de gaps en formato Excel, y comprensión real de necesidades empresariales vs. diseño inicial.

### Entregable 4: Formato Excel Definitivo (Semana 6-7 - 35 HH)
Se implementan todas las correcciones identificadas en la validación piloto para establecer el formato Excel final que se usará en producción. Incluye reestructuración de hojas según feedback, adición/eliminación de campos, mejora de validaciones y clarificación de instrucciones. El entregable es el formato Excel estandarizado y validado con empresas reales, documentación completa del formato, y sistema generador actualizado que produce archivos consistentes y usables.

### Entregable 5: Banco de Datos Reales (Semana 8 - 25 HH)
Se recopilan datos reales de 5+ empresas que generan archivos Excel completos con información operativa real (no datos de prueba). Se valida consistencia entre empresas, se identifican variaciones aceptables vs. errores, y se establecen ejemplos válidos para cada tipo de perfil. Al finalizar se obtiene un banco de datos reales para desarrollo y testing, comprensión profunda de variabilidad real en datos, y casos de prueba representativos del mercado objetivo.

### Entregable 6: Sistema Validación Excel (Semana 9-10 - 25 HH)
Se desarrolla el sistema básico que puede cargar archivos Excel generados y validar su estructura contra el formato establecido. Incluye parser con pandas para leer múltiples hojas, validaciones de estructura (hojas presentes, columnas correctas), detección de errores de formato, y generación de reportes específicos sobre problemas encontrados. El resultado es un validador funcional que puede procesar archivos reales y detectar errores, estableciendo la base técnica para el sistema principal de la Fase 2.

## FASE 2: SISTEMA PRINCIPAL Y CÁLCULOS (Dic-Ene)
**Total**: 200 HH / $20,000
*Nota: Empresas no disponibles, desarrollo con datos recopilados*

### Entregable 7: Base de Datos Operativa (Semana 11-12 - 40 HH)
Se construye la infraestructura de datos que soportará todo el sistema principal, migrando desde el validador básico hacia una base de datos completa. Se diseña el esquema SQLite definitivo con tablas para empresas, plantas, materiales, producción y cálculos, se implementan modelos SQLAlchemy con relaciones apropiadas, y se desarrolla el sistema de carga que toma archivos Excel validados y los convierte en registros estructurados. Al finalizar se obtiene una base de datos funcional que puede almacenar datos de múltiples empresas/años, sistema robusto de carga desde Excel, y operaciones CRUD para gestionar la información.

### Entregable 8: Motor Cálculos Cemento (Semana 13-14 - 35 HH)
Se desarrolla el núcleo de cálculos para productos de cemento, implementando las fórmulas oficiales para determinar factores de emisión. Incluye cálculo del factor clínker/cemento por tipo de producto, procesamiento de emisiones de proceso (calcinación), integración con datos de combustibles de archivos GCCA, y cálculo del factor de emisión total en tCO2/ton cemento. El resultado es un sistema que puede procesar datos reales de cualquier empresa cementera y generar factores de emisión confiables y auditables según estándares internacionales.

### Entregable 9: Motor Cálculos Concreto (Semana 15-16 - 35 HH)
Se implementa el sistema de cálculos para productos de concreto, procesando dosificaciones complejas y múltiples plantas por empresa. Calcula huella de carbono por m³ considerando cemento usado, agregados, aditivos y transporte, genera indicadores por resistencia (f'c 210, 250, 280, etc.), y consolida datos de múltiples plantas para obtener indicadores empresariales. Al completar se obtiene un calculador completo que puede procesar cualquier empresa concretera, indicadores comparables entre empresas, y base para clasificaciones GCCA.

### Entregable 10: Sistema Clasificación GCCA (Semana 17-18 - 30 HH)
Se implementa la clasificación oficial GCCA que ubica productos en bandas de desempeño ambiental. Para cemento se establecen bandas A-G según rangos de emisión por tonelada, para concreto se implementan bandas AA-F por resistencia y emisión por m³, se integran benchmarks internacionales para comparación. El entregable es un sistema que puede clasificar automáticamente cualquier producto según estándares GCCA, generar comparaciones con benchmarks internacionales, y producir rankings de desempeño para uso en reportes.

### Entregable 11: Interfaz Operador FICEM (Semana 19-20 - 30 HH)
Se desarrolla la interfaz principal para que el operador FICEM gestione todo el sistema de manera eficiente. Incluye dashboard principal con métricas clave por país/empresa, sistema de carga masiva de archivos Excel, visualización de resultados de cálculos con filtros dinámicos, y herramientas de exportación de datos procesados. Al finalizar se obtiene una aplicación completa que permite al operador FICEM procesar datos de todas las empresas, monitorear estado del proceso anual, y generar vistas consolidadas para análisis.

### Entregable 12: Sistema Validado con Datos Reales (Semana 21 - 30 HH)
Se valida todo el sistema end-to-end utilizando los datos reales recopilados en Fase 1, asegurando que los cálculos produzcan resultados coherentes y auditables. Se procesan archivos de 5+ empresas reales, se validan resultados contra cálculos manuales, se identifican y corrigen discrepancias, y se optimiza rendimiento para volúmenes de producción. El resultado es un sistema completamente funcional y validado, confianza en la precisión de cálculos, y base sólida para la Fase 3 de reportes.

## FASE 3: REPORTES Y REFINAMIENTO (Feb-Mar)
**Total**: 180 HH / $18,000
*Nota: Empresas disponibles nuevamente*

### Entregable 13: Sistema Generación Reportes (Semana 22-23 - 40 HH)
Se construye el sistema completo de generación de reportes que convierte los cálculos procesados en documentos utilizables por las empresas y FICEM. Incluye generación de reportes individuales por empresa en formato PDF con clasificación GCCA, indicadores clave y comparaciones, reportes comparativos por país que permiten análisis sectorial, y sistema de exportación de datos a Excel con diferentes niveles de detalle. Al finalizar se obtiene una plataforma de reportes funcional que puede generar documentos profesionales automáticamente, capacidad de análisis comparativo entre empresas y países, y exportaciones personalizables para diferentes audiencias.

### Entregable 14: Dashboard Indicadores Interactivos (Semana 24-25 - 40 HH)
Se implementa el dashboard principal que permite explorar y analizar los datos procesados de forma interactiva y visual. Desarrolla visualizaciones específicas como gráficos CO2/Resistencia para productos de concreto, análisis de factor clínker para cementos, comparaciones de desempeño entre empresas por país, y sistema de filtros dinámicos que permiten segmentar por país, empresa, tipo de producto y período. El resultado es una interfaz interactiva que facilita el análisis de tendencias y patrones, herramientas de exploración de datos para identificar oportunidades de mejora, y visualizaciones que soportan toma de decisiones estratégicas.

### Entregable 15: Validación Final con Empresas (Semana 26-27 - 40 HH)
Se ejecuta la validación completa del sistema con empresas reales, probando todo el flujo end-to-end desde la carga de datos hasta la generación de reportes. Coordina pruebas con 5+ empresas que evalúan el sistema completo, recopila feedback estructurado sobre usabilidad de reportes y precisión de cálculos, valida que los resultados sean consistentes con expectativas empresariales, y documenta casos de uso reales para optimización. Al completar se obtiene validación del mercado sobre la utilidad completa del sistema, confianza empresarial en la precisión de resultados, y identificación de ajustes finales necesarios para adopción masiva.

### Entregable 16: Sistema Optimizado y Documentado (Semana 28-29 - 40 HH)
Se implementan todas las correcciones identificadas en la validación final y se optimiza el sistema para operación en producción. Incluye correcciones de funcionalidad según feedback empresarial, optimización de rendimiento para manejo de volúmenes reales de datos, creación de documentación completa para usuarios finales (operador FICEM y empresas), y establecimiento de procedimientos operativos. El resultado es un sistema completamente funcional y optimizado, documentación comprensiva que facilita adopción y mantenimiento, y procesos establecidos para operación continua.

### Entregable 17: Deploy Productivo y Capacitación (Semana 30-31 - 20 HH)
Se realiza el despliegue final del sistema en el ambiente productivo de Railway y se capacita al equipo FICEM para operación independiente. Ejecuta el deploy final con configuraciones de producción, realiza capacitación práctica del operador FICEM en todos los módulos del sistema, entrega documentación técnica y de usuario, y establece protocolo de soporte inicial. Al finalizar se obtiene un sistema completamente operativo en producción, equipo FICEM capacitado para operación autónoma, y transferencia completa del conocimiento técnico y operativo.

## RESUMEN ETAPA 1

### Entregables
1. App principal FICEM operativa
2. App formularios empresas
3. Motor de cálculos 3C completo
4. Reportes y dashboard
5. Documentación técnica y usuario

### Inversión
- **Desarrollo**: 540 HH = $54,000
- **Hosting Railway**: 6 meses × $20 = $120
- **TOTAL**: $54,120

### Riesgos identificados
- Formatos Excel variables por empresa (mitigado con validación Oct-Nov)
- Empresas no disponibles diciembre (mitigado priorizando Oct-Nov)
- 30h/semana durante 6 meses sin buffer
- Trabajar solo sin backup técnico

### Supuestos
- 3-5 empresas comprometidas para Oct-Nov
- Conocimiento GCCA suficiente (desarrollador conoce formato)
- Railway adecuado para hosting inicial
- 30 horas semanales sostenibles por 6 meses