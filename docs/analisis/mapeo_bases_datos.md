# Mapeo Completo de Bases de Datos - LATAM 3C

## Resumen Ejecutivo

Se identificaron **5 bases de datos principales** con datos relevantes para análisis de huella de carbono en la industria cementera.

| Base de Datos | Ubicación | Tamaño | Entidad | Foco Principal |
|---------------|-----------|--------|---------|----------------|
| **pacas-3c** | /home/cpinilla/pacas-3c/data/main.db | 363 MB | Pacasmayo (Perú) | Cemento + Concreto |
| **mzma-3c** | /home/cpinilla/databases/mzma-3c/data/main.db | 2 GB | Moctezuma (México) | Cemento + Concreto |
| **melon-3c** | /home/cpinilla/databases/melon-3c/data/old/Melon_2.db | 296 MB | Melón (Chile) | Cemento + Concreto |
| **yura-2c** | /home/cpinilla/databases/yura-2c/data/main.db | 28 MB | Yura (Perú) | Cemento + Clinker |
| **ficem_bd** | /home/cpinilla/databases/ficem_bd/data/ficem_bd.db | 170 MB | LATAM Regional | Benchmarking + GNR |

---

## 1. PACAS-3C (Pacasmayo, Perú)

### Volumen de Datos
| Tabla | Registros |
|-------|-----------|
| tb_dataset | 2,166 |
| tb_data | 56,925 |
| tb_planta | 59 |
| tb_remitos | 113,058 |

### Plantas de Cemento
| Planta | ID | Tipo |
|--------|-----|------|
| Pacasmayo | 5203 | Cemento |
| Piura | 5204 | Cemento |
| Rioja | 5205 | Cemento |
| Cementos Pacasmayo | 5621 | Cemento |
| Consolidado | 128802 | Cemento |

### Plantas Clinker (Importación)
- Clinker ARGELIA (5578)
- Clinker COREA (5571)
- Clinker ECUADOR (5577)
- Clinker JAPON (5580)
- Clinker VIETNAM (5576)
- Clinker YURA (5574)

### Plantas de Concreto
Cajamarca, Chiclayo, Chimbote, Moche, Piura, Tarapoto, Trujillo

### Distribución Temporal
| Año | Datasets | Registros Data |
|-----|----------|----------------|
| 2020 | 121 | 3,123 |
| 2021 | 145 | 3,826 |
| 2022 | 143 | 2,646 |
| 2023 | 249 | 14,718 |
| 2024 | 261 | 15,366 |
| 2025 | 124 | 2,643 |

### Indicadores Más Frecuentes
| Código | Indicador | Registros |
|--------|-----------|-----------|
| 11 | Clinker consumido | 1,349 |
| 13 | Caliza | 1,013 |
| 12 | Yeso | 967 |
| 16 | Puzolana | 766 |
| 92a | Factor clinker | 703 |
| 14 | Escoria | 552 |
| 8 | Clinker producido | 324 |
| 73 | Específica neta clinker | 324 |
| 60 | Específica bruta clinker | 324 |

---

## 2. MZMA-3C (Moctezuma, México)

### Volumen de Datos
| Tabla | Registros |
|-------|-----------|
| tb_dataset | 1,226 |
| tb_data | 31,205 |
| tb_planta | 98 |

### Plantas de Cemento
| Planta | ID | Tipo |
|--------|-----|------|
| Tepetzingo | 1 | Cemento |
| Apazapan | 2 | Cemento |
| Cerritos | 3 | Cemento |

### Materias Primas por Planta
Cada planta de cemento tiene asociadas:
- Canteras de caliza
- Fuentes de arcilla
- Fuentes de puzolana
- Yeso
- Zeolita
- Mineral de fierro

### Distribución Temporal
| Año | Datasets | Registros Data |
|-----|----------|----------------|
| 2020 | 212 | 2,759 |
| 2021 | 151 | 2,368 |
| 2022 | 160 | 7,404 |
| 2023 | 253 | 8,944 |
| 2024 | 227 | 8,462 |
| 2025 | 27 | 1,267 |

### Indicadores Más Frecuentes
| Código | Indicador | Registros |
|--------|-----------|-----------|
| 92a | Factor clinker | 732 |
| 8 | Clinker producido | 369 |
| 3011 | Arcilla | 348 |
| 1005 | (Producción) | 219 |
| 3010 | Caliza | 210 |
| 3012 | Óxido de hierro | 196 |

---

## 3. MELON-3C (Melón, Chile)

### Ubicación de Datos
**Base principal**: `/home/cpinilla/databases/melon-3c/data/old/Melon_2.db` (296 MB)

### Volumen de Datos
| Tabla | Registros |
|-------|-----------|
| tb_dataset | 381 |
| tb_data | 4,549 |
| tb_planta | 61 |
| tb_remitos | 236,179 |
| corp_concretos | 124,685 |

### Plantas de Cemento
| Planta | ID | Tipo |
|--------|-----|------|
| Ssangyong | 1 | Cemento |
| Unacem Atocongo | 2 | Cemento |
| Halla | 3 | Cemento |
| La Calera | 4 | Cemento |
| Ventanas | 5 | Cemento |
| Cemento Puerto Montt | 6 | Cemento |
| Punta Arenas | 7 | Cemento |
| Unacem RM | 8 | Cemento |
| CEMENTO POLPAICO S.A. | 9 | Cemento |
| CEMENTOS BICENTENARIO S.A. | 10 | Cemento |

### Plantas de Concreto
Lo Espejo 1-3, San Martin 1-4, Maipu, Concon, La Serena 1-2, Puerto Montt

### Plantas de Áridos
17 plantas de áridos y canteras asociadas

### Distribución Temporal
| Año | Datasets |
|-----|----------|
| 2023 | 351 |
| 2024 | 25 |

### Indicadores Más Frecuentes
| Código | Indicador | Registros |
|--------|-----------|-----------|
| 1147 | (Energía) | 142 |
| 1146 | (Energía) | 142 |
| 1134 | Consumo eléctrico específico | 142 |
| 92a | Factor clinker | 130 |
| 1005 | (Producción) | 95 |

---

## 4. YURA-2C (Yura, Perú)

### Ubicación de Datos
**Base principal**: `/home/cpinilla/databases/yura-2c/data/main.db` (28 MB)

### Volumen de Datos
| Tabla | Registros |
|-------|-----------|
| tb_dataset | 274 |
| tb_data | 3,507 |
| tb_planta | 6 |
| cementos_bruto | 927 |

### Plantas
| Planta | ID | Tipo |
|--------|-----|------|
| Yura | 1 | Cemento |
| Cantera Yura | 2 | Cantera |
| Mina Puno | 3 | Mina |
| Proveedor Turquía | 4 | Clinker importado |
| Puerto de Pohang | 5 | Clinker importado |
| Puerto de Fukuyama | 6 | Clinker importado |

### Tipos de Cemento (cementos_bruto)
| Tipo Cemento | Registros |
|--------------|-----------|
| Cemento Tipo IP | 368 |
| Cemento Tipo HE | 337 |
| Cemento Tipo I | 222 |

### Distribución Temporal
| Año | Datasets |
|-----|----------|
| 2020 | 47 |
| 2021 | 57 |
| 2022 | 64 |
| 2023 | 51 |
| 2024 | 49 |

### Indicadores Más Frecuentes
| Código | Indicador | Registros |
|--------|-----------|-----------|
| 11 | Clinker consumido | 552 |
| 12 | Yeso | 241 |
| 3289 | (Específico Yura) | 170 |
| 102 | (Producción) | 130 |
| 3012 | Óxido de hierro | 125 |
| 16 | Puzolana | 125 |
| 8 | Clinker producido | 80 |
| 3010 | Caliza | 80 |
| 3011 | Arcilla | 72 |

---

## 5. FICEM_BD (Regional LATAM)

### Volumen de Datos
| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| remitos_concretos | 255,328 | Transacciones de concreto |
| data_global | 69,583 | Datos consolidados globales |
| gnr_data | 17,722 | Datos del Getting Numbers Right |
| plantas_latam | 265 | Plantas cementeras LATAM |
| cementos | 139 | Tipos de cemento por planta |
| huella_concretos | 260 | Huella de carbono consolidada |

### Tabla: plantas_latam
Contiene 265 plantas cementeras de toda Latinoamérica con:
- Nombre y ubicación geográfica (lat/long)
- Empresa propietaria y grupo
- País (ISO)
- Capacidad instalada
- Tipo (Integrated/Grinding)

### Tabla: cementos
139 registros con tipos de cemento por planta y año:
```
empresa | planta | tipo_cemento | año | factor_co2
mzma    | Apazapan | CPC 40    | 2022 | 867
mzma    | Apazapan | CPC30R    | 2022 | 712
```

### Tabla: gnr_data
17,722 registros del Getting Numbers Right (GCCA) - benchmark mundial.

### Tabla: data_global
69,583 registros de datos consolidados por país/región.

---

## 6. Modelo de Datos: Dataset-Data

### Estructura tb_dataset
```sql
id_dataset      -- Identificador único
fecha           -- Fecha del dataset
id_tipo_origen  -- 1=Planta, 2=Producto
id_origen       -- ID de planta o producto
codigo_dataset  -- Descripción del método/origen
id_rep_temp     -- 1=Anual, 2=Mensual, 3=Evento
id_escenario    -- Escenario de cálculo
```

### Estructura tb_data
```sql
id_data           -- Identificador único
id_dataset        -- FK a tb_dataset
codigo_indicador  -- Código del indicador (ej: "8", "92a")
valor_indicador   -- Valor numérico
id_producto_ext   -- Producto relacionado (opcional)
origen_dato       -- 1=Entrada, 2=Calculado
descripcion       -- Descripción del dato
marca_tiempo      -- Timestamp
```

### Distribución por Tipo de Origen
| Base | Tipo 1 (Planta) | Tipo 2 (Producto) |
|------|-----------------|-------------------|
| pacas-3c | 271 datasets | 1,895 datasets |
| mzma-3c | 373 datasets | 853 datasets |
| melon-3c | (por verificar) | (por verificar) |
| yura-2c | (por verificar) | (por verificar) |

---

## 7. Indicadores Clave (Catálogo Común)

### Indicadores de Cemento
| Código | Nombre | Supergrupo |
|--------|--------|------------|
| 8 | Clinker producido | Cemento |
| 11 | Clinker consumido | Cemento |
| 12 | Yeso | Cemento |
| 13 | Caliza | Cemento |
| 14 | Escoria | Cemento |
| 16 | Puzolana | Cemento |
| 92a | Factor clinker | Cemento |

### Indicadores de Clinker
| Código | Nombre | Supergrupo |
|--------|--------|------------|
| 3010 | Caliza | Clinker |
| 3011 | Arcilla | Clinker |
| 3012 | Óxido de hierro | Clinker |

### Indicadores de Emisiones
| Código | Nombre | Supergrupo |
|--------|--------|------------|
| 60 | Específica bruta clinker | Minerales |
| 60a | Descarbonatación clinker | Minerales |
| 60b | Específica bruta combustibles clinker | Minerales |
| 73 | Específica neta clinker | Minerales |

---

## 8. Datos de Energía por Base de Datos

### Indicadores de Energía Eléctrica - Cemento
| Código | Nombre | Unidad |
|--------|--------|--------|
| 33 | Consumo eléctrico total | MWh/año |
| 33a | Producción eléctrica on-site | MWh/año |
| 33b | Producción eléctrica recuperación calor | MWh/año |
| 33c | Consumo eléctrico externo | MWh/año |
| 33d | Factor emisión red eléctrica | Kg CO2/MWh |
| 33e | Consumo eléctrico hasta clinker | MWh/año |

### Indicadores de Energía Eléctrica - Concreto
| Código | Nombre | Unidad |
|--------|--------|--------|
| 1090 | Consumo eléctrico total | kWh |
| 1134 | Consumo eléctrico específico | kWh/m3 |

### Indicadores de Energía Térmica
| Código | Nombre | Unidad |
|--------|--------|--------|
| 30 | Equipment and on-site vehicles | TJ/año |
| 32 | Total non-kiln fuel consumption | TJ/año |
| 93 | Consumo térmico | MJ/t clinker |

### Disponibilidad de Datos de Energía

| Base | Eléctrico Cemento (33*) | Eléctrico Concreto (1090,1134) | Térmico (30,32,93) |
|------|------------------------|-------------------------------|-------------------|
| **pacas-3c** | 193-211 registros | 19 registros | 193+185 registros |
| **mzma-3c** | 183 registros | 145 registros | 111 registros |
| **melon-3c** | 43-13 registros | 142 registros | 35+1 registros |
| **yura-2c** | 6-80 registros | - | 6 registros |

### Catálogo de Combustibles
Todas las bases comparten el mismo catálogo de **86 combustibles** que incluye:
- **Convencionales**: Carbón, petcoke, fuel oil, diesel, gas natural, lignito
- **Alternativos**: Aceites usados, neumáticos, plásticos, solventes
- **Biomasa**: Residuos agrícolas, harinas animales, lodos, madera

---

## 9. Datos de Transporte y Distancias

### Estructura de Tablas de Distancias

| Base | Tabla | Registros | Tipo de Datos |
|------|-------|-----------|---------------|
| **pacas-3c** | tb_distancias_plantas | 186 | Distancias planta-origen (insumos) |
| **pacas-3c** | tb_distancias_rutas | 0 | - |
| **mzma-3c** | tb_distancias_rutas | 674 | Distancias planta-planta (despachos) |
| **melon-3c** | tb_distancias_rutas | 648 | Distancias planta-planta (despachos) |
| **yura-2c** | tb_distancias_plantas | 1 | Solo clinker importado (barco 17,000 km) |
| **yura-2c** | tb_distancias_rutas | 7 | Rutas básicas |
| **yura-2c** | DISTANCIAS_DEFAULT (código) | 20+ | Diccionario hardcodeado en const.py |

### Detalle tb_distancias_plantas (pacas-3c)
Contiene 186 rutas de insumos hacia plantas de cemento:
- **Origen**: Canteras, puertos de importación, minas
- **Destino**: Plantas de cemento (Pacasmayo, Piura, Rioja)
- **Datos**: Coordenadas origen/destino, distancia en km, modo transporte (camión/barco)

Ejemplo:
| Planta | Origen | Distancia (km) | Modo |
|--------|--------|----------------|------|
| Pacasmayo | Cantera Tembladera | 65.3 | camión |
| Pacasmayo | Clinker Ecuador | 798.5 | barco |
| Pacasmayo | Puzolana Sexi | 239.2 | camión |
| Pacasmayo | Minerales Yura | 1,691.7 | camión |

### Detalle tb_distancias_rutas (mzma-3c)
Contiene 674 rutas de despacho con:
- **Insumos cubiertos**: CE04, CE08 (cementos), AR01-AR11 (áridos), GR02-GR18 (gravas), CA02 (cal)
- **Tipos transporte**: 1 (camión corto), 3 (camión largo)
- **Datos**: Distancia km, kg CO2/t calculado

### Indicadores de Transporte en Concreto
| Código | Nombre | Disponibilidad |
|--------|--------|---------------|
| 1117-1124 | Transporte por tipo insumo | Calculable |
| 1132 | Distancia despacho concreto | Variable |
| 1191 | Transporte agua camión aljibe | Calculable |

### Detalle DISTANCIAS_DEFAULT (yura-2c) - Hardcodeado en código
**Ubicación**: `/home/cpinilla/projects/yura-2c/streamlit/services/const.py`

#### Minerales (locales)
| Material | Origen | Modo | Distancia (km) |
|----------|--------|------|----------------|
| caliza | Peru | camión | 5 |
| arcilla | Peru | camión | 5 |
| silice | Peru | camión | 25 |
| oxido_hierro | Peru | camión | 350 |
| oxido_hierro | Turquía | barco+camión | 12,000 + 1,000 |
| puzolana | Peru | camión | 30 |
| escoria | Peru | camión | 40 |
| fluorita | Peru | camión | 50 |
| desulfurante | Peru | camión | 45 |

#### Combustibles (importados y locales)
| Material | Origen | Modo | Distancia (km) |
|----------|--------|------|----------------|
| antracita | Peru | camión | 50 |
| bituminoso | Colombia | camión+barco | 3,500 + 2,800 |
| bituminoso | USA | barco+camión | 7,000 + 8,000 |
| carbon | Colombia | camión+barco | 3,500 + 2,800 |
| carbon | USA | barco+camión | 7,000 + 8,000 |
| petcoke | Colombia | barco | 2,800 |
| petcoke | USA | barco | 7,000 |
| diesel | Peru | camión | 200 |
| aceite_usado | Peru | camión | 100 |
| neumaticos | Peru | camión | 150 |
| madera | Peru | camión | 80 |

#### Diccionarios adicionales en const.py
- `DISTANCIAS_CEMENTO_DICT`: Distancias para cemento (mínimas, caliza=0)
- `DISTANCIAS_CLINKER_DICT`: Distancias para clinker con valores específicos

### Resumen de Cobertura de Distancias

| Tipo de Transporte | pacas | mzma | melon | yura |
|--------------------|-------|------|-------|------|
| Insumos → Planta Cemento | 186 rutas | - | - | 1 BD + 20+ código |
| Despachos Concreto | - | 674 rutas | 648 rutas | 7 rutas |
| Total | 186 | 674 | 648 | ~28 |

---

## 10. Datos Disponibles para Consolidación

### Total Estimado
| Tipo de Dato | Registros Aproximados |
|--------------|----------------------|
| Datasets (cemento/clinker) | ~4,050 |
| Registros de indicadores | ~96,000 |
| Remitos de concreto | ~605,000 |
| Plantas cementeras LATAM | 265 |
| Benchmark mundial (GNR) | 17,722 |
| Datos de composición cemento | ~927 |
| Rutas de transporte | ~1,516 |
| Combustibles (catálogo) | 86 |

### Cobertura Temporal
- **pacas-3c**: 2014-2025 (foco 2020-2025)
- **mzma-3c**: 2020-2025
- **melon-3c**: 2023-2024
- **yura-2c**: 2020-2024
- **ficem_bd**: Histórico regional + benchmarks

### Cobertura Geográfica
- **México**: 3 plantas integradas (Tepetzingo, Apazapan, Cerritos) - MZMA
- **Perú**:
  - Pacasmayo: 4 plantas (Pacasmayo, Piura, Rioja + clinker importado)
  - Yura: 1 planta integrada + clinker importado
- **Chile**: 10 plantas de cemento (Melón, Polpaico, Bicentenario, etc.)
- **LATAM Regional**: 265 plantas en ficem_bd

### Cobertura de Datos de Energía
| Tipo | Cemento | Concreto |
|------|---------|----------|
| Eléctrico | 4 bases (pacas, mzma, melon, yura) | 3 bases (pacas, mzma, melon) |
| Térmico | 4 bases | N/A |
| Combustibles | 4 bases (catálogo completo) | Indirecto vía cemento |

### Cobertura de Datos de Transporte
| Tipo | Cobertura |
|------|-----------|
| Insumos → Planta Cemento | Pacas (186 rutas), Yura (1 ruta) |
| Despachos Concreto | MZMA (674), Melon (648), Yura (7) |

---

## 11. Próximos Pasos para Consolidación

1. **Definir esquema destino** en PostgreSQL (latam4c_db)
2. **Mapear indicadores** entre bases de datos
3. **Normalizar datos** de plantas y productos
4. **Migrar datasets** de pacas-3c, mzma-3c, melon-3c y yura-2c
5. **Integrar benchmarks** de gnr_data
6. **Consolidar huella_concretos** con datos existentes
7. **Unificar tablas de distancias** en formato común
8. **Completar distancias faltantes** (insumos en mzma/melon, despachos en pacas)
