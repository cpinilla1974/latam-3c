# Estructura Excel v4 - LATAM-3C

## Archivos Separados
- **Archivo 1**: `ACME_Colombia_2024_Clinker_Cemento.xlsx`
- **Archivo 2**: `ACME_Colombia_2024_Concreto.xlsx`

---

## ARCHIVO 1: CLINKER Y CEMENTO

### Hoja 1: EMPRESA
| Campo | Ejemplo |
|-------|---------|
| Nombre_Empresa | ACME Cementos |
| País | Colombia |
| Año_Reporte | 2024 |
| Responsable | Ana García |
| Email | agarcia@acme.com |
| Teléfono | +57 1 234 5678 |

### Hoja 2: PLANTAS_CEMENTO
Para referencia y vínculo con protocolo GCCA
| ID_Planta | Nombre | Ubicación | Archivo_GCCA |
|-----------|--------|-----------|--------------|
| P001 | Planta Norte | Bogotá, Cundinamarca | GCCA_P001_2024.xlsx |
| P002 | Planta Costa | Barranquilla, Atlántico | GCCA_P002_2024.xlsx |

### Hoja 3: PRODUCCION_CLINKER

**A. MINERALES**
| Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
|----------|--------------|--------|--------------|-----------------|
| Caliza | 3,800,000 | Cantera propia | 5 | Banda |
| Arcilla | 450,000 | Cantera local | 25 | Camión |
| Mineral_Hierro | 35,000 | Proveedor A | 150 | Camión |

**B. COMBUSTIBLES**
*Nota: Estos datos también están disponibles en archivos GCCA de cada planta*
| Combustible | Cantidad | Unidad | Origen | Distancia_km | Modo_Transporte |
|-------------|----------|--------|--------|--------------|-----------------|
| Carbón | 280,000 | ton | Mina Nacional | 300 | Tren |
| Pet_Coke | 45,000 | ton | Puerto importación | 2,000 | Barco |
| Gas_Natural | 12,000,000 | m³ | Red nacional | - | Gasoducto |

**C. ENERGÍA ELÉCTRICA**
| Tipo_Energía | Cantidad_kWh | Factor_Emisión_kgCO2/kWh | Fuente |
|--------------|--------------|--------------------------|--------|
| Red_Nacional | 140,000,000 | 0.126 | Sistema Interconectado |
| Solar_Propia | 10,000,000 | 0.000 | Paneles fotovoltaicos |
| Eólica_PPA | 5,000,000 | 0.000 | Contrato parque eólico |

**D. PRODUCCIÓN**
| Concepto | Cantidad_ton |
|----------|--------------|
| Clinker_Producido | 2,500,000 |

### Hoja 4: CEMENTO_TIPO_1
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | CPC 30R |
| Nombre_Comercial | Cemento Estructural |
| Producción_Anual_ton | 800,000 |

**COMPOSICIÓN Y TRANSPORTE**
| ID_Material | Material | Proveedor/Origen | Cantidad_ton | Distancia_km | Modo_Transporte |
|-------------|----------|------------------|--------------|--------------|-----------------|
| CLK_01 | Clinker | Producción propia | 640,000 | 0 | - |
| CLK_02 | Clinker | Importado China | 40,000 | 15,000 | Barco |
| ESC_01 | Escoria | Siderúrgica Nacional | 80,000 | 150 | Camión |
| CAL_01 | Caliza | Cantera propia | 32,000 | 5 | Banda |
| YES_01 | Yeso | Stock planta | 8,000 | 0 | - |

**MOLIENDA**
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Electricidad_Red | 30,000,000 | kWh |
| Electricidad_Solar | 2,000,000 | kWh |

### Hoja 5: CEMENTO_TIPO_2
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | CPO 40 |
| Nombre_Comercial | Cemento Alta Resistencia |
| Producción_Anual_ton | 400,000 |

**COMPOSICIÓN Y TRANSPORTE**
| ID_Material | Material | Proveedor/Origen | Cantidad_ton | Distancia_km | Modo_Transporte |
|-------------|----------|------------------|--------------|--------------|-----------------|
| CLK_01 | Clinker | Producción propia | 340,000 | 0 | - |
| CLK_03 | Clinker | Compra nacional - Empresa B | 36,000 | 200 | Camión |
| CLK_04 | Clinker | Importado Vietnam | 4,000 | 18,000 | Barco |
| CAL_01 | Caliza | Cantera propia | 16,000 | 5 | Banda |
| YES_01 | Yeso | Stock planta | 4,000 | 0 | - |

**MOLIENDA**
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Electricidad_Red | 18,000,000 | kWh |

### Hoja 6: CEMENTO_TIPO_3
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | Cemento Puzolánico |
| Nombre_Comercial | EcoCem |
| Producción_Anual_ton | 200,000 |

**COMPOSICIÓN Y TRANSPORTE**
| ID_Material | Material | Proveedor/Origen | Cantidad_ton | Distancia_km | Modo_Transporte |
|-------------|----------|------------------|--------------|--------------|-----------------|
| CLK_01 | Clinker | Producción propia | 120,000 | 0 | - |
| PUZ_01 | Ceniza Volante | Termoeléctrica X | 60,000 | 300 | Tren |
| PUZ_02 | Puzolana Natural | Cantera volcánica | 12,000 | 400 | Camión |
| CAL_01 | Caliza | Cantera propia | 6,000 | 5 | Banda |
| YES_01 | Yeso | Stock planta | 2,000 | 0 | - |

**MOLIENDA**
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Electricidad_Red | 10,000,000 | kWh |

### Hojas 7-9: CEMENTO_TIPO_4 a 6 (si aplica)

---

## ARCHIVO 2: CONCRETO

### Hoja 1: EMPRESA
(Misma información que Archivo 1)

### Hoja 2: PRODUCCION_CONCRETO

**A. VOLÚMENES POR TIPO**
| Tipo_Concreto | Resistencia | Volumen_m3_Anual |
|---------------|-------------|------------------|
| Estructural | f'c 210 | 150,000 |
| Estructural | f'c 250 | 200,000 |
| Alta_Resistencia | f'c 300 | 80,000 |
| Alta_Resistencia | f'c 350 | 40,000 |
| Especial | Autocompactante | 15,000 |
| Especial | Permeable | 8,000 |

**B. DISEÑOS DE MEZCLA**
| Tipo_Concreto | Resistencia | Cemento_kg/m3 | Tipo_Cemento | Arena_kg/m3 | Grava_kg/m3 | Agua_L/m3 | Aditivo_L/m3 |
|---------------|-------------|---------------|--------------|-------------|-------------|-----------|--------------|
| Estructural | f'c 210 | 280 | CPC 30R | 850 | 950 | 165 | 2.8 |
| Estructural | f'c 250 | 320 | CPC 30R | 820 | 980 | 170 | 3.2 |
| Alta_Resistencia | f'c 300 | 380 | CPO 40 | 800 | 1000 | 155 | 4.5 |
| Alta_Resistencia | f'c 350 | 420 | CPO 40 | 780 | 1020 | 160 | 5.0 |

**C. ORIGEN AGREGADOS**
| Material | Proveedor | Cantidad_ton_Anual | Distancia_km | Modo_Transporte |
|----------|-----------|-------------------|--------------|-----------------|
| Arena_Río | Arenera del Valle | 420,000 | 35 | Camión |
| Arena_Triturada | Cantera Norte | 80,000 | 25 | Camión |
| Grava_3/4" | Cantera Norte | 300,000 | 25 | Camión |
| Grava_1/2" | Cantera Sur | 200,000 | 40 | Camión |

**D. ADITIVOS**
| Tipo_Aditivo | Proveedor | Cantidad_L_Anual | Distancia_km | Modo_Transporte |
|--------------|-----------|------------------|--------------|-----------------|
| Plastificante | BASF | 1,500,000 | 100 | Camión |
| Retardante | Sika | 200,000 | 150 | Camión |
| Acelerante | Local | 100,000 | 50 | Camión |

**E. ENERGÍA Y AGUA**
| Concepto | Cantidad_Anual | Unidad | Observaciones |
|----------|----------------|--------|---------------|
| Electricidad_Plantas | 3,500,000 | kWh | Para mezclado y bombeo |
| Diesel_Camiones | 850,000 | L | Flota propia mixer |
| Agua_Mezcla | 82,000 | m³ | Red municipal + pozo |
| Agua_Lavado | 15,000 | m³ | Reciclada 60% |

## Ventajas de Archivos Separados

✓ **Más manejable**: Cada archivo más pequeño y específico
✓ **Responsables diferentes**: Pueden trabajar en paralelo
✓ **Validación independiente**: Cada producto con sus reglas
✓ **Carga gradual**: No necesitan estar listos todos a la vez

## Identificadores Únicos

- **CLK_XX**: Clinker con diferentes orígenes
- **ESC_XX**: Escorias de diferentes proveedores  
- **PUZ_XX**: Puzolanas de diferentes fuentes
- **CAL_XX**: Calizas de diferentes canteras
- **YES_XX**: Yeso de diferentes orígenes

Esto permite trazabilidad completa y evita confusiones.