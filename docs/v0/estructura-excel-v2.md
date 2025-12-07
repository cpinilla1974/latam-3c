# Estructura Excel v2 - LATAM-3C

## Principios de Agregación
- **Plantas de cemento**: Se listan para vincular con protocolo GCCA
- **Plantas de concreto**: NO se detallan (pueden ser muchas)
- **Datos**: Agregados a nivel empresa (no por planta)

## Estructura de Hojas

### Hoja 1: EMPRESA
| Campo | Ejemplo |
|-------|---------|
| Nombre_Empresa | CEMEX |
| País_Sede | México |
| Año_Reporte | 2024 |
| Responsable | Juan Pérez |
| Email | jperez@cemex.com |

### Hoja 2: PLANTAS_CEMENTO
Solo para referencia y vínculo con GCCA
| ID_Planta | Nombre | País | Archivo_GCCA |
|-----------|--------|------|--------------|
| MX001 | Monterrey | México | GCCA_MX001_2024.xlsx |
| CO001 | Cartagena | Colombia | GCCA_CO001_2024.xlsx |

### Hoja 3: PRODUCCION_CLINKER
Totales a nivel empresa
| Concepto | Cantidad | Unidad |
|----------|----------|--------|
| Producción_Total | 2,500,000 | ton |
| Carbón | 300,000 | ton |
| Pet_Coke | 50,000 | ton |
| Gas_Natural | 15,000,000 | m³ |
| Caliza | 3,800,000 | ton |
| Arcilla | 450,000 | ton |
| Mineral_Hierro | 35,000 | ton |
| Electricidad | 150,000,000 | kWh |

### Hoja 4: COMPOSICION_CEMENTO
Manejo de clinker propio vs importado
| Tipo_Cemento | Producción_ton | Material | Cantidad_ton | Origen | Distancia_km | Modo_Transporte |
|--------------|----------------|----------|--------------|--------|--------------|-----------------|
| CPC 30R | 800,000 | Clinker | 680,000 | Propio | 0 | - |
| CPC 30R | - | Escoria | 80,000 | Proveedor_A | 150 | Camión |
| CPC 30R | - | Caliza | 40,000 | Cantera_B | 50 | Camión |
| CPO 40 | 400,000 | Clinker | 300,000 | Propio | 0 | - |
| CPO 40 | - | Clinker | 80,000 | Importado_China | 15,000 | Barco |
| CPO 40 | - | Caliza | 20,000 | Cantera_B | 50 | Camión |

### Hoja 5: CONCRETO_AGREGADO
Solo totales por tipo/diseño a nivel empresa
| Diseño | Volumen_m3 | Cemento_kg/m3 | Tipo_Cemento | Arena_kg/m3 | Grava_kg/m3 |
|--------|------------|---------------|--------------|-------------|-------------|
| f'c 200 | 150,000 | 280 | CPC 30R | 850 | 950 |
| f'c 250 | 200,000 | 320 | CPC 30R | 820 | 980 |
| f'c 300 | 80,000 | 380 | CPO 40 | 800 | 1000 |

### Hoja 6: TRANSPORTE_ADICIONAL (opcional)
Para materias primas no cubiertas en otras hojas
| Material | Cantidad_ton | Origen | Destino | Distancia_km | Modo |
|----------|--------------|--------|---------|--------------|------|
| Arena | 500,000 | Río_Local | Empresa | 25 | Camión |
| Grava | 600,000 | Cantera_C | Empresa | 40 | Camión |

## Ventajas de este Modelo

### Para Clinker/Cemento agregado:
✓ **Más simple** para las empresas
✓ **Consistente** con reportes corporativos
✓ **Flexible** para clinker importado
✓ **Trazable** con origen y transporte

### Para Concreto:
✓ **Escalable** (no importa cuántas plantas)
✓ **Manejable** (pocos diseños típicos)
✓ **Práctico** (las empresas ya lo manejan así)

## Validaciones Propuestas

### Consistencia de datos:
- Clinker usado en cemento ≤ Clinker producido + importado
- Suma de materiales en cemento = Producción total
- Cemento usado en concreto coherente con producción

### Rangos esperados:
- Factor clinker/cemento: 0.5 - 0.95
- Consumo cemento/m³: 200 - 500 kg
- Consumo eléctrico/ton clinker: 50 - 70 kWh

## Preguntas Pendientes

1. **¿Factores de emisión?** 
   - ¿Vienen en Excel o están pre-cargados en sistema?
   - ¿Diferentes por país?

2. **¿Combustibles alternativos?**
   - ¿Cómo reportar biomasa, residuos, etc.?

3. **¿Energía renovable?**
   - ¿Separar electricidad de red vs solar/eólica propia?