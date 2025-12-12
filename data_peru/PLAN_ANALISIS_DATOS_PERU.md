# Plan de Análisis de Datos - Sector Cemento Perú

## Contexto

Necesitamos reproducir el **Reporte de Seguimiento 2010-2023** usando datos reales de las bases de datos de las 3 empresas principales del sector cemento en Perú:

1. **UNACEM** - `/home/cpinilla/storage/access/UNACEM.accdb`
2. **Pacasmayo** - `/home/cpinilla/pacas-3c/data/main.db`
3. **Yura** - `/home/cpinilla/databases/yura-2c/data/main.db`

## Objetivo

Generar **totales nacionales agregados** para los 6 grupos de indicadores del reporte TDR Ítem 2, identificando qué indicadores se suman y cuáles requieren promedios ponderados.

---

## Grupos de Indicadores del Reporte

### Grupo 1: Producción de Clinker y Cemento
| Código | Indicador | Unidad | Tipo Agregación |
|--------|-----------|--------|-----------------|
| 8 | Producción de Clínker | Mt clínker | **SUMA** |
| 11 | Consumo de Clínker | Mt clínker | **SUMA** |
| 20 | Producción de Cemento | Mt cemento | **SUMA** |
| 21a | Producción de Cementitious | Mt cementitious | **SUMA** |

**Nota**: Estos son **indicadores sumables** - se suman directamente entre empresas.

---

### Grupo 2: Contenido de Clínker
| Código | Indicador | Unidad | Tipo Agregación |
|--------|-----------|--------|-----------------|
| 92a | Factor Clínker | % | **PROMEDIO PONDERADO** (por producción cemento) |
| 12+16 | Adiciones en Cemento | % | **PROMEDIO PONDERADO** (por producción cemento) |

**Cálculo promedio ponderado**:
```
Factor_Clinker_Nacional = Σ(Consumo_Clinker_i) / Σ(Producción_Cemento_i)
Adiciones_Nacional = Σ(Adiciones_i × Producción_i) / Σ(Producción_i)
```

---

### Grupo 3: Emisiones Específicas CO₂
| Código | Indicador | Unidad | Tipo Agregación |
|--------|-----------|--------|-----------------|
| 60a+1008+1010 | Emisiones Netas CO₂ Clínker | kg CO₂/t clínker | **PROMEDIO PONDERADO** (por producción clínker) |
| 62a+1021+1022 | Emisiones Netas CO₂ Cementitious | kg CO₂/t cementitious | **PROMEDIO PONDERADO** (por producción cementitious) |
| 59c | Emisiones Consolidadas IPCC | Mt CO₂ | **SUMA** (emisiones totales) |

**Cálculo promedios ponderados**:
```
Emisiones_Clinker_Nacional = Σ(Emisiones_CO2_Clinker_i × Producción_Clinker_i) / Σ(Producción_Clinker_i)
```

---

### Grupo 4: Eficiencia Energética
| Código | Indicador | Unidad | Tipo Agregación |
|--------|-----------|--------|-----------------|
| 93 | Eficiencia Térmica | MJ/t clínker | **PROMEDIO PONDERADO** (por producción clínker) |
| 95+96 | Coprocesamiento | % | **PROMEDIO PONDERADO** (por energía total) |
| 161-183a | Energía Térmica Consumida | TJ/año | **SUMA** |

---

### Grupo 5: Indicadores Eléctricos
| Código | Indicador | Unidad | Tipo Agregación |
|--------|-----------|--------|-----------------|
| 1042 | Consumo Eléctrico | TWh/año | **SUMA** |
| 97 | Factor Consumo Eléctrico | kWh/t cementitious | **PROMEDIO PONDERADO** (por producción cementitious) |
| 33d | Factor Emisión Matriz Eléctrica | kg CO₂/MWh | **PROMEDIO PONDERADO** (por consumo eléctrico) |

---

### Grupo 6: Mejoras Tecnológicas
Análisis cualitativo por empresa (no requiere agregación numérica).

---

## Metodología de Trabajo

### Fase 1: Análisis de Estructura de Datos

#### 1.1 Explorar base de datos UNACEM (Access)
- **Tecnología**: Convertir .accdb a SQLite o usar `mdb-tools`
- **Objetivo**: Entender tablas, identificar indicadores disponibles
- **Output**: Mapeo de indicadores UNACEM → códigos estándar

#### 1.2 Explorar base de datos Pacasmayo (SQLite)
- **Tecnología**: SQLite nativo
- **Modelo**: Dataset-Data (según documentación)
- **Query ejemplo**:
```sql
SELECT d.codigo_indicador, d.valor_indicador, ds.fecha
FROM tb_data d
JOIN tb_dataset ds ON d.id_dataset = ds.id_dataset
WHERE d.codigo_indicador IN ('8', '11', '20', '21a')
  AND ds.id_tipo_origen = 1 -- Plantas
  AND ds.fecha BETWEEN '2010-01-01' AND '2023-12-31'
```

#### 1.3 Explorar base de datos Yura (SQLite)
- **Tecnología**: SQLite nativo
- **Modelo**: Probablemente similar a Pacasmayo (modelo Dataset-Data)
- **Objetivo**: Confirmar estructura y mapeo de indicadores

---

### Fase 2: Extracción de Datos

#### 2.1 Crear script de extracción unificado
**Archivo**: `data_peru/scripts/extraer_datos_empresas.py`

```python
import sqlite3
import pandas as pd
from pathlib import Path

def extraer_indicadores_pacasmayo(años_inicio, años_fin):
    """Extrae indicadores de Pacasmayo usando modelo Dataset-Data"""
    conn = sqlite3.connect('/home/cpinilla/pacas-3c/data/main.db')

    query = """
    SELECT
        strftime('%Y', ds.fecha) as año,
        d.codigo_indicador,
        d.valor_indicador,
        ds.id_rep_temp
    FROM tb_data d
    JOIN tb_dataset ds ON d.id_dataset = ds.id_dataset
    WHERE d.codigo_indicador IN (?, ?, ?, ...)
      AND ds.fecha BETWEEN ? AND ?
      AND ds.id_tipo_origen = 1
    """

    df = pd.read_sql_query(query, conn, params=[...])
    return df

def extraer_indicadores_unacem(...):
    # Conversión desde Access
    pass

def extraer_indicadores_yura(...):
    # Similar a Pacasmayo
    pass
```

#### 2.2 Consolidar datos por año
**Output**: `data_peru/datos_raw/`
- `pacasmayo_2010_2023.csv`
- `unacem_2010_2023.csv`
- `yura_2010_2023.csv`

---

### Fase 3: Cálculo de Agregados Nacionales

#### 3.1 Script de agregación
**Archivo**: `data_peru/scripts/calcular_agregados_nacionales.py`

```python
def calcular_indicadores_sumables(df_pacas, df_unacem, df_yura):
    """
    Indicadores sumables: 8, 11, 20, 21a, 1042, 161-183a, 59c
    """
    df_nacional = pd.concat([
        df_pacas[df_pacas['codigo_indicador'].isin(['8','11','20','21a'])],
        df_unacem[...],
        df_yura[...]
    ]).groupby(['año', 'codigo_indicador'])['valor_indicador'].sum().reset_index()

    return df_nacional

def calcular_promedios_ponderados(df_pacas, df_unacem, df_yura):
    """
    Indicadores con promedio ponderado: 92a, 60a, 62a, 93, 97, 33d
    """
    # Ejemplo Factor Clinker (92a)
    # Factor_Nacional = Σ(Consumo_Clinker) / Σ(Producción_Cemento)

    consumo_clinker = df_nacional[df_nacional['codigo_indicador'] == '11']['valor_indicador']
    produccion_cemento = df_nacional[df_nacional['codigo_indicador'] == '20']['valor_indicador']

    factor_clinker_nacional = (consumo_clinker / produccion_cemento) * 100

    return factor_clinker_nacional
```

**Output**: `data_peru/datos_procesados/indicadores_nacionales_2010_2023.csv`

---

### Fase 4: Validación contra Reporte Oficial

#### 4.1 Comparación de resultados
Comparar datos calculados vs datos del reporte PDF:

| Año | Indicador | Valor Calculado | Valor Reporte | Diferencia % |
|-----|-----------|-----------------|---------------|--------------|
| 2023 | 8 (Producción Clínker) | 9.45 Mt | 9.45 Mt | 0% |
| 2023 | 92a (Factor Clínker) | 74% | 74% | 0% |
| ... | ... | ... | ... | ... |

**Tolerancia aceptable**: ±2% (debido a redondeos en el reporte)

---

### Fase 5: Generación de Gráficos

#### 5.1 Recrear gráficos del reporte
**Archivo**: `data_peru/notebooks/visualizaciones_reporte_seguimiento.ipynb`

Usando `matplotlib` o `plotly`, recrear:
- Gráfico 1.1: Producción de Clínker 2010-2023
- Gráfico 2.1: Factor Clínker 2010-2023
- Gráfico 3.1: Emisiones Netas CO₂ Clínker
- ... (todos los gráficos del reporte)

#### 5.2 Gráficos adicionales de análisis
- Contribución por empresa (% del total nacional)
- Tendencias y tasas de variación
- Proyecciones a 2030

---

## Estructura de Archivos Propuesta

```
data_peru/
├── PLAN_ANALISIS_DATOS_PERU.md (este documento)
├── reporte_seguimiento_peru_190325.pdf (documento fuente)
│
├── scripts/
│   ├── extraer_datos_empresas.py
│   ├── calcular_agregados_nacionales.py
│   ├── validar_contra_reporte.py
│   └── utils.py
│
├── datos_raw/
│   ├── pacasmayo_2010_2023.csv
│   ├── unacem_2010_2023.csv
│   └── yura_2010_2023.csv
│
├── datos_procesados/
│   ├── indicadores_nacionales_2010_2023.csv
│   └── validacion_vs_reporte.csv
│
├── notebooks/
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_agregacion_nacional.ipynb
│   └── 03_visualizaciones_reporte.ipynb
│
└── graficos/
    ├── grupo1_produccion/
    ├── grupo2_contenido_clinker/
    ├── grupo3_emisiones/
    ├── grupo4_eficiencia/
    ├── grupo5_electricos/
    └── grupo6_mejoras/
```

---

## Reglas de Agregación - Resumen

### ✅ INDICADORES SUMABLES (totales directos)
- **8**: Producción de Clínker
- **11**: Consumo de Clínker
- **20**: Producción de Cemento
- **21a**: Producción de Cementitious
- **1042**: Consumo Eléctrico Total
- **161-183a**: Energía Térmica Consumida
- **59c**: Emisiones Consolidadas IPCC

### ⚖️ INDICADORES CON PROMEDIO PONDERADO
| Indicador | Ponderador |
|-----------|------------|
| 92a (Factor Clínker) | Producción Cemento [20] |
| 60a (Emisiones CO₂ Clínker) | Producción Clínker [8] |
| 62a (Emisiones CO₂ Cementitious) | Producción Cementitious [21a] |
| 93 (Eficiencia Térmica) | Producción Clínker [8] |
| 97 (Consumo Eléctrico Específico) | Producción Cementitious [21a] |
| 33d (Factor Emisión Eléctrica) | Consumo Eléctrico [1042] |
| 95+96 (Coprocesamiento) | Energía Total Consumida |

---

## Próximos Pasos Inmediatos

1. ✅ Verificar acceso a las 3 bases de datos
2. ⏳ Explorar esquema de UNACEM (Access)
3. ⏳ Confirmar estructura Yura
4. ⏳ Escribir script de extracción para Pacasmayo
5. ⏳ Adaptar extracción para UNACEM y Yura
6. ⏳ Consolidar y calcular agregados nacionales
7. ⏳ Validar contra reporte oficial
8. ⏳ Generar gráficos finales

---

## Notas Técnicas

### Conversión de UNACEM.accdb
Opciones:
- **mdb-tools**: `mdb-export UNACEM.accdb tabla > tabla.csv`
- **pyodbc**: Lectura directa desde Python
- **Conversión manual**: Access → SQLite usando herramienta GUI

### Periodos de Datos
Según reporte: **2010, 2014, 2016, 2019, 2021, 2023**
- No todos los años tienen datos
- Priorizar estos 6 años para validación

### Unidades
Convertir correctamente:
- **Mt** = Millones de toneladas = 10⁶ toneladas
- **TJ** = Terajulios = 10¹² julios
- **TWh** = Terawatt-hora = 10¹² watt-hora
