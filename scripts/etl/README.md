# ETL: Consolidación de Datos LATAM 3C

## Objetivo
Migrar datos de 5 bases SQLite a PostgreSQL en estructura unificada (Star Schema) para análisis con IA.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     BASES ORIGEN (SQLite)                    │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│  PACAS   │   MZMA   │  MELON   │   YURA   │     FICEM      │
│  363MB   │   2GB    │  296MB   │   28MB   │     170MB      │
│  México  │  México  │  Chile   │   Perú   │   Benchmark    │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴───────┬────────┘
     │          │          │          │             │
     └──────────┴──────────┴──────────┴─────────────┘
                           │
                     ┌─────▼─────┐
                     │    ETL    │
                     │  Scripts  │
                     └─────┬─────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  PostgreSQL: latam4c_db                      │
├─────────────────┬───────────────────┬───────────────────────┤
│   DIMENSIONES   │      HECHOS       │      REFERENCIAS      │
├─────────────────┼───────────────────┼───────────────────────┤
│ dim_paises      │ fact_indicadores  │ ref_gnr_data          │
│ dim_empresas    │   _planta         │ ref_data_global       │
│ dim_plantas     │ fact_indicadores  │                       │
│ dim_productos   │   _producto       │                       │
│ dim_indicadores │ fact_distancias   │                       │
│ dim_combustibles│ fact_composicion  │                       │
└─────────────────┴───────────────────┴───────────────────────┘
```

## Estructura de Archivos

```
scripts/etl/
├── config.py                  # Configuración centralizada
├── 01_crear_esquema.sql       # DDL PostgreSQL
├── 02_migrar_dimensiones.py   # Migra dim_*
├── 03_migrar_indicadores.py   # Migra fact_indicadores_*
├── 04_migrar_distancias.py    # Migra fact_distancias
├── 05_crear_vistas.sql        # Vistas materializadas
├── 06_validar_datos.py        # Verificación integridad
├── 07_migrar_remitos_co2.py   # Migra remitos concreto con huella CO₂
├── README.md                  # Este archivo
└── output/
    ├── mapeos_dimension.json  # Mapeo IDs origen -> destino
    └── etl_log.txt            # Log de ejecución
```

## Ejecución

### Prerrequisitos
```bash
# Instalar dependencias
pip install psycopg2-binary pandas

# Crear base de datos PostgreSQL
createdb latam4c_db
```

### Pasos de Ejecución

```bash
# 1. Crear esquema
psql -d latam4c_db -f 01_crear_esquema.sql

# 2. Migrar dimensiones
python 02_migrar_dimensiones.py

# 3. Migrar indicadores
python 03_migrar_indicadores.py

# 4. Migrar distancias
python 04_migrar_distancias.py

# 5. Crear vistas materializadas
psql -d latam4c_db -f 05_crear_vistas.sql

# 6. Validar datos
python 06_validar_datos.py
```

### Ejecución Completa
```bash
./run_etl.sh  # Script que ejecuta todo en orden
```

## Configuración

Editar `config.py` para ajustar:
- Rutas de bases de datos SQLite
- Credenciales PostgreSQL
- Parámetros de mapeo

## Volumen de Datos

| Tabla | Registros |
|-------|-----------|
| dim_paises | 28 |
| dim_empresas | ~50 |
| dim_plantas | ~400 |
| dim_indicadores | ~1,400 |
| dim_combustibles | 86 |
| fact_indicadores_planta | ~60,000 |
| fact_indicadores_producto | ~36,000 |
| fact_distancias | ~1,600 |
| fact_composicion_cemento | ~1,100 |
| ref_gnr_data | ~17,700 |
| ref_data_global | ~69,600 |
| **TOTAL** | **~188,000** |

## Mapeo de IDs

El archivo `output/mapeos_dimension.json` contiene el mapeo entre IDs originales de cada base SQLite y los nuevos IDs en PostgreSQL.

Estructura:
```json
{
  "paises": {"MEX": 1, "PER": 2, ...},
  "plantas": {"('pacas', 1)": 101, ...},
  "indicadores": {"8": 1, "20": 2, ...}
}
```

## Repetir Migración

Para reiniciar desde cero:

```bash
# 1. Recrear esquema (elimina datos existentes)
psql -d latam4c_db -f 01_crear_esquema.sql

# 2. Ejecutar ETL completo
python 02_migrar_dimensiones.py
python 03_migrar_indicadores.py
python 04_migrar_distancias.py
psql -d latam4c_db -f 05_crear_vistas.sql
python 06_validar_datos.py
```

## Notas Importantes

1. **Distancias Yura**: No están en base de datos, están hardcodeadas en `config.py` (copiadas de `yura-2c/streamlit/services/const.py`)

2. **Base Melón**: Los datos están en `/databases/melon-3c/data/old/Melon_2.db`, no en la ubicación actual

3. **Mapeo de plantas**: Se usa combinación `(bd_origen, id_original)` como clave única para evitar colisiones entre bases

4. **Indicadores GCCA**: Códigos numéricos < 1000 son indicadores del protocolo GCCA

---

## 07_migrar_remitos_co2.py - Migración de Remitos de Concreto

### Objetivo
Migrar remitos de concreto con resistencia y huella CO₂ de 4 compañías a PostgreSQL.

### Bases de Datos Origen

| Compañía | País | Base de Datos | Registros |
|----------|------|---------------|-----------|
| MZMA (Cementos Moctezuma) | México | `/home/cpinilla/databases/mzma-3c/data/main.db` | 147,050 |
| Melón (Cementos Melón) | Chile | `/home/cpinilla/databases/melon-3c/data/old/main - copia.db` | 107,027 |
| PACAS (Cementos del Pacífico) | México | `/home/cpinilla/pacas-3c/data/main.db` | 99,250 |
| Lomax | Chile | `/home/cpinilla/projects/lomax-3c/streamlit/data/main.db` | 52,308 |
| **TOTAL** | | | **405,635** |

### Tablas Origen por Base

**PACAS:**
- `co2_remitos` → remitos con huella calculada
- `tb_atributos_concreto` → resistencia_mpa por producto

**MZMA:**
- `corp_concretos` → remitos de concreto
- `corp_co2` → huella CO₂ por remito (co2_kg_m3)
- `tb_atributos_concretos` → REST (resistencia en kg/cm², dividir por 10.2 para MPa)

**Melón:**
- `tb_remitos` → remitos
- `tb_producto` → productos de concreto
- `tb_planta` → plantas concreteras
- `tb_atributos_concretos` → REST por nombre_concreto
- `corp_co2` → huella CO₂ por remito

**Lomax:**
- `corp_concretos` → remitos de concreto
- `corp_co2` → huella CO₂ por remito (co2_kg_m3)
- `tb_atributos_concretos` → REST (ya en MPa, NO dividir)

### Tabla Destino PostgreSQL

```sql
CREATE TABLE remitos_co2 (
    id SERIAL PRIMARY KEY,
    id_remito TEXT,
    origen TEXT NOT NULL,        -- 'pacas', 'mzma', 'melon', 'lomax'
    empresa TEXT,
    pais TEXT,
    fecha DATE,
    planta TEXT,
    producto TEXT,
    resistencia_mpa REAL,
    volumen REAL,
    co2_kg_m3 REAL,
    emision_cemento REAL,
    emision_agregados REAL,
    emision_aditivos REAL,
    emision_total REAL,
    fecha_migracion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Ejecución

```bash
python 07_migrar_remitos_co2.py
```

### Estadísticas de Datos

| Origen | Registros | Avg Resistencia (MPa) | Avg CO₂ (kg/m³) |
|--------|-----------|----------------------|-----------------|
| mzma | 147,050 | 28.6 | 302.7 |
| melon | 107,027 | 25.7 | 244.8 |
| pacas | 99,250 | 22.6 | 188.6 |
| lomax | 52,308 | 30.3 | 286.3 |
