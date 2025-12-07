# Estructura Excel v3 - LATAM-3C

## Estructura de Hojas Revisada

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
| P003 | Planta Valle | Cali, Valle del Cauca | GCCA_P003_2024.xlsx |

### Hoja 3: PRODUCCION_CLINKER

**A. MINERALES**
| Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
|----------|--------------|--------|--------------|-----------------|
| Caliza | 3,800,000 | Cantera propia | 5 | Banda |
| Arcilla | 450,000 | Cantera local | 25 | Camión |
| Mineral_Hierro | 35,000 | Proveedor A | 150 | Camión |
| Arena_Sílice | 25,000 | Proveedor B | 200 | Tren |
| Yeso | 80,000 | Importado | 500 | Barco+Camión |

**B. COMBUSTIBLES**
| Combustible | Cantidad | Unidad | Origen | Distancia_km | Modo_Transporte |
|-------------|----------|--------|--------|--------------|-----------------|
| Carbón | 280,000 | ton | Mina Nacional | 300 | Tren |
| Pet_Coke | 45,000 | ton | Importado | 2,000 | Barco |
| Gas_Natural | 12,000,000 | m³ | Red nacional | - | Gasoducto |
| Biomasa | 15,000 | ton | Local | 50 | Camión |
| Residuos | 8,000 | ton | Recolector | 100 | Camión |

**C. ENERGÍA ELÉCTRICA**
| Tipo_Energía | Cantidad | Unidad | Fuente |
|--------------|----------|--------|--------|
| Electricidad_Red | 140,000,000 | kWh | Red nacional |
| Solar_Propia | 10,000,000 | kWh | Paneles propios |

**D. PRODUCCIÓN**
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Clinker_Producido | 2,500,000 | ton |

### Hoja 4: CEMENTO_TIPO_1
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | CPC 30R |
| Nombre_Comercial | Cemento Estructural |
| Producción_Anual_ton | 800,000 |
| | |
| **COMPOSICIÓN** | |
| Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
| Clinker | 680,000 | Propio | 0 | - |
| Escoria | 80,000 | Proveedor C | 150 | Camión |
| Caliza | 32,000 | Cantera propia | 5 | Banda |
| Yeso | 8,000 | Stock | 0 | - |
| | |
| **MOLIENDA** | |
| Electricidad_kWh | 32,000,000 | Red nacional | - | - |

### Hoja 5: CEMENTO_TIPO_2
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | CPO 40 |
| Nombre_Comercial | Cemento Alta Resistencia |
| Producción_Anual_ton | 400,000 |
| | |
| **COMPOSICIÓN** | |
| Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
| Clinker | 340,000 | Propio | 0 | - |
| Clinker | 40,000 | Importado China | 15,000 | Barco |
| Caliza | 16,000 | Cantera propia | 5 | Banda |
| Yeso | 4,000 | Stock | 0 | - |
| | |
| **MOLIENDA** | |
| Electricidad_kWh | 18,000,000 | Red nacional | - | - |

### Hoja 6: CEMENTO_TIPO_3
| Campo | Valor |
|-------|-------|
| **IDENTIFICACIÓN** | |
| Tipo_Cemento | Cemento Puzolánico |
| Nombre_Comercial | EcoCem |
| Producción_Anual_ton | 200,000 |
| | |
| **COMPOSICIÓN** | |
| Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
| Clinker | 120,000 | Propio | 0 | - |
| Puzolana | 72,000 | Proveedor D | 300 | Tren |
| Caliza | 6,000 | Cantera propia | 5 | Banda |
| Yeso | 2,000 | Stock | 0 | - |
| | |
| **MOLIENDA** | |
| Electricidad_kWh | 10,000,000 | Red nacional | - | - |

### Hojas 7-10: CEMENTO_TIPO_4 a 6 (si aplica)
Mismo formato que los anteriores

## Ventajas de esta Estructura

### Para Clinker:
✓ **Clara separación** entre minerales, combustibles y energía
✓ **Trazabilidad completa** con origen y transporte
✓ **Flexibilidad** para combustibles alternativos
✓ **Distinción** entre energía de red vs renovable propia

### Para Cemento:
✓ **Una hoja por tipo** facilita el llenado
✓ **Máximo 6 tipos** es realista para la industria
✓ **Composición detallada** con trazabilidad
✓ **Separación clara** de consumo de molienda

## Validaciones Sugeridas

### Para Clinker:
- Suma de minerales coherente con producción (factor ~1.55)
- Consumo térmico: 3.0 - 4.5 GJ/ton clinker
- Consumo eléctrico: 50 - 70 kWh/ton clinker

### Para Cemento:
- Suma de materiales = Producción total ± 2%
- Clinker total usado ≤ Clinker producido + importado
- Consumo molienda: 30 - 50 kWh/ton cemento

## Notas Importantes

1. **Unidades consistentes**: Siempre en toneladas para sólidos, m³ para gases, kWh para electricidad
2. **Origen "Propio"**: Para materiales de la misma empresa (distancia = 0)
3. **Origen "Stock"**: Para materiales ya en planta de períodos anteriores
4. **Transporte combinado**: Usar "Barco+Camión" cuando aplique