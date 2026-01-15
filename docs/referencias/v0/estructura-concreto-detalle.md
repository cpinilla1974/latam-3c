# Estructura Archivo Concreto - Detalle

## ARCHIVO: `ACME_Colombia_2024_Concreto.xlsx`

### Hoja 1: EMPRESA
| Campo | Ejemplo |
|-------|---------|
| Nombre_Empresa | ACME Cementos |
| País | Colombia |
| Año_Reporte | 2024 |
| Responsable | Carlos Mendoza |
| Email | cmendoza@acme.com |

### Hoja 2: PRODUCCION
Volúmenes agregados por tipo
| Categoría | Tipo_Concreto | Resistencia | Volumen_m3_Anual |
|-----------|---------------|-------------|------------------|
| Estructural | Convencional | f'c 210 | 150,000 |
| Estructural | Convencional | f'c 250 | 200,000 |
| Estructural | Convencional | f'c 280 | 120,000 |
| Alta_Resistencia | Premium | f'c 350 | 40,000 |
| Alta_Resistencia | Premium | f'c 420 | 25,000 |
| Especiales | Autocompactante | - | 15,000 |
| Especiales | Permeable | - | 8,000 |
| Especiales | Ligero | - | 5,000 |

### Hoja 3: MEZCLAS
Diseños típicos utilizados
| ID_Mezcla | Resistencia | Cemento_kg/m3 | Tipo_Cemento | Arena_kg/m3 | Grava_kg/m3 | Agua_L/m3 | Aditivo_Principal_L/m3 |
|-----------|-------------|---------------|--------------|-------------|-------------|-----------|------------------------|
| MZ_210 | f'c 210 | 280 | CPC 30R | 850 | 950 | 165 | 2.8 |
| MZ_250 | f'c 250 | 320 | CPC 30R | 820 | 980 | 170 | 3.2 |
| MZ_280 | f'c 280 | 360 | CPC 30R | 800 | 990 | 168 | 3.8 |
| MZ_350 | f'c 350 | 420 | CPO 40 | 780 | 1020 | 160 | 5.0 |
| MZ_420 | f'c 420 | 480 | CPO 40 RS | 750 | 1030 | 155 | 6.0 |

### Hoja 4: AGREGADOS
Origen y transporte
| Material | Tipo | Proveedor | Cantidad_ton_Anual | Distancia_km | Modo_Transporte |
|----------|------|-----------|-------------------|--------------|-----------------|
| Arena | Río | Arenera del Valle | 320,000 | 35 | Camión |
| Arena | Triturada | Cantera Norte | 100,000 | 25 | Camión |
| Grava | 3/4" | Cantera Norte | 300,000 | 25 | Camión |
| Grava | 1/2" | Cantera Sur | 200,000 | 40 | Camión |
| Grava | 3/8" | Cantera Sur | 150,000 | 40 | Camión |

### Hoja 5: ADITIVOS
Químicos utilizados
| Tipo_Aditivo | Función | Marca | Proveedor | Cantidad_L_Anual | Distancia_km | Modo_Transporte |
|--------------|---------|-------|-----------|------------------|--------------|-----------------|
| Plastificante | Reductor de agua | MasterGlenium | BASF | 1,200,000 | 100 | Camión |
| Superplastificante | Alto rango | Sikament | Sika | 300,000 | 150 | Camión |
| Retardante | Control fraguado | Plastocrete | Sika | 200,000 | 150 | Camión |
| Acelerante | Fraguado rápido | SikaRapid | Sika | 100,000 | 150 | Camión |
| Incorporador aire | Durabilidad | MasterAir | BASF | 50,000 | 100 | Camión |

### Hoja 6: ENERGIA_AGUA
Consumos operativos
| Concepto | Cantidad_Anual | Unidad | Origen/Uso |
|----------|----------------|--------|------------|
| **ELECTRICIDAD** | | | |
| Plantas_Mezclado | 3,200,000 | kWh | Red nacional |
| Plantas_Bombeo | 300,000 | kWh | Red nacional |
| **COMBUSTIBLES** | | | |
| Diesel_Mixers | 750,000 | L | Flota propia 120 unidades |
| Diesel_Bombas | 100,000 | L | Equipos bombeo |
| Gasolina_Supervision | 50,000 | L | Vehículos supervisión |
| **AGUA** | | | |
| Agua_Mezcla | 82,000 | m³ | 70% red, 30% pozo |
| Agua_Lavado | 15,000 | m³ | 60% reciclada |
| Agua_Curado | 5,000 | m³ | Red municipal |

---

## Ventajas de Hojas Separadas

✓ **Claridad**: Cada tema en su lugar
✓ **Mantenibilidad**: Fácil actualizar secciones específicas
✓ **Validación**: Reglas específicas por hoja
✓ **Flexibilidad**: Pueden agregar/quitar hojas según necesidad
✓ **Navegación**: Más fácil encontrar información

## Alternativa: Todo en Una Hoja

Si prefieres simplicidad, podría ir todo en una hoja con secciones claramente marcadas:
- SECCIÓN A: PRODUCCIÓN
- SECCIÓN B: MEZCLAS
- SECCIÓN C: AGREGADOS
- etc.

Pero con hojas separadas es más profesional y manejable.