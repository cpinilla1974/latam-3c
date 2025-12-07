# Flujo de Proceso - Calculadora País 4C Etapa 1

## EXPLICACIÓN DEL PROCESO

### Participantes del Sistema

**Empresa**: La empresa cementera/concretera que necesita calcular su huella de carbono
**FICEM Operador**: Persona que opera el sistema centralizado en FICEM
**Calculadora País 4C**: La aplicación/software de cálculo de huella de carbono
**Calculadora 3C Corporativa**: Sistema existente en 2 empresas piloto (con upgrade y exportación automática)
**Base Datos**: Donde se almacenan todos los datos procesados

### Flujo Completo Paso a Paso

#### Fase 1 - Solicitud Template
1. **Empresa contacta a FICEM** por email/teléfono solicitando template Excel
2. **FICEM identifica perfil de planta** (integrada/molienda/concreto)
3. **FICEM usa el Sistema** para generar Excel personalizado según perfil
4. **FICEM envía Excel** con instrucciones a la empresa

#### Fase 2 - Completado Offline
5. **Opción A - Empresa SIN calculadora 3C corporativa:**
   - Empresa completa Excel manualmente sin conexión a internet
   - Empresa valida internamente los datos técnicos
   - Empresa envía Excel completado a FICEM por email

6. **Opción B - Empresa CON calculadora 3C corporativa:**
   - Empresa ingresa datos en su calculadora corporativa (ya existente)
   - Sistema exporta automáticamente a formato Excel estandarizado
   - Empresa envía Excel generado automáticamente a FICEM por email

#### Fase 3 - Procesamiento FICEM
7. **FICEM carga** el Excel al sistema
8. **Sistema valida estructura** y consistencia de datos (formato, rangos, composiciones)
9. **Si datos válidos**: Sistema calcula emisiones A1-A3 y clasifica bandas GCCA
10. **Si datos inválidos**: FICEM notifica errores específicos a la empresa para corrección

#### Fase 4 - Reportes y Análisis
11. **Sistema calcula** emisiones por producto (clinker 750-950 kg CO₂e/ton, cemento 400-900 kg CO₂e/ton, concreto 150-500 kg CO₂e/m³)
12. **Sistema clasifica** productos en bandas GCCA (A-G para cementos, AA-F para concretos)
13. **Sistema agrega** datos anónimos para benchmarking por país/región
14. **FICEM accede** a dashboard con métricas consolidadas y curvas comparativas
15. **Sistema genera** reporte individual con clasificación GCCA y benchmarking anónimo
16. **FICEM envía reporte** a la empresa por email

## CARACTERÍSTICAS CLAVE DE LA ETAPA 1

### Modelo Operativo Centralizado
- **FICEM actúa como intermediario** entre empresas y sistema
- **No hay acceso directo** de empresas al sistema
- **Comunicación por email/teléfono** únicamente

### Proceso Simplificado
- **Templates Excel personalizados** según perfil de planta (integrada/molienda/concreto)
- **Completado offline** por las empresas
- **2 empresas piloto con calculadora 3C** corporativa upgraded con exportación automática
- **Carga** por operador FICEM
- **Validación automática multinivel** del sistema

### Outputs del Sistema
- **Cálculos de emisiones A1-A3** siguiendo protocolo GCCA riguroso
  - Clinker: 750-950 kg CO₂e/ton
  - Cemento: 400-900 kg CO₂e/ton
  - Concreto: 150-500 kg CO₂e/m³
- **Clasificación en bandas GCCA** (A-G para cementos, AA-F para concretos)
- **Base de datos de benchmarking** anónimo por país/región
- **Curvas comparativas** CO₂ vs resistencia para concretos
- **Dashboard consolidado** para operador FICEM
- **Reportes individuales** por empresa con benchmarking

### Validación del Proceso
- **Validación de formato** automática (estructura, hojas requeridas, campos)
- **Validación de coherencia** automática (rangos, composiciones al 100%, consistencia volumen/densidad)
- **Correcciones iterativas** con indicaciones precisas hasta datos válidos

### Ventajas del Modelo
- **Validación del proceso** de cálculos con 3 empresas piloto
- **Reducción de inversión inicial** antes de escalar a portal web
- **Upgrade de calculadoras existentes** maximiza ROI para 2 empresas
- **Eliminación de re-ingreso manual** para empresas con calculadora corporativa

Este modelo permite **validar el proceso completo** y **construir base de benchmarking** antes de desarrollar la complejidad web de la Etapa 2.