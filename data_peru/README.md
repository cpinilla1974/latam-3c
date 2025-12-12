# Análisis de Datos - Sector Cemento Perú

## Resumen del Proyecto

Este directorio contiene el análisis de datos para el **Reporte de Seguimiento 2010-2023 del Sector Cemento Perú**, según TDR Ítem 2.

## Estado Actual ✅

### ✅ Completado

1. **Entorno virtual creado** (`venv_analisis/`)
   - Pandas, matplotlib, plotly, jupyter, pyodbc, mdbtools instalados

2. **Exploración de bases de datos**
   - ✅ Pacasmayo: 56,925 registros, datos 2010-2025
   - ✅ Yura: 3,507 registros, datos 2010-2024
   - ✅ UNACEM: 44,400 registros, datos 2010-2030

3. **Base de datos consolidada creada** (`peru_consolidado.db`)
   - Tabla `empresas`: 3 empresas cargadas
   - Tabla `metadata_indicadores`: 15 indicadores clave
   - Tabla `indicadores_hist`: ✅ **5,254 registros cargados** (3 empresas)
   - Tabla `agregados_nacionales`: Para totales calculados
   - Tabla `log_carga`: 3 registros de carga exitosa

4. **Extracción de datos históricos completada** ✅
   - ✅ Pacasmayo: 3,288 registros (1,761 nuevos + 1,527 actualizados)
   - ✅ Yura: 94 registros (todos nuevos)
   - ✅ UNACEM: 1,980 registros (todos nuevos)
   - **Total consolidado: 5,362 registros de indicadores históricos**

5. **Cálculo de agregados nacionales completado** ✅
   - ✅ **269 agregados nacionales** calculados (2010-2030)
   - ✅ 142 indicadores sumados directamente (8, 11, 20, 21a, 60, 73, etc.)
   - ✅ 127 promedios ponderados (92a, 60a, 62a, 93, 97, etc.)
   - ✅ 19 indicadores únicos con series temporales completas
   - ✅ Exportado a CSV: `datos_procesados/agregados_nacionales.csv`

6. **Generación de gráficos completada** ✅
   - ✅ **8 gráficos** generados (grupos 1-5 del reporte)
   - ✅ Reporte HTML interactivo creado
   - ✅ Gráficos guardados en: `graficos/`
   - ✅ Abrir: `graficos/reporte_completo.html`

### ⏳ Pendiente

7. **Validar** contra datos oficiales del reporte PDF

---

## Hallazgos Importantes

###  Indicadores Encontrados en Pacasmayo
✅ **TODOS los indicadores clave están disponibles**:
- [8] Producción Clínker: 324 registros (2010-2025)
- [11] Consumo Clínker: 1,349 registros
- [20] Producción Cemento: 193 registros
- [21a] Producción Cementitious: 193 registros
- [92a] Factor Clínker: 703 registros
- [60a] Emisiones CO₂ Clínker: 324 registros
- [62a] Emisiones CO₂ Cementitious: 185 registros
- [93] Eficiencia Térmica: 185 registros
- [97] Consumo Eléctrico Específico: 192 registros

❌ **Indicador faltante**:
- [1042] Consumo Eléctrico Total - Requiere cálculo

### Indicadores Encontrados en Yura
✅ **Indicadores principales disponibles** pero con **menos registros**:
- [8] Producción Clínker: 80 registros (2010-2024)
- [11] Consumo Clínker: 279 registros
- [20-97] Solo 6 registros cada uno (2010-2022)

⚠️ **Yura tiene datos más limitados** - requiere verificación

---

## Estructura de Archivos

```
data_peru/
├── README.md                          (este archivo)
├── PLAN_ANALISIS_DATOS_PERU.md        (plan detallado)
├── reporte_seguimiento_peru_190325.pdf (documento fuente)
├── peru_consolidado.db                 (✅ base de datos consolidada)
│
├── venv_analisis/                     (entorno virtual Python)
│
├── scripts/
│   ├── 01_explorar_bases_datos.py     (✅ completado)
│   ├── 02_crear_base_consolidada.py   (✅ completado)
│   ├── 03_extraer_pacasmayo.py        (✅ completado - 3,288 registros)
│   ├── 04_extraer_yura.py             (✅ completado - 94 registros)
│   ├── 05_extraer_unacem.py           (✅ completado - 1,980 registros)
│   ├── 06_calcular_agregados.py       (✅ completado - 269 agregados)
│   └── 07_generar_graficos.py         (✅ completado - 8 gráficos)
│
├── datos_raw/                         (vacío - para datos extraídos)
├── datos_procesados/
│   └── agregados_nacionales.csv       (✅ 269 agregados 2010-2030)
├── notebooks/                         (vacío - para análisis Jupyter)
└── graficos/                          (✅ 8 gráficos PNG + reporte HTML)
```

---

## Cómo Usar

### 1. Activar entorno virtual
```bash
source venv_analisis/bin/activate
```

### 2. Explorar bases de datos
```bash
python scripts/01_explorar_bases_datos.py
```

### 3. Crear base consolidada
```bash
python scripts/02_crear_base_consolidada.py
```

### 4. Extraer datos de las 3 empresas
```bash
python scripts/03_extraer_pacasmayo.py
python scripts/04_extraer_yura.py
python scripts/05_extraer_unacem.py
```

### 5. Calcular agregados nacionales
```bash
python scripts/06_calcular_agregados.py
```

### 6. Generar gráficos del reporte
```bash
python scripts/07_generar_graficos.py
```

### 7. Ver reporte completo
Abre en tu navegador: `graficos/reporte_completo.html`

### 8. Ejecutar aplicación interactiva
```bash
streamlit run app_visualizacion.py
```

---

## Reglas de Agregación

### ✅ Indicadores Sumables
Se suman directamente entre empresas:
- 8, 11, 20, 21a (producción/consumo)
- 1042 (consumo eléctrico total)
- 59c (emisiones consolidadas)

### ⚖️ Indicadores con Promedio Ponderado
| Indicador | Ponderador |
|-----------|------------|
| 92a | Producción Cemento [20] |
| 60a | Producción Clínker [8] |
| 62a | Producción Cementitious [21a] |
| 93 | Producción Clínker [8] |
| 97 | Producción Cementitious [21a] |

Fórmula:
```
Indicador_Nacional = Σ(Indicador_i × Ponderador_i) / Σ(Ponderador_i)
```

---

## Próximos Pasos

1. ✅ Crear script de extracción Pacasmayo
2. ✅ Crear script de extracción Yura
3. ✅ Extraer datos UNACEM con mdb-tools
4. ✅ Cargar datos en `peru_consolidado.db` (5,362 registros)
5. ✅ **Calcular agregados nacionales** (269 agregados, 2010-2030)
6. ✅ **Generar gráficos del reporte** (8 gráficos + reporte HTML)
7. ⏳ Validar contra datos oficiales del reporte PDF

---

## Contacto

Para dudas sobre este análisis, contactar a FICEM o ASOCEM.
