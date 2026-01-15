# Estructura de Datos de Entrada - Sistema LATAM-3C

## Visión General

Sistema de recopilación de datos anuales de huella de carbono para empresas cementeras en Latinoamérica, basado en archivos Excel estandarizados.

## Archivos Requeridos

Cada empresa debe enviar anualmente:

1. **Por cada planta de cemento**: `[EMPRESA]_[PAIS]_[AÑO]_[ID_PLANTA].xlsx`
2. **Concreto (consolidado)**: `[EMPRESA]_[PAIS]_[AÑO]_Concreto.xlsx`

Ejemplo: 
- `ACME_Colombia_2024_P001.xlsx` (Planta Norte)
- `ACME_Colombia_2024_P002.xlsx` (Planta Sur)  
- `ACME_Colombia_2024_Concreto.xlsx` (Todas las plantas de concreto)

---

## ARCHIVO 1: PLANTA DE CEMENTO (Un archivo por planta)

### Hoja 1: EMPRESA
| Campo          | Descripción        | Ejemplo            |
| -------------- | ------------------ | ------------------ |
| Nombre_Empresa | Razón social       | ACME Cementos S.A. |
| País           | País del reporte   | Colombia           |
| Año_Reporte    | Año calendario     | 2024               |
| Responsable    | Nombre completo    | Ana García López   |
| Email          | Correo corporativo | agarcia@acme.com   |
| Teléfono       | Con código país    | +57 1 234 5678     |

### Hoja 2: PLANTA
Información de la planta específica

| Campo                     | Descripción                   | Ejemplo              |
| ------------------------- | ----------------------------- | -------------------- |
| ID_Planta                 | Código único interno          | P001                 |
| Nombre                    | Nombre de la planta           | Planta Norte         |
| Ubicación                 | Ciudad, Departamento/Estado   | Bogotá, Cundinamarca |
| Latitud                   | Coordenada geográfica decimal | 4.7110               |
| Longitud                  | Coordenada geográfica decimal | -74.0721             |
| Tipo_Planta               | Tipo de operación             | Integrada/Molienda   |
| Capacidad_Clinker_ton/año | Capacidad instalada clinker   | 1200000              |
| Capacidad_Cemento_ton/año | Capacidad instalada cemento   | 1500000              |
| Archivo_GCCA              | Nombre archivo protocolo GCCA | GCCA_P001_2024.xlsx  |

### Hoja 3: CLINKER (Solo si la planta produce clinker)

#### IDENTIFICACIÓN
| Campo | Valor |
|-------|-------|
| Producción_Clinker_Anual_ton | Numeral |
| Emisiones_Proceso_tCO2 | Numeral (si disponible del GCCA) |

#### SECCIÓN A: MINERALES
| Material | Cantidad_ton | Origen | Dist_Camión_km | Dist_Tren_km | Dist_Barco_km | Dist_Banda_km |
|----------|--------------|--------|----------------|--------------|---------------|---------------|
| Caliza | Numeral | Texto | Numeral | 0 | 0 | 0 |
| Arcilla | Numeral | Texto | Numeral | 0 | 0 | 0 |
| Mineral_Hierro | Numeral | Texto | Numeral | Numeral | 0 | 0 |
| Arena_Sílice | Numeral | Texto | 0 | Numeral | 0 | 0 |
| Yeso | Numeral | Texto | Numeral | 0 | Numeral | 0 |
| Otros | Numeral | Texto | Numeral | 0 | 0 | 0 |

#### SECCIÓN B: COMBUSTIBLES HORNO

**[Axioma A001]**: Los combustibles de horno se tomarán directamente de los archivos GCCA reportados por cada planta.

*Esto incluye todos los combustibles utilizados en el horno de clinker: carbón, pet coke, gas natural, biomasa, residuos industriales, fuel oil, etc.*

#### SECCIÓN C: ENERGÍA ELÉCTRICA
| Tipo_Energía | Cantidad_kWh | Factor_Emisión_kgCO2/kWh | Fuente |
|--------------|--------------|--------------------------|--------|
| Red_Nacional | Numeral | Decimal (ej: 0.126) | Sistema Interconectado |
| Solar_Propia | Numeral | 0.000 | Paneles fotovoltaicos |
| Eólica_PPA | Numeral | 0.000 | Contrato parque eólico |
| Otra_Renovable | Numeral | Decimal | Descripción |


### Hojas 4+: CEMENTO_TIPO_[X]
**Nota:** Una hoja por cada tipo de cemento producido en esta planta

#### IDENTIFICACIÓN
| Campo | Valor |
|-------|-------|
| Tipo_Cemento | Nomenclatura oficial (ej: CPC 30R, CPO 40) |
| Nombre_Comercial | Nombre de mercado |
| Resistencia_28d_MPa | Resistencia a 28 días en MPa |
| Resistencia_28d_psi | Resistencia a 28 días en psi |
| Norma_Técnica | Norma aplicable (NTC, ASTM, etc.) |
| Producción_Anual_ton | Numeral |

#### COMPOSICIÓN Y TRANSPORTE
| ID_Material | Material | Proveedor/Origen | Cantidad_ton | Dist_Camión_km | Dist_Tren_km | Dist_Barco_km | Dist_Banda_km |
|-------------|----------|------------------|--------------|----------------|--------------|---------------|---------------|
| CLK_01 | Clinker | Producción propia | Numeral | 0 | 0 | 0 | 0 |
| CLK_02 | Clinker | [Nombre proveedor] | Numeral | Numeral | Numeral | 0 | 0 |
| ESC_01 | Escoria | [Nombre proveedor] | Numeral | Numeral | Numeral | 0 | 0 |
| PUZ_01 | Puzolana/Ceniza | [Nombre proveedor] | Numeral | Numeral | 0 | 0 | 0 |
| CAL_01 | Caliza | Cantera propia/proveedor | Numeral | Numeral | 0 | 0 | Numeral |
| YES_01 | Yeso | Stock/proveedor | Numeral | Numeral | 0 | 0 | 0 |

#### MOLIENDA Y COMBUSTIBLES
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Electricidad_Red | Numeral | kWh |
| Electricidad_Renovable | Numeral | kWh |

**[Axioma A002]**: Los combustibles fuera de horno (molienda, secado, etc.) se tomarán directamente de los archivos GCCA de cada planta.

---

## ARCHIVO 2: CONCRETO

### Hoja 1: EMPRESA
(Misma estructura que Archivo 1)

### Hoja 2: PLANTAS_CONCRETO
Listado de plantas de concreto

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|  
| ID_Planta | Código único interno | PC001 |
| Nombre | Nombre de la planta | Planta Concreto Norte |
| Ubicación | Ciudad, Departamento | Bogotá, Cundinamarca |
| Latitud | Coordenada geográfica | 4.7110 |
| Longitud | Coordenada geográfica | -74.0721 |
| Tipo | Fija o Móvil | Fija |
| Capacidad_m3_año | Capacidad instalada | 250000 |

### Hoja 3: PRODUCCION
Volúmenes anuales por planta

| ID_Planta | Categoría | Tipo_Concreto | Resistencia | Volumen_m3_Anual |
|-----------|-----------|---------------|-------------|------------------|
| PC001 | Estructural | Convencional | f'c 210 | Numeral |
| PC001 | Estructural | Convencional | f'c 250 | Numeral |
| PC001 | Estructural | Convencional | f'c 280 | Numeral |
| PC001 | Alta_Resistencia | Premium | f'c 350 | Numeral |
| PC002 | Alta_Resistencia | Premium | f'c 420 | Numeral |
| PC002 | Especiales | [Tipo] | [Especificación] | Numeral |

### Hoja 4: MEZCLAS
Diseños típicos utilizados

| ID_Mezcla | Resistencia | Cemento_kg/m3 | Tipo_Cemento | Arena_kg/m3 | ID_Arena | Grava_kg/m3 | ID_Grava | Agua_L/m3 | Aditivo_L/m3 | ID_Aditivo | Adiciones_kg/m3 | ID_Adicion |
|-----------|-------------|---------------|--------------|-------------|----------|-------------|----------|-----------|--------------|------------|-----------------|------------|
| MZ_210 | f'c 210 | 320 | CPC 30R | 850 | ARE_01 | 950 | GRA_01 | 180 | 2.5 | ADI_01 | 0 | - |
| MZ_280 | f'c 280 | 380 | CPO 40 | 820 | ARE_02 | 920 | GRA_01 | 175 | 3.2 | ADI_02 | 30 | ESC_01 |

### Hoja 5: AGREGADOS Y ADICIONES
| ID_Material | Material | Tipo | Proveedor | Cantidad_ton_Anual | Dist_Camión_km | Dist_Tren_km | Dist_Barco_km |
|-------------|----------|------|-----------|-------------------|----------------|--------------|---------------|
| ARE_01 | Arena | Río | Cantera XYZ | Numeral | Numeral | 0 | 0 |
| ARE_02 | Arena | Triturada | Cantera ABC | Numeral | Numeral | 0 | 0 |
| GRA_01 | Grava | 3/4" | Cantera XYZ | Numeral | Numeral | 0 | 0 |
| GRA_02 | Grava | 1/2" | Cantera ABC | Numeral | 0 | Numeral | 0 |
| ESC_01 | Escoria | Granulada | Acerería DEF | Numeral | Numeral | 0 | 0 |
| CEN_01 | Ceniza | Volante | Termoeléctrica GHI | Numeral | Numeral | 0 | 0 |

### Hoja 6: ADITIVOS
| ID_Aditivo | Tipo_Aditivo | Función | Marca | Proveedor | Cantidad_L_Anual | Dist_Camión_km | Dist_Tren_km | Dist_Barco_km |
|------------|--------------|---------|-------|-----------|------------------|----------------|--------------|---------------|
| ADI_01 | Plastificante | Reductor de agua | Texto | Texto | Numeral | Numeral | 0 | 0 |
| ADI_02 | Superplastificante | Alto rango | Texto | Texto | Numeral | Numeral | 0 | 0 |
| ADI_03 | Retardante | Control fraguado | Texto | Texto | Numeral | Numeral | 0 | 0 |
| ADI_04 | Otros | Descripción | Texto | Texto | Numeral | Numeral | 0 | 0 |

### Hoja 7: ENERGIA_AGUA
| Concepto | Cantidad_Anual | Unidad | Origen/Uso |
|----------|----------------|--------|------------|
| **ELECTRICIDAD** | | | |
| Plantas_Mezclado | Numeral | kWh | Red nacional |
| Plantas_Bombeo | Numeral | kWh | Red nacional |
| **COMBUSTIBLES** | | | |
| Diesel_Mixers | Numeral | L | Flota propia |
| Diesel_Bombas | Numeral | L | Equipos bombeo |
| Gasolina | Numeral | L | Vehículos |
| **AGUA** | | | |
| Agua_Mezcla | Numeral | m³ | % red / % pozo |
| Agua_Lavado | Numeral | m³ | % reciclada |

---

### Hoja 8: CONSUMOS_ESPECIFICOS_PLANTA
Consumos específicos por planta para producción de concreto

| ID_Planta | Electricidad_kWh/m3 | Diesel_Cargador_L/m3 | Diesel_Otros_L/m3 | Notas |
|-----------|---------------------|----------------------|-------------------|-------|
| PC001 | 4.5 | 0.8 | 0.2 | Incluye iluminación |
| PC002 | 5.2 | 0.9 | 0.3 | Planta móvil |

*Nota: Consumos promedio anual por m³ de concreto producido*

### Hoja 9: TRANSPORTE_MIXER
Consumo de combustible de camiones mixer por planta

| ID_Planta | Radio_Promedio_km | Diesel_L/m3 | Tipo_Camión | Capacidad_m3 | Factor_Retorno |
|-----------|-------------------|-------------|-------------|--------------|----------------|
| PC001 | 15 | 3.5 | Mixer estándar | 8 | 0.7 |
| PC002 | 25 | 5.8 | Mixer estándar | 8 | 0.7 |
| PC003 | 10 | 2.8 | Mixer pequeño | 6 | 0.7 |

*Nota: Factor_Retorno = proporción del viaje de retorno con carga (0.7 = retorna vacío 30% del tiempo)*

### Hoja 10: SITIOS_MINERALES (Opcional)
Solo si la empresa tiene canteras o minas propias

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|  
| ID_Sitio | Código único | M001 |
| Tipo | Cantera/Mina | Cantera |
| Material_Principal | Material extraído | Caliza |
| Ubicación | Municipio, Departamento | Soacha, Cundinamarca |
| Latitud | Coordenada geográfica | 4.5854 |
| Longitud | Coordenada geográfica | -74.2197 |
| Capacidad_Anual_ton | Capacidad de extracción | 2000000 |
| Distancia_Planta_km | Distancia a planta principal | 35 |

---

## NOTAS IMPORTANTES

### Estructura por Planta
- **Clinker y Cemento**: Los datos deben reportarse por planta, no agregados por empresa
- **Concreto**: Los volúmenes se reportan por planta de concreto
- **Trazabilidad**: Cada planta tiene un ID único que se mantiene consistente entre años
- **Empresas con una planta**: Usar "P001" como ID default

### Identificadores Únicos
Los materiales deben identificarse con códigos únicos para trazabilidad:
- **CLK_XX**: Diferentes fuentes de clinker
- **ESC_XX**: Diferentes proveedores de escoria
- **PUZ_XX**: Diferentes fuentes de puzolana
- **CAL_XX**: Diferentes canteras de caliza
- **YES_XX**: Diferentes orígenes de yeso

### Unidades Estándar
- Sólidos: toneladas (ton)
- Líquidos: litros (L)
- Gases: metros cúbicos (m³)
- Energía: kilovatios-hora (kWh)
- Distancia: kilómetros (km)

### Valores Especiales
- **Origen "Propio"**: Material de la misma empresa (distancia = 0)
- **Origen "Stock"**: Material en inventario de períodos anteriores
- **Transporte "-"**: No aplica (material propio o sin transporte)
- **Transporte múltiple**: Usar "Barco+Camión" cuando sea combinado

### Validaciones Básicas
1. Todos los campos numéricos deben ser positivos
2. Las sumatorias de composición deben cuadrar con producción total
3. Los tipos de cemento en concreto deben existir en archivo de cemento
4. Los factores de emisión eléctrica deben estar en rango válido por país