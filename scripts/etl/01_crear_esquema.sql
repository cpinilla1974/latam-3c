-- ============================================================
-- ESQUEMA DE CONSOLIDACIÓN DE DATOS - LATAM 3C
-- Base de datos: latam4c_db (PostgreSQL)
-- Fecha: 2025-12-03
-- ============================================================

-- Eliminar tablas existentes si es necesario (en orden inverso de dependencias)
DROP TABLE IF EXISTS fact_composicion_cemento CASCADE;
DROP TABLE IF EXISTS fact_distancias CASCADE;
DROP TABLE IF EXISTS fact_indicadores_producto CASCADE;
DROP TABLE IF EXISTS fact_indicadores_planta CASCADE;
DROP TABLE IF EXISTS ref_gnr_data CASCADE;
DROP TABLE IF EXISTS ref_data_global CASCADE;
DROP TABLE IF EXISTS dim_combustibles CASCADE;
DROP TABLE IF EXISTS dim_indicadores CASCADE;
DROP TABLE IF EXISTS dim_productos CASCADE;
DROP TABLE IF EXISTS dim_plantas CASCADE;
DROP TABLE IF EXISTS dim_empresas CASCADE;
DROP TABLE IF EXISTS dim_paises CASCADE;

-- ============================================================
-- DIMENSIONES (Catálogos)
-- ============================================================

-- Dimensión: Países
CREATE TABLE dim_paises (
    id_pais SERIAL PRIMARY KEY,
    codigo_iso3 VARCHAR(3) UNIQUE,
    codigo_iso2 VARCHAR(2),
    nombre VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dim_paises IS 'Catálogo de países LATAM';

-- Dimensión: Empresas
CREATE TABLE dim_empresas (
    id_empresa SERIAL PRIMARY KEY,
    codigo_origen VARCHAR(50),
    bd_origen VARCHAR(20),
    nombre VARCHAR(200) NOT NULL,
    grupo_empresarial VARCHAR(200),
    id_pais INTEGER REFERENCES dim_paises(id_pais),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE dim_empresas IS 'Catálogo de empresas cementeras';
CREATE INDEX idx_empresas_pais ON dim_empresas(id_pais);

-- Dimensión: Plantas
CREATE TABLE dim_plantas (
    id_planta SERIAL PRIMARY KEY,
    codigo_origen VARCHAR(50),
    bd_origen VARCHAR(20) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    tipo_planta VARCHAR(50),
    id_empresa INTEGER REFERENCES dim_empresas(id_empresa),
    id_pais INTEGER REFERENCES dim_paises(id_pais),
    latitud DECIMAL(10,7),
    longitud DECIMAL(10,7),
    capacidad_instalada DECIMAL(12,2),
    tipo_operacion VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),

    UNIQUE(bd_origen, codigo_origen)
);

COMMENT ON TABLE dim_plantas IS 'Catálogo unificado de plantas de todas las BDs';
CREATE INDEX idx_plantas_empresa ON dim_plantas(id_empresa);
CREATE INDEX idx_plantas_pais ON dim_plantas(id_pais);
CREATE INDEX idx_plantas_tipo ON dim_plantas(tipo_planta);
CREATE INDEX idx_plantas_bd ON dim_plantas(bd_origen);

-- Dimensión: Productos
CREATE TABLE dim_productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_origen VARCHAR(50),
    bd_origen VARCHAR(20),
    nombre VARCHAR(200) NOT NULL,
    tipo_producto VARCHAR(50),
    subtipo_producto VARCHAR(100),
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    activo BOOLEAN DEFAULT TRUE,

    UNIQUE(bd_origen, codigo_origen)
);

COMMENT ON TABLE dim_productos IS 'Catálogo de productos (cementos, clinker, etc.)';
CREATE INDEX idx_productos_planta ON dim_productos(id_planta);
CREATE INDEX idx_productos_tipo ON dim_productos(tipo_producto);

-- Dimensión: Indicadores
CREATE TABLE dim_indicadores (
    id_indicador SERIAL PRIMARY KEY,
    codigo_indicador VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(300),
    supergrupo VARCHAR(50),
    grupo VARCHAR(150),
    subgrupo VARCHAR(150),
    unidad VARCHAR(50),
    objeto VARCHAR(100),
    tipo_objeto VARCHAR(50),
    tipo_dato VARCHAR(20),
    descripcion TEXT,
    es_gcca BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dim_indicadores IS 'Catálogo de indicadores del protocolo GCCA y extensiones';
CREATE INDEX idx_indicadores_supergrupo ON dim_indicadores(supergrupo);
CREATE INDEX idx_indicadores_grupo ON dim_indicadores(grupo);

-- Dimensión: Combustibles
CREATE TABLE dim_combustibles (
    id_combustible SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE,
    nombre VARCHAR(200),
    categoria VARCHAR(50),
    tipo VARCHAR(50),
    poder_calorifico DECIMAL(10,4),
    factor_emision DECIMAL(10,4),
    pct_biomasa DECIMAL(6,4),
    ubicacion_horno VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dim_combustibles IS 'Catálogo de combustibles convencionales, alternativos y biomasa';

-- ============================================================
-- TABLAS DE HECHOS (Datos Transaccionales)
-- ============================================================

-- Fact: Indicadores por Planta
CREATE TABLE fact_indicadores_planta (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER NOT NULL REFERENCES dim_plantas(id_planta),
    id_indicador INTEGER NOT NULL REFERENCES dim_indicadores(id_indicador),
    fecha DATE NOT NULL,
    valor DECIMAL(18,6),
    temporalidad VARCHAR(20),
    escenario INTEGER DEFAULT 1,
    bd_origen VARCHAR(20),
    id_dataset_origen INTEGER,
    fecha_carga TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE fact_indicadores_planta IS 'Valores de indicadores por planta (cemento, clinker, etc.)';
CREATE INDEX idx_fip_planta ON fact_indicadores_planta(id_planta);
CREATE INDEX idx_fip_indicador ON fact_indicadores_planta(id_indicador);
CREATE INDEX idx_fip_fecha ON fact_indicadores_planta(fecha);
CREATE INDEX idx_fip_bd ON fact_indicadores_planta(bd_origen);
CREATE UNIQUE INDEX idx_fip_unique ON fact_indicadores_planta(id_planta, id_indicador, fecha, escenario);

-- Fact: Indicadores por Producto
CREATE TABLE fact_indicadores_producto (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    id_producto INTEGER NOT NULL REFERENCES dim_productos(id_producto),
    id_indicador INTEGER NOT NULL REFERENCES dim_indicadores(id_indicador),
    fecha DATE NOT NULL,
    valor DECIMAL(18,6),
    temporalidad VARCHAR(20),
    escenario INTEGER DEFAULT 1,
    bd_origen VARCHAR(20),
    id_dataset_origen INTEGER,
    fecha_carga TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE fact_indicadores_producto IS 'Valores de indicadores por producto (composición, etc.)';
CREATE INDEX idx_fipr_producto ON fact_indicadores_producto(id_producto);
CREATE INDEX idx_fipr_indicador ON fact_indicadores_producto(id_indicador);
CREATE INDEX idx_fipr_fecha ON fact_indicadores_producto(fecha);

-- Fact: Distancias Unificadas
CREATE TABLE fact_distancias (
    id SERIAL PRIMARY KEY,
    id_planta_origen INTEGER REFERENCES dim_plantas(id_planta),
    id_planta_destino INTEGER REFERENCES dim_plantas(id_planta),
    nombre_origen VARCHAR(200),
    nombre_destino VARCHAR(200),
    tipo_ruta VARCHAR(50),
    material VARCHAR(100),
    codigo_material VARCHAR(50),
    modo_transporte VARCHAR(50),
    distancia_km DECIMAL(10,2),
    lat_origen DECIMAL(10,7),
    lon_origen DECIMAL(10,7),
    lat_destino DECIMAL(10,7),
    lon_destino DECIMAL(10,7),
    factor_emision DECIMAL(10,6),
    kg_co2_tonelada DECIMAL(10,4),
    pais_origen VARCHAR(50),
    bd_origen VARCHAR(20),
    fuente VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE fact_distancias IS 'Distancias de transporte unificadas de todas las BDs';
CREATE INDEX idx_fd_origen ON fact_distancias(id_planta_origen);
CREATE INDEX idx_fd_destino ON fact_distancias(id_planta_destino);
CREATE INDEX idx_fd_tipo ON fact_distancias(tipo_ruta);
CREATE INDEX idx_fd_material ON fact_distancias(material);

-- Fact: Composición Cemento
CREATE TABLE fact_composicion_cemento (
    id SERIAL PRIMARY KEY,
    id_planta INTEGER REFERENCES dim_plantas(id_planta),
    nombre_planta VARCHAR(200),
    tipo_cemento VARCHAR(100),
    año INTEGER,
    mes INTEGER,
    factor_clinker DECIMAL(8,6),
    pct_yeso DECIMAL(8,6),
    pct_caliza DECIMAL(8,6),
    pct_puzolana DECIMAL(8,6),
    pct_escoria DECIMAL(8,6),
    pct_ceniza DECIMAL(8,6),
    pct_aditivo DECIMAL(8,6),
    factor_co2 DECIMAL(10,4),
    bd_origen VARCHAR(20),
    fecha_carga TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE fact_composicion_cemento IS 'Composición de tipos de cemento por planta';
CREATE INDEX idx_fcc_planta ON fact_composicion_cemento(id_planta);
CREATE INDEX idx_fcc_tipo ON fact_composicion_cemento(tipo_cemento);
CREATE INDEX idx_fcc_año ON fact_composicion_cemento(año);

-- ============================================================
-- TABLAS DE REFERENCIA (Benchmarks)
-- ============================================================

-- Referencia: GNR Data (Getting Numbers Right - GCCA)
CREATE TABLE ref_gnr_data (
    id SERIAL PRIMARY KEY,
    año INTEGER,
    region VARCHAR(100),
    pais VARCHAR(100),
    indicador VARCHAR(100),
    codigo_indicador VARCHAR(20),
    valor DECIMAL(18,6),
    unidad VARCHAR(50),
    percentil_10 DECIMAL(18,6),
    percentil_25 DECIMAL(18,6),
    percentil_50 DECIMAL(18,6),
    percentil_75 DECIMAL(18,6),
    percentil_90 DECIMAL(18,6),
    num_plantas INTEGER,
    fuente VARCHAR(100),
    fecha_carga TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE ref_gnr_data IS 'Datos de benchmark mundial GNR (GCCA)';
CREATE INDEX idx_gnr_año ON ref_gnr_data(año);
CREATE INDEX idx_gnr_region ON ref_gnr_data(region);
CREATE INDEX idx_gnr_indicador ON ref_gnr_data(codigo_indicador);

-- Referencia: Data Global
CREATE TABLE ref_data_global (
    id SERIAL PRIMARY KEY,
    año INTEGER,
    pais VARCHAR(100),
    region VARCHAR(100),
    indicador VARCHAR(200),
    codigo_indicador VARCHAR(50),
    valor DECIMAL(18,6),
    unidad VARCHAR(50),
    fuente VARCHAR(200),
    fecha_carga TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE ref_data_global IS 'Datos globales consolidados por país/región';
CREATE INDEX idx_dg_año ON ref_data_global(año);
CREATE INDEX idx_dg_pais ON ref_data_global(pais);

-- ============================================================
-- EXTENSIONES ÚTILES
-- ============================================================

-- Habilitar extensión para búsqueda difusa (si no existe)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- FUNCIONES AUXILIARES
-- ============================================================

-- Función para actualizar timestamp de modificación
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para dim_plantas
CREATE TRIGGER update_plantas_modtime
    BEFORE UPDATE ON dim_plantas
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ============================================================
-- DATOS INICIALES: Países LATAM
-- ============================================================

INSERT INTO dim_paises (codigo_iso3, codigo_iso2, nombre, region) VALUES
('MEX', 'MX', 'México', 'Norteamérica'),
('PER', 'PE', 'Perú', 'Sudamérica'),
('CHL', 'CL', 'Chile', 'Sudamérica'),
('COL', 'CO', 'Colombia', 'Sudamérica'),
('ARG', 'AR', 'Argentina', 'Sudamérica'),
('BRA', 'BR', 'Brasil', 'Sudamérica'),
('ECU', 'EC', 'Ecuador', 'Sudamérica'),
('VEN', 'VE', 'Venezuela', 'Sudamérica'),
('BOL', 'BO', 'Bolivia', 'Sudamérica'),
('PRY', 'PY', 'Paraguay', 'Sudamérica'),
('URY', 'UY', 'Uruguay', 'Sudamérica'),
('PAN', 'PA', 'Panamá', 'Centroamérica'),
('CRI', 'CR', 'Costa Rica', 'Centroamérica'),
('GTM', 'GT', 'Guatemala', 'Centroamérica'),
('HND', 'HN', 'Honduras', 'Centroamérica'),
('NIC', 'NI', 'Nicaragua', 'Centroamérica'),
('SLV', 'SV', 'El Salvador', 'Centroamérica'),
('DOM', 'DO', 'República Dominicana', 'Caribe'),
('CUB', 'CU', 'Cuba', 'Caribe'),
('JAM', 'JM', 'Jamaica', 'Caribe'),
('TTO', 'TT', 'Trinidad y Tobago', 'Caribe'),
('KOR', 'KR', 'Corea del Sur', 'Asia'),
('JPN', 'JP', 'Japón', 'Asia'),
('TUR', 'TR', 'Turquía', 'Europa'),
('ARE', 'AE', 'Emiratos Árabes Unidos', 'Medio Oriente'),
('DZA', 'DZ', 'Argelia', 'África'),
('VNM', 'VN', 'Vietnam', 'Asia'),
('USA', 'US', 'Estados Unidos', 'Norteamérica')
ON CONFLICT (codigo_iso3) DO NOTHING;

-- ============================================================
-- RESUMEN DE TABLAS CREADAS
-- ============================================================
/*
DIMENSIONES:
  - dim_paises: Catálogo de países (28 registros iniciales)
  - dim_empresas: Empresas cementeras
  - dim_plantas: Plantas unificadas de todas las BDs
  - dim_productos: Productos (cementos, clinker, etc.)
  - dim_indicadores: Indicadores GCCA y extensiones
  - dim_combustibles: Catálogo de combustibles

HECHOS:
  - fact_indicadores_planta: Datos por planta (~60,000 registros esperados)
  - fact_indicadores_producto: Datos por producto (~36,000 registros esperados)
  - fact_distancias: Rutas de transporte (~1,600 registros esperados)
  - fact_composicion_cemento: Composición de cementos (~1,100 registros esperados)

REFERENCIAS:
  - ref_gnr_data: Benchmark GNR (~17,700 registros)
  - ref_data_global: Datos globales (~69,600 registros)
*/
