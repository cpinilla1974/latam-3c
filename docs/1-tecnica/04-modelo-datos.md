# Modelo de Datos - LATAM-3C

## Modelo Entidad-Relación

```
                    TB_EMPRESA
                   (empresa_uuid)
                         |
        +----------------+----------------+
        |                |                |
   TB_PLANTA        TB_PRODUCTO      TB_CARGA
   (id_planta)      (id_producto)    (id_carga)
                                          |
                                          |
                    TB_DATASET <----------+
                   (id_dataset)
                  [id_origen=empresa_uuid]
                  [id_carga=carga]
                         |
                     TB_DATA
                    (id_data)
                         |
                         v
                  TB_INDICADORES
                (codigo_indicador)
                [tabla de referencia]

                TB_CORRIDA_CALCULO
                   (id_corrida)
                [empresa_uuid=empresa]
```

## Relaciones Principales

```
EMPRESA (1) ──────────> (*) PLANTA
        │                    [plantas de la empresa]
        │
        ├──────────────> (*) PRODUCTO  
        │                    [productos específicos empresa]
        │
        ├──────────────> (*) CARGA
        │                    [archivos Excel cargados]
        │
        ├──────────────> (*) DATASET
        │                    [via id_origen cuando tipo=3]
        │
        └──────────────> (*) CORRIDA_CALCULO
                             [tracking de cálculos]

CARGA (1) ─────────────> (*) DATASET
                             [datasets generados por esta carga]

DATASET (1) ───────────> (*) DATA
                             [valores con indicadores]

DATA (*) ──────────────> (1) INDICADORES
                             [referencia a definición semántica]
```

## Estructura Base (Reutilizando Dataset-Data)

### 1. EMPRESAS
```sql
CREATE TABLE tb_empresa (
    empresa_uuid TEXT PRIMARY KEY,      -- UUID generado, no reversible
    pais TEXT NOT NULL,                 -- Colombia, México, Brasil, etc.
    fecha_registro DATE,                 -- Cuándo se registró
    codigo_acceso TEXT UNIQUE,          -- Hash para que puedan re-ingresar
    activa BOOLEAN DEFAULT 1
);
```

### 2. CARGAS DE ARCHIVOS
```sql
CREATE TABLE tb_carga (
    id_carga INTEGER PRIMARY KEY,
    empresa_uuid TEXT,
    periodo INTEGER,                     -- 2024, 2025, etc.
    fecha_carga TIMESTAMP,
    archivo_tipo TEXT,                   -- 'clinker_cemento' o 'concreto'
    archivo_nombre TEXT,
    estado TEXT,                         -- 'borrador', 'validado', 'aprobado'
    errores_json TEXT,                   -- Errores de validación en JSON
    usuario_carga TEXT,                  -- Email pseudonimizado
    FOREIGN KEY (empresa_uuid) REFERENCES tb_empresa(empresa_uuid)
);
```

### 3. DATASET (Adaptado para empresas)
```sql
CREATE TABLE tb_dataset (
    id_dataset INTEGER PRIMARY KEY,
    fecha TEXT,                          -- '2024-01-01' para año 2024
    id_tipo_origen INTEGER,              -- 3 = EMPRESA (nuevo)
    id_origen TEXT,                      -- empresa_uuid
    codigo_dataset TEXT,                 -- 'clinker_anual', 'cemento_tipo1', etc.
    id_rep_temp INTEGER DEFAULT 1,       -- 1 = Anual (siempre)
    id_escenario INTEGER DEFAULT 1,
    version INTEGER DEFAULT 1,           -- Para manejar re-cargas
    id_carga INTEGER,                    -- Referencia a la carga que lo generó
    FOREIGN KEY (id_origen) REFERENCES tb_empresa(empresa_uuid),
    FOREIGN KEY (id_carga) REFERENCES tb_carga(id_carga)
);
```

### 4. DATA (Sin cambios)
```sql
CREATE TABLE tb_data (
    id_data INTEGER PRIMARY KEY,
    id_dataset INTEGER,
    codigo_indicador TEXT,               -- Ref a tabla indicadores
    valor_indicador REAL,
    origen_dato INTEGER,                 -- 1=Excel crudo, 2=Calculado
    descripcion TEXT,
    marca_tiempo TIMESTAMP,
    FOREIGN KEY (id_dataset) REFERENCES tb_dataset(id_dataset),
    FOREIGN KEY (codigo_indicador) REFERENCES tb_indicadores(codigo_indicador)
);
```

### 5. INDICADORES
```sql
CREATE TABLE tb_indicadores (
    codigo_indicador TEXT PRIMARY KEY,   -- ID único (ej: '3010', 'L001')
    supergrupo TEXT,                     -- 'Clinker', 'Cemento', 'Concreto'
    grupo TEXT,                          -- 'Insumos', 'Emisiones', 'Transporte'
    subgrupo TEXT,                       -- Subcategoría específica
    nombre_indicador TEXT NOT NULL,      -- Descripción humana
    unidad TEXT,                         -- 't/año', 'kg CO2/ton', '%', 'km'
    objeto TEXT,                         -- 'caliza', 'clinker', 'diesel'
    tipo_objeto TEXT,                    -- 'minerales', 'combustibles'
    id_subtipo_producto INTEGER,         -- FK opcional a productos
    activo BOOLEAN DEFAULT 1
);
```

### 6. PRODUCTOS
```sql
CREATE TABLE tb_producto (
    id_producto INTEGER PRIMARY KEY,
    empresa_uuid TEXT,                   -- NULL para productos estándar
    tipo_producto TEXT,                  -- 'clinker', 'cemento', 'concreto'
    codigo_producto TEXT,                -- 'CPC_30R', 'CPO_40', 'f250'
    nombre_comercial TEXT,               -- Nombre que usa la empresa
    descripcion TEXT,
    resistencia_mpa REAL,               -- Resistencia en MPa
    resistencia_psi REAL,               -- Resistencia en PSI
    id_subtipo_producto INTEGER,         -- Para vincular con indicadores
    activo BOOLEAN DEFAULT 1,
    FOREIGN KEY (empresa_uuid) REFERENCES tb_empresa(empresa_uuid)
);
```

### 7. PLANTAS
```sql
CREATE TABLE tb_planta (
    id_planta INTEGER PRIMARY KEY,
    empresa_uuid TEXT NOT NULL,
    codigo_planta TEXT,                  -- 'P001', 'P002'
    nombre_planta TEXT,                  -- Para referencia interna
    ubicacion TEXT,                      -- 'Bogotá, Cundinamarca'
    coordenadas_lat REAL,               -- Latitud en formato decimal
    coordenadas_lng REAL,               -- Longitud en formato decimal
    tipo_planta TEXT,                    -- 'integrada', 'molienda', 'concreto'
    archivo_gcca TEXT,                   -- Referencia a protocolo GCCA
    activa BOOLEAN DEFAULT 1,
    FOREIGN KEY (empresa_uuid) REFERENCES tb_empresa(empresa_uuid),
    UNIQUE(empresa_uuid, codigo_planta)
);
```

### 8. CORRIDAS DE CÁLCULO
```sql
CREATE TABLE tb_corrida_calculo (
    id_corrida INTEGER PRIMARY KEY,
    empresa_uuid TEXT,
    periodo INTEGER,
    fecha_ejecucion TIMESTAMP,
    estado TEXT,                         -- 'en_proceso', 'completado', 'error'
    tipo_calculo TEXT,                   -- 'clinker', 'cemento', 'concreto', 'consolidado'
    parametros_json TEXT,                -- Parámetros usados en el cálculo
    log_json TEXT,                       -- Log de ejecución
    version_motor TEXT,                  -- Versión del motor de cálculo
    FOREIGN KEY (empresa_uuid) REFERENCES tb_empresa(empresa_uuid)
);
```

