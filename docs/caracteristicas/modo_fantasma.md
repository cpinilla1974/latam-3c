# Modo Fantasma en LATAM-3C

**Descripción breve:** Funcionalidad de anonimización de datos empresariales para presentaciones y reportes con datos sensibles.

---

## ¿Qué es el Modo Fantasma?

El **Modo Fantasma** (Ghost Mode) es una característica de privacidad que anonimiza automáticamente:

- **Nombres de compañías/empresas** (campo `origen` o `compania`)
- **Nombres de plantas productivas** (campo `planta`)

Mientras mantiene **completamente visibles** todos los datos técnicos y de performance:

- Resistencias del concreto (kg/cm², MPa)
- Emisiones CO2 (kg/m³)
- Volúmenes de despacho (m³)
- Tipos de cemento y fórmulas
- Fechas y períodos
- Todos los KPIs y métricas

---

## Cómo Funciona

### Activación
```python
modo_fantasma = st.sidebar.checkbox("👻 Modo Fantasma", value=True)
```

**Nota:** Viene **habilitado por defecto** en la aplicación. El usuario puede desactivarlo desmarcando el checkbox.

### Mecanismo de Anonimización

1. **Lectura de datos únicos:** Se extrae la lista completa de compañías y plantas
2. **Ordenamiento alfabético:** Se ordenan para garantizar consistencia
3. **Mapeo automático:**
   ```python
   origenes_unicos = sorted(df['origen'].unique())
   mapeo_fantasma = {origen: f"Compañía {i+1}" for i, origen in enumerate(origenes_unicos)}
   ```
4. **Aplicación condicional:** Se aplica el mapeo SOLO si el checkbox está activado
5. **Conversión bidireccional:** Los filtros aceptan nombres anónimos pero consultan BD con nombres reales

---

## Mapeo de Nombres

### Estructura General

| Nombre Real (BD) | Nombre en Clave | Tipo |
|------------------|-----------------|------|
| [Compañía 1] | Compañía 1 | Empresa |
| [Compañía 2] | Compañía 2 | Empresa |
| [Compañía 3] | Compañía 3 | Empresa |
| ... | ... | ... |

### Ejemplo de Plantas

Para plantas, el mapeo es **jerárquico** (compañía + planta):

| Nombre Real (BD) | Nombre en Clave | Estructura |
|------------------|-----------------|-----------|
| Planta Apazapan (de Compañía X) | Compañía X - Planta 1 | Empresa - Planta |
| Planta Bajío (de Compañía X) | Compañía X - Planta 2 | Empresa - Planta |
| Planta Sur (de Compañía Y) | Compañía Y - Planta 1 | Empresa - Planta |

**Lógica:** Se ordena alfabéticamente cada compañía, luego se numeran sus plantas secuencialmente.

---

## Implementación en Código

### Archivos que usan Modo Fantasma

| Archivo | Línea | Campos Anonimizados | Descripción |
|---------|-------|-------------------|------------|
| `/v1/pages/bandas/01_estadisticas_concretos.py` | 40-50 | `origen` | Estadísticas de concreto |
| `/v1/pages/bandas/02_estadisticas_remitos.py` | 231-358 | `compania`, `planta` | Análisis de despachos |
| `/v1/pages/bandas/03_bandas_concretos.py` | 218-235 | `origen` | Bandas GCCA concreto |
| `/v1/pages/analisis/07_bandas_concreto.py` | 218-235 | `origen` | Análisis detallado concreto |

### Ejemplo de Código

#### Creación del mapeo (01_estadisticas_concretos.py, líneas 40-50)
```python
if modo_fantasma:
    # Crear mapeo para compañías
    origenes_unicos = sorted(df_csv['origen'].unique())
    mapeo_fantasma = {origen: f"Compañía {i+1}" for i, origen in enumerate(origenes_unicos)}

    # Aplicar mapeo a datos
    df_csv['origen'] = df_csv['origen'].map(mapeo_fantasma)
```

#### Mapeo jerárquico para plantas (02_estadisticas_remitos.py, líneas 239-244)
```python
if modo_fantasma:
    # Crear mapeo compañía primero
    companias_unicas_sorted = sorted(df_comp_plantas['compania'].unique())
    mapeo_fantasma_comp = {compania: f"Compañía {i+1}"
                           for i, compania in enumerate(companias_unicas_sorted)}

    # Luego mapeo de plantas dentro de cada compañía
    mapeo_fantasma_planta = {}
    for compania in companias_unicas_sorted:
        plantas_de_compania = sorted(
            df_comp_plantas[df_comp_plantas['compania'] == compania]['planta'].unique()
        )
        for j, planta in enumerate(plantas_de_compania, 1):
            compania_anonima = mapeo_fantasma_comp[compania]
            mapeo_fantasma_planta[planta] = f"{compania_anonima} - Planta {j}"

    # Aplicar mapeos
    df_remitos['compania'] = df_remitos['compania'].map(mapeo_fantasma_comp)
    df_remitos['planta'] = df_remitos['planta'].map(mapeo_fantasma_planta)
```

#### Conversión bidireccional para filtros
```python
if modo_fantasma:
    # Usuario selecciona "Compañía 1" pero BD consulta nombre real
    companias_sel_display = st.multiselect("Compañías", options=list(mapeo_fantasma.values()))
    companias_sel = tuple([mapeo_inverso[c] for c in companias_sel_display])

    # Consulta SQL usa nombres reales
    query = f"SELECT * FROM tabla WHERE compania IN {companias_sel}"
```

---

## Casos de Uso

### 1. Demostraciones a Terceros
```
Escenario: Presentar análisis de eficiencia a potencial cliente
Problema: Revelaría identidades de competidores
Solución: Activar Modo Fantasma
Resultado: "Compañía 1, Compañía 2, Compañía 3" sin identidades reales
```

### 2. Reportes Públicos
```
Escenario: Publicar análisis de sostenibilidad en web
Problema: Datos sensibles de empresas privadas
Solución: Activar Modo Fantasma
Resultado: Análisis técnico transparente sin exponer nombres
```

### 3. Presentaciones Internas
```
Escenario: Mostrar performance por planta a stakeholders
Problema: Información competitiva entre plantas
Solución: Activar Modo Fantasma
Resultado: Análisis sin sesgo de identidad
```

---

## Características Técnicas

### Ventajas

- **Reversible:** Mantiene mapeos inversos para recuperar datos originales
- **Consistente:** Usa el mismo mapeo durante toda la sesión
- **Selectivo:** Solo afecta identificadores (compañías/plantas), no datos técnicos
- **Automático:** Ordenamiento alfabético garantiza reproducibilidad
- **Transparente:** Usuario ve claramente cuándo está activo (checkbox)

### Limitaciones

- Solo anonimiza **nombres de entidades** (compañías y plantas)
- NO anonimiza:
  - Fórmulas de productos (ej: "C210-MS-H67")
  - Tipos de cemento (ej: "Tipo I", "Tipo IP")
  - Fechas y períodos
  - Datos numéricos

---

## Estado de Implementación

**Fully Implemented:** ✅

- Disponible en 4 páginas de análisis
- Habilitado por defecto
- Documentado en código
- Funcionalidad probada

**Potencial de Expansión:**

- [ ] Anonimizar también clientes (si existe campo `cliente`)
- [ ] Anonimizar proyectos (si existe campo `proyecto`)
- [ ] Opción de guardar mapeo para auditoría

---

**Documentación:** Basada en código de `/v1/pages/bandas/` y `/v1/pages/analisis/`

**Fecha:** 2025-12-03
