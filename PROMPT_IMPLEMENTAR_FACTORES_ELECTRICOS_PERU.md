# PROMPT: Implementar Módulo de Factores de Emisión Eléctrica para Perú

## Contexto
Estás trabajando en el proyecto `latam-3c` (calculadora de CO2 para Perú). Necesitas implementar un módulo completo para gestionar factores históricos de emisión eléctrica del Sistema Eléctrico Interconectado Nacional (SEIN) de Perú, siguiendo el mismo patrón implementado exitosamente en el proyecto hermano `mzma-3c` (México).

## Objetivo
Implementar un sistema completo para:
1. Almacenar factores históricos de emisión eléctrica en la base de datos
2. Visualizar y gestionar estos factores mediante interfaz Streamlit
3. Permitir agregar/editar factores para nuevos años
4. Consultar factores programáticamente para uso en cálculos de CO2

## Arquitectura a Implementar

### Modelo de Datos: Planta → Producto → Dataset → Data

```
tb_planta (nueva: SEIN_PE)
  ├─ id_tipo_planta: 3 (Proveedor Externo)
  ├─ codigo_planta: "SEIN_PE"
  └─ planta: "SEIN - Sistema Eléctrico Interconectado Nacional"
      │
      └─ tb_producto (nuevo: Electricidad SEIN)
          ├─ codigo_producto: "ELEC_SEIN_PE"
          ├─ producto: "Electricidad - SEIN Perú"
          └─ id_subtipo_producto: 30 (Electricidad)
              │
              └─ tb_dataset (uno por año: 2010-2018)
                  ├─ fecha: "YYYY-01-01"
                  ├─ id_tipo_origen: 2 (Producto)
                  ├─ id_origen: [id_producto]
                  ├─ codigo_dataset: "DGEE_MINEM"
                  └─ id_rep_temp: 1 (Anual)
                      │
                      └─ tb_data (un registro por año)
                          ├─ codigo_indicador: "1137"
                          ├─ valor_indicador: [factor tCO2/MWh]
                          ├─ origen_dato: 1 (Entrada)
                          └─ descripcion: "Factor SEIN {año} - DGEE/MINEM"
```

## Datos de Entrada

### JSON con Factores Históricos
**Ubicación**: `/home/cpinilla/projects/latam-3c/data/factores-emision-sein-peru.json`

**Estructura** (ya existente):
```json
{
  "pais": "Perú",
  "sistema_electrico": "SEIN",
  "unidad": "tCO2/MWh",
  "fuente": "DGEE-MINEM",
  "factores_historicos": [
    {"año": 2010, "factor_tco2_mwh": 0.240},
    {"año": 2011, "factor_tco2_mwh": 0.230},
    {"año": 2012, "factor_tco2_mwh": 0.224},
    {"año": 2013, "factor_tco2_mwh": 0.209},
    {"año": 2014, "factor_tco2_mwh": 0.207},
    {"año": 2015, "factor_tco2_mwh": 0.203},
    {"año": 2016, "factor_tco2_mwh": 0.222},
    {"año": 2017, "factor_tco2_mwh": 0.184},
    {"año": 2018, "factor_tco2_mwh": 0.151}
  ]
}
```

## Archivos a Crear

### 1. Script de Inicialización
**Ubicación**: `scripts/inicializar_energia_electrica_peru.py`

**Función**: Crear estructura base y cargar datos históricos desde JSON

**Referencia del proyecto México**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/scripts/inicializar_energia_electrica.py`

**Tareas del script**:
- Verificar/crear subtipo_producto "Electricidad" (id=30)
- Verificar código indicador "1137" en tb_indicador
- Crear planta "SEIN_PE" si no existe
- Crear producto "ELEC_SEIN_PE" asociado a la planta
- Leer JSON de factores históricos
- Crear un dataset por cada año (2010-2018)
- Crear un registro tb_data por cada factor
- Reportar resumen de carga

**Adaptaciones necesarias**:
- Cambiar `REN_MX` → `SEIN_PE`
- Cambiar `ELEC_REN` → `ELEC_SEIN_PE`
- Cambiar `RENE_SEMARNAT` → `DGEE_MINEM`
- Adaptar ruta JSON a `/home/cpinilla/projects/latam-3c/data/factores-emision-sein-peru.json`
- Campo JSON: `factor_tco2_mwh` (no `factor`)

### 2. Página Streamlit de Gestión
**Ubicación**: `paginas/energia_electrica.py`

**Función**: Interfaz web para visualizar/editar factores

**Referencia del proyecto México**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/energia_electrica.py`

**Características**:
- **Sección 1**: Tabla de factores históricos ordenados por año (descendente)
- **Sección 2**: Gráfico de evolución temporal (línea con marcadores)
- **Sección 3**: Formulario para agregar nuevo factor (año + factor + notas)
- **Sección 4**: Formulario para editar factor existente (selector de año)
- **Expander final**: Información sobre fuente DGEE-MINEM

**Funciones principales**:
```python
def obtener_id_producto_electricidad(engine, schema)
def cargar_factores_historicos(engine, schema, id_producto)
def agregar_factor(engine, schema, id_producto, anio, factor, notas)
def actualizar_factor(engine, schema, id_dataset, nuevo_factor, nuevas_notas)
def crear_grafico_evolucion(df)
```

**Adaptaciones necesarias**:
- `CODIGO_PRODUCTO_ELECTRICO = "ELEC_SEIN_PE"`
- `CODIGO_INDICADOR_FACTOR = "1137"`
- Títulos: "SEIN" en lugar de "CFE/CENACE"
- URL información: MINEM Perú (https://www.gob.pe/minem)
- Fuente: "DGEE-MINEM" en lugar de "SEMARNAT/RENE"

### 3. Módulo Python de Consulta (Opcional pero recomendado)
**Ubicación**: `comunes_negocio/factores_emision_electrica.py`

**Función**: API programática para consultar factores desde calculadores

**Funciones principales**:
```python
def obtener_factor_emision_electrica(año: int) -> float:
    """
    Obtiene factor de emisión eléctrica para un año específico.

    Args:
        año: Año del factor (ej: 2018)

    Returns:
        Factor en tCO2/MWh

    Raises:
        ValueError si no existe factor para ese año
    """
```

## Configuración de Navegación

### Archivo `pages.toml` o similar
Agregar entrada en sección "HERRAMIENTAS":

```toml
[[pages]]
section = "HERRAMIENTAS"
path = "paginas/energia_electrica.py"
name = "Energía Eléctrica"
icon = "⚡"
```

## Verificación del Código Indicador

Antes de ejecutar el script, verificar que existe en `tb_indicador`:

```sql
SELECT codigo_indicador, nombre_indicador, unidad
FROM tb_indicador
WHERE codigo_indicador = '1137';
```

Si NO existe, crear:

```sql
INSERT INTO tb_indicador (
    codigo_indicador,
    nombre_indicador,
    unidad,
    supergrupo,
    grupo,
    subgrupo
) VALUES (
    '1137',
    'Factor de emisión eléctrica',
    'tCO2/MWh',
    'Energía',
    'Electricidad',
    'Factor de emisión'
);
```

## Orden de Implementación

### Paso 1: Verificación de Estructura
```bash
# Verificar que existe tb_subtipo_producto
SELECT * FROM tb_subtipo_producto WHERE id_subtipo_producto = 30;

# Verificar código indicador
SELECT * FROM tb_indicador WHERE codigo_indicador = '1137';

# Verificar id_tipo_planta=3 (Proveedor Externo)
SELECT * FROM tb_tipo_planta WHERE id_tipo_planta = 3;
```

### Paso 2: Crear Script de Inicialización
```bash
# Copiar y adaptar desde proyecto México
cp /home/cpinilla/projects/mzma-3c/streamlit_v3/scripts/inicializar_energia_electrica.py \
   /home/cpinilla/projects/latam-3c/scripts/inicializar_energia_electrica_peru.py

# Editar adaptaciones mencionadas arriba
```

### Paso 3: Ejecutar Script
```bash
cd /home/cpinilla/projects/latam-3c
python scripts/inicializar_energia_electrica_peru.py
```

**Salida esperada**:
```
✅ Subtipo producto 'Electricidad' (id=30) ya existe
✅ Creada planta 'SEIN' (id=X)
✅ Creado producto 'Electricidad - SEIN Perú' (id=Y)
✅ Año 2010: Factor 0.240 tCO2/MWh cargado
✅ Año 2011: Factor 0.230 tCO2/MWh cargado
...
📊 Resumen: 9 factores nuevos, 0 ya existentes
```

### Paso 4: Crear Página Streamlit
```bash
# Copiar y adaptar desde proyecto México
cp /home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/energia_electrica.py \
   /home/cpinilla/projects/latam-3c/paginas/energia_electrica.py

# Editar adaptaciones mencionadas arriba
```

### Paso 5: Agregar a Navegación
Editar archivo de configuración de páginas (pages.toml o similar)

### Paso 6: Verificación Final
```bash
# Iniciar aplicación Streamlit
streamlit run app.py

# Navegar a: HERRAMIENTAS → Energía Eléctrica
# Verificar que aparecen los 9 factores (2010-2018)
# Verificar gráfico de evolución temporal
# Probar agregar factor para año 2019 (ej: 0.140)
# Probar editar factor existente
```

## Validación de Datos Cargados

```sql
-- Verificar planta creada
SELECT * FROM tb_planta WHERE codigo_planta = 'SEIN_PE';

-- Verificar producto creado
SELECT * FROM tb_producto WHERE codigo_producto = 'ELEC_SEIN_PE';

-- Verificar datasets (debe haber 9: 2010-2018)
SELECT
    ds.id_dataset,
    ds.fecha,
    ds.codigo_dataset,
    d.valor_indicador as factor
FROM tb_dataset ds
JOIN tb_data d ON ds.id_dataset = d.id_dataset
WHERE d.codigo_indicador = '1137'
  AND ds.id_origen = (SELECT id_producto FROM tb_producto WHERE codigo_producto = 'ELEC_SEIN_PE')
ORDER BY ds.fecha;
```

**Resultado esperado**: 9 registros con factores desde 2010 hasta 2018

## Documentación de Referencia

### Archivos del Proyecto México (para copiar/adaptar):
1. **Script**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/scripts/inicializar_energia_electrica.py`
2. **Página Streamlit**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/energia_electrica.py`
3. **JSON factores**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/data/factores_emision_electrica_rene.json`
4. **Sesión completa**: `/home/cpinilla/projects/mzma-3c/sesion_2025-10-04.md`

### Diferencias México vs Perú

| Aspecto | México (MZMA) | Perú (LATAM) |
|---------|---------------|--------------|
| Sistema eléctrico | CFE/CENACE | SEIN |
| Código planta | REN_MX | SEIN_PE |
| Código producto | ELEC_REN | ELEC_SEIN_PE |
| Fuente de datos | SEMARNAT/RENE | DGEE-MINEM |
| código_dataset | RENE_SEMARNAT | DGEE_MINEM |
| Años disponibles | 2018-2024 (7 años) | 2010-2018 (9 años) |
| Rango de factores | 0.423 - 0.527 | 0.151 - 0.240 |
| Campo JSON factor | `factor` | `factor_tco2_mwh` |
| URL información | gob.mx/semarnat | gob.pe/minem |

## Notas Importantes

1. **Código indicador 1137**: Debe existir en `tb_indicador` antes de ejecutar el script
2. **Subtipo producto 30**: Debe existir como "Electricidad" en `tb_subtipo_producto`
3. **id_tipo_planta=3**: Debe ser "Proveedor Externo" en `tb_tipo_planta`
4. **Unidad consistente**: Siempre tCO2/MWh (no kg, no g)
5. **Origen dato = 1**: Significa "Entrada" (no calculado)
6. **id_rep_temp = 1**: Significa "Anual"
7. **id_escenario = 1**: Escenario base/real

## Uso Posterior en Calculadores

Una vez implementado, en los calculadores de CO2 se podrá consultar:

```python
from comunes_negocio.factores_emision_electrica import obtener_factor_emision_electrica

# En cálculo de alcance A3 - Electricidad
año_calculo = 2018
consumo_electrico_mwh = 1500.5

factor_emision = obtener_factor_emision_electrica(año_calculo)  # 0.151 tCO2/MWh
emision_co2_toneladas = consumo_electrico_mwh * factor_emision  # 226.58 t CO2

# Guardar en tb_data con codigo_indicador apropiado para "Emisión A3 Electricidad"
```

## Resultado Final Esperado

Al completar esta implementación, el sistema tendrá:

✅ Base de datos poblada con 9 factores históricos (2010-2018)
✅ Página web para visualizar factores históricos
✅ Gráfico interactivo de evolución temporal
✅ Capacidad de agregar factores para nuevos años
✅ Capacidad de editar factores existentes
✅ API programática para consultar factores desde calculadores
✅ Documentación clara de fuente de datos (DGEE-MINEM)
✅ Trazabilidad completa usando modelo data-dataset

---

## Pregunta de Validación

Una vez implementado, ejecutar esta validación:

```sql
-- Debe retornar 9 registros
SELECT
    EXTRACT(YEAR FROM ds.fecha) as año,
    d.valor_indicador as factor_tco2_mwh,
    pr.producto,
    pl.planta
FROM tb_data d
JOIN tb_dataset ds ON d.id_dataset = ds.id_dataset
JOIN tb_producto pr ON ds.id_origen = pr.id_producto
JOIN tb_planta pl ON pr.id_planta = pl.id_planta
WHERE d.codigo_indicador = '1137'
  AND pl.codigo_planta = 'SEIN_PE'
ORDER BY año;
```

**Resultado esperado**: 9 filas, años 2010-2018, factores descendentes desde 0.240 hasta 0.151

---

## Comandos Rápidos

```bash
# Navegar al proyecto
cd /home/cpinilla/projects/latam-3c

# Ejecutar script de inicialización
python scripts/inicializar_energia_electrica_peru.py

# Iniciar aplicación
streamlit run app.py

# Verificar logs
tail -f logs/app.log
```

---

## Fin del Prompt

¿Alguna duda sobre la implementación? Puedes consultar directamente los archivos de referencia en el proyecto México listados arriba.
