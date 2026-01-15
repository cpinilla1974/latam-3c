# Plan de Consolidación de Datos - LATAM 3C

## Objetivo
Consolidar datos de 5 bases SQLite en una estructura PostgreSQL unificada que permita análisis profundo potenciado con IA.

---

## 1. Arquitectura Propuesta

### 1.1 Esquema de Base de Datos Unificada

```
latam4c_db (PostgreSQL)
│
├── DIMENSIONES (Catálogos)
│   ├── dim_paises
│   ├── dim_empresas
│   ├── dim_plantas
│   ├── dim_productos
│   ├── dim_indicadores
│   ├── dim_combustibles
│   └── dim_modos_transporte
│
├── HECHOS (Datos Transaccionales)
│   ├── fact_indicadores_planta    ← tb_dataset + tb_data consolidado
│   ├── fact_indicadores_producto  ← tb_dataset + tb_data consolidado
│   ├── fact_remitos_concreto      ← tb_remitos consolidado
│   ├── fact_composicion_cemento   ← cementos_bruto + cementos
│   └── fact_distancias            ← distancias unificadas
│
├── BENCHMARKS (Referencias)
│   ├── ref_gcca_benchmarks        ← existente
│   ├── ref_gnr_data               ← gnr_data de ficem_bd
│   └── ref_data_global            ← data_global de ficem_bd
│
└── ANÁLISIS (Vistas Materializadas)
    ├── mv_kpi_plantas_mensual
    ├── mv_kpi_plantas_anual
    ├── mv_benchmark_comparativo
    └── mv_tendencias_co2
```

### 1.2 Modelo Dimensional (Star Schema)

```
                    ┌─────────────────┐
                    │  dim_indicadores │
                    └────────┬────────┘
                             │
┌──────────────┐    ┌────────┴────────┐    ┌─────────────┐
│  dim_plantas  │────│ fact_indicadores │────│  dim_tiempo  │
└──────────────┘    └────────┬────────┘    └─────────────┘
                             │
                    ┌────────┴────────┐
                    │  dim_productos   │
                    └─────────────────┘
```

---

## 2. Estructura de Tablas

### 2.1 Dimensión: Plantas

```sql
CREATE TABLE dim_plantas (
    id_planta SERIAL PRIMARY KEY,
    codigo_origen VARCHAR(50),      -- ID original de la BD fuente
    bd_origen VARCHAR(20),          -- pacas, mzma, melon, yura, ficem
    nombre VARCHAR(200),
    tipo_planta VARCHAR(50),        -- cemento, concreto, agregados, etc.
    id_empresa INTEGER REFERENCES dim_empresas(id_empresa),
    id_pais INTEGER REFERENCES dim_paises(id_pais),
    latitud DECIMAL(10,7),
    longitud DECIMAL(10,7),
    capacidad_instalada DECIMAL(12,2),
    tipo_operacion VARCHAR(50),     -- integrated, grinding
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Dimensión: Indicadores

```sql
CREATE TABLE dim_indicadores (
    id_indicador SERIAL PRIMARY KEY,
    codigo_indicador VARCHAR(20) UNIQUE,
    nombre VARCHAR(200),
    supergrupo VARCHAR(50),         -- Cemento, Clinker, Concreto, etc.
    grupo VARCHAR(100),
    subgrupo VARCHAR(100),
    unidad VARCHAR(50),
    tipo_dato VARCHAR(20),          -- entrada, calculado
    descripcion TEXT,
    es_gcca BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);
```

### 2.3 Fact: Indicadores por Planta

```sql
CREATE TABLE fact_indicadores_planta (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    id_indicador INTEGER REFERENCES dim_indicadores(id_indicador),
    fecha DATE,
    valor DECIMAL(18,6),
    temporalidad VARCHAR(20),       -- anual, mensual, evento
    escenario INTEGER DEFAULT 1,
    bd_origen VARCHAR(20),
    id_dataset_origen INTEGER,      -- referencia al dataset original
    fecha_carga TIMESTAMP DEFAULT NOW(),

    -- Índices para consultas rápidas
    UNIQUE(id_planta, id_indicador, fecha, escenario)
);

CREATE INDEX idx_fact_ind_planta_fecha ON fact_indicadores_planta(fecha);
CREATE INDEX idx_fact_ind_planta_indicador ON fact_indicadores_planta(id_indicador);
```

### 2.4 Fact: Indicadores por Producto

```sql
CREATE TABLE fact_indicadores_producto (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    id_producto INTEGER REFERENCES dim_productos(id_producto),
    id_indicador INTEGER REFERENCES dim_indicadores(id_indicador),
    fecha DATE,
    valor DECIMAL(18,6),
    temporalidad VARCHAR(20),
    escenario INTEGER DEFAULT 1,
    bd_origen VARCHAR(20),
    id_dataset_origen INTEGER,
    fecha_carga TIMESTAMP DEFAULT NOW()
);
```

### 2.5 Fact: Distancias Unificadas

```sql
CREATE TABLE fact_distancias (
    id SERIAL PRIMARY KEY,
    id_planta_origen INTEGER REFERENCES dim_plantas(id_planta),
    id_planta_destino INTEGER REFERENCES dim_plantas(id_planta),
    tipo_ruta VARCHAR(50),          -- insumo, despacho
    material VARCHAR(100),          -- caliza, cemento, clinker, etc.
    modo_transporte VARCHAR(50),    -- camion, barco, tren
    distancia_km DECIMAL(10,2),
    factor_emision DECIMAL(10,6),   -- kg CO2/t.km
    kg_co2_tonelada DECIMAL(10,4),  -- precalculado
    pais_origen VARCHAR(50),
    bd_origen VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);
```

### 2.6 Fact: Composición Cemento

```sql
CREATE TABLE fact_composicion_cemento (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    tipo_cemento VARCHAR(100),
    año INTEGER,
    mes INTEGER,
    -- Composición (%)
    factor_clinker DECIMAL(6,4),
    pct_yeso DECIMAL(6,4),
    pct_caliza DECIMAL(6,4),
    pct_puzolana DECIMAL(6,4),
    pct_escoria DECIMAL(6,4),
    pct_ceniza DECIMAL(6,4),
    -- Emisiones
    factor_co2 DECIMAL(10,4),       -- kg CO2/t cemento
    bd_origen VARCHAR(20),
    fecha_carga TIMESTAMP DEFAULT NOW()
);
```

---

## 3. Proceso de Migración (ETL)

### 3.1 Fase 1: Dimensiones (Catálogos)

1. **dim_paises**: Cargar desde plantas_latam (ficem_bd)
2. **dim_empresas**: Extraer de plantas_latam + tb_planta de cada BD
3. **dim_plantas**: Unificar tb_planta de las 4 BDs + plantas_latam
4. **dim_indicadores**: Cargar desde indicadores.db (comun)
5. **dim_combustibles**: Cargar tabla combustibles (compartida)

### 3.2 Fase 2: Hechos (Datos)

1. **fact_indicadores_planta**:
   - Extraer de pacas, mzma, melon, yura donde id_tipo_origen = 1
   - ~2,800 datasets → ~60,000 registros

2. **fact_indicadores_producto**:
   - Extraer donde id_tipo_origen = 2
   - ~1,250 datasets → ~36,000 registros

3. **fact_distancias**:
   - Pacas: tb_distancias_plantas (186)
   - MZMA: tb_distancias_rutas (674)
   - Melon: tb_distancias_rutas (648)
   - Yura: DISTANCIAS_DEFAULT hardcodeado (~20)

4. **fact_composicion_cemento**:
   - Yura: cementos_bruto (927)
   - FICEM: cementos (139)

### 3.3 Fase 3: Benchmarks

1. **ref_gnr_data**: Copiar gnr_data de ficem_bd (17,722)
2. **ref_data_global**: Copiar data_global de ficem_bd (69,583)

---

## 4. Vistas Materializadas para Análisis IA

### 4.1 Vista: KPIs por Planta Anual

```sql
CREATE MATERIALIZED VIEW mv_kpi_plantas_anual AS
SELECT
    p.nombre as planta,
    e.nombre as empresa,
    pa.nombre as pais,
    EXTRACT(YEAR FROM f.fecha) as año,
    -- Producción
    MAX(CASE WHEN i.codigo_indicador = '8' THEN f.valor END) as clinker_producido_t,
    MAX(CASE WHEN i.codigo_indicador = '20' THEN f.valor END) as cemento_producido_t,
    -- Factor clinker
    MAX(CASE WHEN i.codigo_indicador = '92a' THEN f.valor END) as factor_clinker,
    -- Energía
    MAX(CASE WHEN i.codigo_indicador = '93' THEN f.valor END) as consumo_termico_mj_t,
    MAX(CASE WHEN i.codigo_indicador = '33' THEN f.valor END) as consumo_electrico_mwh,
    -- Emisiones
    MAX(CASE WHEN i.codigo_indicador = '73' THEN f.valor END) as emision_especifica_clinker,
    MAX(CASE WHEN i.codigo_indicador = '60' THEN f.valor END) as emision_bruta_clinker,
    -- Conteos
    COUNT(DISTINCT i.codigo_indicador) as indicadores_disponibles
FROM fact_indicadores_planta f
JOIN dim_plantas p ON f.id_planta = p.id_planta
JOIN dim_empresas e ON p.id_empresa = e.id_empresa
JOIN dim_paises pa ON p.id_pais = pa.id_pais
JOIN dim_indicadores i ON f.id_indicador = i.id_indicador
WHERE p.tipo_planta = 'cemento'
GROUP BY p.nombre, e.nombre, pa.nombre, EXTRACT(YEAR FROM f.fecha);
```

### 4.2 Vista: Benchmark Comparativo

```sql
CREATE MATERIALIZED VIEW mv_benchmark_comparativo AS
SELECT
    p.nombre as planta,
    pa.nombre as pais,
    f.año,
    f.factor_clinker,
    f.consumo_termico_mj_t,
    f.emision_especifica_clinker,
    -- Comparación con GCCA
    g.valor_referencia as gcca_referencia,
    g.percentil_25,
    g.percentil_50,
    g.percentil_75,
    -- Posición relativa
    CASE
        WHEN f.emision_especifica_clinker <= g.percentil_25 THEN 'A (Top 25%)'
        WHEN f.emision_especifica_clinker <= g.percentil_50 THEN 'B (25-50%)'
        WHEN f.emision_especifica_clinker <= g.percentil_75 THEN 'C (50-75%)'
        ELSE 'D (Bottom 25%)'
    END as clasificacion_gcca
FROM mv_kpi_plantas_anual f
JOIN dim_paises pa ON f.pais = pa.nombre
LEFT JOIN ref_gnr_data g ON g.indicador = 'emision_especifica_clinker'
    AND g.region = 'LATAM';
```

---

## 5. Capacidades de Análisis IA

### 5.1 Queries que la IA podrá ejecutar

```sql
-- 1. Análisis de tendencias por planta
SELECT planta, año, factor_clinker,
       LAG(factor_clinker) OVER (PARTITION BY planta ORDER BY año) as año_anterior,
       factor_clinker - LAG(factor_clinker) OVER (PARTITION BY planta ORDER BY año) as variacion
FROM mv_kpi_plantas_anual;

-- 2. Ranking de eficiencia por país
SELECT pais, planta, año, emision_especifica_clinker,
       RANK() OVER (PARTITION BY pais ORDER BY emision_especifica_clinker) as ranking
FROM mv_kpi_plantas_anual
WHERE año = 2024;

-- 3. Correlaciones entre variables
SELECT
    CORR(factor_clinker, emision_especifica_clinker) as corr_factor_emision,
    CORR(consumo_termico_mj_t, emision_especifica_clinker) as corr_termico_emision,
    CORR(consumo_electrico_mwh, emision_especifica_clinker) as corr_electrico_emision
FROM mv_kpi_plantas_anual;

-- 4. Análisis de gaps con benchmark
SELECT planta, año,
       emision_especifica_clinker - gcca_referencia as gap_vs_benchmark,
       (emision_especifica_clinker - gcca_referencia) / gcca_referencia * 100 as pct_gap
FROM mv_benchmark_comparativo;
```

### 5.2 Análisis Avanzados Posibles

1. **Clustering de plantas** por perfil de eficiencia
2. **Detección de anomalías** en datos reportados
3. **Predicción de emisiones** basada en insumos
4. **Análisis de escenarios** (what-if)
5. **Identificación de mejores prácticas** entre plantas
6. **Benchmarking dinámico** por región/tecnología

---

## 6. Estimación de Volumen Final

| Tabla | Registros Estimados |
|-------|---------------------|
| dim_plantas | ~400 |
| dim_indicadores | ~1,400 |
| dim_empresas | ~50 |
| fact_indicadores_planta | ~60,000 |
| fact_indicadores_producto | ~36,000 |
| fact_distancias | ~1,600 |
| fact_composicion_cemento | ~1,100 |
| ref_gnr_data | ~17,700 |
| ref_data_global | ~69,600 |
| **TOTAL** | **~188,000** |

---

## 7. Implementación

### 7.1 Scripts a Crear

1. `scripts/etl/01_crear_esquema.sql` - DDL completo
2. `scripts/etl/02_migrar_dimensiones.py` - Carga de catálogos
3. `scripts/etl/03_migrar_indicadores.py` - Carga de facts
4. `scripts/etl/04_migrar_distancias.py` - Unificación distancias
5. `scripts/etl/05_crear_vistas.sql` - Vistas materializadas
6. `scripts/etl/06_validar_datos.py` - Verificación de integridad

### 7.2 Dependencias

- Python: psycopg2, pandas, sqlite3
- PostgreSQL: pg_trgm (búsqueda difusa)

---

## 8. Próximos Pasos

1. ✅ **Diseñar esquema** (este documento)
2. ⬜ **Crear tablas** en PostgreSQL
3. ⬜ **Desarrollar ETL** de dimensiones
4. ⬜ **Desarrollar ETL** de hechos
5. ⬜ **Crear vistas** materializadas
6. ⬜ **Validar datos** migrados
7. ⬜ **Integrar con IA** para análisis
