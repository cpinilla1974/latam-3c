# Modelo Propuesto LATAM-3C

## Contexto
Basado en proyectos existentes (melon-3c, mzma-3c) que ya manejan:
- Cálculo de huella de carbono para clinker, cemento y concreto
- Arquitectura con clases abstractas y repositorio pattern
- Sistema de códigos semánticos
- 85% de código reutilizable entre productos

## Arquitectura Propuesta: Excel + Web

### Flujo de Datos
```
[Excel CEMEX_MX_2024] ──┐
[Excel ARGOS_CO_2024] ──┼──► [Web: Validación] ──► [Consolidación] ──► [Reportes]
[Excel VIAKON_BR_2024] ─┘           ↓                     ↓
                               [Base Datos]          [Cálculos CO2]
```

### Excel - Captura de Datos
**Estructura por empresa:**
- Un archivo Excel anual por empresa
- Nombre: `[EMPRESA]_[PAIS]_[AÑO].xlsx`
- Hojas:
  1. **Info_Empresa**: Datos generales, plantas
  2. **Clinker**: Producción, combustibles, materias primas
  3. **Cemento**: Tipos, composiciones, molienda
  4. **Concreto**: Diseños de mezcla, volúmenes
  5. **Transporte**: Rutas, vehículos, distancias
  6. **Validación**: Pre-cálculos y verificaciones

**Funcionalidades en Excel:**
- Validaciones de rangos
- Cálculos preliminares de verificación
- Totales y subtotales automáticos
- Alertas de valores atípicos
- Menús desplegables para códigos estándar

### Web - Procesamiento Central
**Stack tecnológico (basado en existente):**
- Python + Streamlit (ya probado en mzma-3c)
- SQLite/PostgreSQL 
- Repository pattern para multi-empresa

**Módulos principales:**
1. **Carga**: Recepción y validación de Excel
2. **Procesamiento**: Aplicar clases abstractas existentes
3. **Cálculo**: Motor de CO2 ya desarrollado
4. **Consolidación**: Por país y región LATAM
5. **Reportes**: Dashboard y exportación

## Diferencias con Proyectos Actuales

### Lo que cambia:
- **Multi-empresa**: Aislamiento de datos por compañía
- **Periodicidad anual**: No mensual/diaria
- **Consolidación regional**: Vista LATAM agregada

### Lo que se reutiliza (85%):
- Clases abstractas de cálculo
- Sistema de códigos semánticos
- Lógica de cálculo CO2
- Estructura de base de datos base

## Ventajas del Modelo
1. **Simplicidad**: Un solo proyecto web
2. **Familiaridad**: Empresas ya usan Excel
3. **Reutilización**: Aprovecha código existente
4. **Escalabilidad**: Fácil agregar empresas/países

## Próximos Pasos
1. Definir estructura exacta del Excel
2. Mapear campos con sistema existente
3. Diseñar permisos multi-empresa
4. Definir reportes consolidados LATAM