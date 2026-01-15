# Validaciones del Sistema - LATAM-3C

## VALIDACIONES REQUERIDAS

### Estructura básica Excel
- Archivo Excel válido (.xlsx)
- Hojas requeridas según tipo de planta (definidas en 01-estructura-datos-entrada.md)
- Columnas según especificación

### Consistencia de datos
- Suma de componentes = Producción total
- Referencias a ID_Material válidos entre hojas
- Datos numéricos en campos numéricos

### Mensajes de validación
El sistema debe generar reportes indicando:
- Errores que impiden procesamiento
- Advertencias para revisión
- Ubicación exacta de problemas (hoja, fila, columna)