# Metodología de Cálculo - Protocolo MRV FICEM-ASOCEM Perú

**Versión:** 1.0
**Fecha:** 2025-10-03
**Base:** Protocolo MRV Perú 2025 v01 (18-03-2025)
**Compatible con:** CSI Protocol 3.1, IPCC 2006, GNR

---

## 1. ESTRUCTURA GENERAL

### 1.1 Arquitectura del Cálculo

```
DATOS ENTRADA (CSI Protocol 3.1)
         ↓
    VALIDACIÓN
         ↓
    AGREGACIÓN DE FACTORES
    (SEIN, Combustibles Perú)
         ↓
    CÁLCULO POR PLANTA
    (Línea Base + Escenarios)
         ↓
    CONSOLIDACIÓN PAÍS
         ↓
    REPORTES MRV
```

### 1.2 Niveles de Cálculo

1. **Planta individual**: Emisiones históricas y proyectadas 2010-2030
2. **Escenarios de mitigación**: Línea base vs medidas de reducción
3. **Consolidado país**: Agregación anónima para reporte a autoridad

---

## 2. FACTORES DE EMISIÓN Y ECUACIONES

### A. FACTOR CLÍNKER

#### A.1 Factor de Emisión por Defecto

**Ecuación 2.14: Factor de Emisión para el Clínker**

```
EFCa = 0.51 × 1.02 × (corrección de CDK) - 0.52 toneladas de CO₂ / toneladas de clínker
```

**Fuente:** GI.2006, Vol. 3, p. 2.13, Ecuación 2.14

**Componentes:**

| Parámetro | Valor | Unidad | Descripción |
|-----------|-------|--------|-------------|
| Factor de emisión del clinker (sin corrección) | 0.51 | tCO₂/tcl | GI.2006, Vol. 3, p. 2.13 |
| Factor de corrección CDK (CFCDK) | 1.02 | adimensional | GI.2006, Vol. 3, p. 2.14 (corrección aditiva del 2%) |
| Factor de emisión clínker con corrección de CKD | 0.52 | tCO₂/tcl | GI.2006, Vol. 3, p. 2.13 |

#### A.2 Factor de Emisión por Planta Industrial

##### A.2.1 Constantes

| Parámetro | Valor | Unidad | Fuente |
|-----------|-------|--------|--------|
| Participación del CaO en los productos de la calcinación del CaCO₃ | 56.03% | % en peso de CO₂ | GI.2006, Vol. 3, p. 2.13 |
| Participación del CO₂ en los productos de la calcinación del CaCO₃ | 43.97% | % en peso de CaO | GI.2006, Vol. 3, p. 2.13 |
| Factor de corrección CDK (CFCDK) | 1.02 | adimensional | GI.2006, Vol. 3, p. 2.14 |

##### A.2.2 Ecuación 2.2: Emisiones Basadas en Producción de Clínker

```
EmisionescO₂ = EFclinker × Mcl × CFCKD
```

**Donde:**
- `Emisiones CO₂`: Emisiones de CO₂ proveniente de la producción de cemento (toneladas)
- `Mcl`: Peso (masa) de clínker producido (toneladas)
- `EFcl`: Factor de emisión para el clínker (toneladas de CO₂/toneladas de clínker)
- `CFCKD`: Factor corrector de las emisiones para el CKD, sin dimensión, Valor = 1

**Fuente:** GI.2006, Vol. 3, p. 2.10, Ecuación 2.2

##### A.2.3 Cálculo del Factor de Emisión por Planta

**Método 1: Factor producido + clinker consumido**
```
si clinker producido + clinker consumido:
    FE = Σ[{Ci}i × (811/311)] / Σ[{Ci}i] × 1000

    Donde:
    {Ci}i = clinker producido o clinker consumido del año i
    811/311 = conversión estequiométrica
```

**Método 2: Factor producido × clinker consumido**
```
si clinker producido × clinker consumido:
    FE = Σ[({Ci}i × (811/311)) / Σ{Ci}i] × 1000

    Donde n = número de plantas
```

---

### B. EFICIENCIA ENERGÉTICA

#### B.1 Cálculo de Emisiones del Consumo Eléctrico del SEIN

**Ecuación:**
```
EAy = CEAy × EFy
```

**Donde:**
- `EAy`: Emisiones por consumo de energía eléctrica del SEIN, en el año y (tCO₂)
- `CEAy`: Consumo de energía activa, en el año y (MWh)
- `EFy`: Factor de emisión por consumo de energía, en el año y (tCO₂/MWh)

**Fuente:** Basado en Apéndice A del Protocolo de Gases de Efecto Invernadero "Estándar Corporativo de Contabilidad y Reporte", p 98.

#### B.2 Factores del Sistema Eléctrico Interconectado Nacional - SEIN

**Histórico de Factores de Emisión 2010-2018:**

| Año | tCO₂/MWh | Gg CO₂/kWh |
|-----|----------|------------|
| 2010 | 0.240 | 0.000002404 |
| 2011 | 0.230 | 0.000002302 |
| 2012 | 0.224 | 0.000002243 |
| 2013 | 0.209 | 0.000001091 |
| 2014 | 0.207 | 0.000002066 |
| 2015 | 0.203 | 0.000002026 |
| 2016 | 0.222 | 0.000002221 |
| 2017 | 0.184 | 0.000001843 |
| 2018 | 0.151 | 0.000001511 |

**Proyecciones 2019-2030:**
Todos los años: `0.000000000`

**Fuente:** Comunicación remitida por especialista Alfonso Córdova de la DGEE del MINEM 2019.

**Nota:** Espacios a completar con la información proporcionada por MINEM

---

### C. COPROCESAMIENTO

#### C.1 Cálculo de Emisiones del Coprocesamiento

**Ecuación:**
```
Emisionesgas_efecto_invernadero = Consumo_combustiblecombustible × Factor_de_emisiónGEI,combustible
```

**Fuente:** GI.2006, Vol. 2, p. 2.11, Ecuación 2.1

**Donde:**
- `Emisionesgas_combustible`: Emisiones de un gas de efecto invernadero dado por tipo de combustible (kg GEI)
- `Consumo_combustiblecombustible`: Cantidad de combustible quemado (TJ)
- `Factor_de_emisiónGEI,combustible`: Factor de emisión por defecto de un gas de efecto invernadero dado por tipo de combustible (kg gas/TJ)

#### C.2 Factores de Emisión de Combustibles

##### C.2.1 Combustibles Tradicionales

| Combustible | FE CO₂ (Valor) | FE CO₂ (Unidades) | Fuente | Nota |
|-------------|----------------|-------------------|--------|------|
| **Carbón mineral** | 96.3 | kg CO₂e/GJ | Diseño de medidades de mitigación apropiadas para cada tipo de Cemento en el Perú y diseño de su respectivo sistema de Monitoreo, Reporte y Verificación (LECB, 2015) | Calculado en base a Cuadro 2.3, Capítulo2, Volumen 2, Guías del IPCC 2006. A partir del promedio entre los valores para el antracita, carbón de coque y carbón bituminoso. |
| **Fueloil residual** | 77.4 | kg CO₂e/GJ | Cuadro 2.3, Capítulo2, Volumen 2, Guías del IPCC 2006. | |
| **Gas natural** | 56.1 | kg CO₂e/GJ | Cuadro 2.3, Capítulo2, Volumen 2, Guías del IPCC 2006. | |
| **Petróleo crudo** | 73.3 | kg CO₂e/GJ | Cuadro 2.3, Capítulo2, Volumen 2, Guías del IPCC 2006. | |

##### C.2.2 Valor Calorífico Neto (VCN)

| Combustible | Valor | Unidades | Fuente |
|-------------|-------|----------|--------|
| **Carbón mineral** | 26.25 | TJ/Gg | Directrices del IPCC de 2006 para los inventarios nacionales de gases de efecto invernadero; WBCSD - Cement Sustainability Initiative (CSI): CO2 and Energy Accounting and Reporting Standard for the Cement Industry, Mayo 2011 LECB 2015. |
| **Fueloil residual** | 40.4 | TJ/Gg | |
| **Gas natural** | 48.0 | TJ/Gg | |
| **Gas natural** | 8,154.06 | kcal/m3 | WBCSD - Cement Sustainability Initiative (CSI): CO2 and Energy Accounting and Reporting Standard for the Cement Industry, Mayo 2011 LECB 2015. |
| **Petróleo crudo** | 42.3 | TJ/Gg | |

##### C.2.3 Combustibles Alternativos

| Combustible alternativo | Valor | Unidades | Fuente |
|------------------------|-------|----------|--------|
| Combustible alternativo 1 | | ton CO₂e/ton combustible | completar con la información correspondiente |
| Combustible alternativo 2 | | ton CO₂e/ton combustible | completar con la información correspondiente |
| Combustible alternativo 3 | | ton CO₂e/ton combustible | completar con la información correspondiente |

**Nota:** Espacio a completar con los factores de emisión que corresponden a los combustibles alternativos que se utilicen en los proyectos de coprocesamiento de las empresas

---

### D. FACTORES DE CONVERSIÓN

| Cantidad | Unidad Origen | Factor | Unidad Destino |
|----------|---------------|--------|----------------|
| 1 | Gg | 1000 | t |
| 1 | MWh | 1000 | KWh |
| 1 | t | 1000 | kg |
| 1 | TJ | 1000 | GJ |

---

## 3. ESTRUCTURA DE DATOS POR PLANTA

### 3.1 Emisiones de Línea Base de Gases de Efecto Invernadero

**Período:** 2010-2030 (histórico 2010-presente, proyección hasta 2030)

#### Sección 1: Emisiones de GEI Escenario de Línea Base

| Campo | Descripción | Unidad |
|-------|-------------|--------|
| Año | Año calendario | YYYY |
| Producción de cemento (ton) | Producción anual de cemento | ton/año |
| Reducción clinker (ton) | Reducción anual de clinker | ton/año |
| Emisiones producción de CaO y MgO (tCO₂) | Emisiones de calcinación | tCO₂/año |
| Consumo de energía primaria (tCO₂) | Emisiones por combustibles primarios | tCO₂/año |
| Uso de combustibles alternativos, tradicionales y biomasa (tCO₂) | Emisiones por combustibles horno | tCO₂/año |
| Generación de energía eléctrica on-site (tCO₂) | Emisiones generación eléctrica in-situ | tCO₂/año |
| Consumo de energía eléctrica de la red nacional (tCO₂) | Emisiones por electricidad externa | tCO₂/año |
| Reducción de pagos por adquisición de bonos de carbono (tCO₂) | Créditos de carbono | tCO₂/año |

**Totalizadores:**
- Emisiones de gases de efecto invernadero GEI (sin remociones) (tCO₂/año)
- Emisiones por la captura de gases de efecto invernadero GEI (tCO₂/año)
- Emisiones netas de gases de efecto invernadero GEI (tCO₂/año)

#### Sección 2: Emisiones de GEI Escenario de Mitigación

**Misma estructura que Sección 1**

Incluye campos adicionales:
- Valor del nivel de reducción del factor clinker/cemento asociados (tCO₂)
- Valor de las palancas de la hoja Escenarios de las medidas (tCO₂)
- Valor de la proyección de la reducción de las palancas del Coprocesamiento (tCO₂)

#### Sección 3: Reducción de Emisiones de GEI

| Campo | Fórmula |
|-------|---------|
| FC, CP, EE (por separado) | Emisiones_Línea_Base - Emisiones_Escenario_Mitigación |
| Reducción Total | Suma de todas las reducciones |

---

### 3.2 Combustibles Tradicionales

**Tabla de consumo de combustibles por año:**

| Año | Consumo de Carbón Mineral (TJ) | Valor Calorífico Neto Carbón Mineral (TJ/Gg) | Factor de emisión de carbón mineral (kg CO₂e/TJ) | Consumo de Fueloil residual (TJ) | Valor Calorífico Neto fueloil residual (TJ/Gg) | Factor de emisión de fueloil (kg CO₂e/TJ) | [continúa para gas natural, petróleo crudo] |
|-----|------|------|------|------|------|------|------|

**Valores por defecto:**
- Valores de factores de emisión: Tabla C.2.1
- Valores de VCN: Tabla C.2.2
- Valores calculados de manera automática

---

### 3.3 Combustibles Alternativos

**Similar a 3.2 pero para combustibles alternativos específicos de cada empresa**

Campos adicionales:
- Tipo de combustible alternativo (descripción)
- Factor de emisión específico (kg CO₂e/TJ)
- VCN específico

---

## 4. CONSOLIDACIÓN A NIVEL PAÍS

### 4.1 Agregación de Plantas

```
Indicador_País = Σ(Indicador_Planta_i) para i = 1 to n

Donde:
  n = número de plantas
  Indicador_Planta_i = valor del indicador para la planta i
```

### 4.2 Indicadores Consolidados

#### Producción
- Cemento producido (Σ ton cemento/año)
- Cementitious producido (Σ ton cementitious/año)
- Clinker producido (Σ ton clinker/año)
- Clinker consumido (Σ ton clinker/año)

#### Indicadores Técnicos
- Factor Clinker (promedio ponderado, mínimo, máximo) %
- Consumo Térmico Plantas Integradas (promedio ponderado, mínimo, máximo) MJ/ton Clinker
- Coprocesamiento (promedio ponderado, mínimo, máximo) %
- Consumo Eléctrico País (promedio) KWh/ton cemento

#### Emisiones CO₂
**Por alcance:**

**Alcance 1 - Absolutas directas:**
- Descarbonatación (KgCO₂/ton Clinker, KgCO₂/ton Cementitious, KgCO₂/ton Cemento)
- Combustibles convencionales horno
- Combustibles fuera de horno
- Combustibles alternativos horno
- Combustible generación eléctrica on-site

**Alcance 2 - Electricidad Externa:**
- Emisiones por electricidad de red

**Alcance 3 - Clinker Externo:**
- Factor de emisión CSI: 865 kg CO₂/t clínker

**Emisiones Netas vs Brutas:**
- Netas: Sin combustibles alternativos
- Brutas: Incluyendo combustibles alternativos
- Absolutas directas: Todas las fuentes de Alcance 1

---

## 5. REPORTES DE SALIDA

### 5.1 Reporte Indicadores-Año

**Estructura:**
- Encabezado: País, Año, Fecha Reporte
- Sección I: Producción (cemento, clinker, cementitious)
- Sección II: Indicadores Técnicos (factor clinker, consumos, eficiencias)
- Sección III: Emisión CO₂ (por alcance, netas/brutas)

**Formato:** PDF consolidado con datos del año específico

### 5.2 Reporte de Seguimiento

**Estructura:**
- Serie temporal 2010-2030
- Gráficos de evolución de indicadores clave:
  - Producción de Clínker
  - Consumo de Clínker
  - Producción de Cemento
  - Producción de Cementitious
  - Emisiones Netas CO₂ Clínker
  - Emisiones Netas CO₂ Cementitious
  - Factor Clínker
  - Adiciones en el Cemento
  - Coprocesamiento
  - Eficiencia Energética
  - Energía Térmica Consumida
  - Consumo Eléctrico
  - Factor Consumo Eléctrico
  - Factor de la Matriz Eléctrica
  - Emisiones Consolidadas de Proceso y Energía IPCC 2006

**Formato:** PDF con tendencias históricas y proyecciones

### 5.3 Reporte Reducciones Totales GEI

**Estructura:**

```
REDUCCIONES TOTALES DE GEI - [NOMBRE PLANTA/EMPRESA]

Año | ELB-FC | ELB-CP | ELB-EE | EM-FC | EM-CP | EM-EE | RE-FC | RE-CP | RE-EE | RT
----|--------|--------|--------|-------|-------|-------|-------|-------|-------|----
2010|        |        |        |       |       |       |       |       |       |
2011|        |        |        |       |       |       |       |       |       |
...
2030|        |        |        |       |       |       |       |       |       |

Donde:
  ELB = Emisiones de Línea Base (Gg CO₂ eq)
  EM  = Emisiones netas de las Medidas (Gg CO₂ eq)
  RE  = Reducción de emisiones (RE = ELB - EM) (Gg CO₂ eq)
  RT  = Reducción Total de emisiones (Gg CO₂ eq)

  FC  = Factor Clinker
  CP  = Coprocesamiento
  EE  = Eficiencia Energética
```

**Formato:** Tabla con valores calculados de manera automática

---

## 6. VALIDACIONES Y CONTROLES

### 6.1 Validaciones de Entrada

- Consistencia de datos CSI Protocol 3.1
- Rangos válidos para factores de emisión
- Completitud de datos históricos
- Coherencia temporal (tendencias razonables)

### 6.2 Validaciones de Cálculo

- Balance de masa de clinker (producido + comprado = consumido + vendido ± stock)
- Coherencia entre emisiones y producción
- Rangos técnicamente viables para indicadores

### 6.3 Trazabilidad

- Registro de fuente de cada dato
- Versionado de factores de emisión
- Log de cálculos realizados
- Timestamps de procesamiento

---

## 7. REFERENCIAS NORMATIVAS

### Protocolos Base
- **CSI Protocol 3.1**: WBCSD Cement Sustainability Initiative Cement CO₂ and Energy Protocol, Version 3.1
- **IPCC 2006**: Guidelines for National Greenhouse Gas Inventories
  - Volume 2: Energy
  - Volume 3: Industrial Processes
- **GHG Protocol**: Greenhouse Gas Protocol Corporate Standard

### Fuentes de Datos Perú
- **SEIN**: Sistema Eléctrico Interconectado Nacional - Factores de emisión
- **MINEM**: Ministerio de Energía y Minas - DGEE
- **PRODUCE**: Ministerio de la Producción
- **LECB 2015**: Low Emission Capacity Building Programme

### Documentos Específicos
- GI.2006, Vol. 3, p. 2.10-2.14: Ecuaciones de proceso
- Cuadro 2.3, Capítulo 2, Volumen 2: Factores de emisión combustibles
- Alfonso Córdova (DGEE-MINEM 2019): Factores SEIN

---

## 8. NOTAS DE IMPLEMENTACIÓN

### 8.1 Pseudonimización

Según el protocolo FICEM:
- Todos los datos de planta individual deben ser pseudonimizados
- Solo reportes consolidados a nivel país son entregados a autoridad
- FICEM mantiene mapeo real empresa-planta en base de datos segura

### 8.2 Períodos de Reporte

- **Histórico**: 2010 hasta año actual (datos reales)
- **Proyección**: Año actual+1 hasta 2030 (escenarios)
- **Actualización**: Anual, tras cierre de año fiscal

### 8.3 Escenarios de Mitigación

Los escenarios incluyen:
- **FC**: Reducción de factor clinker/cemento
- **CP**: Incremento de coprocesamiento
- **EE**: Mejora de eficiencia energética

Cada escenario se calcula independientemente y luego se consolida.

---

**Fin del Documento**
