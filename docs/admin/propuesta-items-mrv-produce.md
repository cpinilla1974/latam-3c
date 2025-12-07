# PROPUESTA TÉCNICA - ÍTEMS MRV PRODUCE

**Cliente:** FICEM / ASOCEM
**Fecha:** Octubre 2025
**Contexto:** Protocolo MRV Perú 2025 - FICEM-ASOCEM-PRODUCE

---

## Ítem 1. MRV - Adecuación de MRV de acuerdo a criterios PRODUCE

### Descripción:

Implementación del Protocolo MRV (Medición, Reporte y Validación) específico para el sector cemento peruano según estándares del Ministerio de la Producción (PRODUCE) y lineamientos FICEM-ASOCEM.

Este ítem comprende la adecuación de la metodología de cálculo internacional (CSI Protocol 3.1, IPCC 2006) a los requerimientos específicos del contexto peruano, integrando:

1. **Factores de Emisión Locales**:
   - Factores del Sistema Eléctrico Interconectado Nacional (SEIN) históricos 2010-2018 y proyecciones hasta 2030
   - Factores de combustibles tradicionales específicos de Perú (carbón mineral, fueloil residual, gas natural, petróleo crudo)
   - Valores caloríficos netos (VCN) ajustados a mezclas de combustibles utilizadas en el país

2. **Estructura de Reporte según Protocolo MRV**:
   - Reporte Indicadores-Año: consolidación anual por planta
   - Reporte de Seguimiento: serie histórica 2010-2030 con proyecciones
   - Reporte de Reducciones de GEI: comparación línea base vs escenarios de mitigación

3. **Escenarios de Mitigación**:
   - Factor Clinker (FC): reducción de ratio clinker/cemento
   - Coprocesamiento (CP): incremento de combustibles alternativos
   - Eficiencia Energética (EE): optimización de consumo térmico y eléctrico

4. **Pseudonimización y Confidencialidad**:
   - Procesamiento de datos individuales de plantas manteniendo confidencialidad
   - Agregación anónima para reportes consolidados a nivel país
   - Cumplimiento con protocolo de privacidad FICEM

### Entregables:

1. **Documento de Metodología de Cálculo MRV Perú** (PDF)
   - Ecuaciones completas del Protocolo MRV
   - Factores de emisión SEIN y combustibles
   - Referencias normativas IPCC 2006, CSI Protocol 3.1
   - Validaciones y controles de calidad

2. **Especificaciones Técnicas de Implementación** (PDF)
   - Estructura de datos entrada/salida
   - Mapeo CSI Protocol 3.1 → MRV Perú
   - Reglas de validación específicas
   - Formatos de reportes según estándar PRODUCE

3. **Tabla de Factores de Emisión Perú** (Excel)
   - Factores SEIN 2010-2030
   - Factores combustibles tradicionales
   - VCN por tipo de combustible
   - Plantilla para combustibles alternativos

4. **Plantillas de Reporte MRV** (Excel/PDF)
   - Template Reporte Indicadores-Año
   - Template Reporte de Seguimiento
   - Template Reducciones Totales GEI

**Tiempo estimado:** 2 semanas (15 HH)
**Costo:** $1,230 USD

---

## Ítem 2. Calculadora MRV Interna

### Descripción Fase 1:

Desarrollo de motor de cálculo automatizado que procesa datos individuales de plantas cementeras según Protocolo MRV Perú, generando indicadores y reportes listos para ser entregados a PRODUCE/ASOCEM.

**Fase 1** se enfoca en el núcleo de cálculo y procesamiento de datos:

1. **Parser de Archivos CSI Protocol 3.1**:
   - Lectura automatizada de archivos Excel formato GCCA/CSI Protocol 3.1
   - Extracción de datos de producción, combustibles, electricidad
   - Validación de consistencia con estructura esperada
   - Mapeo a modelo de datos interno

2. **Motor de Cálculo MRV**:
   - Implementación de ecuaciones del Complemento 5 (Protocolo MRV)
   - Cálculo de Factor Clínker (FE por defecto y por planta)
   - Procesamiento de emisiones de proceso (descarbonatación)
   - Cálculo de emisiones por combustibles (tradicionales y alternativos)
   - Integración de factores SEIN para emisiones eléctricas

3. **Gestión de Datos Históricos y Proyecciones**:
   - Almacenamiento de series temporales 2010-2030
   - Cálculo automático de línea base
   - Sistema de versionado de datos por año/período

4. **Base de Datos Específica MRV**:
   - Extensión del modelo de datos existente
   - Tablas para factores de emisión por país/región
   - Almacenamiento de escenarios de mitigación
   - Trazabilidad de cálculos realizados

### Entregables Fase 1:

1. **Módulo Parser CSI Protocol** (Python)
   - Biblioteca de lectura de archivos .xlsx CSI Protocol 3.1
   - Validador de estructura y completitud
   - Conversor a modelo de datos interno
   - Documentación de mapeo de campos

2. **Motor de Cálculo MRV Core** (Python)
   - Implementación de todas las ecuaciones Protocolo MRV
   - Funciones de cálculo por planta
   - Sistema de agregación a nivel país
   - Tests unitarios con datos reales

3. **Base de Datos MRV** (SQLite)
   - Esquema extendido con tablas MRV
   - Factores de emisión precargados (SEIN, combustibles)
   - Datos de referencia IPCC/CSI
   - Scripts de migración/inicialización

4. **Documentación Técnica** (Markdown/PDF)
   - Manual de integración con sistema existente
   - Especificación de API del motor de cálculo
   - Diccionario de datos
   - Casos de uso y ejemplos

**Tiempo estimado:** 2 semanas (15 HH)
**Costo:** $1,230 USD

---

### Descripción Fase 2:

Desarrollo de interfaz de usuario y sistema de generación de reportes oficiales MRV, completando la solución end-to-end para gestión del Protocolo MRV Perú.

**Fase 2** se enfoca en la capa de presentación y reportería:

1. **Interfaz de Gestión de Plantas MRV**:
   - Dashboard específico para datos MRV en aplicación Streamlit existente
   - Carga masiva de archivos CSI Protocol por planta
   - Vista de validación de datos importados
   - Gestión de factores de emisión personalizados

2. **Módulo de Escenarios de Mitigación**:
   - Interfaz para definir escenarios FC, CP, EE
   - Cálculo automático de reducciones proyectadas
   - Comparación línea base vs escenarios
   - Visualización de impacto por medida

3. **Generador de Reportes MRV**:
   - Generación automática de "Reporte Indicadores-Año" (formato oficial)
   - Generación de "Reporte de Seguimiento" con series temporales
   - Generación de "Reporte Reducciones Totales GEI"
   - Exportación en formatos Excel y PDF

4. **Visualizaciones y Análisis**:
   - Gráficos de evolución temporal de indicadores clave
   - Comparaciones país vs benchmarks internacionales
   - Curvas de trayectoria de emisiones
   - Análisis de efectividad de medidas de mitigación

5. **Sistema de Exportación para PRODUCE**:
   - Generación de paquete completo de entrega a autoridad
   - Compilación de reportes consolidados
   - Validación final de consistencia
   - Carta de transmisión automática

### Entregables Fase 2:

1. **Módulo Interfaz MRV** (Streamlit/Python)
   - Páginas integradas al sistema Calculadora 4C existente
   - Formularios de carga y validación de datos
   - Dashboard de monitoreo de plantas
   - Sistema de alertas y notificaciones

2. **Generador de Reportes Oficiales** (Python + ReportLab/Jinja2)
   - Templates de los 3 tipos de reporte MRV
   - Motor de generación PDF con formato oficial
   - Exportador a Excel estructurado
   - Sistema de firma digital (opcional)

3. **Módulo de Visualizaciones MRV** (Plotly/Matplotlib)
   - 15+ visualizaciones estándar
   - Gráficos interactivos de series temporales
   - Comparativas multi-planta anónimas
   - Exportación de gráficos en alta resolución

4. **Sistema de Gestión de Escenarios** (Python)
   - Calculador de impacto de medidas
   - Simulador de proyecciones 2024-2030
   - Optimizador de mix de medidas
   - Generador de recomendaciones

5. **Documentación de Usuario** (PDF)
   - Manual operativo para operador FICEM
   - Guía de generación de reportes MRV
   - Procedimientos de validación
   - FAQs y troubleshooting

**Tiempo estimado:** 3 semanas (20 HH)
**Costo:** $1,640 USD

---

## Ítem 3: Desarrollo y Aplicación Calculadora Perú 4C

### Descripción:

Implementación completa de la **Calculadora País 4C** como sistema centralizado de gestión de huella de carbono para el sector cemento y concreto en Perú, integrando tanto el estándar internacional GCCA como el Protocolo MRV específico de PRODUCE.

Este ítem representa el **sistema integral completo** que combina:

1. **Sistema Base GCCA** (Calculadora 4C estándar):
   - Generación de plantillas Excel personalizadas por tipo de planta
   - Sistema de validación multinivel de datos de entrada
   - Motor de cálculos según protocolo GCCA/CSI Protocol 3.1
   - Cálculo de huella de carbono para clinker, cemento y concreto
   - Clasificación en bandas GCCA (A-G para cemento, AA-F para concreto)
   - Benchmarking anónimo por país y región
   - Reportes empresariales individuales
   - Dashboard consolidado para FICEM

2. **Extensión MRV Perú** (Ítems 1 y 2 integrados):
   - Motor de cálculo según Protocolo MRV FICEM-ASOCEM
   - Factores de emisión específicos de Perú (SEIN, combustibles locales)
   - Gestión de escenarios de mitigación (FC, CP, EE)
   - Reportes oficiales para PRODUCE/ASOCEM
   - Serie histórica y proyecciones 2010-2030
   - Pseudonimización y agregación para reporte país

3. **Integración Dual**:
   - Una única carga de datos genera ambos reportes (GCCA + MRV)
   - Validación cruzada entre ambas metodologías
   - Interfaz unificada de gestión
   - Base de datos consolidada
   - Trazabilidad completa de cálculos

4. **Modelo Operativo**:
   - **Operador**: FICEM procesa datos centralizadamente
   - **Empresas**: Envían archivos Excel anuales (opcionalmente desde calculadora corporativa)
   - **Salidas**: Reportes individuales GCCA + reportes consolidados MRV para autoridad
   - **Privacidad**: Datos individuales confidenciales, solo agregados se comparten

### Alcance Completo:

**A. INFRAESTRUCTURA Y DATOS (40 HH)**
- Base de datos SQLite extendida con modelo dual GCCA/MRV
- Sistema de gestión de empresas y plantas
- Módulo de carga y validación de archivos
- Parser CSI Protocol 3.1 integrado
- Gestión de factores de emisión por país
- Sistema de versionado y trazabilidad

**B. MOTORES DE CÁLCULO (55 HH)**
- Motor GCCA para clinker, cemento y concreto (A1-A3)
- Motor MRV con ecuaciones específicas Perú
- Clasificación bandas GCCA automática
- Cálculo de escenarios de mitigación
- Agregación y consolidación país
- Validaciones cruzadas entre metodologías

**C. INTERFAZ Y EXPERIENCIA DE USUARIO (45 HH)**
- Dashboard principal FICEM con KPIs consolidados
- Módulo de gestión de empresas y plantas
- Sistema de carga masiva y validación
- Visualizaciones interactivas (GCCA + MRV)
- Gestión de escenarios de mitigación
- Preview de reportes antes de generar

**D. REPORTERÍA Y EXPORTACIÓN (40 HH)**
- Generador de reportes individuales empresas (GCCA)
- Generador de reportes MRV oficiales (3 tipos)
- Exportación Excel estructurada
- Generación PDF con formato oficial
- Sistema de firma digital
- Paquete de entrega a PRODUCE

**E. INTEGRACIÓN CON CALCULADORAS CORPORATIVAS (20 HH)**
- Módulo de exportación desde calculadoras 3C existentes
- Actualización de 2-3 calculadoras corporativas
- Sistema de importación automática
- Validación de datos exportados
- Documentación de integración

**F. VALIDACIÓN Y PRUEBAS (25 HH)**
- Testing con datos reales de 5+ empresas peruanas
- Validación cruzada GCCA vs MRV
- Pruebas de carga con múltiples años
- Verificación de reportes oficiales
- Ajustes y refinamiento final

**G. DOCUMENTACIÓN Y CAPACITACIÓN (15 HH)**
- Manual de usuario para operador FICEM
- Guía metodológica GCCA + MRV
- Documentación técnica del sistema
- Procedimientos operativos estándar
- Video tutoriales (opcional)

### Entregables:

#### 1. Sistema Completo Calculadora Perú 4C

**Aplicación Web (Streamlit/Python)**
- Interfaz completa multi-módulo
- Dashboard ejecutivo con métricas clave
- Módulo de gestión de datos
- Módulo de cálculos GCCA
- Módulo de cálculos MRV
- Módulo de reportería
- Sistema de administración

**Base de Datos Operativa (SQLite)**
- Esquema completo empresas/plantas/productos
- Datos históricos 2010-2030
- Factores de emisión GCCA y MRV
- Benchmarks internacionales
- Log de cálculos y auditoría

**Motores de Cálculo (Python Libraries)**
- Motor GCCA (clinker, cemento, concreto)
- Motor MRV Perú (protocolo FICEM-ASOCEM)
- Sistema de clasificación bandas
- Calculador de escenarios mitigación
- Agregador y consolidador país

#### 2. Sistema de Templates y Validación

**Generador de Plantillas Excel**
- Templates dinámicos por tipo de planta
- Validaciones integradas (listas, rangos)
- Instrucciones contextuales
- Formatos profesionales

**Validador Multinivel**
- Validación de estructura
- Validación de rangos
- Validación de coherencia
- Reporte de errores detallado

#### 3. Sistema de Reportería

**Reportes GCCA (por empresa)**
- Reporte individual con clasificación
- Gráficos comparativos anónimos
- Indicadores clave de desempeño
- Recomendaciones de mejora

**Reportes MRV (consolidado país)**
- Reporte Indicadores-Año
- Reporte de Seguimiento 2010-2030
- Reporte Reducciones Totales GEI
- Anexos técnicos y metodológicos

**Exportaciones**
- Excel estructurado multi-hoja
- PDF con formato oficial
- CSV para análisis externo
- JSON para integraciones

#### 4. Integración Calculadoras Corporativas

**Módulo de Exportación**
- Plugin para calculadoras 3C existentes
- Exportación automática a formato estándar
- Validación pre-envío
- Log de exportaciones

**Actualización de Calculadoras**
- Upgrade de 2-3 calculadoras corporativas
- Nuevas funcionalidades de exportación
- Documentación de cambios
- Soporte post-implementación

#### 5. Documentación Completa

**Para Operador FICEM**
- Manual de usuario completo (PDF)
- Procedimientos paso a paso
- Casos de uso comunes
- Solución de problemas

**Técnica**
- Arquitectura del sistema
- Especificación de cálculos
- Diccionario de datos
- API documentation

**Metodológica**
- Documento Metodología GCCA
- Documento Metodología MRV Perú
- Referencias normativas
- Casos de validación

#### 6. Validación con Empresas Reales

**Dataset de Validación**
- Datos procesados de 5+ empresas peruanas
- Múltiples años (histórico 2020-2024)
- Diferentes tipos de plantas
- Reportes generados verificados

**Informe de Validación**
- Resultados de testing
- Comparación con cálculos manuales
- Verificación cruzada GCCA vs MRV
- Certificación de precisión

### Cronograma:

**Total:** 26 semanas (Octubre 2025 - Marzo 2026)

| Fase | Duración | HH | Entregables Clave |
|------|----------|----|--------------------|
| **Fase 0: Adecuación MRV** | 2 semanas | 15 | Metodología, factores emisión, templates |
| **Fase 1: Excel + Corporativas** | 8 semanas | 80 | Generador Excel, integración calculadoras, piloto con empresas |
| **Fase 2: Sistema + Cálculos** | 7 semanas* | 125 | BD, motores GCCA/MRV, clasificación |
| **Fase 3: Interfaz + Reportes** | 5 semanas | 65 | Dashboard, reportes GCCA/MRV, exportaciones |
| **Fase 4: Validación + Ajustes** | 6 semanas | 40 | Testing empresas, refinamiento, docs |

*Incluye período vacacional 11-31 Diciembre

### Inversión:

**Desarrollo:** $26,240 USD (305 HH + 15 HH MRV)

**Desglose:**
- Adecuación MRV (Ítem 1): $1,230 USD
- Motor MRV Fase 1 (Ítem 2.1): $1,230 USD
- Motor MRV Fase 2 (Ítem 2.2): $1,640 USD
- Sistema Base 4C: $22,140 USD

**Modelo de Pago:**
- Pago inicial (20%): $5,248 USD - Al firmar contrato
- Fase 0+1 (28%): $7,347 USD - Semana 10 (Fin Nov 2025)
- Fase 2 (39%): $10,234 USD - Semana 17 (Fin Ene 2026)
- Fase 3 (20%): $5,248 USD - Semana 22 (Fin Feb 2026)
- Fase 4 (13%): $3,411 USD - Semana 26 (Fin Mar 2026)

### Valor Agregado:

**Para FICEM:**
- ✅ Sistema centralizado único para toda América Latina (escalable)
- ✅ Doble cumplimiento: GCCA internacional + MRV Perú
- ✅ Datos consolidados para análisis sectorial
- ✅ Herramienta de gestión para miembros
- ✅ Posicionamiento técnico ante autoridades

**Para Empresas Peruanas:**
- ✅ Cumplimiento regulatorio PRODUCE automático
- ✅ Clasificación GCCA oficial de sus productos
- ✅ Benchmarking anónimo vs competencia
- ✅ Identificación de oportunidades de mejora
- ✅ Reporte profesional listo para stakeholders

**Para el Sector:**
- ✅ Estandarización metodológica GCCA en Perú
- ✅ Trazabilidad de emisiones y reducciones
- ✅ Datos confiables para política pública
- ✅ Transparencia y comparabilidad
- ✅ Base para compromisos de descarbonización

---

## RESUMEN COMPARATIVO DE ÍTEMS

| Concepto | Ítem 1 (MRV Adecuación) | Ítem 2.1 (MRV Motor) | Ítem 2.2 (MRV Interfaz) | Ítem 3 (Sistema 4C Completo) |
|----------|-------------------------|----------------------|-------------------------|-------------------------------|
| **HH** | 15 | 15 | 20 | 305 + 15 = 320 |
| **Costo** | $1,230 | $1,230 | $1,640 | $26,240 |
| **Duración** | 2 sem | 2 sem | 3 sem | 26 sem |
| **Entregables** | Docs + specs | Motor + BD | UI + reportes | Sistema completo |
| **Alcance** | Metodología | Backend | Frontend | End-to-end |

**Nota:** El Ítem 3 incluye los ítems 1 y 2 como subsistemas integrados.

---

**Fin del Documento**
