# Cálculos y Salidas - LATAM-3C

## 1. CÁLCULOS DE EMISIONES

### 1.1 CLINKER
**Unidad**: kg CO₂e/ton clinker

**Componentes del cálculo**:
- **A1 - Materias Primas y Combustibles**: Emisiones de extracción y procesamiento de materias primas y combustibles
- **A2 - Transporte**: Emisiones del transporte de materias primas y combustibles
- **A3 - Producción**:
  - Emisiones de proceso (descarbonatación caliza ~525 kg CO₂/ton clinker)
  - Combustión de combustibles para energía térmica del horno
  - Electricidad consumida en planta (factor emisión por país)
  - Gestión de residuos
  - Consumo de agua
- **Total A1-A3**: Suma de todos los componentes

**Valores de referencia para benchmarking**: 750-950 kg CO₂e/ton clinker

### 1.2 CEMENTO
**Unidad**: kg CO₂e/ton cemento

**Componentes del cálculo**:
- **A1 - Materias Primas y Combustibles**: Emisiones de extracción y procesamiento de materias primas y combustibles
- **A2 - Transporte**: Emisiones del transporte de materias primas y combustibles
- **A3 - Producción**:
  - Combustibles fuera de horno
  - Electricidad consumida en planta (factor emisión por país)
  - Gestión de residuos
  - Consumo de agua
- **Total A1-A3**: Suma de todos los componentes


**Bandas GCCA para Cemento**:
- Basadas en ratio clinker/cemento del país
- 7 bandas con valores equidistantes
- AA = "Near Zero Emissions Cement"
- Cada país define su propio ratio base (ej: Alemania usa 0.706)
- Los valores específicos dependen del ratio elegido

**Curvas CO₂-Resistencia FICEM**:
- Relación emisiones vs resistencia por tipo de cemento
- Benchmarking regional LATAM

**Rango típico**: 400-900 kg CO₂e/ton cemento

### 1.3 CONCRETO
**Unidad**: kg CO₂e/m³ concreto

**Componentes del cálculo**:
- **A1 - Materias Primas y Combustibles**: Emisiones de extracción y procesamiento de materias primas y combustibles
- **A2 - Transporte**: Emisiones del transporte de materias primas y combustibles
- **A3 - Producción**:
  - Combustibles para proceso de producción
  - Electricidad consumida en planta (factor emisión por país)
  - Gestión de residuos
  - Consumo de agua
- **Total A1-A3**: Suma de todos los componentes

**Bandas GCCA para Concreto**:

| Resistencia | AA | A | B | C | D | E | F |
|------------|-----|-----|-----|-----|-----|-----|-----|
| 20 MPa | 21 | 68 | 115 | 161 | 208 | 255 | 302 |
| 25 MPa | 23 | 75 | 127 | 179 | 231 | 283 | 335 |
| 30 MPa | 26 | 83 | 141 | 199 | 256 | 314 | 372 |
| 35 MPa | 29 | 94 | 159 | 224 | 288 | 353 | 418 |
| 40 MPa | 32 | 101 | 171 | 241 | 310 | 380 | 450 |
| 50 MPa | 36 | 113 | 190 | 268 | 345 | 422 | 500 |

**Nota**: AA = "Near Zero Emissions Concrete"

**Rango típico**: 150-500 kg CO₂e/m³ concreto

## 2. REPORTES DE SALIDA

### 2.1 Reporte Individual por Empresa
**Contenido**:
- Emisiones unitarias clinker: kg CO₂e/ton
- Por cada tipo de cemento:
  - Emisiones: kg CO₂e/ton
  - Banda GCCA (AA-F) según ratio país
- Por cada diseño de concreto:
  - Emisiones: kg CO₂e/m³
  - Banda GCCA según tabla de resistencia

### 2.2 Reporte Consolidado País
**Contenido**:
- Promedio ponderado emisiones por producto
- Distribución de empresas por bandas GCCA
- Comparación año anterior

### 2.3 Reporte Regional LATAM
**Contenido**:
- Ranking países por emisiones promedio
- Distribución regional por bandas GCCA
- Progreso hacia metas de reducción

