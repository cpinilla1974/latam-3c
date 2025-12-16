# Fórmulas de Agregación Nacional - Protocolo FICEM

**Fuente oficial:** Anexo: Definición de Indicadores y Fórmulas de Cálculo V1.4 (FICEM, 14 Feb 2023)
**Propósito:** Referencia para cálculo de indicadores agregados a nivel país

## Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2025-12-15 | CPinilla | Creación inicial con fórmulas oficiales FICEM |
| 1.1 | 2025-12-15 | CPinilla | Añadidos indicadores de emisiones brutas/netas (60, 73, 62, 74, 1044, 1045, 63, 75) |
| 1.2 | 2025-12-15 | CPinilla | Corregidos códigos cem. equivalente según BD común (63a, 63b, 82c, 1410-1417) |
| 1.3 | 2025-12-16 | CPinilla | Corregida fórmula cemento equivalente: [21b] = [8] / [92a] según hoja Comments protocolo GNR |

---

## Principio de Agregación

Para indicadores de intensidad (ratios, porcentajes), se usa **promedio ponderado**:

```
Indicador Nacional = Σ(numerador_i) / Σ(denominador_i)
```

**NO** promedio simple.

---

## Campos GNR Completos (Anexo V1.4 FICEM)

### Producción
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 8 | Clínker producido | t/año | Σ[8]ᵢ |
| 9 | Clínker comprado | t/año | Σ[9]ᵢ |
| 10 | Clínker vendido | t/año | Σ[10]ᵢ |
| 10a | Cambio en stock clínker | t/año | Σ[10a]ᵢ |
| 10b | Transferencia interna clínker | t/año | Σ[10b]ᵢ |
| 11 | Clínker consumido | t/año | Σ[11]ᵢ |
| 20 | Cemento producido | t cem/año | Σ[20]ᵢ |
| 21a | Producto cementitious | t/año | Σ[21a]ᵢ |

### Eficiencia y Sustitución
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 33d | Factor emisión red eléctrica | kgCO₂/MWh | Σ[49a]ᵢ / Σ[33c]ᵢ |
| 92a | Factor clínker | % | Σ[11]ᵢ / Σ[20]ᵢ |
| 93 | Consumo térmico | MJ/t clínker | (Σ[25]ᵢ / Σ[8]ᵢ) × 1000000 |
| 95 | Fósiles alternativos | % | (Σ[27]ᵢ / Σ[25]ᵢ) × 100 |
| 96 | Biomasa | % | (Σ[28]ᵢ / Σ[25]ᵢ) × 100 |
| 96a | Factor emisión combustibles | kgCO₂/GJ | (Σ[43]ᵢ / Σ[25]ᵢ) × 1000 |
| 97 | Consumo eléctrico específico planta | kWh/t cementitious | (Σ[33]ᵢ / Σ[20]ᵢ) × 1000 |

**Coprocesamiento** = Campo 95 + Campo 96 = (Σ[27]ᵢ + Σ[28]ᵢ) / Σ[25]ᵢ

### Emisiones Específicas - Clínker
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 60a | Descarbonatación | kgCO₂/t clínker | (Σ[39]ᵢ / Σ[8]ᵢ) × 1000 |
| 1008 | Combustibles fósiles convencionales | kgCO₂/t clínker | (Σ[40]ᵢ / Σ[8]ᵢ) × 1000 |
| 1009 | Combustibles fósiles alternativos | kgCO₂/t clínker | (Σ[41]ᵢ / Σ[8]ᵢ) × 1000 |
| 1010 | Combustibles fuera de horno | kgCO₂/t clínker | (Σ[44]ᵢ + Σ[45a]ᵢ + Σ[45b]ᵢ) / Σ[8]ᵢ × 1000 |
| 1011 | Específica biomasa | kgCO₂/t clínker | (Σ[225]ᵢ / Σ[8]ᵢ) × 1000 |
| 1012 | Electricidad externa | kgCO₂/t clínker | Σ([33d]ᵢ × [33c]ᵢ × [33e]ᵢ/[33]ᵢ) / Σ[8]ᵢ |
| 1088 | Generación eléctrica on-site | kgCO₂/t clínker | Σ([45c]ᵢ × [33aa]ᵢ/[33a]ᵢ × [33e]ᵢ/[33]ᵢ) / Σ[8]ᵢ × 1000 |
| **60** | **Específica bruta** | kgCO₂/t clínker | 60a + 1010 + 1008 + 1009 |
| **73** | **Específica neta** | kgCO₂/t clínker | 60a + 1010 + 1008 |

### Emisiones Específicas - Cementitious
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 62a | Descarbonatación | kgCO₂/t cementitious | (Σ[59a]ᵢ / Σ[21a]ᵢ) × 1000 |
| 82a | Electricidad externa | kgCO₂/t cementitious | (Σ[49a]ᵢ / Σ[21a]ᵢ) × 1000 |
| 1020 | Generación eléctrica on-site | kgCO₂/t cementitious | Σ([33aa]ᵢ/[33a]ᵢ × [45c]ᵢ) / Σ[21a]ᵢ × 1000 |
| 1021 | Combustibles fuera de horno | kgCO₂/t cementitious | (Σ[44]ᵢ + Σ[45a]ᵢ + Σ[45b]ᵢ) / Σ[21a]ᵢ × 1000 |
| 1022 | Combustibles fósiles convencionales | kgCO₂/t cementitious | (Σ[40]ᵢ / Σ[21a]ᵢ) × 1000 |
| 1023 | Combustibles fósiles alternativos | kgCO₂/t cementitious | (Σ[41]ᵢ / Σ[21a]ᵢ) × 1000 |
| 1024 | Específica biomasa | kgCO₂/t cementitious | (Σ[50]ᵢ / Σ[21a]ᵢ) × 1000 |
| **62** | **Específica bruta** | kgCO₂/t cementitious | 62a + 1021 + 1022 + 1023 |
| **74** | **Específica neta** | kgCO₂/t cementitious | 62a + 1021 + 1022 |

### Emisiones Específicas - Cemento
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 1001 | Descarbonatación | kgCO₂/t cem | Si [8]≥[11]: Σ([39]ᵢ×[11]ᵢ/[8]ᵢ) / Σ[20]ᵢ × 1000; Si [8]<[11]: Σ[39]ᵢ / Σ[20]ᵢ × 1000 |
| 1002 | Combustibles fuera de horno | kgCO₂/t cem | (Σ[44]ᵢ + Σ[45a]ᵢ + Σ[45b]ᵢ) / Σ[20]ᵢ × 1000 |
| 1003 | Combustibles fósiles convencionales | kgCO₂/t cem | Si [8]≥[11]: Σ([40]ᵢ×[11]ᵢ/[8]ᵢ) / Σ[20]ᵢ × 1000; Si [8]<[11]: Σ[40]ᵢ / Σ[20]ᵢ × 1000 |
| 1004 | Combustibles fósiles alternativos | kgCO₂/t cem | Si [8]≥[11]: Σ([41]ᵢ×[11]ᵢ/[8]ᵢ) / Σ[20]ᵢ × 1000; Si [8]<[11]: Σ[41]ᵢ / Σ[20]ᵢ × 1000 |
| 1005 | Electricidad externa | kgCO₂/t cem | Σ(Aᵢ) / Σ[20]ᵢ (ver nota) |
| 1006 | Clínker externo | kgCO₂/t cem | 865 × Σ(([11]ᵢ-[8]ᵢ)/[20]ᵢ) |
| 1025 | Generación eléctrica on-site | kgCO₂/t cem | Σ([33aa]ᵢ/[33a]ᵢ × [45c]ᵢ) / Σ[20]ᵢ × 1000 |
| 1043 | Específica biomasa | kgCO₂/t cem | Fórmula compleja (ver Anexo V1.4) |
| **1044** | **Intensidad bruta** | kgCO₂/t cem | 1001 + 1002 + 1003 + 1004 |
| **1045** | **Intensidad neta** | kgCO₂/t cem | 1001 + 1002 + 1003 |

**Nota 1005:** Plantas integradas: Aᵢ = [33d]ᵢ × [33c]ᵢ/[33]ᵢ × ([33e]ᵢ × [11]ᵢ/[8]ᵢ + [33]ᵢ - [33e]ᵢ); Moliendas: Aᵢ = [33d]ᵢ × [33c]ᵢ

### Emisiones Específicas - Cemento Equivalente
| Campo | Indicador | Unidad | Fórmula |
|-------|-----------|--------|---------|
| 63a | Descarbonatación (Calcination) | kgCO₂/t cem eq | (Σ[59a]ᵢ / Σ[cem_eq]ᵢ) × 1000 |
| 82c | Electricidad externa | kgCO₂/t cem eq | (Σ[49a]ᵢ / Σ[cem_eq]ᵢ) × 1000 |
| 1410 | Fósiles convencionales | kgCO₂/t cem eq | (Σ[40]ᵢ / Σ[cem_eq]ᵢ) × 1000 |
| 1411 | Fósiles alternativos | kgCO₂/t cem eq | (Σ[41]ᵢ / Σ[cem_eq]ᵢ) × 1000 |
| 1412 | Biomasa | kgCO₂/t cem eq | (Σ[50]ᵢ / Σ[cem_eq]ᵢ) × 1000 |
| 1416 | Fuera de horno | kgCO₂/t cem eq | (Σ[44]ᵢ + Σ[45a]ᵢ + Σ[45b]ᵢ) / Σ[cem_eq]ᵢ × 1000 |
| 1417 | Generación on-site | kgCO₂/t cem eq | Σ([33aa]ᵢ/[33a]ᵢ × [45c]ᵢ) / Σ[cem_eq]ᵢ × 1000 |
| **63** | **Específica bruta** | kgCO₂/t cem eq | 63a + 1416 + 1410 + 1411 |
| **75** | **Específica neta** | kgCO₂/t cem eq | 63a + 1416 + 1410 |

**Nota:** Cemento equivalente [21b] = Σ([8]ᵢ / [92a]ᵢ) = Suma de [21b] por planta (Fuente: hoja Comments protocolo GNR)

---

## Campos Auxiliares Referenciados

| Campo | Descripción |
|-------|-------------|
| 25 | Consumo térmico total hornos (TJ/año) |
| 27 | Energía fósiles alternativos (TJ/año) |
| 28 | Energía biomasa (TJ/año) |
| 33 | Consumo eléctrico total (MWh/año) |
| 33a | Consumo eléctrico autogenerado (MWh/año) |
| 33aa | Consumo eléctrico autogenerado usado (MWh/año) |
| 33c | Consumo eléctrico externo (MWh/año) |
| 33e | Consumo eléctrico hasta clínker (MWh/año) |
| 39 | Emisiones CO₂ descarbonatación (t CO₂/año) |
| 40 | Emisiones CO₂ fósiles convencionales (t CO₂/año) |
| 41 | Emisiones CO₂ fósiles alternativos (t CO₂/año) |
| 43 | Emisiones CO₂ combustibles fósiles hornos (t CO₂/año) |
| 44 | Emisiones CO₂ equipos on-site (t CO₂/año) |
| 45a | Emisiones CO₂ vehículos on-site (t CO₂/año) |
| 45b | Emisiones CO₂ otros fuera horno (t CO₂/año) |
| 45c | Emisiones CO₂ generación eléctrica on-site (t CO₂/año) |
| 49a | Emisiones CO₂ electricidad externa (t CO₂/año) |
| 50 | Emisiones CO₂ biomasa (t CO₂/año) |
| 59a | Emisiones netas materias primas (t CO₂/año) |
| 225 | Emisiones CO₂ biomasa hornos (t CO₂/año) |

---

**Fin del documento**