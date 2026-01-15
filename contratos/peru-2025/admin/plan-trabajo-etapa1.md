# PLAN DE TRABAJO - ETAPA 1
## Calculadora País 4C de Huella de Carbono

**Período:** 01 Octubre 2025 - 31 Marzo 2026 (26 semanas)
**Objetivo:** Desarrollo e implementación del sistema centralizado de cálculo de huella de carbono

---

## FASE 1: Generador Excel, Validación e Integración Calculadoras
**Duración:** Semanas 1-8 (01 Oct - 26 Nov 2025)
**Costo:** $6,000

### Hitos Intermedios

**Hito 1.1 - Semana 3 (22 Oct 2025): Template Excel Borrador**
- **Entregable:** Primera versión de plantilla Excel para planta integrada
- **Verificación:** Excel con 5-10 hojas estructuradas, validaciones básicas, instrucciones
- **Demo:** Presentación del template a FICEM

**Hito 1.2 - Semana 5 (05 Nov 2025): Validación con Primera Empresa**
- **Entregable:** Template validado con 1 empresa piloto + reporte de ajustes necesarios
- **Verificación:** Empresa completa el Excel, se identifican problemas, se documentan mejoras
- **Demo:** Revisión de feedback y plan de ajustes

**Hito 1.3 - Semana 7 (19 Nov 2025): Upgrade Calculadora 3C Operativo**
- **Entregable:** Módulo de exportación instalado en calculadora corporativa
- **Verificación:** Calculadora 3C exporta datos en formato compatible con sistema 4C
- **Demo:** Demostración de exportación automática

### Entregable Final de Fase 1 (26 Nov 2025)
- ✅ Generador dinámico de plantillas Excel (código fuente)
- ✅ Templates validados con 3 empresas piloto
- ✅ Upgrade completo de 2 calculadoras corporativas 3C
- ✅ Módulo de exportación automática funcionando
- ✅ Formato Excel definitivo estandarizado
- ✅ Documento de definiciones técnicas acordadas

**Criterio de completitud:** Las 3 empresas piloto pueden generar datos válidos (manual o automático)

---

## FASE 2: Sistema Principal y Cálculos
**Duración:** Semanas 9-15 (27 Nov 2025 - 14 Ene 2026)
**Costo:** $9,500

### Hitos Intermedios

**Hito 2.1 - Semana 11 (10 Dic 2025): Base de Datos Operativa**
- **Entregable:** Base de datos SQLite con modelos completos implementados
- **Verificación:** Script de migración ejecuta correctamente, tablas creadas, relaciones definidas
- **Demo:** Diagrama de base de datos + inserción de datos de prueba

**Hito 2.2 - Semana 13 (24 Dic 2025): Motor de Cálculos Cemento (A1-A2)**
- **Entregable:** Algoritmos de cálculo para clinker y cemento implementados
- **Verificación:** Tests con datos reales de 2 empresas, resultados comparados con cálculos manuales
- **Demo:** Carga de Excel → cálculo automático → resultados verificados

**Hito 2.3 - Semana 14 (31 Dic 2025): Motor de Cálculos Concreto (A3)**
- **Entregable:** Algoritmo de cálculo para concreto implementado
- **Verificación:** Cálculo de huella por m³, integración con huella de cemento
- **Demo:** Ejemplos de diferentes tipos de mezcla calculados correctamente

### Entregable Final de Fase 2 (14 Ene 2026)
- ✅ Base de datos operativa (SQLite) con modelos completos
- ✅ Motor de cálculos A1-A3 (Clinker, Cemento, Concreto) completo
- ✅ Sistema de clasificación GCCA (bandas A-G, AA-F) implementado
- ✅ Interfaz web básica para operador FICEM
- ✅ Sistema validado con datos reales de 5+ empresas
- ✅ Documentación técnica de algoritmos de cálculo

**Criterio de completitud:** Sistema calcula correctamente huella de carbono para los 3 productos siguiendo metodología GCCA

---

## FASE 3: Interfaz y Reportes
**Duración:** Semanas 16-20 (15 Ene - 18 Feb 2026)
**Costo:** $4,900

### Hitos Intermedios

**Hito 3.1 - Semana 17 (28 Ene 2026): Dashboard Principal**
- **Entregable:** Interfaz web con dashboard de métricas clave
- **Verificación:** Visualización de datos agregados por país/empresa/año
- **Demo:** Navegación por dashboard mostrando datos de empresas piloto

**Hito 3.2 - Semana 19 (11 Feb 2026): Sistema de Reportes**
- **Entregable:** Generador de reportes individuales por empresa (Excel)
- **Verificación:** Reporte incluye clasificación GCCA, gráficos comparativos, benchmarking
- **Demo:** Generación de 3 reportes ejemplo

### Entregable Final de Fase 3 (18 Feb 2026)
- ✅ Dashboard principal con métricas clave completo
- ✅ Sistema de carga masiva de archivos Excel
- ✅ Reportes individuales por empresa (Excel) con benchmarking anónimo
- ✅ Sistema de exportación de resultados
- ✅ Filtros dinámicos por país/empresa/año/producto
- ✅ Manual de usuario para operador FICEM

**Criterio de completitud:** FICEM puede cargar datos, calcular y generar reportes de forma autónoma

---

## FASE 4: Retroalimentación y Mejoras
**Duración:** Semanas 21-26 (19 Feb - 31 Mar 2026)
**Costo:** $1,900

### Hitos Intermedios

**Hito 4.1 - Semana 23 (11 Mar 2026): Ciclo de Mejoras 1**
- **Entregable:** Ajustes basados en feedback de uso real por FICEM
- **Verificación:** Lista de bugs corregidos, mejoras implementadas
- **Demo:** Presentación de cambios realizados

**Hito 4.2 - Semana 25 (25 Mar 2026): Testing Final**
- **Entregable:** Sistema probado end-to-end con datos de todas las empresas
- **Verificación:** Todos los casos de uso funcionan correctamente
- **Demo:** Sesión de testing completo con FICEM

### Entregable Final de Fase 4 (31 Mar 2026)
- ✅ Sistema optimizado y estabilizado
- ✅ Correcciones de bugs identificados
- ✅ Mejoras de usabilidad implementadas
- ✅ Documentación técnica completa actualizada
- ✅ Manual de resolución de problemas
- ✅ Código fuente final con licencia de uso

**Criterio de completitud:** Sistema en producción, estable y documentado

---

## BENCHMARKING (Fase Continua)
**Duración:** Semanas 10-26 (09 Ene - 31 Mar 2026)
**Costo:** $2,700

### Hitos Intermedios

**Hito B.1 - Semana 13 (24 Dic 2025): Repositorio de Referencias**
- **Entregable:** Base de datos de benchmarking con estructura definida
- **Verificación:** Sistema almacena datos agregados anónimos por país/región
- **Demo:** Consultas de agregación funcionando

**Hito B.2 - Semana 18 (04 Feb 2026): Visualizaciones Comparativas**
- **Entregable:** Gráficos de curvas CO₂ vs resistencia, percentiles P25/P50/P75
- **Verificación:** Visualizaciones integradas en reportes empresariales
- **Demo:** Dashboard muestra benchmarking anónimo

**Hito B.3 - Semana 22 (18 Feb 2026): Integración Completa**
- **Entregable:** Benchmarking totalmente integrado en sistema de reportes
- **Verificación:** Cada reporte empresarial incluye contexto comparativo
- **Demo:** Reportes finales con benchmarking completo

### Entregable Final Benchmarking (31 Mar 2026)
- ✅ Repositorio de referencias operativo
- ✅ Sistema de agregación anónima implementado
- ✅ Visualizaciones comparativas (curvas, percentiles, indicadores)
- ✅ Integración completa en reportes empresariales
- ✅ Documentación de metodología de benchmarking

**Criterio de completitud:** Empresas reciben contexto comparativo anónimo en sus reportes

---

## CALENDARIO DE PAGOS

| Pago | Fecha | Monto | Entregable |
|------|-------|-------|------------|
| **Pago 1** | 01 Oct 2025 | $5,000 | Contrato firmado + Plan de trabajo |
| **Pago 2** | 26 Nov 2025 | $6,000 | Fase 1 completa |
| **Pago 3** | 14 Ene 2026 | $9,500 | Fase 2 completa |
| **Pago 4** | 18 Feb 2026 | $4,900 | Fase 3 completa |
| **Pago 5** | 31 Mar 2026 | $4,600 | Fase 4 + Benchmarking completos |
| **TOTAL** | - | **$25,000** | Sistema completo en producción |

---

## COMUNICACIÓN Y SEGUIMIENTO

### Reportes de Progreso
- **Frecuencia:** Semanal (viernes)
- **Formato:** Email con resumen ejecutivo + detalle técnico
- **Contenido:** Avances de la semana, próximos pasos, blockers

### Reuniones de Seguimiento
- **Kick-off:** Semana 1 (01 Oct 2025)
- **Revisión mensual:** Última semana de cada mes
- **Demo de hitos:** Según calendario de hitos intermedios
- **Cierre de fase:** Al completar cada fase 1-4

### Canales de Comunicación
- **Email:** Comunicación formal y reportes
- **Video llamada:** Reuniones de seguimiento y demos
- **Repositorio:** Código fuente y documentación técnica

---

## SUPUESTOS Y DEPENDENCIAS

### Supuestos Críticos
- 3 empresas comprometidas para validación Fase 1 (confirmadas semana 2)
- 2 de las 3 empresas tienen calculadoras 3C accesibles (confirmadas semana 2)
- FICEM provee contactos técnicos de empresas piloto
- Disponibilidad de datos reales para validación

### Dependencias Externas
- Acceso a calculadoras corporativas 3C para upgrade (semanas 4-7)
- Disponibilidad de empresas piloto para validación (semanas 3-8)
- Feedback de FICEM en tiempo oportuno (máximo 3 días por consulta)
- Definiciones técnicas acordadas en Fase 1

---

**Versión:** 1.0
**Fecha de emisión:** Octubre 2025
**Vigencia:** Durante ejecución de Etapa 1
