# Proceso de Agregación Nacional - Perú

**Propósito:** Documentar el proceso para calcular indicadores agregados a nivel país
**Fuente de verdad:** `FORMULAS_AGREGACION.md`

## Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2025-12-15 | CPinilla | Creación inicial |
| 1.1 | 2025-12-16 | CPinilla | Corregida fórmula cemento equivalente: [21b] = [8] / [92a] |
| 1.2 | 2025-12-16 | CPinilla | Filtro por años válidos (cobertura completa de plantas) |

---

## Años Válidos para Agregación

Solo se calculan agregados nacionales para años con **cobertura completa de plantas**:

| Año | Plantas | Notas |
|-----|---------|-------|
| 2010 | 5 | Piura no existía |
| 2014 | 5 | Piura no existía |
| 2019 | 6 | Completo |
| 2020 | 6 | Completo |
| 2021 | 6 | Completo |
| 2024 | 6 | Completo |

**Años excluidos** (datos incompletos): 2015, 2016, 2017, 2018, 2022, 2023

---

## Tablas Involucradas

```
datos_plantas          → Indicadores GNR por planta (fuente)
agregados_nacionales   → Indicadores país (resultado)
```

---

## Proceso de Cálculo

### Paso 1: Limpiar tabla agregados_nacionales
```sql
DELETE FROM agregados_nacionales;
```

### Paso 2: Insertar campos sumables

Sumar desde `datos_plantas` agrupando por año. Estos son los campos auxiliares que se usan como numeradores/denominadores en las fórmulas:

| Campo | Descripción |
|-------|-------------|
| 8 | Clínker producido |
| 9 | Clínker comprado |
| 10 | Clínker vendido |
| 10a | Cambio en stock clínker |
| 10b | Transferencia interna clínker |
| 11 | Clínker consumido |
| 20 | Cemento producido |
| 21a | Producto cementitious |
| 25 | Consumo térmico total hornos |
| 27 | Energía fósiles alternativos |
| 28 | Energía biomasa |
| 33 | Consumo eléctrico total |
| 33a | Consumo eléctrico autogenerado |
| 33aa | Consumo eléctrico autogenerado usado |
| 33c | Consumo eléctrico externo |
| 33e | Consumo eléctrico hasta clínker |
| 39 | Emisiones CO₂ descarbonatación |
| 40 | Emisiones CO₂ fósiles convencionales |
| 41 | Emisiones CO₂ fósiles alternativos |
| 43 | Emisiones CO₂ combustibles fósiles hornos |
| 44 | Emisiones CO₂ equipos on-site |
| 45a | Emisiones CO₂ vehículos on-site |
| 45b | Emisiones CO₂ otros fuera horno |
| 45c | Emisiones CO₂ generación eléctrica on-site |
| 49a | Emisiones CO₂ electricidad externa |
| 50 | Emisiones CO₂ biomasa |
| 59a | Emisiones netas materias primas |
| 225 | Emisiones CO₂ biomasa hornos |

### Paso 3: Calcular indicadores según FORMULAS_AGREGACION.md

#### Eficiencia y Sustitución
| Campo | Fórmula |
|-------|---------|
| 33d | Σ[49a] / Σ[33c] |
| 92a | Σ[11] / Σ[20] |
| 93 | (Σ[25] / Σ[8]) × 1000000 |
| 95 | (Σ[27] / Σ[25]) × 100 |
| 96 | (Σ[28] / Σ[25]) × 100 |
| 96a | (Σ[43] / Σ[25]) × 1000 |
| 97 | (Σ[33] / Σ[20]) × 1000 |
| coprocesamiento | (Σ[27] + Σ[28]) / Σ[25] |

#### Emisiones Específicas - Clínker
| Campo | Fórmula |
|-------|---------|
| 60a | (Σ[39] / Σ[8]) × 1000 |
| 1008 | (Σ[40] / Σ[8]) × 1000 |
| 1009 | (Σ[41] / Σ[8]) × 1000 |
| 1010 | (Σ[44] + Σ[45a] + Σ[45b]) / Σ[8] × 1000 |
| 1011 | (Σ[225] / Σ[8]) × 1000 |
| 1012 | Σ([33d] × [33c] × [33e]/[33]) / Σ[8] |
| 1088 | Σ([45c] × [33aa]/[33a] × [33e]/[33]) / Σ[8] × 1000 |

#### Emisiones Específicas - Cementitious
| Campo | Fórmula |
|-------|---------|
| 62a | (Σ[59a] / Σ[21a]) × 1000 |
| 82a | (Σ[49a] / Σ[21a]) × 1000 |
| 1020 | Σ([33aa]/[33a] × [45c]) / Σ[21a] × 1000 |
| 1021 | (Σ[44] + Σ[45a] + Σ[45b]) / Σ[21a] × 1000 |
| 1022 | (Σ[40] / Σ[21a]) × 1000 |
| 1023 | (Σ[41] / Σ[21a]) × 1000 |
| 1024 | (Σ[50] / Σ[21a]) × 1000 |

#### Emisiones Específicas - Cemento
| Campo | Fórmula |
|-------|---------|
| 1001 | Si [8]≥[11]: Σ([39]×[11]/[8]) / Σ[20] × 1000; Si no: Σ[39] / Σ[20] × 1000 |
| 1002 | (Σ[44] + Σ[45a] + Σ[45b]) / Σ[20] × 1000 |
| 1003 | Si [8]≥[11]: Σ([40]×[11]/[8]) / Σ[20] × 1000; Si no: Σ[40] / Σ[20] × 1000 |
| 1004 | Si [8]≥[11]: Σ([41]×[11]/[8]) / Σ[20] × 1000; Si no: Σ[41] / Σ[20] × 1000 |
| 1005 | Ver nota en FORMULAS_AGREGACION.md |
| 1006 | 865 × Σ(([11]-[8])/[20]) |
| 1025 | Σ([33aa]/[33a] × [45c]) / Σ[20] × 1000 |
| 1043 | Fórmula compleja (ver Anexo V1.4 FICEM) |

#### Emisiones Específicas - Cemento Equivalente
| Campo | Fórmula |
|-------|---------|
| 62a_eq | (Σ[59a] / Σ[cem_eq]) × 1000 |
| 82a_eq | (Σ[49a] / Σ[cem_eq]) × 1000 |
| 1020_eq | Σ([33aa]/[33a] × [45c]) / Σ[cem_eq] × 1000 |
| 1021_eq | (Σ[44] + Σ[45a] + Σ[45b]) / Σ[cem_eq] × 1000 |
| 1022_eq | (Σ[40] / Σ[cem_eq]) × 1000 |
| 1023_eq | (Σ[41] / Σ[cem_eq]) × 1000 |
| 1024_eq | (Σ[50] / Σ[cem_eq]) × 1000 |

**Nota:** [21b] = [8] / [92a] = Clínker producido / Factor clínker (Fuente: hoja Comments protocolo GNR)

---

## Script a Implementar

`scripts/calcular_agregados_nacionales.py`

---

**Fin del documento**