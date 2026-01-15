# Axiomas del Proyecto LATAM-3C

## Definición

Los axiomas son principios fundamentales y decisiones de diseño que no se cuestionan durante la implementación. Estos sirven como base para la consistencia del sistema y reducen la ambigüedad en el desarrollo.

---

## A001: Combustibles de Horno desde GCCA y Cálculo Consolidado

**Enunciado**: Los datos de combustibles utilizados en hornos de clinker se tomarán exclusivamente de los archivos GCCA reportados por cada planta. No existirá cálculo separado por horno individual, sino un único cálculo consolidado de clinker por planta.

**Justificación**: 
- Evita duplicación de datos entre sistemas
- Mantiene consistencia con protocolo internacional establecido
- Reduce carga de trabajo para las empresas
- Los archivos GCCA ya contienen esta información validada
- Simplifica la granularidad de cálculo manteniendo precisión a nivel planta
- Las plantas reportan consolidadamente en GCCA independientemente del número de hornos

**Alcance**: 
- Combustibles: carbón, pet coke, gas natural, biomasa, residuos industriales, fuel oil, etc.
- Granularidad: Una planta = un cálculo de clinker (independiente del número de hornos)
- Datos fuente: Exclusivamente archivos GCCA por planta

**Impacto en diseño**: 
- No se solicita información de combustibles de horno en archivos Excel
- No se diferencia entre hornos dentro de una planta
- El cálculo de huella de carbono es por planta, no por horno individual

---

## A002: Combustibles Fuera de Horno desde GCCA con Aplicación Uniforme

**Enunciado**: Los datos de combustibles utilizados en procesos fuera del horno (molienda, secado, transporte interno, etc.) se tomarán exclusivamente de los archivos GCCA reportados por cada planta. Estos combustibles se aplicarán uniformemente a todos los tipos de cemento producidos en la planta, a diferencia del consumo eléctrico que se reporta específicamente por tipo de cemento.

**Justificación**: 
- Consistencia con A001
- Los archivos GCCA incluyen todos los combustibles de la planta de forma consolidada
- Evita errores por reporte manual duplicado
- Los combustibles fuera de horno (diesel para equipos, gas para secado, etc.) son compartidos por toda la planta
- El consumo eléctrico sí puede variar por tipo de cemento (diferentes tiempos de molienda)
- Simplifica la asignación sin perder precisión significativa

**Alcance**: 
- Combustibles: diesel para equipos móviles, gas para secado, combustibles auxiliares
- Aplicación: Distribución proporcional uniforme entre todos los tipos de cemento de la planta
- Diferenciación: El consumo eléctrico sí se reporta específicamente por tipo de cemento

**Impacto en diseño**: 
- Se solicita electricidad específica por tipo de cemento en archivos Excel
- No se solicita combustibles fuera de horno diferenciados por tipo de cemento
- El cálculo distribuye combustibles GCCA proporcionalmente entre tipos de cemento

---

## A003: [Reservado para futuros axiomas]

---

## Formato de Referencia

En documentos técnicos, referenciar axiomas usando el formato: **[Axioma A001]**

Ejemplo:
```
#### SECCIÓN B: COMBUSTIBLES HORNO

**[Axioma A001]**: Los combustibles de horno se tomarán directamente de los archivos GCCA reportados por cada planta.
```

---

## Control de Cambios

| Versión | Fecha | Axioma | Descripción |
|---------|-------|--------|-------------|
| 1.0 | 2025-09-09 | A001 | Combustibles de horno desde GCCA y cálculo consolidado |
| 1.0 | 2025-09-09 | A002 | Combustibles fuera de horno desde GCCA con aplicación uniforme |
